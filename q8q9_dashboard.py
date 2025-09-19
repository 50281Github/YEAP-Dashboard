#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Q8Q9 Survey Analysis Results Display Module
Specialized in displaying analysis results for Q8 (Financial Support) and Q9 (Project Details)

Usage:
    from q8q9_dashboard import Q8Q9Dashboard
    dashboard = Q8Q9Dashboard()
    layout = dashboard.get_layout()

Features:
    - Q8Q9 analysis results visualization
    - Project details table display
    - Statistical summary cards
    - Geographic distribution and classification statistics
    - Extensible modular design
"""

import dash
from dash import dcc, html, Input, Output, State, dash_table
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import json
from collections import defaultdict

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import style manager
from styles import style_manager
from q8q9_analysis import analyze_q8q9_data

class Q8Q9DataProcessor:
    """Q8Q9 Data Processor - Responsible for data loading and preprocessing"""
    
    def __init__(self, csv_file_path: str = "orignaldata/Q8Q9_basic_data.csv"):
        self.csv_file_path = csv_file_path
        self.analysis_results = None
        self.projects_df = None
        self._load_data()
    
    def _load_data(self):
        """Load and process Q8Q9 data"""
        try:
            # Use existing analysis function
            self.analysis_results = analyze_q8q9_data(self.csv_file_path)
            
            # Convert project data to DataFrame for display
            if self.analysis_results and 'projects_info' in self.analysis_results:
                projects_data = []
                for i, project in enumerate(self.analysis_results['projects_info'], 1):
                    projects_data.append({
                    'No.': i,
                    'User ID': project.get('user_id', ''),
                    'Department/Region': project.get('department_region', ''),  # New department/region information
                    'Project Name': project.get('project_name', ''),
                    'Country/Region': project.get('country', ''),
                    'Project Type': project.get('new_or_longstanding', ''),
                    'Funding Source': project.get('funding_source', ''),
                    'Focus': project.get('focus', ''),
                    'Project Description': project.get('description', '')[:100] + '...' if len(project.get('description', '')) > 100 else project.get('description', ''),
                    'Website Link': project.get('web_link', '')
                })
                self.projects_df = pd.DataFrame(projects_data)
            else:
                self.projects_df = pd.DataFrame()
                
        except Exception as e:
            print(f"Data loading error: {e}")
            self.analysis_results = {
                'total_questionnaires': 0,
                'q8_yes_count': 0,
                'q8_no_count': 0,
                'q8_yes_percentage': 0,
                'q8_no_percentage': 0,
                'projects_info': []
            }
            self.projects_df = pd.DataFrame()
    
    def get_summary_stats(self) -> Dict[str, Dict[str, str]]:
        """Get summary statistics data"""
        if not self.analysis_results:
            return {
                "stat1": {"value": "--", "label": "Total Questionnaires"},
                "stat2": {"value": "--", "label": "Supported Projects"},
                "stat3": {"value": "--", "label": "Support Rate"},
                "stat4": {"value": "--", "label": "Total Projects"}
            }
        
        return {
            "stat1": {
                "value": str(self.analysis_results['total_questionnaires']),
                "label": "Total Questionnaires"
            },
            "stat2": {
                "value": str(self.analysis_results['q8_yes_count']),
                "label": "Supported Projects"
            },
            "stat3": {
                "value": f"{self.analysis_results['q8_yes_percentage']:.1f}%",
                "label": "Support Rate"
            },
            "stat4": {
                "value": str(len(self.analysis_results['projects_info'])),
                "label": "Total Projects"
            }
        }
    
    def get_q8_distribution_data(self) -> Dict[str, int]:
        """Get Q8 response distribution data"""
        if not self.analysis_results:
            return {}
        
        return {
            "YES (Financial Support)": self.analysis_results['q8_yes_count'],
            "NO (No Support)": self.analysis_results['q8_no_count'],
            "No Answer": self.analysis_results['q8_no_answer_count']
        }
    
    def get_q8_yes_no_data(self) -> Dict[str, int]:
        """Get Q8 YES/NO only data (no answer counted as NO)"""
        if not self.analysis_results:
            return {}
        
        # Count unanswered users as NO, merge with explicit NO responses
        total_no_count = self.analysis_results['q8_no_count'] + self.analysis_results['q8_no_answer_count']
        
        return {
            "YES": self.analysis_results['q8_yes_count'],
            "NO": total_no_count
        }
    
    def get_country_distribution_data(self) -> Dict[str, int]:
        """Get country distribution data"""
        if not self.analysis_results or not self.analysis_results['projects_info']:
            return {}
        
        country_counts = defaultdict(int)
        for project in self.analysis_results['projects_info']:
            country = project.get('country', 'Unknown')
            if country:
                country_counts[country] += 1
        
        return dict(country_counts)
    
    def get_focus_distribution_data(self) -> Dict[str, int]:
        """Get focus distribution data"""
        if not self.analysis_results or not self.analysis_results['projects_info']:
            return {}
        
        focus_counts = defaultdict(int)
        for project in self.analysis_results['projects_info']:
            focus = project.get('focus', 'Unknown')
            if focus:
                focus_counts[focus] += 1
        
        return dict(focus_counts)
    
    def get_funding_source_data(self) -> Dict[str, int]:
        """Get funding source distribution data"""
        if not self.analysis_results or not self.analysis_results['projects_info']:
            return {}
        
        funding_counts = defaultdict(int)
        for project in self.analysis_results['projects_info']:
            funding = project.get('funding_source', 'Unknown')
            if funding:
                funding_counts[funding] += 1
        
        return dict(funding_counts)
    
    def refresh_data(self):
        """Refresh data from file - enables real-time updates"""
        self._load_data()
    
    @property
    def original_data(self):
        """Return original data for region filtering"""
        # Q8Q9 module data structure contains department/region information, return project data
        return self.projects_df.copy() if self.projects_df is not None else pd.DataFrame()
    
    def _process_data(self, filtered_data):
        """Process filtered data - supports region filtering"""
        if filtered_data is None or filtered_data.empty:
            return self.projects_df.copy() if self.projects_df is not None else pd.DataFrame()
        
        # Return filtered data
        return filtered_data.copy()
    
    def get_filtered_analysis_results(self, region_filter: str = None) -> Dict[str, Any]:
        """Recalculate analysis results based on region filtering"""
        try:
            if not region_filter or region_filter == 'all':
                return self.analysis_results
            
            # Re-analyze filtered data
            from q8q9_analysis import analyze_q8q9_data_filtered
            
            # If no filtering analysis function available, manually filter
            if not self.projects_df.empty and 'Department/Region' in self.projects_df.columns:
                # Filter project data
                filtered_projects = self.projects_df[self.projects_df['Department/Region'] == region_filter]
                
                # Recalculate statistics
                filtered_results = self.analysis_results.copy()
                
                # Update project-related statistics
                filtered_results['projects_info'] = []
                for _, row in filtered_projects.iterrows():
                    project_info = {
                        'user_id': row.get('User ID', ''),
                        'department_region': row.get('Department/Region', ''),
                        'project_name': row.get('Project Name', ''),
                        'country': row.get('Country/Region', ''),
                        'new_or_longstanding': row.get('Project Type', ''),
                        'funding_source': row.get('Funding Source', ''),
                        'focus': row.get('Focus', ''),
                        'description': row.get('Project Description', ''),
                        'web_link': row.get('Website Link', '')
                    }
                    filtered_results['projects_info'].append(project_info)
                
                # Recalculate Q8 statistics (based on filtered users)
                # Should re-analyze from original CSV, but for simplicity, estimate by ratio
                total_original = self.analysis_results['total_questionnaires']
                if total_original > 0:
                    # Get user count for this region
                    region_users = len(filtered_projects['User ID'].unique()) if not filtered_projects.empty else 0
                    total_users = len(self.projects_df['User ID'].unique()) if not self.projects_df.empty else 1
                    
                    ratio = region_users / total_users if total_users > 0 else 0
                    
                    filtered_results['q8_yes_count'] = int(self.analysis_results['q8_yes_count'] * ratio)
                    filtered_results['q8_no_count'] = int(self.analysis_results['q8_no_count'] * ratio)
                    filtered_results['q8_no_answer_count'] = int(self.analysis_results['q8_no_answer_count'] * ratio)
                    filtered_results['total_questionnaires'] = filtered_results['q8_yes_count'] + filtered_results['q8_no_count'] + filtered_results['q8_no_answer_count']
                    
                    # Recalculate percentages
                    if filtered_results['total_questionnaires'] > 0:
                        filtered_results['q8_yes_percentage'] = (filtered_results['q8_yes_count'] / filtered_results['total_questionnaires']) * 100
                        filtered_results['q8_no_percentage'] = (filtered_results['q8_no_count'] / filtered_results['total_questionnaires']) * 100
                    else:
                        filtered_results['q8_yes_percentage'] = 0
                        filtered_results['q8_no_percentage'] = 0
                
                return filtered_results
            
            return self.analysis_results
            
        except Exception as e:
            print(f"Error getting filtered analysis results: {e}")
            return self.analysis_results

class Q8Q9ComponentFactory:
    """Q8Q9 Component Factory - Responsible for creating various UI components"""
    
    def __init__(self, style_manager, data_processor):
        self.style_manager = style_manager
        self.data_processor = data_processor
    
    def create_summary_card(self, icon: str, value: str, title: str, 
                           subtitle: str, footer: str, color: str) -> html.Div:
        """Create responsive summary statistics card"""
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
            'width': '22%',
            'display': 'inline-block',
            'margin': '0 1.5%',
            'verticalAlign': 'top'
        })
    
    def create_chart_container(self, chart_id: str, title: str) -> html.Div:
        """Create responsive chart container"""
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
            'border': '1px solid #e9ecef',
            'width': '100%',
            'maxWidth': '100%'
        }
        
        # Merge styles
        final_container_style = {**default_container_style, **container_style}
        
        return html.Div([
            html.H3(self.style_manager._wrap_title(title) if self.style_manager else title, style={
                'textAlign': 'center',
                'color': '#2c3e50',
                'marginBottom': '10px',
                'fontSize': '1.2em',
                'lineHeight': '1.3',
                'whiteSpace': 'pre-line'
            }),
            dcc.Graph(
                id=chart_id,
                style={
                    'height': '400px',
                    'width': '100%'
                },
                config={
                    'responsive': True,
                    'displayModeBar': True,
                    'displaylogo': False,
                    'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d']
                }
            )
        ], style=final_container_style)
    
    def create_projects_table(self) -> html.Div:
        """Create project details table"""
        if self.data_processor.projects_df.empty:
            return html.Div([
                html.P("No project data available", style={
                    'textAlign': 'center',
                    'color': '#7f8c8d',
                    'fontSize': '1.2em',
                    'margin': '50px 0'
                })
            ])
        
        return html.Div([
            html.H3("Project Details Table", style={
                'textAlign': 'center',
                'color': '#2c3e50',
                'marginBottom': '20px',
                'fontSize': '1.3em'
            }),
            dash_table.DataTable(
                id='q8q9-projects-table',
                data=self.data_processor.projects_df.to_dict('records'),
                columns=[
                    {"name": col, "id": col, "presentation": "markdown" if col == "Website Link" else "input"}
                    for col in self.data_processor.projects_df.columns
                ],
                style_cell={
                    'textAlign': 'left',
                    'padding': '10px',
                    'fontFamily': 'Arial, sans-serif',
                    'fontSize': '12px',
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'maxWidth': '200px'
                },
                style_header={
                    'backgroundColor': '#3498db',
                    'color': 'white',
                    'fontWeight': 'bold',
                    'textAlign': 'center'
                },
                style_data={
                    'backgroundColor': '#f8f9fa',
                    'border': '1px solid #dee2e6'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': '#ffffff'
                    }
                ],
                page_size=10,
                sort_action="native",
                filter_action="native"
            )
        ], style={
            'maxWidth': '1200px',
            'margin': '0 auto 30px auto',
            'padding': '20px'
        })

class Q8Q9Dashboard:
    """Q8Q9 Dashboard Main Class - Integrating all functional modules"""
    
    def __init__(self, csv_file_path: str = "orignaldata/Q8Q9_basic_data.csv"):
        self.data_processor = Q8Q9DataProcessor(csv_file_path)
        self.component_factory = Q8Q9ComponentFactory(style_manager, self.data_processor)
        self.style_manager = style_manager
    
    def create_summary_cards(self) -> List[html.Div]:
        """Create summary statistics cards"""
        stats = self.data_processor.get_summary_stats()
        
        cards = [
            self.component_factory.create_summary_card(
                icon="fas fa-file-alt",
                value=stats["stat1"]["value"],
                title=stats["stat1"]["label"],
                subtitle="Total Survey Count",
                footer="Data Statistics",
                color="#3498db"
            ),
            self.component_factory.create_summary_card(
                icon="fas fa-hand-holding-usd",
                value=stats["stat2"]["value"],
                title=stats["stat2"]["label"],
                subtitle="Organizations Providing Financial Support",
                footer="Q8 Statistics",
                color="#2ecc71"
            ),
            self.component_factory.create_summary_card(
                icon="fas fa-percentage",
                value=stats["stat3"]["value"],
                title=stats["stat3"]["label"],
                subtitle="Financial Support Ratio",
                footer="Ratio Statistics",
                color="#f39c12"
            ),
            # Q9 related statistics cards are temporarily commented out because the question categories are different
            # self.component_factory.create_summary_card(
            #     icon="fas fa-project-diagram",
            #     value=stats["stat4"]["value"],
            #     title=stats["stat4"]["label"],
            #     subtitle="Total Youth Projects",
            #     footer="Q9 Statistics",
            #     color="#e74c3c"
            # )
        ]
        
        return cards
    
    def create_summary_cards_with_data(self, analysis_results: Dict[str, Any]) -> List[html.Div]:
        """Create summary cards with specific analysis results data"""
        if not analysis_results:
            stats = {
                "stat1": {"value": "--", "label": "Total Questionnaires"},
                "stat2": {"value": "--", "label": "Supported Projects"},
                "stat3": {"value": "--", "label": "Support Rate"},
                "stat4": {"value": "--", "label": "Total Projects"}
            }
        else:
            stats = {
                "stat1": {
                    "value": str(analysis_results['total_questionnaires']),
                    "label": "Total Questionnaires"
                },
                "stat2": {
                    "value": str(analysis_results['q8_yes_count']),
                    "label": "Supported Projects"
                },
                "stat3": {
                    "value": f"{analysis_results['q8_yes_percentage']:.1f}%",
                    "label": "Support Rate"
                },
                "stat4": {
                    "value": str(len(analysis_results['projects_info'])),
                    "label": "Total Projects"
                }
            }
        
        cards = [
            self.component_factory.create_summary_card(
                icon="fas fa-users",
                value=stats["stat1"]["value"],
                title=stats["stat1"]["label"],
                subtitle="Survey Participants",
                footer="Q8 Statistics",
                color="#3498db"
            ),
            self.component_factory.create_summary_card(
                icon="fas fa-check-circle",
                value=stats["stat2"]["value"],
                title=stats["stat2"]["label"],
                subtitle="Financial Support Provided",
                footer="Q8 YES Responses",
                color="#2ecc71"
            ),
            self.component_factory.create_summary_card(
                icon="fas fa-percentage",
                value=stats["stat3"]["value"],
                title=stats["stat3"]["label"],
                subtitle="Financial Support Ratio",
                footer="Ratio Statistics",
                color="#f39c12"
            )
        ]
        
        return cards
    
    def create_chart(self, chart_type: str, data: Dict[str, int], title: str) -> go.Figure:
        """Create standardized chart"""
        if not data:
            fig = go.Figure()
            fig.add_annotation(
                text="No data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False, font_size=14
            )
            return fig
        
        # Use style manager to create standardized chart
        fig = self.style_manager.create_standardized_chart(data, chart_type, title)
        return fig
    
    def get_layout(self) -> html.Div:
        """Get complete dashboard layout"""
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
            html.H1("Q8 survey analysis results", style={
                'textAlign': 'center',
                'color': '#2c3e50',
                'marginBottom': '30px',
            'fontFamily': 'Arial, sans-serif'
            }),
            
            # Summary statistics cards area
            html.Div(id='q8q9-summary-stats', children=self.create_summary_cards(), style={
                'textAlign': 'center',
            'marginBottom': '40px'
            }),
            
            # Region filter component
            html.Div([
                html.H3("Display options", style={
                    'color': '#2c3e50',
                    'marginBottom': '20px',
                    'textAlign': 'center'
                }),
                html.Div([
                    self.style_manager.create_region_filter_component('q8q9-region-filter')
                ], style={'maxWidth': '400px', 'margin': '0 auto', 'marginBottom': '30px'})
            ], style={'textAlign': 'center', 'marginBottom': '30px'}),
            
            # Chart display area
            html.Div([
                # Q8 Response Distribution Chart (All responses)
                self.component_factory.create_chart_container(
                    'q8q9-q8-chart', 
                    'Q8: youth project financial support distribution (all responses)'
                ),
                
                # Add spacing between charts
                html.Div(style={'marginBottom': '40px'}),
                
                # Q8 YES/NO Only Chart (Excluding no answer)
                self.component_factory.create_chart_container(
                    'q8q9-q8-yesno-chart', 
                    'Q8: yes vs no responses only'
                )
                
                # Q9 related charts are temporarily commented out due to different question categories
                # # Funding Source Distribution Chart
                # self.component_factory.create_chart_container(
                #     'q8q9-funding-chart', 
                #     'Q9: Project Funding Source Distribution'
                # )
            ]),
            
            # Q9 project details table is temporarily commented out due to different question categories
            # self.component_factory.create_projects_table()
            
        ], style={
            'maxWidth': '1400px',
            'margin': '0 auto',
            'padding': '20px',
            'fontFamily': 'Arial, sans-serif',
            'backgroundColor': '#f8f9fa',
            'minHeight': '100vh'
        })
    
    def setup_callbacks(self, app):
        """Setup callback functions - Reserved interface for integration into main application"""
        
        @app.callback(
            [Output('q8q9-q8-chart', 'figure'),
             Output('q8q9-q8-yesno-chart', 'figure'),
             Output('q8q9-summary-stats', 'children')],
            [Input('q8q9-region-filter', 'value')]
        )
        def update_q8_charts(region_filter):
            """Update Q8 charts and summary stats with region filtering"""
            # Output region filtering information
            if region_filter and region_filter != 'all':
                original_data = self.data_processor.original_data
                filtered_count = len(original_data[original_data['Department/Region'] == region_filter]) if 'Department/Region' in original_data.columns else 0
                print(f"✓ {region_filter} region loaded successfully, {filtered_count} records loaded")
            else:
                original_data = self.data_processor.original_data
                print(f"✓ All regions loaded successfully, {len(original_data)} records loaded")
            
            # Get filtered analysis results
            filtered_results = self.data_processor.get_filtered_analysis_results(region_filter)
            
            # Check if there is data
            has_data = (filtered_results['q8_yes_count'] > 0 or 
                       filtered_results['q8_no_count'] > 0 or 
                       filtered_results['q8_no_answer_count'] > 0)
            
            # Get data based on filtered results
            if has_data:
                q8_data = {
                    "YES (Financial Support)": filtered_results['q8_yes_count'],
                    "NO (No Support)": filtered_results['q8_no_count'],
                    "No Answer": filtered_results['q8_no_answer_count']
                }
                
                q8_yesno_data = {
                    "YES": filtered_results['q8_yes_count'],
                    "NO": filtered_results['q8_no_count'] + filtered_results['q8_no_answer_count']
                }
            else:
                # If no data, return empty dictionary to trigger no data prompt
                q8_data = {}
                q8_yesno_data = {}
            
            # Update chart titles
            title_suffix = f" ({region_filter})" if region_filter and region_filter != 'all' else ""
            
            q8_chart = self.create_chart('pie', q8_data, f'Q8 Response Distribution{title_suffix}')
            q8_yesno_chart = self.create_chart('pie', q8_yesno_data, f'Q8 Yes Vs No Only{title_suffix}')
            
            # Update summary cards with filtered data
            summary_cards = self.create_summary_cards_with_data(filtered_results)
            
            return q8_chart, q8_yesno_chart, summary_cards
        
        # Q9 related callback functions are temporarily commented out due to different question categories
        # @app.callback(
        #     Output('q8q9-funding-chart', 'figure'),
        #     [Input('q8q9-summary-stats', 'children')]
        # )
        # def update_funding_chart(children):
        #     data = self.data_processor.get_funding_source_data()
        #     return self.create_chart('pie', data, 'Funding Source Distribution')
    
    # Reserved interface methods - For easy integration into main application
    def get_module_stats(self) -> Dict[str, Dict[str, str]]:
        """Get module statistics data - For main application portal page use"""
        return self.data_processor.get_summary_stats()
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """Get summary statistics data - For main application statistics use"""
        if not self.data_processor.analysis_results:
            return {
                'total_responses': 0,
                'q8_yes_percentage': 0,
                'q8_yes_count': 0,
                'q8_no_count': 0
            }
        
        return {
            'total_responses': self.data_processor.analysis_results['total_questionnaires'],
            'q8_yes_percentage': self.data_processor.analysis_results['q8_yes_percentage'],
            'q8_yes_count': self.data_processor.analysis_results['q8_yes_count'],
            'q8_no_count': self.data_processor.analysis_results['q8_no_count'] + self.data_processor.analysis_results['q8_no_answer_count']
        }
    
    def get_module_info(self) -> Dict[str, Any]:
        """Get module information - For main application registration use"""
        return {
            'name': 'Q8 Analysis',
            'description': 'Display analysis results for Q8 (Financial Support)',
            'route': '/q8q9',
            'icon': 'fas fa-chart-line',
            'color': '#9b59b6',
            'features': ['Financial Support Statistics', 'Support Rate Analysis', 'Response Distribution Charts']
        }

# Independent running support
if __name__ == '__main__':
    # Create independent Dash application for testing
    app = dash.Dash(__name__)
    
    # Create Q8Q9 dashboard instance
    q8q9_dashboard = Q8Q9Dashboard()
    
    # Set application layout
    app.layout = q8q9_dashboard.get_layout()
    
    # Set callback functions
    q8q9_dashboard.setup_callbacks(app)
    
    # Run application
    print("Q8Q9 Analysis Dashboard starting...")
    print("Access URL: http://127.0.0.1:8050")
    app.run(debug=True, port=8050)