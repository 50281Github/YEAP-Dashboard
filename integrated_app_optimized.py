#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Analytics Dashboard - Unified Entry (Optimized)
Architectural design for multi-page routing integration

Usage:
    python integrated_app_optimized.py

Features:
    - Unified entry portal
    - Multi-page routing management
    - Modular dashboard integration
    - Scalable architecture design
    - External style management
"""

import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go
import sys
from pathlib import Path
from typing import Dict, List, Any

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import existing dashboard modules
from general_dashboard import GeneralDashboard
from q345_dashboard import Q345Dashboard
from q8q9_dashboard import Q8Q9Dashboard
from q6q7q10q11_dashboard import Q6Q7Q10Q11Dashboard
from visualizer import visualizer
from styles import style_manager

class PageManager:
    """Page Manager - Responsible for page layout and styles"""
    
    def __init__(self, style_manager, general_dashboard=None, q345_dashboard=None, q8q9_dashboard=None, q6q7q10q11_dashboard=None):
        self.style_manager = style_manager
        self.general_dashboard = general_dashboard
        self.q345_dashboard = q345_dashboard
        self.q8q9_dashboard = q8q9_dashboard
        self.q6q7q10q11_dashboard = q6q7q10q11_dashboard
        self.page_styles = self._load_page_styles()
    
    def _load_page_styles(self) -> Dict[str, Dict[str, Any]]:
        """Load page style configuration"""
        return {
            'portal': {
                'container': {
                    'maxWidth': '1400px',
                    'margin': '0 auto',
                    'padding': '40px 20px',
                    'fontFamily': 'Arial, sans-serif',
                    'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    'minHeight': '100vh'
                },
                'title': {
                    'textAlign': 'center',
                    'color': '#2c3e50',
                    'marginBottom': '50px',
                    'fontFamily': 'Arial, sans-serif',
                    'fontSize': '3em',
                    'textShadow': '2px 2px 4px rgba(0,0,0,0.1)'
                },
                'card_container': {
                    'display': 'grid',
                    'gridTemplateColumns': 'repeat(auto-fit, minmax(300px, 1fr))',
                    'gridAutoRows': 'auto',
                    'gap': '15px',
                    'marginBottom': '50px',
                    'padding': '0 20px',
                    'justifyItems': 'center'
                },
                'module_card': {
                    'width': '100%',
                    'maxWidth': '280px',
                    'display': 'block'
                },
                'portal_card_style': {
                    'backgroundColor': 'white',
                    'borderRadius': '15px',
                    'padding': '30px',
                    'textAlign': 'center',
                    'boxShadow': '0 8px 25px rgba(0,0,0,0.15)',
                    'transition': 'transform 0.3s ease, boxShadow 0.3s ease',
                    'display': 'flex',
                    'flexDirection': 'column'
                }
            },
            'dashboard': {
                'container': {
                    'maxWidth': '1400px',
                    'margin': '0 auto',
                    'padding': '20px',
                    'fontFamily': 'Arial, sans-serif'
                },
                'nav_button': {
                    'backgroundColor': '#34495e',
                    'color': 'white',
                    'textDecoration': 'none',
                    'padding': '10px 20px',
                    'borderRadius': '5px',
                    'marginBottom': '20px',
                    'display': 'inline-block',
                    'fontWeight': 'bold'
                },
                'title': {
                    'textAlign': 'center',
                    'color': '#2c3e50',
                    'marginBottom': '30px',
                    'fontFamily': 'Arial, sans-serif'
                }
            }
        }
    
    def get_module_stats(self, module_type: str) -> Dict[str, str]:
        """Get module statistics data"""
        try:
            if module_type == "general":
                if hasattr(self, 'general_dashboard') and self.general_dashboard:
                    try:
                        stats = self.general_dashboard.get_summary_stats()
                        return {
                            "stat1": {"value": str(stats.get('stat1', {}).get('value', 0)), "label": stats.get('stat1', {}).get('label', 'Total Questions')},
                            "stat2": {"value": str(stats.get('stat2', {}).get('value', 0)), "label": stats.get('stat2', {}).get('label', 'Total Responses')},
                            "stat3": {"value": str(stats.get('stat3', {}).get('value', 0)), "label": stats.get('stat3', {}).get('label', 'Avg Responses')},
                            "stat4": {"value": str(stats.get('stat4', {}).get('value', 0)), "label": stats.get('stat4', {}).get('label', 'Max Responses')}
                        }
                    except Exception:
                        pass
            elif module_type == "q345":
                if hasattr(self, 'q345_dashboard') and self.q345_dashboard:
                    try:
                        stats = self.q345_dashboard.get_summary_stats()
                        return {
                            "stat1": {"value": str(stats.get('stat1', {}).get('value', 0)), "label": stats.get('stat1', {}).get('label', 'Q3 Options')},
                            "stat2": {"value": str(stats.get('stat2', {}).get('value', 0)), "label": stats.get('stat2', {}).get('label', 'Q4 Options')},
                            "stat3": {"value": str(stats.get('stat3', {}).get('value', 0)), "label": stats.get('stat3', {}).get('label', 'Q5 Options')},
                            "stat4": {"value": str(stats.get('stat4', {}).get('value', 0)), "label": stats.get('stat4', {}).get('label', 'Total Options')}
                        }
                    except Exception:
                        pass
            elif module_type == "q8q9":
                if hasattr(self, 'q8q9_dashboard') and self.q8q9_dashboard:
                    try:
                        stats = self.q8q9_dashboard.get_summary_stats()
                        return {
                            "stat1": {"value": str(stats.get('total_responses', 0)), "label": "Total Surveys"},
                            "stat2": {"value": f"{stats.get('q8_yes_percentage', 0):.1f}%", "label": "Q8 Yes Rate"},
                            "stat3": {"value": str(stats.get('q8_yes_count', 0)), "label": "Support Yes"},
                            "stat4": {"value": str(stats.get('q8_no_count', 0)), "label": "Support No"}
                        }
                    except Exception:
                        pass
            elif module_type == "q6q7q10q11":
                if hasattr(self, 'q6q7q10q11_dashboard') and self.q6q7q10q11_dashboard:
                    try:
                        stats = self.q6q7q10q11_dashboard.get_summary_stats()
                        return {
                            "stat1": {"value": str(stats.get('stat1', {}).get('value', 0)), "label": stats.get('stat1', {}).get('label', 'Questions')},
                            "stat2": {"value": str(stats.get('stat2', {}).get('value', 0)), "label": stats.get('stat2', {}).get('label', 'Participants')},
                            "stat3": {"value": str(stats.get('stat3', {}).get('value', 0)), "label": stats.get('stat3', {}).get('label', 'Avg Works')},
                            "stat4": {"value": str(stats.get('stat4', {}).get('value', 0)), "label": stats.get('stat4', {}).get('label', 'Works/Person')}
                        }
                    except Exception:
                        pass
        except Exception:
            pass
        
        # Return placeholder data by default
        return {
            "stat1": {"value": "--", "label": "Loading"},
            "stat2": {"value": "--", "label": "Loading"},
            "stat3": {"value": "--", "label": "Loading"},
            "stat4": {"value": "--", "label": "Loading"}
        }
    
    def create_module_card(self, title: str, description: str, features: List[str], 
                          button_text: str, button_id: str, icon_class: str, 
                          color: str, disabled: bool = False, module_type: str = None) -> html.Div:
        """Create module card"""
        card_config = self.style_manager.get_global_chart_config('card_style')
        
        # Get statistics data or use feature list
        # if module_type and not disabled:
        #     stats = self.get_module_stats(module_type)
        #     # Create statistics data display
        #     stats_elements = []
        #     for key in ['stat1', 'stat2', 'stat3', 'stat4']:
        #         if key in stats:
        #             stat_item = html.Div([
        #                 html.Div(stats[key]['value'], style={
        #                             'fontSize': '1.8em',
        #                     'fontWeight': 'bold',
        #                     'color': color,
        #                     'marginBottom': '3px',
        #                     'lineHeight': '1.2'
        #                 }),
        #                 html.Div(stats[key]['label'], style={
        #                     'fontSize': '0.8em',
        #                     'color': '#7f8c8d',
        #                     'lineHeight': '1.2'
        #                 })
        #             ], style={
        #                 'display': 'inline-block',
        #                 'width': '48%',
        #                 'margin': '5px 0.2%',
        #                 'textAlign': 'center',
        #                 'verticalAlign': 'top'
        #             })
        #             stats_elements.append(stat_item)
        #     content_elements = stats_elements
        if False:  # hide
            pass
        else:
            # Use original feature list
            feature_elements = []
            for i, feature in enumerate(features):
                feature_elements.append(html.Div(f"✓ {feature}", style={
                    'marginBottom': '8px',
                    'color': color if not disabled else '#95a5a6',
                    'fontSize': '0.9em',
                    'lineHeight': '1.3'
                }))
            content_elements = feature_elements
        
        # Button style
        button_style = {
            'backgroundColor': color if not disabled else '#95a5a6',
            'color': 'white',
            'border': 'none',
            'padding': '12px 30px',
            'borderRadius': '25px',
            'cursor': 'pointer' if not disabled else 'default',
            'fontSize': '1em',
            'fontWeight': '600',
            'transition': 'all 0.3s ease',
            'boxShadow': f'0 4px 15px {color}30' if not disabled else 'none',
            'width': '80%',
            'maxWidth': '200px'
        }
        
        # Use homepage-specific card style
        card_inner_style = self.page_styles['portal']['portal_card_style'].copy()
        if disabled:
            card_inner_style.update({
                'backgroundColor': '#f8f9fa',
                'boxShadow': '0 5px 15px rgba(0,0,0,0.05)'
            })
        
        return html.Div([
            html.Div([
                # Top area: icon and title
                html.Div([
                    html.I(className=icon_class, style={
                        'fontSize': '3.5em',
                        'color': color if not disabled else '#95a5a6',
                        'marginBottom': '15px'
                    }),
                    html.H3(title, style={
                        'color': '#2c3e50' if not disabled else '#95a5a6',
                        'marginBottom': '15px',
                        'fontSize': '1.2em',
                         'lineHeight': '1.3'
                    }),
                    html.P(description, style={
                        'color': '#7f8c8d' if not disabled else '#bdc3c7',
                        'marginBottom': '20px',
                        'lineHeight': '1.5',
                        'fontSize': '1em'
                    })
                ], style={'flex': '0 0 auto'}),
                
                # Middle area: content (statistics data or feature list)
                html.Div(content_elements, style={
                    'flex': '1 1 auto',
                    'marginBottom': '20px',
                    'overflow': 'hidden'
                }),
                
                # Bottom area: button
                html.Div([
                    html.Button(button_text, id=button_id, disabled=disabled, style=button_style)
                ], style={'flex': '0 0 auto'})
            ], style=card_inner_style)
        ], style=self.page_styles['portal']['module_card'])
    
    def create_portal_page(self) -> html.Div:
        """Create portal homepage"""
        return html.Div([
            # Main title area
            html.Div([
                html.H1("📊 Analytics Dashboard", style=self.page_styles['portal']['title'])
            ]),
            
            # Module navigation card area
            html.Div([
                html.Div([
                    # General Survey Analysis Module
                    self.create_module_card(
                        title="📈 General Survey Analysis",
                        description="Supports visual analysis of all questions with multiple chart types and interactive features",
                        features=["Visual Analysis", "Multiple Chart Types", "Interactive Features"],
                        button_text="Enter Analysis",
                        button_id="btn-general",
                        icon_class="fas fa-chart-bar",
                        color="#3498db",
                        module_type="general"
                    ),
                    
                    # Specialized Analysis Module
                    self.create_module_card(
                        title="🎯 Specialized Analysis",
                        description="In-depth analysis focused on implementation frameworks, policy areas, and target groups",
                        features=["Q3: Implementation Framework", "Q4: Policy Areas", "Q5: Target Groups"],
                        button_text="Enter Analysis",
                        button_id="btn-q345",
                        icon_class="fas fa-chart-pie",
                        color="#e74c3c",
                        module_type="q345"
                    ),
                    
                    # Q8 Specialized Analysis Module - HIDDEN
                    # self.create_module_card(
                    #     title="Q8 Specialized Analysis",
                    #     description="Q8 response analysis and country distribution",
                    #     features=["Q8: Response Status", "Country Distribution", "Response Statistics"],
                    #     button_text="Enter Analysis",
                    #     button_id="btn-q8q9",
                    #     icon_class="fas fa-chart-line",
                    #     color="#27ae60",
                    #     module_type="q8q9"
                    # ),
                    
                    # Q6Q7Q10Q11 Specialized Analysis Module
        self.create_module_card(
            title="📋 Specialized Analysis",
            description="Outputs statistics and frequency analysis across areas",
            features=["Outputs Count Statistics", "Frequency Analysis", "Outputs List"],
                        button_text="Enter Analysis",
                        button_id="btn-q6q7q10q11",
                        icon_class="fas fa-project-diagram",
                        color="#9b59b6",
                        module_type="q6q7q10q11"
                    )
                ], style=self.page_styles['portal']['card_container'])
            ])
        ], style=self.page_styles['portal']['container'])

class ComponentFactory:
    """Component Factory - Responsible for creating various UI components"""
    
    def __init__(self, style_manager):
        self.style_manager = style_manager
    
    def create_summary_card(self, icon: str, value: str, title: str, 
                           subtitle: str, footer: str, color: str) -> html.Div:
        """Create summary statistics card"""
        card_config = self.style_manager.get_global_chart_config('card_style')
        
        card_style = {
            'backgroundColor': card_config['backgroundColor'],
            'borderRadius': card_config['borderRadius'],
            'padding': card_config['padding'],
            'textAlign': 'center',
            'boxShadow': card_config['boxShadow'],
            'width': '220px',
            'display': 'inline-block',
            'transition': card_config['transition']
        }
        
        return html.Div([
            html.Div([
                html.I(className=icon, style={
                    'fontSize': '2em', 
                    'color': color, 
                    'marginBottom': '10px'
                })
            ]),
            html.H3(value, style={
                'color': color, 
                'margin': '0', 
                'fontSize': '2.8em', 
                'fontWeight': 'bold'
            }),
            html.P(title, style={
                'margin': '10px 0 5px 0', 
                'fontWeight': 'bold', 
                'fontSize': '1.1em'
            }),
            html.P(subtitle, style={
                'margin': '0', 
                'color': '#7f8c8d', 
                'fontSize': '0.9em'
            }),
            html.Hr(style={
                'margin': '15px 0', 
                'borderColor': color, 
                'opacity': '0.3'
            }),
            html.P(footer, style={
                'margin': '0', 
                'color': color, 
                'fontSize': '0.85em', 
                'fontWeight': 'bold'
            })
        ], style=card_style)
    
    def create_control_panel(self, children: List, style_override: Dict = None) -> html.Div:
        """Create control panel"""
        container_config = self.style_manager.get_global_chart_config('container_style')
        
        panel_style = {
            'backgroundColor': container_config['backgroundColor'],
            'borderRadius': container_config['borderRadius'],
            'padding': container_config['padding'],
            'marginBottom': '30px',
            'boxShadow': container_config['boxShadow'],
            'border': container_config['border']
        }
        
        if style_override:
            panel_style.update(style_override)
        
        return html.Div(children, style=panel_style)

class CallbackManager:
    """Callback Manager - Responsible for managing all callback functions"""
    
    def __init__(self, app, general_dashboard, q345_dashboard, q8q9_dashboard, q6q7q10q11_dashboard, style_manager):
        self.app = app
        self.general_dashboard = general_dashboard
        self.q345_dashboard = q345_dashboard
        self.q8q9_dashboard = q8q9_dashboard
        self.q6q7q10q11_dashboard = q6q7q10q11_dashboard
        self.style_manager = style_manager
        self.component_factory = ComponentFactory(style_manager)
    
    def setup_routing_callbacks(self):
        """Setup routing callback functions"""
        
        # Main routing callback
        @self.app.callback(
            Output('main-page-content', 'children'),
            [Input('main-url', 'pathname')]
        )
        def display_page(pathname):
            """Display corresponding page based on URL path"""
            try:
                if pathname == '/general' or pathname == '/general/':
                    return self._get_general_dashboard_layout()
                elif pathname == '/q345' or pathname == '/q345/':
                    return self.q345_dashboard.get_layout()
                elif pathname == '/q8q9' or pathname == '/q8q9/':
                    return self.q8q9_dashboard.get_layout()
                elif pathname == '/q6q7q10q11' or pathname == '/q6q7q10q11/':
                    return self.q6q7q10q11_dashboard.get_layout()
                else:
                    page_manager = PageManager(self.style_manager, self.general_dashboard, self.q345_dashboard, self.q8q9_dashboard, self.q6q7q10q11_dashboard)
                    return page_manager.create_portal_page()
            except Exception as e:
                return self._create_error_page(str(e))
        
        # Navigation button callbacks
        @self.app.callback(
            Output('main-url', 'pathname', allow_duplicate=True),
            [Input('btn-general', 'n_clicks')],
            prevent_initial_call=True
        )
        def navigate_to_general(n_clicks):
            if n_clicks:
                return '/general'
            return dash.no_update
        
        @self.app.callback(
            Output('main-url', 'pathname', allow_duplicate=True),
            [Input('btn-q345', 'n_clicks')],
            prevent_initial_call=True
        )
        def navigate_to_q345(n_clicks):
            if n_clicks:
                return '/q345'
            return dash.no_update
        
        @self.app.callback(
            Output('main-url', 'pathname', allow_duplicate=True),
            [Input('btn-q8q9', 'n_clicks')],
            prevent_initial_call=True
        )
        def navigate_to_q8q9(n_clicks):
            if n_clicks:
                return '/q8q9'
            return dash.no_update
        
        @self.app.callback(
            Output('main-url', 'pathname', allow_duplicate=True),
            [Input('btn-q6q7q10q11', 'n_clicks')],
            prevent_initial_call=True
        )
        def navigate_to_q6q7q10q11(n_clicks):
            if n_clicks:
                return '/q6q7q10q11'
            return dash.no_update
    
    def setup_general_callbacks(self):
        """Setup general dashboard callback functions"""
        if hasattr(self.general_dashboard, 'setup_callbacks'):
            try:
                self.general_dashboard.setup_callbacks(self.app)
                print("✓ General module callback functions setup completed")
            except Exception as e:
                print(f"❌ General module callback functions setup failed: {e}")
        else:
            print("⚠️ General module does not provide callback function setup method")
    
    def setup_q345_callbacks(self):
        """Setup Q345 module callback functions"""
        if hasattr(self.q345_dashboard, 'setup_callbacks'):
            try:
                self.q345_dashboard.setup_callbacks(self.app)
                print("✓ Q345 module callback functions setup completed")
            except Exception as e:
                print(f"❌ Q345 module callback functions setup failed: {e}")
        else:
            print("⚠️ Q345 module does not provide callback function setup method")
    
    def _create_error_page(self, error_message: str) -> html.Div:
        """Create error page"""
        return html.Div([
            html.H1("Page Loading Error", style={'color': '#e74c3c'}),
            html.P(f"Error Message: {error_message}", style={'color': '#7f8c8d'}),
            html.A("Back to Home", href="/", style={'color': '#3498db'})
        ])
    
    def _get_general_dashboard_layout(self) -> html.Div:
        """Get general dashboard layout"""
        return self.general_dashboard.get_layout()
    

    

    

    

    

    
    def setup_q8q9_callbacks(self):
        """Setup Q8Q9 module callback functions"""
        if hasattr(self.q8q9_dashboard, 'setup_callbacks'):
            try:
                self.q8q9_dashboard.setup_callbacks(self.app)
                print("✓ Q8Q9 module callback functions setup completed")
            except Exception as e:
                print(f"❌ Q8Q9 module callback functions setup failed: {e}")
        else:
            print("⚠️ Q8Q9 module does not provide callback function setup method")
    
    def setup_q6q7q10q11_callbacks(self):
        """Setup Q6Q7Q10Q11 module callback functions"""
        if hasattr(self.q6q7q10q11_dashboard, 'setup_callbacks'):
            try:
                self.q6q7q10q11_dashboard.setup_callbacks(self.app)
                print("✓ Q6Q7Q10Q11 module callback functions setup completed")
            except Exception as e:
                print(f"❌ Q6Q7Q10Q11 module callback functions setup failed: {e}")
        else:
            print("⚠️ Q6Q7Q10Q11 module does not provide callback function setup method")

class IntegratedDashboardApp:
    """Integrated Dashboard Application - Architectural Design"""
    
    def __init__(self, title: str = "Analytics Dashboard"):
        # Create main application
        self.app = dash.Dash(__name__, suppress_callback_exceptions=True)
        self.app.title = title
        
        # Initialize components
        self.style_manager = style_manager
        self.visualizer = visualizer
        
        # Run data analysis scripts to ensure fresh data BEFORE initializing dashboards
        print("\n🔄 Running data analysis scripts before dashboard initialization...")
        self._run_data_analysis_scripts()
        print("✅ Data analysis scripts completed, now initializing dashboards...\n")
        
        # Initialize sub-modules AFTER data analysis scripts complete
        self.general_dashboard = GeneralDashboard(csv_file_path="orignaldata/question_response_count_statistics.csv")
        self.q345_dashboard = Q345Dashboard()  # New Q345Dashboard doesn't need parameters
        self.q8q9_dashboard = Q8Q9Dashboard(csv_file_path="orignaldata/Q8Q9_basic_data.csv")
        self.q6q7q10q11_dashboard = Q6Q7Q10Q11Dashboard()
        
        # Initialize managers
        self.callback_manager = CallbackManager(
            self.app, self.general_dashboard, self.q345_dashboard, self.q8q9_dashboard, self.q6q7q10q11_dashboard, self.style_manager
        )
        
        # Setup application
        self._setup_app()
    
    def _run_data_analysis_scripts(self):
        """Run data analysis scripts to ensure fresh data"""
        import subprocess
        import os
        import sys
        
        print("\n🔄 Running data analysis scripts to update base data...")
        print("="*60)
        
        # List of analysis scripts to run
        scripts = [
            ("q345_analyze_data_new.py", "Q3-Q5 Data Analysis"),
            ("q8q9_analysis.py", "Q8-Q9 Data Analysis"),
            ("q6q7q10q11_analysis.py", "Q6Q7Q10Q11 Data Analysis")
        ]
        
        for script_name, description in scripts:
            try:
                print(f"\n📊 Running {description}...")
                script_path = os.path.join(os.path.dirname(__file__), script_name)
                
                if os.path.exists(script_path):
                    # Run the script
                    result = subprocess.run(
                        [sys.executable, script_path],
                        capture_output=True,
                        text=True,
                        cwd=os.path.dirname(__file__)
                    )
                    
                    if result.returncode == 0:
                        print(f"✅ {description} completed successfully")
                        # Print last few lines of output for confirmation
                        if result.stdout:
                            output_lines = result.stdout.strip().split('\n')
                            if len(output_lines) > 0:
                                print(f"   📝 {output_lines[-1]}")
                    else:
                        print(f"⚠️ {description} completed with warnings")
                        if result.stderr:
                            print(f"   ❌ Error: {result.stderr.strip()[:200]}...")
                else:
                    print(f"⚠️ Script {script_name} not found, skipping...")
                    
            except Exception as e:
                print(f"❌ Error running {description}: {str(e)[:200]}...")
                print(f"   Continuing with existing data...")
        
        print("\n✅ Data analysis scripts execution completed")
        print("="*60)
    
    def _setup_app(self):
        """Setup application"""
        # Setup main layout
        self.app.layout = html.Div([
            dcc.Location(id='main-url', refresh=False),
            html.Div(id='main-page-content')
        ])
        
        # Setup callback functions
        self.callback_manager.setup_routing_callbacks()
        self.callback_manager.setup_general_callbacks()
        self.callback_manager.setup_q345_callbacks()
        self.callback_manager.setup_q8q9_callbacks()
        self.callback_manager.setup_q6q7q10q11_callbacks()
    
    def run(self, debug: bool = True, host: str = '127.0.0.1', port: int = 8080):
        """Launch integrated dashboard application"""
        print(f"\n{'='*60}")
        print("Analytics Dashboard - Unified Entry (Optimized)")
        print(f"{'='*60}")
        print(f"🌐 Access URL: http://{host}:{port}")
        print(f"📊 Integrated Modules: General Analysis, Specialized Analysis, Q8-Q9 Specialized Analysis, Q6Q7Q10Q11 Analysis")
        print(f"🔗 Route Addresses:")
        print(f"   Home: http://{host}:{port}/")
        print(f"   General Analysis: http://{host}:{port}/general")
        print(f"   Specialized Analysis: http://{host}:{port}/q345")
        print(f"   Q8-Q9 Analysis: http://{host}:{port}/q8q9")
        print(f"   Q6Q7Q10Q11 Analysis: http://{host}:{port}/q6q7q10q11")
        print(f"{'='*60}")
        print(f"\n✓ Integrated dashboard platform initialization completed")
        print(f"✓ Integrated modules: General Survey Analysis, Specialized Analysis, Q8-Q9 Specialized Analysis, Q6Q7Q10Q11 Analysis")
        print(f"✓ Architectural design loaded")
        print("\n🚀 Starting integrated dashboard server...")
        
        try:
            self.app.run(debug=debug, host=host, port=port)
        except Exception as e:
            print(f"❌ Startup failed: {e}")
            print("\nPossible solutions:")
            print(f"1. Check if port {port} is occupied")
            print("2. Ensure all dependency modules are normal")
            print("3. Check if data files exist")

def main():
    """Main function"""
    try:
        # Create and launch integrated application
        app = IntegratedDashboardApp()
        app.run(debug=True, host='127.0.0.1', port=8080)
    except KeyboardInterrupt:
        print("\n\n⏹️  Application stopped")
    except Exception as e:
        print(f"\n❌ Application runtime error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()