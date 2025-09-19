import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, List, Any
import logging
import datetime
import os
import json

# Import existing modules
from data_handler import DataHandler
from visualizer import visualizer

# Import style manager if available
try:
    from styles import style_manager
except ImportError:
    style_manager = None

class GeneralDataProcessor:
    """General Survey Data Processing Class - Handles data loading and analysis"""
    
    def __init__(self, csv_file_path: str = "orignaldata/question_response_count_statistics.csv"):
        self.csv_file_path = csv_file_path
        self.data_handler = DataHandler()
        self.questions_data = {}
        self.analysis_results = None
        self.unique_users_count = 0
        self._setup_logging()
        self.load_data()
        self._load_user_data()
    
    def _setup_logging(self):
        """Setup logging system"""
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        log_filename = f'logs/general_data_processor_{timestamp}.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler(log_filename, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger('GeneralDataProcessor')
        self.logger.info(f"General Data Processor initialized, log file: {log_filename}")
    
    def load_data(self):
        """Load survey data with real-time refresh capability"""
        try:
            self.questions_data = self.data_handler.import_data_from_external(self.csv_file_path, 'csv')
            self.logger.info(f"Data loaded successfully: {len(self.questions_data)} questions")
            
            # Merge Other options for Q4 and Q5
            self._merge_other_options()
            
            # Process analysis results
            self._process_analysis_results()
            
            print(f"General Survey Data loaded: {len(self.questions_data)} questions")
        except Exception as e:
            self.logger.error(f"Data loading failed: {e}")
            print(f"General Survey Data loading failed: {e}")
            self.questions_data = {}
            self.analysis_results = None
    
    def _process_analysis_results(self):
        """Process data and generate analysis results"""
        if not self.questions_data:
            self.analysis_results = None
            return
        
        try:
            total_questions = len(self.questions_data)
            total_responses = 0
            max_responses = 0
            avg_responses = 0
            
            # Calculate statistics
            # Data structure: {question_name: {option: count, ...}, ...}
            for question, options_data in self.questions_data.items():
                if isinstance(options_data, dict):
                    # Sum all option counts for this question
                    question_total = sum(count for count in options_data.values() if isinstance(count, (int, float)))
                    total_responses += question_total
                    max_responses = max(max_responses, question_total)
            
            if total_questions > 0:
                avg_responses = total_responses / total_questions
            
            self.analysis_results = {
                'total_questions': total_questions,
                'total_responses': total_responses,
                'max_responses': max_responses,
                'avg_responses': round(avg_responses, 1)
            }
            
            self.logger.info(f"Analysis results processed: {self.analysis_results}")
        except Exception as e:
            self.logger.error(f"Error processing analysis results: {e}")
            self.analysis_results = None
    
    def get_summary_stats(self) -> Dict[str, Dict[str, str]]:
        """Get summary statistics data for main application cards"""
        if not self.analysis_results:
            return {
                "stat1": {"value": "--", "label": "Total Questions"},
                "stat2": {"value": "--", "label": "Total Responses"},
                "stat3": {"value": "--", "label": "Avg Responses"},
                "stat4": {"value": "--", "label": "Total Participants"}
            }
        
        return {
            "stat1": {
                "value": str(self.analysis_results['total_questions']),
                "label": "Total Questions"
            },
            "stat2": {
                "value": str(self.analysis_results['total_responses']),
                "label": "Total Responses"
            },
            "stat3": {
                "value": str(self.analysis_results['avg_responses']),
                "label": "Avg Responses"
            },
            "stat4": {
                "value": str(self.unique_users_count),
                "label": "Total Participants"
            }
        }
    
    def get_questions_data(self) -> Dict[str, Any]:
        """Get all questions data"""
        return self.questions_data
    
    def get_question_data(self, question: str) -> Dict[str, Any]:
        """Get data for specific question"""
        return self.questions_data.get(question, {})
    
    def refresh_data(self):
        """Refresh data from file - enables real-time updates"""
        self.load_data()
    
    def _merge_other_options(self):
        """Merge 'Other' and 'Other (elaborated answ)' options for Q4 and Q5 questions"""
        if not self.questions_data:
            return
        
        try:
            for question_key, options_data in self.questions_data.items():
                # Check if this is a Q4 or Q5 question
                if ('Q4:' in question_key or 'Q5:' in question_key) and isinstance(options_data, dict):
                    other_count = 0
                    other_elaborated_count = 0
                    
                    # Get counts for both Other options
                    if 'Other' in options_data:
                        other_count = options_data['Other']
                    if 'Other (elaborated answ)' in options_data:
                        other_elaborated_count = options_data['Other (elaborated answ)']
                    
                    # If both exist, merge them
                    if other_count > 0 or other_elaborated_count > 0:
                        # Remove the separate options
                        if 'Other' in options_data:
                            del options_data['Other']
                        if 'Other (elaborated answ)' in options_data:
                            del options_data['Other (elaborated answ)']
                        
                        # Add merged option
                        options_data['Other'] = other_count + other_elaborated_count
                        
                        self.logger.info(f"Merged Other options for {question_key}: {other_count} + {other_elaborated_count} = {other_count + other_elaborated_count}")
        
        except Exception as e:
            self.logger.error(f"Error merging Other options: {e}")
    
    def _load_user_data(self):
        """Load original data files to count unique users"""
        try:
            unique_users = set()
            
            # Load Q8Q9 data (skip first 2 rows as they contain headers)
            q8q9_path = "orignaldata/Q8Q9_basic_data.csv"
            if os.path.exists(q8q9_path):
                q8q9_df = pd.read_csv(q8q9_path, encoding='utf-8', skiprows=2)
                if len(q8q9_df.columns) > 0:
                    # First column contains UserId
                    user_ids = q8q9_df.iloc[:, 0].dropna().unique()
                    unique_users.update(user_ids)
                    self.logger.info(f"Q8Q9 data: {len(user_ids)} unique users")
            
            # Load Q6Q7Q10Q11 data
            q6q7q10q11_path = "orignaldata/Q6Q7Q10Q11_basic_data.csv"
            if os.path.exists(q6q7q10q11_path):
                q6q7q10q11_df = pd.read_csv(q6q7q10q11_path, encoding='utf-8')
                if 'UserId' in q6q7q10q11_df.columns:
                    unique_users.update(q6q7q10q11_df['UserId'].dropna().unique())
                    self.logger.info(f"Q6Q7Q10Q11 data: {len(q6q7q10q11_df['UserId'].dropna().unique())} unique users")
            
            self.unique_users_count = len(unique_users)
            self.logger.info(f"Total unique users across all data: {self.unique_users_count}")
            
        except Exception as e:
            self.logger.error(f"Error loading user data: {e}")
            self.unique_users_count = 0
    
    def _extract_question_number(self, question_text: str) -> int:
        """Extract question number from question text for sorting"""
        import re
        match = re.match(r'^[Qq](\d+):', question_text)
        if match:
            return int(match.group(1))
        return 999

