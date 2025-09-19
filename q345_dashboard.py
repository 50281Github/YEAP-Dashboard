import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dash import html, dcc, callback, Input, Output
import logging
import os
import datetime
from typing import Dict, List, Any, Optional
from styles import style_manager

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Q345DataProcessor:
    """Q345 Data Processor for analysis results"""
    
    def __init__(self, data_path: str = None):
        self.base_path = data_path or os.path.dirname(os.path.abspath(__file__))
        self.csv_file_path = 'result/q345_analysis_results.csv'
        self.other_file_path = 'orignaldata/q345_option_other.csv'
        self.data = None
        self.other_data = None
        self.analysis_results = None
        self._setup_logging()
        self.load_data()
        print(f"🚀 DEBUG: Q345DataProcessor initialization completed")
        print(f"📊 DEBUG: Data loading status - data: {self.data is not None and not self.data.empty}, other_data: {self.other_data is not None and not self.other_data.empty}")
        if self.other_data is not None and not self.other_data.empty:
            print(f"📋 DEBUG: other_data columns: {len(self.other_data.columns)}, rows: {len(self.other_data)}")
            print(f"📋 DEBUG: other_data column names: {list(self.other_data.columns)}")
    
    def _setup_logging(self):
        """Setup logging system"""
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        # Create logger without affecting global configuration
        self.logger = logging.getLogger('Q345DataProcessor')
        self.logger.setLevel(logging.WARNING)  # Reduce log level to WARNING to reduce noise
        
        # Only add handlers if not already present
        if not self.logger.handlers:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            log_filename = f'logs/q345_data_processor_{timestamp}.log'
            
            # File handler
            file_handler = logging.FileHandler(log_filename, encoding='utf-8')
            file_handler.setLevel(logging.INFO)
            
            # Console handler with higher level to reduce console noise
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.WARNING)
            
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
        
        self.logger.info(f"Q345 Data Processor initialized")
    
    def load_data(self):
        """Load analysis results data with real-time refresh capability"""
        try:
            self.data = pd.read_csv(self.csv_file_path, encoding='utf-8-sig')
            self.logger.info(f"Data loaded successfully: {len(self.data)} records")
            self.logger.info(f"Data columns: {list(self.data.columns)}")
            
            # Load other options data
            try:
                # CSV file has headers on row 3 (index 2), skip first 2 rows
                self.other_data = pd.read_csv(self.other_file_path, encoding='utf-8-sig', header=2)
                self.logger.info(f"Other data loaded successfully: {len(self.other_data)} records")
                self.logger.info(f"Other data columns: {list(self.other_data.columns)}")
            except Exception as e:
                self.logger.warning(f"Other data loading failed: {e}")
                self.other_data = pd.DataFrame()
            
            # Process analysis results
            self._process_analysis_results()
            
            # Display region loading information
            self._display_region_loading_info()

        except Exception as e:
            self.logger.error(f"Data loading failed: {e}")
            print(f"Q345 Data loading failed: {e}")
            self.data = pd.DataFrame()
            self.other_data = pd.DataFrame()
            self.analysis_results = None
    
    def _process_analysis_results(self):
        """Process data and generate analysis results"""
        if self.data is None or self.data.empty:
            self.analysis_results = None
            return
        
        try:
            # Calculate statistics for each group
            q3_data = self.data[self.data['group'] == 'Q3']
            q4_data = self.data[self.data['group'] == 'Q4']
            q5_data = self.data[self.data['group'] == 'Q5']
            
            # Use 'count' column instead of 'yes_count' and 'total_count' instead of 'total_responses'
            self.analysis_results = {
                'q3_count': len(q3_data),
                'q4_count': len(q4_data),
                'q5_count': len(q5_data),
                'total_questions': len(self.data),
                'total_responses': self.data['count'].sum() if 'count' in self.data.columns else 0,
                'q3_total_responses': q3_data['total_count'].iloc[0] if not q3_data.empty and 'total_count' in q3_data.columns else 0,
                'q4_total_responses': q4_data['total_count'].iloc[0] if not q4_data.empty and 'total_count' in q4_data.columns else 0,
                'q5_total_responses': q5_data['total_count'].iloc[0] if not q5_data.empty and 'total_count' in q5_data.columns else 0
            }
            
            self.logger.info(f"Analysis results processed: {self.analysis_results}")
        except Exception as e:
            self.logger.error(f"Error processing analysis results: {e}")
            self.analysis_results = None
    
    def _display_region_loading_info(self):
        """Display region data loading information"""
        try:
            loaded_info = []
            
            # Analysis results data info
            if self.data is not None and not self.data.empty:
                # Get unique regions from analysis data
                if 'region' in self.data.columns:
                    unique_regions = self.data['region'].nunique()
                    total_records = len(self.data)
                    loaded_info.append(f"Analysis results ({total_records} records, {unique_regions} regions)")
                else:
                    total_records = len(self.data)
                    loaded_info.append(f"Analysis results ({total_records} records)")
            
            # Other options data info
            if self.other_data is not None and not self.other_data.empty:
                if 'Department/Region' in self.other_data.columns:
                    unique_regions = self.other_data['Department/Region'].nunique()
                    total_users = self.other_data['UserId'].nunique() if 'UserId' in self.other_data.columns else len(self.other_data)
                    loaded_info.append(f"Other options data ({total_users} users, {unique_regions} regions)")
                else:
                    total_users = self.other_data['UserId'].nunique() if 'UserId' in self.other_data.columns else len(self.other_data)
                    loaded_info.append(f"Other options data ({total_users} users)")
            
            if loaded_info:
                print(f"✓ Q345 module data loading completed: {', '.join(loaded_info)}")
            else:
                print(f"⚠ Q345 module data loading completed: No data available")
                
        except Exception as e:
            print(f"❌ Q345 module region info display error: {e}")
            self.logger.error(f"Error displaying region loading info: {e}")
    
    def get_group_data(self, group: str) -> pd.DataFrame:
        """Get data for specific group (Q3, Q4, or Q5)"""
        if self.data is None or self.data.empty:
            return pd.DataFrame()
        
        return self.data[self.data['group'] == group].copy()
    
    def refresh_data(self):
        """Refresh data from file - enables real-time updates"""
        self.load_data()
    
    def get_groups(self) -> List[str]:
        """Get all available question groups"""
        return ['Q3', 'Q4', 'Q5']
    
    def get_other_options_data(self, question: str, region_filter: str = None) -> List[str]:
        """Get other options elaborated answers for Q4 or Q5"""
        if self.other_data is None or self.other_data.empty:
            print(f"❌ DEBUG: other_data is empty or not loaded")
            return []
        
        print(f"🔍 DEBUG: Getting Other option data for {question}")
        print(f"📊 DEBUG: other_data shape: {self.other_data.shape}")
        print(f"📋 DEBUG: Column list: {list(self.other_data.columns)}")
        

        
        # Map question to correct column name based on actual CSV structure
        column_mapping = {
            'Q4': 'Other (elaborated answ)',      # First occurrence
            'Q5': 'Other (elaborated answ).1'    # Second occurrence (with .1 suffix)
        }
        
        if question not in column_mapping:
            print(f"❌ DEBUG: Question {question} is not in supported question list")
            return []
        
        target_column = column_mapping[question]
        if target_column not in self.other_data.columns:
            print(f"❌ DEBUG: Column '{target_column}' does not exist in data")
            print(f"📋 DEBUG: Available column names: {list(self.other_data.columns)}")
            return []
        
        print(f"📍 DEBUG: {question} using column '{target_column}'")
        
        # Use column name to get the correct data
        try:
            # Apply region filter if specified
            filtered_data = self.other_data
            if region_filter and region_filter != 'all' and 'Department/Region' in self.other_data.columns:
                filtered_data = self.other_data[self.other_data['Department/Region'] == region_filter]
                print(f"🌍 DEBUG: Applied region filter '{region_filter}', filtered data count: {len(filtered_data)}")
            else:
                print(f"🌍 DEBUG: No region filter applied, using all data: {len(filtered_data)} records")
            
            # Get data from the specific column by name
            responses = filtered_data[target_column]
            print(f"📊 DEBUG: {question} column '{target_column}' raw data count: {len(responses)}")
            
            # Debug: show first few raw values
            print(f"🔍 DEBUG: First 5 raw values: {responses.head().tolist()}")
            
            # Filter out empty values and return unique non-empty responses
            responses = responses.dropna()
            print(f"📊 DEBUG: Data count after removing null values: {len(responses)}")
            
            responses = responses[responses.astype(str).str.strip() != '']
            print(f"📊 DEBUG: Data count after removing empty strings: {len(responses)}")
            
            unique_responses = responses.unique().tolist()
            print(f"✅ DEBUG: {question} finally got {len(unique_responses)} unique Other responses")
            
            # Show first few results
            if unique_responses:
                print(f"📝 DEBUG: First 3 Other response examples: {unique_responses[:3]}")
            else:
                print(f"❌ DEBUG: No {question} Other responses found")
            
            return unique_responses
            
        except (KeyError, Exception) as e:
            print(f"❌ DEBUG: Error accessing {question} column '{target_column}': {e}")
            self.logger.error(f"Error accessing column '{target_column}' for {question}: {e}")
            return []
    
    def get_regions(self) -> List[str]:
        """Get all available regions from other_data"""
        if self.other_data is None or self.other_data.empty or 'Department/Region' not in self.other_data.columns:
            self.logger.warning("No other_data or Department/Region column not found")
            return []
        
        regions = self.other_data['Department/Region'].dropna().unique().tolist()
        self.logger.info(f"Found regions: {regions}")
        return sorted(regions)
    
    def get_group_data_by_region(self, group: str, region_filter: str = None) -> pd.DataFrame:
        """Get data for specific group filtered by region"""
        if self.data is None or self.data.empty:
            return pd.DataFrame()
        
        # Get base group data
        group_data = self.data[self.data['group'] == group].copy()
        
        # If no region filter or 'all', return all data
        if not region_filter or region_filter == 'all':
            print(f"📊 DEBUG: get_group_data_by_region({group}, {region_filter}) - returning all data: {len(group_data)} records")
            return group_data
        
        # For region filtering, filter the data based on the region column
        if 'region' in group_data.columns:
            # Direct region filtering if region column exists
            filtered_data = group_data[group_data['region'] == region_filter]
            print(f"📊 DEBUG: get_group_data_by_region({group}, {region_filter}) - direct filter: {len(filtered_data)} records")
            return filtered_data
        else:
            # If no region column in analysis results, return proportional sample
            # This is a fallback approach when region info is not in the analysis results
            if self.other_data is not None and 'Department/Region' in self.other_data.columns:
                # Get the proportion of users from this region
                region_users = self.other_data[self.other_data['Department/Region'] == region_filter]['UserId'].unique()
                total_users = self.other_data['UserId'].unique()
                region_proportion = len(region_users) / len(total_users) if len(total_users) > 0 else 0
                
                print(f"📊 DEBUG: get_group_data_by_region({group}, {region_filter}) - region proportion: {region_proportion:.2f}")
                
                # Apply proportional filtering to group data
                if region_proportion > 0:
                    sample_size = max(1, int(len(group_data) * region_proportion))
                    sampled_data = group_data.head(sample_size)
                    print(f"📊 DEBUG: get_group_data_by_region({group}, {region_filter}) - proportional sample: {len(sampled_data)} records")
                    return sampled_data
            
            print(f"📊 DEBUG: get_group_data_by_region({group}, {region_filter}) - fallback to all data: {len(group_data)} records")
            return group_data
    
    def get_summary_stats(self) -> Dict[str, Dict[str, str]]:
        """Get summary statistics for dashboard cards"""
        if self.analysis_results is None:
            return {
                'stat1': {'value': '0', 'label': 'Total Questions'},
                'stat2': {'value': '0', 'label': 'Q3 Questions'},
                'stat3': {'value': '0', 'label': 'Q4 Questions'},
                'stat4': {'value': '0', 'label': 'Q5 Questions'}
            }
        
        try:
            return {
                'stat1': {
                    'value': str(self.analysis_results['total_questions']),
                    'label': 'Total Questions'
                },
                'stat2': {
                    'value': str(self.analysis_results['q3_count']),
                    'label': f"Q3 Questions ({self.analysis_results['q3_total_responses']} responses)"
                },
                'stat3': {
                    'value': str(self.analysis_results['q4_count']),
                    'label': f"Q4 Questions ({self.analysis_results['q4_total_responses']} responses)"
                },
                'stat4': {
                    'value': str(self.analysis_results['q5_count']),
                    'label': f"Q5 Questions ({self.analysis_results['q5_total_responses']} responses)"
                }
            }
        except Exception as e:
            self.logger.error(f"Error getting summary stats: {e}")
            return {
                'stat1': {'value': 'Error', 'label': 'Total Questions'},
                'stat2': {'value': 'Error', 'label': 'Q3 Questions'},
                'stat3': {'value': 'Error', 'label': 'Q4 Questions'},
                'stat4': {'value': 'Error', 'label': 'Q5 Questions'}
            }

