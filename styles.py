from typing import Dict, Any
import json

class StyleManager:
    """Style management module - responsible for global style configuration and theme management"""
    
    # Default theme styles
    DEFAULT_THEME_COLORS = {
        "primary": "#3498DB",
        "secondary": "#F39C12",
        "success": "#2ECC71",
        "danger": "#E74C3C",
        "warning": "#F1C40F",
        "info": "#17A2B8",
        "light": "#F8F9FA",
        "dark": "#343A40",
        "background": "#FFFFFF",
        "text": "#2C3E50",
        "border": "#DEE2E6"
    }
    
    DEFAULT_CHART_COLORS = [
        "#3498DB", "#E74C3C", "#2ECC71", "#F39C12", "#9B59B6",
        "#1ABC9C", "#34495E", "#F1C40F", "#E67E22", "#95A5A6"
    ]
    
    DEFAULT_LAYOUT_STYLES = {
        "container": {
            "margin": "0 auto",
            "padding": "20px",
            "maxWidth": "1200px",
            "fontFamily": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
        },
        "header": {
            "backgroundColor": "#3498DB",
            "color": "white",
            "padding": "20px",
            "marginBottom": "20px",
            "borderRadius": "8px",
            "textAlign": "center"
        },
        "card": {
            "backgroundColor": "white",
            "border": "1px solid #DEE2E6",
            "borderRadius": "8px",
            "padding": "20px",
            "marginBottom": "20px",
            "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"
        },
        "control_panel": {
            "backgroundColor": "#F8F9FA",
            "padding": "15px",
            "borderRadius": "8px",
            "marginBottom": "20px"
        }
    }
    
    def __init__(self):
        self.current_theme = self.DEFAULT_THEME_COLORS.copy()
        self.current_chart_colors = self.DEFAULT_CHART_COLORS.copy()
        self.current_layout = self.DEFAULT_LAYOUT_STYLES.copy()
        self.external_styles = {}
        # Global chart style configuration - unified standard based on Q345 module
        self.global_chart_config = self._load_global_chart_config()
    
    def load_external_style(self, style_config: Dict[str, Any]) -> bool:
        """Load external style configuration, override default theme"""
        try:
            if isinstance(style_config, str):
                # If it's a file path, read JSON file
                with open(style_config, 'r', encoding='utf-8') as f:
                    style_config = json.load(f)
            
            self.external_styles = style_config
            
            # Override theme colors
            if 'theme_colors' in style_config:
                self.current_theme.update(style_config['theme_colors'])
            
            # Override chart colors
            if 'chart_colors' in style_config:
                self.current_chart_colors = style_config['chart_colors']
            
            # Override layout styles
            if 'layout_styles' in style_config:
                for component, styles in style_config['layout_styles'].items():
                    if component in self.current_layout:
                        self.current_layout[component].update(styles)
                    else:
                        self.current_layout[component] = styles
            
            return True
        except Exception as e:
            print(f"Style loading error: {e}")
            return False
    
    def get_theme_colors(self) -> Dict[str, str]:
        """Get current theme colors"""
        return self.current_theme
    
    def get_chart_colors(self) -> list:
        """Get chart color sequence"""
        return self.current_chart_colors
    
    def _load_global_chart_config(self) -> dict:
        """Load global chart configuration - unify chart styles across all modules"""
        return {
            'pie_chart': {
                'color_sequence': 'Set3',  # plotly.express.colors.qualitative.Set3
                'text_position': 'inside',
                'text_info': 'percent+label',
                'hover_template': '<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>',
                'hole_size': 0.3
            },
            'bar_chart': {
                'color_scale': 'Viridis',  # Continuous color mapping
                'x_angle': -45,  # X-axis label angle
                'hover_template': '<b>%{x}</b><br>Count: %{y}<br>Percentage: %{customdata:.1f}%<extra></extra>',
                'text_position': 'auto'
            },
            'horizontal_bar_chart': {
                'color_scale': 'Viridis',
                'hover_template': '<b>%{y}</b><br>Count: %{x}<br>Percentage: %{customdata:.1f}%<extra></extra>',
                'text_position': 'auto'
            },
            'layout': {
                'height': 450,
                'margin': {'l': 50, 'r': 220, 't': 40, 'b': 50},
                'font': {'size': 11},
                'plot_bgcolor': 'rgba(0,0,0,0)',
                'paper_bgcolor': 'rgba(0,0,0,0)',
                'autosize': True,
                'title': {
                    'font': {
                        'size': 16,
                        'color': '#2C3E50',
                        'family': "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
                    },
                    'x': 0.5,
                    'xanchor': 'center',
                    'y': 0.95,
                    'yanchor': 'top'
                },
                'legend': {
                    'orientation': 'v',
                    'yanchor': 'top',
                    'y': 1,
                    'xanchor': 'left',
                    'x': 1.02,
                    'font': {'size': 11},
                    'itemsizing': 'trace',
                    'itemwidth': 30
                }
            },
            'card_style': {
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
            },
            'container_style': {
                'backgroundColor': '#f8f9fa',
                'borderRadius': '12px',
                'padding': '10px',
                'boxShadow': '0 3px 10px rgba(0,0,0,0.1)',
                'border': '1px solid #e9ecef',
                'margin': '0 auto',
                'textAlign': 'center',
                'width': '100%',
                'boxSizing': 'border-box'
            }
        }
    
    def get_style(self, style_name: str) -> dict:
        """Get specified style configuration
        
        Args:
            style_name: Style name ('card_style', 'container_style')
            
        Returns:
            dict: Style configuration dictionary
        """
        if style_name in self.global_chart_config:
            return self.global_chart_config[style_name]
        return {}
    
    def get_global_chart_config(self, chart_type: str = None) -> dict:
        """Get global chart configuration
        
        Args:
            chart_type: Chart type ('pie_chart', 'bar_chart', 'horizontal_bar_chart', 'layout', 'card_style', 'container_style')
            
        Returns:
            dict: Configuration dictionary, returns specific type configuration if chart_type is specified, otherwise returns all configurations
        """
        if chart_type and chart_type in self.global_chart_config:
            return self.global_chart_config[chart_type]
        return self.global_chart_config
    
    def create_region_filter_component(self, filter_id: str, regions: list = None, csv_file_path: str = None) -> 'html.Div':
        """Create standardized region filter dropdown component
        
        Args:
            filter_id: ID of the dropdown menu
            regions: Optional region list, uses regions from CSV file if None
            csv_file_path: Path to CSV file containing region data (optional)
            
        Returns:
            html.Div: Region filter component
        """
        from dash import html, dcc
        import pandas as pd
        import os
        
        if regions is None:
            # Try to load regions from CSV file
            if csv_file_path is None:
                # Default path for Q6Q7Q10Q11 works list
                csv_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'result', 'q6q7q10q11_works_list.csv')
            
            try:
                if os.path.exists(csv_file_path):
                    df = pd.read_csv(csv_file_path, encoding='utf-8')
                    if 'Department/Region' in df.columns:
                        # Extract unique regions from CSV file
                        unique_regions = df['Department/Region'].dropna().unique()
                        regions = sorted([str(region) for region in unique_regions])
                    else:
                        raise KeyError("Department/Region column not found")
                else:
                    raise FileNotFoundError(f"CSV file not found: {csv_file_path}")
            except Exception as e:
                print(f"Warning: Could not load regions from CSV file ({e}). Using fallback default regions.")
                # Fallback to default region list if CSV loading fails
                regions = [
                    'Communication and Public Information',
                    'Conditions of Work and Equality',
                    'Employment Policy, Job Creation and Livelihoods',
                    'Governance and Tripartism',
                    'International Training Centre of the ILO',
                    'Region: Africa',
                    'Region: Arab States',
                    'Region: Asia and the Pacific',
                    'Region: Europe and Central Asia',
                    'Region: Latin America and the Caribbean',
                    'Research and Publications',
                    'Sectoral Policies',
                    'Statistics',
                    'Sustainable Enterprises, Productivity and Just Transition',
                    'Universal Social Protection'
                ]
        
        # Create options list, including "All" option
        options = [{'label': 'All', 'value': 'all'}]
        options.extend([{'label': region, 'value': region} for region in sorted(regions)])
        
        return html.Div([
            html.Label("Select Organizational unit:", style={
                'fontWeight': 'bold',
                'marginBottom': '5px',
                'color': '#2c3e50'
            }),
            dcc.Dropdown(
                id=filter_id,
                options=options,
                value='all',  # Default selection "All"
                style={
                    'marginBottom': '20px',
                    'textAlign': 'left'  # Set to left alignment
                },
                placeholder="Select region or department..."
            )
        ], style={
            'backgroundColor': '#f8f9fa',
            'padding': '15px',
            'borderRadius': '8px',
            'marginBottom': '20px',
            'border': '1px solid #dee2e6'
        })
    
    def get_filtered_data_by_region(self, data, region_filter: str, region_column: str = 'Department/Region'):
        """Generic method for filtering data by region
        
        Args:
            data: Data to filter (DataFrame or dict)
            region_filter: Selected region filter value
            region_column: Name of the region column
            
        Returns:
            Filtered data
        """
        import pandas as pd
        
        if region_filter == 'all' or region_filter is None:
            return data
        
        if isinstance(data, pd.DataFrame):
            if region_column in data.columns:
                return data[data[region_column] == region_filter]
            else:
                return data
        elif isinstance(data, dict):
            # For dictionary type data, need to handle based on specific situation
            return data
        
        return data
    
    def _wrap_title(self, title: str, max_length: int = 100) -> str:
        """Wrap long titles into multiple lines with improved single-line display
        
        Args:
            title: Original title
            max_length: Maximum characters per line (increased for better single-line display)
            
        Returns:
            str: Title with line breaks (optimized for single-line when possible)
        """
        # Try to keep titles on single line by increasing max_length
        if len(title) <= max_length:
            return title
        
        # For very long titles, use intelligent wrapping
        words = title.split(' ')
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 <= max_length:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return '\n'.join(lines)
    
    def create_standardized_chart(self, data: dict, chart_type: str, title: str = '', custom_order: list = None, preserve_order: bool = False) -> 'go.Figure':
        """Create charts using global standard styles
        
        Args:
            data: Chart data dictionary {label: value}
            chart_type: Chart type ('pie', 'bar', 'horizontal_bar')
            title: Chart title
            custom_order: Custom order list for specific chart labels
            preserve_order: If True, don't sort the data, preserve the input order
            
        Returns:
            plotly.graph_objects.Figure: Standardized style chart
        """
        import plotly.express as px
        import plotly.graph_objects as go
        
        if not data:
            fig = go.Figure()
            fig.add_annotation(
                text="No data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False, font_size=14
            )
            return fig
        
        # Data preprocessing
        # Apply custom ordering if provided, otherwise sort by values in descending order
        if preserve_order:
            # Don't sort, preserve the input order
            sorted_data = data
        elif custom_order and title == 'Types Of Advocacy Or Partnership Outputs In 2024':
            # Custom ordering for "Types Of Advocacy Or Partnership Outputs In 2024"
            ordered_data = {}
            remaining_data = data.copy()
            
            # First, add items in custom order if they exist in data
            for item in custom_order:
                if item in remaining_data:
                    ordered_data[item] = remaining_data.pop(item)
            
            # Then add remaining items sorted by value (descending)
            remaining_sorted = dict(sorted(remaining_data.items(), key=lambda x: x[1], reverse=True))
            ordered_data.update(remaining_sorted)
            
            sorted_data = ordered_data
        else:
            # Sort data by values in descending order for bar charts (left high, right low)
            sorted_data = dict(sorted(data.items(), key=lambda x: x[1], reverse=True))
        labels = list(sorted_data.keys())
        values = list(sorted_data.values())
        total = sum(values)
        percentages = [(v/total*100) if total > 0 else 0 for v in values]
        
        # Process labels for better display with line wrapping
        def wrap_label(label, max_length=20):
            """Wrap long labels into multiple lines and capitalize first letter"""
            label_str = str(label)
            # Capitalize first letter of the label
            if label_str:
                label_str = label_str[0].upper() + label_str[1:] if len(label_str) > 1 else label_str.upper()
            
            if len(label_str) <= max_length:
                return label_str
            
            # Split by spaces first
            words = label_str.split(' ')
            if len(words) == 1:
                # If it's a single long word, split by character
                lines = []
                for i in range(0, len(label_str), max_length):
                    lines.append(label_str[i:i+max_length])
                return '<br>'.join(lines)
            else:
                # Wrap by words
                lines = []
                current_line = []
                current_length = 0
                
                for word in words:
                    if current_length + len(word) + 1 <= max_length:
                        current_line.append(word)
                        current_length += len(word) + 1
                    else:
                        if current_line:
                            lines.append(' '.join(current_line))
                        current_line = [word]
                        current_length = len(word)
                
                if current_line:
                    lines.append(' '.join(current_line))
                
                return '<br>'.join(lines)
        
        # Apply label wrapping
        wrapped_labels = [wrap_label(label) for label in labels]
        
        # Wrap title for better display
        wrapped_title = self._wrap_title(title)
        
        # Create chart based on chart type
        if chart_type == 'pie':
            config = self.get_global_chart_config('pie_chart')
            fig = px.pie(
                values=values,
                names=wrapped_labels,
                color_discrete_sequence=getattr(px.colors.qualitative, config['color_sequence'])
            )
            fig.update_traces(
                textposition=config['text_position'],
                textinfo=config['text_info'],
                hovertemplate=config['hover_template'],
                hole=config.get('hole_size', 0)
            )
            # Legend configuration is already set in global layout, no need to repeat
            

            
        elif chart_type == 'bar':
            config = self.get_global_chart_config('bar_chart')
            fig = px.bar(
                x=wrapped_labels,
                y=values,
                color=values,  # Use actual values instead of percentages for color mapping
                color_continuous_scale=config['color_scale']
            )
            fig.update_layout(
                xaxis_tickangle=config['x_angle'],
                yaxis=dict(
                    range=[0, max(values) * 1.1] if values else [0, 10]  # Set Y-axis range to 1.1 times the maximum data value
                )
            )
            fig.update_traces(
                hovertemplate=config['hover_template'],
                customdata=percentages,
                text=None,
                textposition=None
            )
            # Update colorbar title
            fig.update_coloraxes(colorbar_title="count")
            
        elif chart_type == 'horizontal_bar':
            config = self.get_global_chart_config('horizontal_bar_chart')
            # For horizontal bar charts, reverse the order to show highest at top
            reversed_labels = wrapped_labels[::-1]
            reversed_values = values[::-1]
            reversed_percentages = percentages[::-1]
            
            # Create short labels for horizontal bars
            short_labels = [wrap_label(label, 15) for label in reversed(labels)]
            
            fig = px.bar(
                x=reversed_values,
                y=short_labels,
                orientation='h',
                color=reversed_values,  # Use actual values instead of percentages for color mapping
                color_continuous_scale=config['color_scale']
            )
            fig.update_layout(
                xaxis=dict(
                    range=[0, max(values) * 1.1] if values else [0, 10]  # Set X-axis range to 1.1 times the maximum data value
                )
            )
            fig.update_traces(
                hovertemplate=config['hover_template'],
                customdata=percentages
            )
            # Update colorbar title
            fig.update_coloraxes(colorbar_title="Count")
        
        else:
            raise ValueError(f"Unsupported chart type: {chart_type}")
        
        # Apply global layout styles (excluding title to avoid conflicts)
        layout_config = self.get_global_chart_config('layout')
        layout_config_copy = layout_config.copy()
        title_config = layout_config_copy.pop('title', {})
        
        # Comment out internal chart titles, keep only HTML main titles
        # title_config['text'] = wrapped_title
        # layout_config_copy['title'] = title_config
        
        # Apply all layout styles including title in one call to avoid conflicts
        fig.update_layout(**layout_config_copy)
        
        return fig
    
    def get_layout_style(self, component: str) -> Dict[str, Any]:
        """Get layout style for specified component"""
        return self.current_layout.get(component, {})
    
    def get_dash_style(self, component: str) -> Dict[str, Any]:
        """Get style dictionary applicable to Dash components"""
        style = self.get_layout_style(component)
        # Convert CSS style names to Dash format (camelCase)
        dash_style = {}
        for key, value in style.items():
            # Convert hyphenated naming to camelCase
            dash_key = ''.join(word.capitalize() if i > 0 else word for i, word in enumerate(key.split('-')))
            dash_style[dash_key] = value
        return dash_style
    
    def create_plotly_theme(self) -> Dict[str, Any]:
        """Create Plotly chart theme configuration"""
        return {
            'layout': {
                'colorway': self.current_chart_colors,
                'font': {'family': "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"},
                'paper_bgcolor': self.current_theme['background'],
                'plot_bgcolor': self.current_theme['background'],
                'title': {
                    'font': {'color': self.current_theme['text'], 'size': 18},
                    'x': 0.5
                },
                'xaxis': {
                    'gridcolor': self.current_theme['border'],
                    'linecolor': self.current_theme['border'],
                    'tickfont': {'color': self.current_theme['text']}
                },
                'yaxis': {
                    'gridcolor': self.current_theme['border'],
                    'linecolor': self.current_theme['border'],
                    'tickfont': {'color': self.current_theme['text']}
                }
            }
        }
    
    def export_current_style(self, file_path: str = None) -> Dict[str, Any]:
        """Export current style configuration"""
        style_config = {
            'theme_colors': self.current_theme,
            'chart_colors': self.current_chart_colors,
            'layout_styles': self.current_layout,
            'external_styles': self.external_styles
        }
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(style_config, f, indent=2, ensure_ascii=False)
            except Exception as e:
                print(f"Style export error: {e}")
        
        return style_config
    
    def reset_to_default(self):
        """Reset to default styles"""
        self.current_theme = self.DEFAULT_THEME_COLORS.copy()
        self.current_chart_colors = self.DEFAULT_CHART_COLORS.copy()
        self.current_layout = self.DEFAULT_LAYOUT_STYLES.copy()
        self.external_styles = {}

# Global style manager instance
style_manager = StyleManager()