class GeneralComponentFactory:
    """General Survey Component Factory - Creates standardized UI components"""
    
    def __init__(self, style_manager, data_processor):
        self.style_manager = style_manager
        self.data_processor = data_processor
    
    def create_summary_card(self, icon: str, value: str, title: str, subtitle: str, footer: str, color: str) -> html.Div:
        """Create standardized summary card with responsive design"""
        # Get base card style from style manager
        try:
            base_card_style = self.style_manager.get_global_chart_config('card_style') if self.style_manager else {}
        except:
            base_card_style = {}
        
        # Default card style if style_manager is not available
        default_card_style = {
            'backgroundColor': 'white',
            'borderRadius': '12px',
            'padding': '25px',
            'textAlign': 'center',
            'boxShadow': '0 4px 15px rgba(0,0,0,0.1)',
            'transition': 'transform 0.3s ease, boxShadow 0.3s ease',
            'height': '200px',
            'display': 'flex',
            'flexDirection': 'column',
            'justifyContent': 'center'
        }
        
        # Merge styles with color-specific border
        card_style = {**default_card_style, **base_card_style}
        card_style['border'] = f'2px solid {color}20'
        
        return html.Div([
            html.Div([
                html.I(className=icon, style={
                    'fontSize': '2.5em',
                    'color': color,
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
                }),
                html.Hr(style={'margin': '10px 0', 'border': f'1px solid {color}'}),
                html.P(footer, style={
                    'margin': '0',
                    'color': color,
                    'fontSize': '0.8em',
                    'fontWeight': '500'
                })
            ], style=card_style)
        ], style={
            'flex': '1',
            'minWidth': '200px',
            'maxWidth': '300px'
        })
    
    def create_chart_container(self, chart_id: str, title: str, description: str = "") -> html.Div:
        """Create standardized chart container with responsive design"""
        # Get container style from style manager
        try:
            container_style = self.style_manager.get_global_chart_config('container_style') if self.style_manager else {}
        except:
            container_style = {}
        
        # Default container style if style_manager is not available
        default_container_style = {
            'backgroundColor': 'white',
            'borderRadius': '10px',
            'padding': '20px',
            'marginBottom': '30px',
            'boxShadow': '0 2px 10px rgba(0,0,0,0.1)',
            'border': '1px solid #e9ecef'
        }
        
        # Merge styles
        final_container_style = {**default_container_style, **container_style}
        
        return html.Div([
            # html.H3(title, style={
            #     'textAlign': 'center',
            #     'color': '#2c3e50',
            #     'marginBottom': '10px',
            #     'fontSize': '1.4em'
            # }),
            html.P(description, style={
                'textAlign': 'center',
                'color': '#7f8c8d',
                'marginBottom': '20px',
                'fontSize': '0.9em'
            }) if description else None,
            dcc.Graph(
                id=chart_id, 
                style={
                    'height': '400px'
                },
                config={
                    'responsive': True,
                    'displayModeBar': True,
                    'displaylogo': False,
                    'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d']
                }
            )
        ], style=final_container_style)
    
    def create_control_panel(self) -> html.Div:
        """Create control panel with dropdowns only"""
        return html.Div([
            html.Div([
                html.Div([
                    html.Label("Select Question:", style={'marginRight': '10px', 'fontWeight': 'bold'}),
                    dcc.Dropdown(
                        id='general-question-dropdown',
                        options=[],
                        value=None,
                        style={
                            'width': '100%', 
                            'marginBottom': '10px',
                            'fontSize': '13px',
                            'lineHeight': '1.4'
                        },
                        optionHeight=80
                    )
                ], style={'flex': '1', 'marginRight': '20px'}),
                
                html.Div([
                    html.Label("Chart Type:", style={'marginRight': '10px', 'fontWeight': 'bold'}),
                    dcc.Dropdown(
                        id='general-chart-type-dropdown',
                        options=[
                            {'label': '📊 Bar Chart', 'value': 'bar'},
                            {'label': '📈 Horizontal Bar Chart', 'value': 'horizontal_bar'},
                            {'label': '🥧 Pie Chart', 'value': 'pie'}
                        ],
                        value='bar',
                        style={
                            'width': '100%', 
                            'marginBottom': '10px',
                            'fontSize': '13px',
                            'lineHeight': '1.6'
                        },
                        optionHeight=40
                    )
                ], style={'flex': '1'})
            ], style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '0px'})
        ], style={
            'backgroundColor': 'white',
            'borderRadius': '10px',
            'padding': '20px',
            'marginBottom': '30px',
            'boxShadow': '0 2px 10px rgba(0,0,0,0.1)',
            'border': '1px solid #e9ecef'
        })