class Q345ComponentFactory:
    """Q345 Component Factory - responsible for creating various UI components"""
    
    def __init__(self, style_manager):
        self.style_manager = style_manager
        self.default_colors = {
            'primary': '#3498db',
            'success': '#2ecc71',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'info': '#17a2b8',
            'secondary': '#6c757d'
        }
    
    def create_summary_card(self, icon: str, value: str, title: str, 
                           subtitle: str = "", footer: str = "", color: str = "primary") -> html.Div:
        """Create summary statistics card"""
        # If hex color value is passed, use directly; otherwise look up from default colors
        if color.startswith('#'):
            card_color = color
        else:
            card_color = self.default_colors.get(color, self.default_colors['primary'])
        
        # Get base card style
        base_style = self.style_manager.get_style('card_style') if self.style_manager else {}
        
        # Define color-related styles
        color_style = {
            'border': f'2px solid {card_color}20',
            'backgroundColor': 'white',
            'padding': '20px',
            'borderRadius': '10px',
            'boxShadow': '0 2px 10px rgba(0,0,0,0.1)'
        }
        
        # Merge styles
        card_style = {**base_style, **color_style}
        
        return html.Div([
            html.Div([
                html.I(className=icon, style={
                    'fontSize': '2.5em',
                    'color': card_color,
                    'marginBottom': '10px'
                }),
                html.H2(value, style={
                    'margin': '0',
                    'color': '#2c3e50',
                    'fontSize': '2.2em',
                    'fontWeight': 'bold'
                }),
                html.P(title, style={
                    'margin': '5px 0',
                    'color': '#34495e',
                    'fontSize': '1.1em',
                    'fontWeight': '600'
                }),
                html.P(subtitle, style={
                    'margin': '0',
                    'color': '#7f8c8d',
                    'fontSize': '0.9em'
                }) if subtitle else None,
                html.Hr(style={'margin': '10px 0', 'border': f'1px solid {card_color}'}),
                html.P(footer, style={
                    'margin': '0',
                    'color': card_color,
                    'fontSize': '0.8em',
                    'fontWeight': '500'
                }) if footer else None
            ], style=card_style)
        ], style={
            'width': '22%',
            'display': 'inline-block',
            'margin': '0 1.5%',
            'verticalAlign': 'top'
        })
    
    def create_chart_container(self, title: str, chart_component, description: str = "") -> html.Div:
        """Create chart container"""
        # Get base container style
        base_style = self.style_manager.get_style('container_style') if self.style_manager else {}
        
        # Define default style
        default_style = {
            'marginBottom': '30px',
            'backgroundColor': 'white',
            'padding': '20px',
            'borderRadius': '10px',
            'boxShadow': '0 2px 10px rgba(0,0,0,0.1)'
        }
        
        # Merge styles
        container_style = {**base_style, **default_style}
        
        return html.Div([
            html.H3(self.style_manager._wrap_title(title) if self.style_manager else title, style={
                'textAlign': 'center',
                'color': '#2c3e50',
                'marginBottom': '5px',
                'fontSize': '1.2em',
                'whiteSpace': 'pre-line',
                'lineHeight': '1.3'
            }),
            html.P(description, style={
                'textAlign': 'center',
                'color': '#7f8c8d',
                'marginBottom': '20px',
                'fontSize': '0.9em'
            }) if description else None,
            html.Div(chart_component, style={'textAlign': 'center'})
        ], style=container_style)
    
    def create_pie_chart(self, data: pd.DataFrame, group: str) -> go.Figure:
        """Create pie chart or bar chart based on data size - using global standardized styles"""
        if data.empty:
            return self._create_empty_chart(f"No data available for {group}")
        
        print(f"📊 DEBUG: Creating chart for {group}")
        print(f"📊 DEBUG: Data shape: {data.shape}")
        print(f"📊 DEBUG: Data columns: {list(data.columns)}")
        print(f"📊 DEBUG: First 3 rows:\n{data.head(3)}")
        
        # Convert data format to dictionary to match standardized method
        # The data structure from Q345 analysis results has 'option' and 'yes_count' columns
        if 'option' in data.columns and 'yes_count' in data.columns:
            # Filter out zero counts
            filtered_data = data[data['yes_count'] > 0]
            print(f"📊 DEBUG: After filtering zero counts: {len(filtered_data)} records")
            if filtered_data.empty:
                return self._create_empty_chart(f"No responses for {group}")
            data_dict = dict(zip(filtered_data['option'], filtered_data['yes_count']))
        elif 'option' in data.columns and 'count' in data.columns:
            # Alternative data structure
            filtered_data = data[data['count'] > 0]
            print(f"📊 DEBUG: After filtering zero counts: {len(filtered_data)} records")
            if filtered_data.empty:
                return self._create_empty_chart(f"No responses for {group}")
            data_dict = dict(zip(filtered_data['option'], filtered_data['count']))
        else:
            print(f"❌ DEBUG: Unexpected data structure for {group}: {list(data.columns)}")
            return self._create_empty_chart(f"Invalid data structure for {group}")
        
        # Determine chart type based on number of items
        chart_type = 'bar' if len(data_dict) >= 5 else 'pie'
        print(f"📊 DEBUG: Creating {chart_type} chart for {group} with {len(data_dict)} items")
        print(f"📊 DEBUG: Data dict keys: {list(data_dict.keys())[:3]}...")
        
        # Use style manager's standardized chart creation method
        try:
            fig = self.style_manager.create_standardized_chart(
                data=data_dict,
                chart_type=chart_type,
                title=f"{group} Response Distribution"
            )
            print(f"✅ DEBUG: Successfully created {chart_type} chart for {group}")
            return fig
        except Exception as e:
            print(f"❌ DEBUG: Error creating {chart_type} chart for {group}: {e}")
            return self._create_empty_chart(f"Error creating chart for {group}: {str(e)}")
    
    def _create_empty_chart(self, message: str) -> go.Figure:
        """Create an empty chart with a message"""
        fig = go.Figure()
        fig.add_annotation(
            text=message,
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            xanchor='center', yanchor='middle',
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            plot_bgcolor='white'
        )
        return fig