class GeneralDashboard:
    """General Survey Dashboard Main Class - Standard Interface Implementation"""
    
    def __init__(self, csv_file_path: str = "orignaldata/question_response_count_statistics.csv"):
        self.data_processor = GeneralDataProcessor(csv_file_path)
        self.component_factory = GeneralComponentFactory(style_manager, self.data_processor)
        self.style_manager = style_manager
        self.visualizer = visualizer
    
    # def create_summary_cards(self) -> List[html.Div]:
    #     """Create summary statistics cards"""
    #     # Refresh data to ensure real-time updates
    #     self.data_processor.refresh_data()
    #     
    #     stats = self.data_processor.get_summary_stats()
    #     
    #     cards = [
    #         self.component_factory.create_summary_card(
    #             icon="fas fa-question-circle",
    #             value=stats["stat1"]["value"],
    #             title=stats["stat1"]["label"],
    #             subtitle="Survey Questions",
    #             footer="Total Count",
    #             color="#3498db"
    #         ),
    #         self.component_factory.create_summary_card(
    #             icon="fas fa-chart-bar",
    #             value=stats["stat2"]["value"],
    #             title=stats["stat2"]["label"],
    #             subtitle="Survey Responses",
    #             footer="Total Count",
    #             color="#27ae60"
    #         ),
    #         self.component_factory.create_summary_card(
    #             icon="fas fa-calculator",
    #             value=stats["stat3"]["value"],
    #             title=stats["stat3"]["label"],
    #             subtitle="Per Question",
    #             footer="Average",
    #             color="#f39c12"
    #         ),
    #         self.component_factory.create_summary_card(
    #             icon="fas fa-trophy",
    #             value=stats["stat4"]["value"],
    #             title=stats["stat4"]["label"],
    #             subtitle="Single Question",
    #             footer="Maximum",
    #             color="#e74c3c"
    #         )
    #     ]
    #     
    #     return cards
    
    def create_summary_cards(self) -> List[html.Div]:
        """Create summary statistics cards - Hidden for now"""
        # Return empty list to hide summary cards
        return []
    
    def get_layout(self) -> html.Div:
        """Get complete dashboard layout - Standard Interface Method"""
        return html.Div([
            # Back button
            html.Div([
                html.A("← Back to Home", href="/", style={
                    'backgroundColor': '#34495e',
                    'color': 'white',
                    'textDecoration': 'none',
                    'padding': '10px 20px',
                    'borderRadius': '5px',
                    'marginBottom': '20px',
                    'display': 'inline-block',
                    'fontWeight': 'bold'
                })
            ]),
            
            # Page title
            html.H1("General Survey Analysis", style={
                'textAlign': 'center',
                'color': '#2c3e50',
                'marginBottom': '10px',
                'fontSize': '28px',
                'fontWeight': 'bold'
            }),
            
            html.P(
                "Comprehensive analysis of all survey questions with interactive visualization and data exploration",
                style={
                    'textAlign': 'center',
                    'color': '#7f8c8d',
                    'marginBottom': '30px',
                    'fontSize': '16px'
                }
            ),
            
            # Summary statistics cards - Hidden
            # html.Div([
            #     html.H2("📊 Summary Statistics", style={
            #         'color': '#2c3e50',
            #         'marginBottom': '20px',
            #         'textAlign': 'center'
            #     }),
            #     html.Div(id='general-summary-stats', children=self.create_summary_cards(), style={
            #         'display': 'flex',
            #         'flexWrap': 'nowrap',
            #         'justifyContent': 'space-around',
            #         'gap': '15px',
            #         'marginBottom': '40px'
            #     })
            # ]),
            
            # Control panel
            html.Div([
                html.H2("🎛️ Interactive Controls", style={
                    'color': '#2c3e50',
                    'marginBottom': '20px',
                    'textAlign': 'center'
                }),
                self.component_factory.create_control_panel()
            ]),
            
            # Main chart container
            html.Div([
                self.component_factory.create_chart_container(
                    'general-main-chart',
                    'Question Analysis Chart',
                    'Select a question from the dropdown above to view detailed analysis'
                )
            ], id='general-main-chart-container', style={'textAlign': 'center'}),
            
            # Hidden data stores
            dcc.Store(id='general-questions-data-store', data={}),
            dcc.Store(id='general-current-question-store', data=None)
            
        ], style={
            'maxWidth': '1400px',
            'margin': '0 auto',
            'padding': '20px',
            'fontFamily': 'Arial, sans-serif',
            'backgroundColor': '#f8f9fa',
            'minHeight': '100vh'
        })
    
    def _filter_q4_q5_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Filter Q4 and Q5 data to exclude 'Other' options and options below 5%"""
        if not isinstance(data, dict):
            return data
        
        filtered_data = {}
        total_count = sum(count for count in data.values() if isinstance(count, (int, float)))
        
        if total_count == 0:
            return data
        
        for option, count in data.items():
            if not isinstance(count, (int, float)):
                continue
            
            # Skip 'Other' options
            if 'Other' in option or 'other' in option:
                continue
            
            # Calculate percentage
            percentage = (count / total_count) * 100
            
            # Skip options below 5%
            if percentage < 5.0:
                continue
            
            filtered_data[option] = count
        
        return filtered_data
    
    def setup_callbacks(self, app):
        """Setup callback functions - Standard Interface Method"""
        
        @app.callback(
            [Output('general-question-dropdown', 'options'),
             Output('general-questions-data-store', 'data')],
            [Input('general-question-dropdown', 'id')]
        )
        def update_question_options(_):
            """Update question dropdown options"""
            # Refresh data to ensure real-time updates
            self.data_processor.refresh_data()
            
            questions_data = self.data_processor.get_questions_data()
            if not questions_data:
                return [], {}
            
            options = []
            # Sort questions by question number
            sorted_questions = sorted(questions_data.keys(), key=lambda x: self.data_processor._extract_question_number(x))
            
            # Filter out Q6 and later questions (only show Q1-Q5)
            filtered_questions = []
            for question in sorted_questions:
                question_num = self.data_processor._extract_question_number(question)
                if question_num <= 5:  # Only include Q1-Q5
                    filtered_questions.append(question)
            
            for question in filtered_questions:
                # Don't truncate the question text, show full text for better readability
                options.append({'label': question, 'value': question})
            
            return options, questions_data
        
        @app.callback(
            Output('general-chart-type-dropdown', 'value'),
            [Input('general-question-dropdown', 'value')],
            prevent_initial_call=True
        )
        def update_chart_type_default(selected_question):
            """Update chart type default value based on number of options"""
            if not selected_question:
                return 'bar'  # Default fallback
            
            questions_data = self.data_processor.get_questions_data()
            if selected_question not in questions_data:
                return 'bar'  # Default fallback
            
            data = questions_data[selected_question]
            if isinstance(data, dict):
                option_count = len(data)
                # 选项数量>=5时用柱状图，<5时用饼图
                if option_count >= 5:
                    return 'bar'
                else:
                    return 'pie'
            
            return 'bar'  # Default fallback
        
        @app.callback(
            [Output('general-main-chart', 'figure'),
             Output('general-current-question-store', 'data')],
            [Input('general-question-dropdown', 'value'),
             Input('general-chart-type-dropdown', 'value')],
            prevent_initial_call=True
        )
        def update_main_chart(selected_question, chart_type):
            """Update main chart"""
            questions_data = self.data_processor.get_questions_data()
            
            if not selected_question or selected_question not in questions_data:
                # Create empty chart and display prompt information
                fig = go.Figure()
                fig.add_annotation(
                    text="Please select a question from the dropdown above",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5, xanchor='center', yanchor='middle',
                    showarrow=False, font_size=16, font_color="#7f8c8d"
                )
                fig.update_layout(
                    title="Question Analysis Chart",
                    title_font_size=20,
                    title_x=0.5,
                    title_xanchor='center',
                    height=400,
                    paper_bgcolor='white',
                    plot_bgcolor='white'
                )
                return fig, None
            
            data = questions_data[selected_question]
            
            # Filter data for Q4 and Q5 questions
            if ('Q4:' in selected_question or 'Q5:' in selected_question) and isinstance(data, dict):
                filtered_data = self._filter_q4_q5_data(data)
            else:
                filtered_data = data
            
            # Create chart
            fig = self.visualizer.create_chart(filtered_data, chart_type, title=selected_question)
            
            return fig, selected_question
        
        # Removed show_all_questions and export_data callbacks as requested
    
    # Standard Interface Methods
    def get_summary_stats(self) -> Dict[str, Dict[str, str]]:
        """Get summary statistics data - Standard Interface Method"""
        # Refresh data to ensure real-time updates
        self.data_processor.refresh_data()
        return self.data_processor.get_summary_stats()
    
    def get_module_stats(self) -> Dict[str, Any]:
        """Get module statistics data - For main application statistics use"""
        # Refresh data to ensure real-time updates
        self.data_processor.refresh_data()
        
        if not self.data_processor.analysis_results:
            return {
                'total_questions': 0,
                'total_responses': 0,
                'avg_responses': 0,
                'max_responses': 0
            }
        
        return {
            'total_questions': self.data_processor.analysis_results['total_questions'],
            'total_responses': self.data_processor.analysis_results['total_responses'],
            'avg_responses': self.data_processor.analysis_results['avg_responses'],
            'max_responses': self.data_processor.analysis_results['max_responses']
        }
    
    def get_module_info(self) -> Dict[str, Any]:
        """Get module information - Standard Interface Method"""
        return {
            'name': 'General Survey Analysis',
            'description': 'Comprehensive analysis of all survey questions with interactive visualization and data exploration',
            'route': '/general',
            'icon': 'fas fa-chart-line',
            'color': '#3498db',
            'features': ['Visual Analysis of All Questions', 'Multiple Chart Types', 'Interactive Features', 'Data Export Capabilities']
        }

# Independent running support
if __name__ == '__main__':
    # Create independent Dash application for testing
    app = dash.Dash(__name__)
    app.title = "General Survey Analysis Dashboard"
    
    # Initialize dashboard
    dashboard = GeneralDashboard()
    
    # Set layout
    app.layout = dashboard.get_layout()
    
    # Setup callbacks
    dashboard.setup_callbacks(app)
    
    # Run application
    print("General Survey Analysis Dashboard starting...")
    print("Access URL: http://localhost:8050")
    app.run(debug=True, port=8050)