class Q345Dashboard:
    """Q345 Analysis Dashboard"""
    
    def __init__(self, data_path: str = None):
        """Initialize the dashboard"""
        print(f"🚀 DEBUG: Q345Dashboard initialization started")
        self.data_processor = Q345DataProcessor(data_path)
        print(f"🚀 DEBUG: Q345DataProcessor created")
        self.style_manager = style_manager
        self.component_factory = Q345ComponentFactory(style_manager)
        self.groups = self.data_processor.get_groups()
        
        # Log initialization
        print(f"🚀 DEBUG: Q345Dashboard initialized with {len(self.groups)} groups")
        logger.info(f"Q345Dashboard initialized with {len(self.groups)} groups")
    
    def get_groups(self) -> List[str]:
        """Get all available groups (Q3, Q4, Q5)"""
        if self.data_processor.data is None or self.data_processor.data.empty:
            return []
        return sorted(self.data_processor.data['group'].unique().tolist())
    
    def get_summary_stats(self) -> Dict[str, Dict[str, str]]:
        """Get summary statistics data"""
        return self.data_processor.get_summary_stats()
    
    # def create_summary_cards(self) -> html.Div:
    #     """Create summary statistics cards"""
    #     stats = self.get_summary_stats()
    #     
    #     # Define card configurations - unified color scheme consistent with other modules
    #     card_configs = {
    #         "stat1": {"icon": "fas fa-question-circle", "color": "#3498db", "footer": "Total questions"},
    #         "stat2": {"icon": "fas fa-chart-bar", "color": "#27ae60", "footer": "Q3 questions"},
    #         "stat3": {"icon": "fas fa-chart-pie", "color": "#f39c12", "footer": "Q4 questions"},
    #         "stat4": {"icon": "fas fa-chart-line", "color": "#e74c3c", "footer": "Q5 questions"}
    #     }
    #     
    #     cards = []
    #     for stat_key, stat_data in stats.items():
    #         config = card_configs.get(stat_key, {"icon": "fas fa-info", "color": "#95a5a6", "footer": "Data point"})
    #         card = self.component_factory.create_summary_card(
    #             icon=config["icon"],
    #             value=str(stat_data["value"]),
    #             title=stat_data["label"],
    #             subtitle="",
    #             footer=config["footer"],
    #             color=config["color"]
    #         )
    #         cards.append(card)
    #     
    #     return html.Div(cards, style={
    #         'textAlign': 'center', 
    #         'marginBottom': '30px', 
    #         'width': '100%',
    #         'maxWidth': '1200px',
    #         'margin': '0 auto'
    #     })
    
    def create_summary_cards(self) -> html.Div:
        """Create summary statistics cards - Hidden for now"""
        # Return empty div to hide summary cards
        return html.Div([], style={'display': 'none'})
    
    def create_other_options_display(self, question: str, region_filter: str = None) -> html.Div:
        """Create display for 'Other' options elaborated answers"""
        print(f"🔍 DEBUG: create_other_options_display called, question={question}, region_filter={region_filter}")
        
        # Hide Q4 and Q5 Other Responses completely
        if question in ['Q4', 'Q5']:
            return html.Div()  # Return empty div for Q4 and Q5
        
        other_responses = self.data_processor.get_other_options_data(question, region_filter)
        
        if not other_responses:
            print(f"❌ DEBUG: {question} no other responses found")
            # Q3 has no other options, don't show prompt message
            if question == 'Q3':
                return html.Div()  # Return empty div
            
            region_text = f" for {region_filter}" if region_filter and region_filter != 'all' else ""
            return html.Div(
                f"No 'Other' responses available for this question{region_text}.",
                style={
                    'padding': '20px',
                    'backgroundColor': '#f8f9fa',
                    'borderRadius': '5px',
                    'color': '#6c757d',
                    'textAlign': 'center',
                    'fontStyle': 'italic'
                }
            )
        
        # Create response items with card-style design (left-aligned)
        response_items = []
        for i, response in enumerate(other_responses, 1):
            response_items.append(
                html.Div([
                    html.Div(f"{i}.", style={
                        'fontWeight': 'bold',
                        'color': '#3498db',
                        'marginRight': '10px',
                        'minWidth': '25px'
                    }),
                    html.Div(response, style={
                        'flex': '1',
                        'lineHeight': '1.5',
                        'textAlign': 'left'  # Ensure text is left-aligned
                    })
                ], style={
                    'display': 'flex',
                    'alignItems': 'flex-start',
                    'marginBottom': '12px',
                    'padding': '15px',
                    'backgroundColor': 'white',
                    'borderRadius': '8px',
                    'border': '1px solid #e9ecef',
                    'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
                    'transition': 'transform 0.2s ease, box-shadow 0.2s ease',
                    'cursor': 'default'
                })
            )
        
        region_text = f" ({region_filter})" if region_filter and region_filter != 'all' else ""
        return html.Div([
            html.H5(f"{question} - Other Responses{region_text}:", style={
                'color': '#2c3e50',
                'marginBottom': '20px',
                'fontWeight': 'bold',
                'fontSize': '1.3em',
                'textAlign': 'left'  # Title also left-aligned
            }),
            html.Div(response_items, style={
                'maxHeight': '300px',
                'overflowY': 'auto',
                'padding': '5px',
                'textAlign': 'left'  # Container left-aligned
            })
        ], style={
            'backgroundColor': '#f8f9fa',
            'padding': '25px',
            'borderRadius': '12px',
            'boxShadow': '0 4px 15px rgba(0,0,0,0.1)',
            'marginTop': '25px',
            'border': '1px solid #dee2e6'
        })
    
    def _get_region_options(self) -> List[Dict[str, str]]:
        """Get region options for dropdown"""
        regions = self.data_processor.get_regions()
        options = [{'label': 'All Department/Region', 'value': 'all'}]
        
        for region in regions:
            options.append({'label': region, 'value': region})
        
        return options
    
    def get_layout(self):
        """Get dashboard layout - standard interface method"""
        return self.create_layout()
    
    def setup_callbacks(self, app):
        """Setup callback functions - standard interface method"""
        logger.info("Q345 module callbacks registered automatically via decorators")
        
        @app.callback(
            [Output('q345-q3-chart', 'figure'),
             Output('q345-q4-chart', 'figure'),
             Output('q345-q5-chart', 'figure'),
             Output('q345-q3-other', 'children'),
             Output('q345-q4-other', 'children'),
             # Output('q345-q5-other', 'children'),  # Q5 Other Responses commented out
             Output('q345-summary-stats', 'children')],
            [Input('q345-chart-type', 'value'),
             Input('q345-region-filter', 'value')]
        )
        def update_q345_charts(chart_type, region_filter):
            """Update Q345 charts and summary statistics with region filter"""
            try:
                print(f"🔄 Q345 callback triggered - chart_type: {chart_type}, region_filter: {region_filter}")
                
                # Refresh data to ensure latest
                self.data_processor.refresh_data()
                
                # Debug: Check data status
                print(f"📊 Data status check:")
                print(f"   - data loaded: {self.data_processor.data is not None and not self.data_processor.data.empty}")
                print(f"   - other_data loaded: {self.data_processor.other_data is not None and not self.data_processor.other_data.empty}")
                
                if self.data_processor.data is not None:
                    print(f"   - data shape: {self.data_processor.data.shape}")
                    print(f"   - data columns: {list(self.data_processor.data.columns)}")
                    print(f"   - unique groups: {self.data_processor.data['group'].unique() if 'group' in self.data_processor.data.columns else 'No group column'}")
                
                # Output region filter information
                if region_filter and region_filter != 'all':
                    # Get data count for this region (from other_data)
                    if hasattr(self.data_processor, 'other_data') and not self.data_processor.other_data.empty and 'Department/Region' in self.data_processor.other_data.columns:
                        region_data = self.data_processor.other_data[self.data_processor.other_data['Department/Region'] == region_filter]
                        filtered_count = len(region_data)
                        print(f"✓ {region_filter} region loaded successfully, loaded {filtered_count} records")
                    else:
                        print(f"✓ {region_filter} region filter applied")
                else:
                    if hasattr(self.data_processor, 'other_data') and not self.data_processor.other_data.empty:
                        total_count = len(self.data_processor.other_data)
                        print(f"✓ All regions loaded successfully, loaded {total_count} records")
                    else:
                        total_count = len(self.data_processor.data) if hasattr(self.data_processor, 'data') and not self.data_processor.data.empty else 0
                        print(f"✓ All regions loaded successfully, loaded {total_count} analysis results")
                
                # Create charts for each group with region filter
                print(f"📈 Getting group data...")
                if region_filter == 'all':
                    q3_data = self.data_processor.get_group_data('Q3')
                    q4_data = self.data_processor.get_group_data('Q4')
                    q5_data = self.data_processor.get_group_data('Q5')
                else:
                    q3_data = self.data_processor.get_group_data_by_region('Q3', region_filter)
                    q4_data = self.data_processor.get_group_data_by_region('Q4', region_filter)
                    q5_data = self.data_processor.get_group_data_by_region('Q5', region_filter)
                
                print(f"📊 Group data shapes - Q3: {q3_data.shape}, Q4: {q4_data.shape}, Q5: {q5_data.shape}")
                
                if chart_type == 'pie':
                    q3_chart = self.component_factory.create_pie_chart(q3_data, 'Q3')
                    q4_chart = self.component_factory.create_pie_chart(q4_data, 'Q4')
                    q5_chart = self.component_factory.create_pie_chart(q5_data, 'Q5')
                else:  # bar chart
                    q3_chart = self.component_factory._create_empty_chart("Bar chart not implemented yet")
                    q4_chart = self.component_factory._create_empty_chart("Bar chart not implemented yet")
                    q5_chart = self.component_factory._create_empty_chart("Bar chart not implemented yet")
                
                # Create other options displays with region filter
                q3_other = self.create_other_options_display('Q3', region_filter)
                q4_other = self.create_other_options_display('Q4', region_filter)
                # q5_other = self.create_other_options_display('Q5', region_filter)  # Q5 Other Responses commented out
                
                # Update summary statistics cards
                summary_cards = self.create_summary_cards()
                
                return q3_chart, q4_chart, q5_chart, q3_other, q4_other, summary_cards
                
            except Exception as e:
                logger.error(f"Error updating Q345 charts: {e}")
                empty_fig = self.component_factory._create_empty_chart("Error loading data")
                empty_other = html.Div("Error loading other options")
                summary_cards = self.create_summary_cards()
                return empty_fig, empty_fig, empty_fig, empty_other, empty_other, summary_cards
    
    def get_module_stats(self) -> Dict[str, Any]:
        """Get module statistics - standard interface method"""
        if self.data_processor.analysis_results is None:
            return {
                'total_records': 0,
                'q3_count': 0,
                'q4_count': 0,
                'q5_count': 0
            }
        
        try:
            return {
                'total_records': self.data_processor.analysis_results['total_questions'],
                'q3_count': self.data_processor.analysis_results['q3_count'],
                'q4_count': self.data_processor.analysis_results['q4_count'],
                'q5_count': self.data_processor.analysis_results['q5_count']
            }
        except Exception as e:
            logger.error(f"Error getting module stats: {e}")
            return {
                'total_records': 0,
                'q3_count': 0,
                'q4_count': 0,
                'q5_count': 0
            }
    
    def get_module_info(self) -> Dict[str, str]:
        """Get module information - standard interface method"""
        return {
            'name': 'Q345 Analysis Dashboard',
            'version': '2.0.0',
            'description': 'Q3, Q4, Q5 question analysis results display module',
            'questions': 'Q3, Q4, Q5',
            'data_source': 'q345_analysis_results_new.csv'
        }
    
    def create_layout(self):
        """Create the main dashboard layout"""
        return html.Div([
            # Back button
            html.Div([
                html.Button(
                    "← Back to Home",
                    id="btn-back-to-home",
                    style={
                        'backgroundColor': '#95a5a6',
                        'color': 'white',
                        'border': 'none',
                        'padding': '10px 20px',
                        'borderRadius': '5px',
                        'cursor': 'pointer',
                        'fontSize': '14px',
                        'marginBottom': '20px'
                    }
                )
            ], style={'textAlign': 'left'}),
            
            # Page title
            html.Div([
                html.H1(
                    "Overview of 2024 outputs",
                    style={
                        'textAlign': 'center',
                        'color': '#2c3e50',
                        'marginBottom': '30px',
                        'fontSize': '28px',
                        'fontWeight': 'bold'
                    }
                )
            ], style={'textAlign': 'center'}),
            
            # Summary statistics cards
            html.Div([
                html.H2("📊 Summary Statistics", style={'color': '#2c3e50', 'marginBottom': '20px', 'textAlign': 'center'}),
                html.Div(id='q345-summary-stats', children=self.create_summary_cards())
            ], style={'marginBottom': '40px', 'textAlign': 'center'}),
            
            # Control panel
            html.Div([
                html.H3("Control Panel", style={
                    'color': '#2c3e50',
                    'marginBottom': '20px',
                    'textAlign': 'center'
                }),
                html.Div([
                    # Region filter
                    html.Div([
                        html.Label("Select Organizational Unit:", style={
                            'fontWeight': 'bold', 
                            'marginBottom': '10px',
                            'color': '#2c3e50',
                            'display': 'block',
                            'textAlign': 'center'
                        }),
                        dcc.Dropdown(
                            id='q345-region-filter',
                            options=self._get_region_options(),
                            value='all',  # Default to all regions
                            style={
                                'marginBottom': '20px',
                                'borderRadius': '5px',
                                'maxWidth': '300px',
                                'textAlign': 'left'  # 设置为左对齐
                            }
                        )
                    ], style={'marginBottom': '20px'}),
                    
                    # Hidden chart type selector - only pie chart
                    html.Div([
                        # Hidden dropdown to maintain compatibility
                        dcc.Dropdown(
                            id='q345-chart-type',
                            options=[{'label': 'Pie Chart', 'value': 'pie'}],
                            value='pie',
                            style={'display': 'none'}  # Hide the dropdown
                        )
                    ], style={'display': 'none'})
                ], style={
                    'maxWidth': '400px', 
                    'margin': '0 auto', 
                    'marginBottom': '30px',
                    'backgroundColor': 'white',
                    'padding': '20px',
                    'borderRadius': '10px',
                    'boxShadow': '0 2px 10px rgba(0,0,0,0.1)'
                })
            ], style={'textAlign': 'center', 'marginBottom': '30px'}),
            
            # Charts display area - all groups shown, no side-by-side tables
            html.Div([
                # Q3 Chart
                html.Div([
                    self.component_factory.create_chart_container(
                        title='Distribution Of Outputs Across The Clusters Of The Implementation Framework',
                        chart_component=dcc.Graph(id='q345-q3-chart', style={'height': '400px'})
                    )
                ], style={'marginBottom': '30px'}),
                
                # Q3 Other options
                html.Div(id='q345-q3-other', children=self.create_other_options_display('Q3', 'all')),
                
                # Q4 Chart
                html.Div([
                    self.component_factory.create_chart_container(
                        title='Distribution Of Outputs Across The Pillars Of The Call For Action On Youth Employment',
                        chart_component=dcc.Graph(id='q345-q4-chart', style={'height': '400px'})
                    )
                ], style={'marginBottom': '30px'}),
                
                # Q4 Other options
                html.Div(id='q345-q4-other', children=self.create_other_options_display('Q4', 'all')),
                
                # Q5 Chart
                html.Div([
                    self.component_factory.create_chart_container(
                        title='Distribution Of Outputs Across Target Youth Groups, When Applicable',
                        chart_component=dcc.Graph(id='q345-q5-chart', style={'height': '400px'})
                    )
                ], style={'marginBottom': '30px'}),
                
                # Q5 Other options
                # html.Div(id='q345-q5-other', children=self.create_other_options_display('Q5', 'all'))
            ], style={'marginBottom': '40px', 'textAlign': 'center'})
            
        ], style={
            'maxWidth': '1400px',
            'margin': '0 auto',
            'padding': '20px',
            'fontFamily': 'Arial, sans-serif',
            'backgroundColor': '#f8f9fa',
            'minHeight': '100vh',
            'textAlign': 'center'
        })

# Global instance will be created by the main application
q345_dashboard = None

def get_layout():
    """
    Get Q345 dashboard layout
    Note: This function is for backward compatibility.
    The main application should create its own Q345Dashboard instance.
    """
    global q345_dashboard
    if q345_dashboard is None:
        q345_dashboard = Q345Dashboard()
    return q345_dashboard.create_layout()