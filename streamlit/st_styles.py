"""
Streamlit unified style management module

"""

from typing import Dict, Any, List
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd

class StreamlitStyleManager:
    """Streamlit style manager - responsible for global style configuration and theme management"""
    
    # Default theme colors
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
    
    # Default chart color sequence
    DEFAULT_CHART_COLORS = [
        "#3498DB", "#E74C3C", "#2ECC71", "#F39C12", "#9B59B6",
        "#1ABC9C", "#34495E", "#F1C40F", "#E67E22", "#95A5A6",
        "#8E44AD", "#16A085", "#2C3E50", "#D35400", "#7F8C8D"
    ]
    
    def __init__(self):
        self.current_theme = self.DEFAULT_THEME_COLORS.copy()
        self.current_chart_colors = self.DEFAULT_CHART_COLORS.copy()
        # Global chart style configuration - based on unified standards from Q345 module
        self.global_chart_config = self._load_global_chart_config()
    
    def _load_global_chart_config(self) -> dict:
        """Load global chart configuration - unify chart styles across all modules"""
        return {
            'pie_chart': {
                'color_sequence': px.colors.qualitative.Set3,
                'text_position': 'inside',
                'text_info': 'percent+label',
                'hover_template': '<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>',
                'hole_size': 0.3,
                'marker_line': {'color': '#FFFFFF', 'width': 2}
            },
            'bar_chart': {
                'color_scale': 'Viridis',  # Use continuous color mapping, referencing dash version
                'hover_template': '<b>%{x}</b><br>Count: %{y}<br>Percentage: %{customdata:.1f}%<extra></extra>',
                'text_position': 'auto',
                'x_angle': -45
            },
            'horizontal_bar_chart': {
                'color_scale': 'Viridis',  # Use continuous color mapping, referencing dash version
                'hover_template': '<b>%{y}</b><br>Count: %{x}<br>Percentage: %{customdata:.1f}%<extra></extra>',
                'text_position': 'auto'
            },
            'layout': {
                'height': 550,  # Increased height from 450 to 550 for larger chart frame
                'margin': {'l': 50, 'r': 220, 't': 120, 'b': 60},  # Increased margins for larger frame
                'font': {
                    'size': 11,  # Reference dash version font size
                    'family': "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
                },
                'plot_bgcolor': 'rgba(0,0,0,0)',  # Transparent background
                'paper_bgcolor': 'rgba(0,0,0,0)',  # Transparent background
                'autosize': True,  # Auto-resize
                'title': {
                    'font': {
                        'size': 16,  # Title font size
                        'color': '#2C3E50',
                        'family': "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
                    },
                    'x': 0.5,
                    'xanchor': 'center',
                    'y': 0.95,  # Adjusted title position for better visibility
                    'yanchor': 'top',  # Title anchor
                    'pad': {'b': 20}  # Add bottom padding for title
                },
                'legend': {
                    'orientation': 'v',
                    'yanchor': 'top',  # Legend position
                    'y': 1,
                    'xanchor': 'left',
                    'x': 1.02,  # Legend position
                    'font': {'size': 11},
                    'itemsizing': 'trace',  # Legend item sizing
                    'itemwidth': 30  # Legend item width
                }
            }
        }
    
    def get_theme_colors(self) -> Dict[str, str]:
        """Get current theme colors"""
        return self.current_theme
    
    def get_chart_colors(self) -> List[str]:
        """Get chart color sequence"""
        return self.current_chart_colors
    
    def get_global_chart_config(self, chart_type: str = None) -> dict:
        """Get global chart configuration"""
        if chart_type and chart_type in self.global_chart_config:
            return self.global_chart_config[chart_type]
        return self.global_chart_config
    
    def apply_custom_css(self):
        """Apply custom CSS styles to Streamlit application"""
        theme_colors = self.get_theme_colors()
        
        custom_css = f"""
        <style>
        /* Use unified color scheme */
        :root {{
            --primary-color: {theme_colors.get('primary', '#3498DB')};
            --secondary-color: {theme_colors.get('secondary', '#F39C12')};
            --success-color: {theme_colors.get('success', '#2ECC71')};
            --danger-color: {theme_colors.get('danger', '#E74C3C')};
            --warning-color: {theme_colors.get('warning', '#F1C40F')};
            --info-color: {theme_colors.get('info', '#17A2B8')};
            --light-color: {theme_colors.get('light', '#F8F9FA')};
            --dark-color: {theme_colors.get('dark', '#343A40')};
            --background-color: {theme_colors.get('background', '#FFFFFF')};
            --text-color: {theme_colors.get('text', '#2C3E50')};
            --border-color: {theme_colors.get('border', '#DEE2E6')};
        }}
        
        /* Main container styles */
        .main .block-container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        
        /* Metrics container styles */
        .metrics-container {{
            background-color: var(--light-color);
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            border: 1px solid var(--border-color);
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        /* Data table styles */
        .data-table {{
            background-color: var(--background-color);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        /* Select box styles - Force text wrapping with highest priority */
        .stSelectbox > div > div {{
            background-color: var(--background-color);
            border: 1px solid var(--border-color);
            border-radius: 4px;
        }}
        
        /* CRITICAL: Universal text wrapping for all selectbox elements - including keyed selectboxes */
        .stSelectbox,
        .stSelectbox *,
        .stSelectbox div,
        .stSelectbox span,
        .stSelectbox [role="option"],
        .stSelectbox [data-baseweb="select"],
        .stSelectbox [data-baseweb="single-value"],
        .stSelectbox [data-baseweb="input"],
        .stSelectbox [data-baseweb="input-container"],
        .stSelectbox [data-baseweb="base-input"],
        div[data-testid*="stSelectbox"],
        div[data-testid*="stSelectbox"] *,
        div[data-testid*="stSelectbox"] div,
        div[data-testid*="stSelectbox"] span,
        div[data-testid="stSelectbox"],
        div[data-testid="stSelectbox"] *,
        div[data-testid="stSelectbox"] div,
        div[data-testid="stSelectbox"] span,
        [data-testid*="selectbox"],
        [data-testid*="selectbox"] *,
        [data-testid*="selectbox"] div,
        [data-testid*="selectbox"] span {{
            white-space: pre-wrap !important;
            word-wrap: break-word !important;
            overflow-wrap: break-word !important;
            word-break: break-word !important;
            text-overflow: unset !important;
            overflow: visible !important;
            max-width: none !important;
            width: auto !important;
            height: auto !important;
            min-height: auto !important;
        }}
        
        /* Select box main container - enhanced targeting */
        .stSelectbox,
        div[data-testid*="stSelectbox"],
        div[data-testid="stSelectbox"],
        [data-testid*="selectbox"] {{
            width: 100% !important;
            min-width: 350px !important;
            max-width: 100% !important;
        }}
        
        /* Select box root element - enhanced targeting */
        .stSelectbox [data-baseweb="select"],
        div[data-testid*="stSelectbox"] [data-baseweb="select"],
        div[data-testid="stSelectbox"] [data-baseweb="select"],
        [data-testid*="selectbox"] [data-baseweb="select"] {{
            width: 100% !important;
            min-width: 350px !important;
            max-width: 100% !important;
            height: auto !important;
            min-height: 60px !important;
        }}
        
        /* Main select container - enhanced targeting */
        .stSelectbox [data-baseweb="select"] > div,
        div[data-testid*="stSelectbox"] [data-baseweb="select"] > div,
        div[data-testid="stSelectbox"] [data-baseweb="select"] > div,
        [data-testid*="selectbox"] [data-baseweb="select"] > div {{
            min-height: 60px !important;
            height: auto !important;
            line-height: 1.8 !important;
            padding: 15px 20px !important;
            display: flex !important;
            align-items: flex-start !important;
            flex-wrap: wrap !important;
        }}
        
        /* Dropdown menu container - enhanced targeting */
        .stSelectbox [data-baseweb="popover"],
        div[data-testid*="stSelectbox"] [data-baseweb="popover"],
        div[data-testid="stSelectbox"] [data-baseweb="popover"],
        [data-testid*="selectbox"] [data-baseweb="popover"] {{
            max-width: none !important;
            width: auto !important;
            min-width: 450px !important;
            z-index: 9999 !important;
        }}
        
        /* Dropdown menu list - enhanced targeting */
        .stSelectbox [data-baseweb="menu"],
        div[data-testid*="stSelectbox"] [data-baseweb="menu"],
        div[data-testid="stSelectbox"] [data-baseweb="menu"],
        [data-testid*="selectbox"] [data-baseweb="menu"] {{
            max-width: none !important;
            width: auto !important;
            min-width: 450px !important;
            max-height: 400px !important;
            overflow-y: auto !important;
        }}
        
        /* Individual dropdown options - enhanced targeting */
        .stSelectbox [data-baseweb="menu"] [role="option"],
        div[data-testid*="stSelectbox"] [data-baseweb="menu"] [role="option"],
        div[data-testid="stSelectbox"] [data-baseweb="menu"] [role="option"],
        [data-testid*="selectbox"] [data-baseweb="menu"] [role="option"] {{
            line-height: 1.8 !important;
            padding: 18px 24px !important;
            display: block !important;
        }}
        
        /* Selected option display - enhanced targeting */
        .stSelectbox [data-baseweb="select"] [data-baseweb="base-input"],
        div[data-testid*="stSelectbox"] [data-baseweb="select"] [data-baseweb="base-input"],
        div[data-testid="stSelectbox"] [data-baseweb="select"] [data-baseweb="base-input"],
        [data-testid*="selectbox"] [data-baseweb="select"] [data-baseweb="base-input"] {{
            line-height: 1.8 !important;
            flex: 1 !important;
        }}
        
        /* Input container - enhanced targeting */
        .stSelectbox [data-baseweb="select"] [data-baseweb="input"],
        div[data-testid*="stSelectbox"] [data-baseweb="select"] [data-baseweb="input"],
        div[data-testid="stSelectbox"] [data-baseweb="select"] [data-baseweb="input"],
        [data-testid*="selectbox"] [data-baseweb="select"] [data-baseweb="input"] {{
            height: auto !important;
            min-height: 60px !important;
            display: flex !important;
            align-items: flex-start !important;
        }}
        
        /* Value container - enhanced targeting */
        .stSelectbox [data-baseweb="select"] [data-baseweb="input"] > div,
        div[data-testid*="stSelectbox"] [data-baseweb="select"] [data-baseweb="input"] > div,
        div[data-testid="stSelectbox"] [data-baseweb="select"] [data-baseweb="input"] > div,
        [data-testid*="selectbox"] [data-baseweb="select"] [data-baseweb="input"] > div {{
            flex-wrap: wrap !important;
            flex: 1 !important;
        }}
        
        /* Input container inner - enhanced targeting */
        .stSelectbox [data-baseweb="select"] [data-baseweb="input"] [data-baseweb="input-container"],
        div[data-testid*="stSelectbox"] [data-baseweb="select"] [data-baseweb="input"] [data-baseweb="input-container"],
        div[data-testid="stSelectbox"] [data-baseweb="select"] [data-baseweb="input"] [data-baseweb="input-container"],
        [data-testid*="selectbox"] [data-baseweb="select"] [data-baseweb="input"] [data-baseweb="input-container"] {{
            min-height: 40px !important;
            flex: 1 !important;
        }}
        
        /* Single value display - MOST IMPORTANT for selected text - enhanced targeting */
        .stSelectbox [data-baseweb="select"] [data-baseweb="single-value"],
        div[data-testid*="stSelectbox"] [data-baseweb="select"] [data-baseweb="single-value"],
        div[data-testid="stSelectbox"] [data-baseweb="select"] [data-baseweb="single-value"],
        [data-testid*="selectbox"] [data-baseweb="select"] [data-baseweb="single-value"] {{
            display: block !important;
            line-height: 1.8 !important;
            padding: 0 !important;
            margin: 0 !important;
        }}
        
        /* Placeholder text - enhanced targeting */
        .stSelectbox [data-baseweb="select"] [data-baseweb="placeholder"],
        div[data-testid*="stSelectbox"] [data-baseweb="select"] [data-baseweb="placeholder"],
        div[data-testid="stSelectbox"] [data-baseweb="select"] [data-baseweb="placeholder"],
        [data-testid*="selectbox"] [data-baseweb="select"] [data-baseweb="placeholder"] {{
            line-height: 1.8 !important;
        }}
        
        /* Dropdown arrow positioning - enhanced targeting */
        .stSelectbox [data-baseweb="select"] [data-baseweb="select-arrow"],
        div[data-testid*="stSelectbox"] [data-baseweb="select"] [data-baseweb="select-arrow"],
        div[data-testid="stSelectbox"] [data-baseweb="select"] [data-baseweb="select-arrow"],
        [data-testid*="selectbox"] [data-baseweb="select"] [data-baseweb="select-arrow"] {{
            flex-shrink: 0 !important;
            margin-left: 15px !important;
            align-self: flex-start !important;
            margin-top: 6px !important;
        }}
        
        /* Force override any conflicting styles - enhanced targeting */
        .stSelectbox [data-baseweb="select"] [data-baseweb="single-value"],
        .stSelectbox [data-baseweb="select"] [data-baseweb="single-value"] > div,
        .stSelectbox [data-baseweb="select"] [data-baseweb="single-value"] span,
        div[data-testid*="stSelectbox"] [data-baseweb="select"] [data-baseweb="single-value"],
        div[data-testid*="stSelectbox"] [data-baseweb="select"] [data-baseweb="single-value"] > div,
        div[data-testid*="stSelectbox"] [data-baseweb="select"] [data-baseweb="single-value"] span,
        div[data-testid="stSelectbox"] [data-baseweb="select"] [data-baseweb="single-value"],
        div[data-testid="stSelectbox"] [data-baseweb="select"] [data-baseweb="single-value"] > div,
        div[data-testid="stSelectbox"] [data-baseweb="select"] [data-baseweb="single-value"] span,
        [data-testid*="selectbox"] [data-baseweb="select"] [data-baseweb="single-value"],
        [data-testid*="selectbox"] [data-baseweb="select"] [data-baseweb="single-value"] > div,
        [data-testid*="selectbox"] [data-baseweb="select"] [data-baseweb="single-value"] span {{
            white-space: pre-wrap !important;
            word-wrap: break-word !important;
            overflow-wrap: break-word !important;
            word-break: break-word !important;
            text-overflow: unset !important;
            overflow: visible !important;
            max-width: none !important;
            width: auto !important;
            display: block !important;
        }}
        
        /* Title styles */
        .main-title {{
            color: var(--primary-color);
            text-align: center;
            margin-bottom: 30px;
        }}
        
        /* Chart container styles */
        .js-plotly-plot {{
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        
        /* Metric card styles */
        [data-testid="metric-container"] {{
            background-color: var(--background-color);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        
        /* Divider styles */
        hr {{
            border: none;
            height: 2px;
            background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
            margin: 20px 0;
        }}
        
        /* Q3-Q4-Q5 Summary Table symbol styles */
        .summary-table td {{
            font-size: 16px !important;
        }}
        
        .summary-table td:contains('○'),
        .summary-table td:contains('×') {{
            font-size: 20px !important;
            font-weight: bold !important;
            text-align: center !important;
        }}
        
        /* Alternative approach for symbol styling */
        .symbol-cell {{
            font-size: 20px !important;
            font-weight: bold !important;
            text-align: center !important;
        }}
        
        /* Sidebar styles */
        .css-1d391kg {{
            background-color: var(--light-color);
        }}
        
        /* Sidebar minimum width to accommodate long text, but keep resizable */
        section[data-testid="stSidebar"] {{
            min-width: 15px;
        }}
        
        /* Sidebar selectbox improvements for long text */
        section[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] {{
            min-width: 10px;
        }}
        
        /* Dropdown menu width for better text display */
        section[data-testid="stSidebar"] .stSelectbox [data-baseweb="popover"] {{
            min-width: 10px;
            max-width: 600px;
        }}
        
        section[data-testid="stSidebar"] .stSelectbox [data-baseweb="menu"] {{
            min-width: 10px;
            max-width: 600px;
        }}
        
        /* Chart title styles */
        .plotly .gtitle {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
            color: var(--text-color) !important;
        }}
        </style>
        """
        
        st.markdown(custom_css, unsafe_allow_html=True)
    
    def create_standardized_chart(self, data: Dict[str, Any], chart_type: str, title: str = '', 
                                custom_order: List[str] = None, preserve_order: bool = False, 
                                filter_threshold: float = 0.0) -> go.Figure:
        """Create chart using global standard styles with frequency filtering"""
        # Fix pandas Series boolean check issue
        if data is None or (hasattr(data, 'empty') and data.empty) or (isinstance(data, dict) and not data):
            fig = go.Figure()
            fig.add_annotation(
                text="No data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False, font_size=14
            )
            fig.update_layout(title=title, **self.get_global_chart_config('layout'))
            return fig
            
        # Apply frequency filtering - filter out items with percentage < filter_threshold
        # Exception: Q2 questions (YES/NO) should not be filtered
        if filter_threshold > 0 and not (title and 'Q2:' in title):
            total = sum(data.values()) if data.values() else 1
            filtered_data = {}
            
            for key, value in data.items():
                percentage = value / total
                if percentage >= filter_threshold:
                    filtered_data[key] = value
            
            # Use filtered data for chart creation (no "Others" category)
            data = filtered_data if filtered_data else data
            
        # Data preprocessing
        if preserve_order:
            sorted_data = data
        elif custom_order:
            ordered_data = {}
            remaining_data = data.copy()
            for item in custom_order:
                if item in remaining_data:
                    ordered_data[item] = remaining_data.pop(item)
            remaining_sorted = dict(sorted(remaining_data.items(), key=lambda x: x[1], reverse=True))
            ordered_data.update(remaining_sorted)
            sorted_data = ordered_data
        else:
            sorted_data = dict(sorted(data.items(), key=lambda x: x[1], reverse=True))
        labels = list(sorted_data.keys())
        values = list(sorted_data.values())
        total = sum(values) if values else 1
        percentages = [v / total * 100 for v in values]
        def wrap_label(label, max_length=15):
            """Label wrapping and legend display format optimization"""
            label_str = str(label)
            
            # Optimize legend display format: handle common format issues
            # 1. Unified capitalization format
            if label_str.lower() in ['extrabudgetary', 'regular budget', 'youth only', 
                                   'youth is one of the target groups', 'global', 'regional', 
                                   'national/local', 'yes', 'no', 'in person', 'online', 'both']:
                # For these standard values, use standardized format
                format_map = {
                    'extrabudgetary': 'Extrabudgetary',
                    'regular budget': 'Regular Budget',
                    'youth only': 'Youth Only',
                    'youth is one of the target groups': 'Youth Is One Of The Target Groups',
                    'global': 'Global',
                    'regional': 'Regional', 
                    'national/local': 'National/Local',
                    'yes': 'Yes',
                    'no': 'No',
                    'in person': 'In Person',
                    'online': 'Online',
                    'both': 'Both'
                }
                label_str = format_map.get(label_str.lower(), label_str)
            else:
                # For other labels, apply standard capitalization rules
                # But keep existing uppercase letters unchanged (like acronyms)
                words = label_str.split()
                formatted_words = []
                for word in words:
                    # If word is all uppercase and length > 1, keep as is (might be acronym)
                    if word.isupper() and len(word) > 1:
                        formatted_words.append(word)
                    # If word contains special characters like /, handle separately
                    elif '/' in word:
                        parts = word.split('/')
                        formatted_parts = [part.capitalize() if not (part.isupper() and len(part) > 1) else part for part in parts]
                        formatted_words.append('/'.join(formatted_parts))
                    else:
                        # Regular word capitalization
                        formatted_words.append(word.capitalize())
                label_str = ' '.join(formatted_words)
            
            # 2. Label length handling and line wrapping
            if len(label_str) <= max_length:
                return label_str
            words = label_str.split(' ')
            lines = []
            current_line = ""
            for word in words:
                if len(current_line) + len(word) + 1 <= max_length:
                    current_line += (" " if current_line else "") + word
                else:
                    lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)
            return "<br>".join(lines)
        wrapped_labels = [wrap_label(label) for label in labels]
        if chart_type == 'pie':
            config = self.get_global_chart_config('pie_chart')
            fig = go.Figure(data=[go.Pie(
                labels=wrapped_labels,
                values=values,
                hole=config['hole_size'],
                marker=dict(
                    colors=config['color_sequence'][:len(labels)],
                    line=config['marker_line']
                ),
                textinfo=config['text_info'],
                textposition=config['text_position'],
                hovertemplate=config['hover_template']
            )])
        elif chart_type == 'bar':
            config = self.get_global_chart_config('bar_chart')
            # Bar chart: arrange from left to right, high to low (no reversal, maintain original high to low order)
            
            # Create DataFrame to ensure order is not changed by plotly
            import pandas as pd
            df = pd.DataFrame({
                'labels': wrapped_labels,
                'values': values,
                'percentages': percentages
            })
            
            # If need to preserve order, set category_orders
            category_orders = None
            if preserve_order and wrapped_labels:
                category_orders = {'x': wrapped_labels}
            
            fig = px.bar(
                df,
                x='labels',
                y='values',
                color='values',
                color_continuous_scale=config['color_scale'],
                category_orders=category_orders
            )
            
            fig.update_layout(
                xaxis_tickangle=config['x_angle'],
                yaxis=dict(range=[0, max(values) * 1.1] if values else [0, 10])
            )
            fig.update_traces(
                hovertemplate=config['hover_template'],
                customdata=percentages,
                text=None,
                textposition=None
            )
            fig.update_coloraxes(colorbar_title="Count")
        elif chart_type == 'horizontal_bar':
            config = self.get_global_chart_config('horizontal_bar_chart')
            fig = px.bar(
                x=values,
                y=wrapped_labels,
                orientation='h',
                color=values,
                color_continuous_scale=config['color_scale']
            )
            fig.update_layout(
                xaxis=dict(range=[0, max(values) * 1.1] if values else [0, 10])
            )
            fig.update_traces(
                hovertemplate=config['hover_template'],
                customdata=percentages
            )
            fig.update_coloraxes(colorbar_title="Count")
        # Chart generation section (maintain original unified style logic)
        layout_config = self.get_global_chart_config('layout')
        if title:
            layout_config['title']['text'] = title
        fig.update_layout(**layout_config)
        # Force each chart to display in one row (Streamlit)
        fig.update_layout(
            autosize=True,
            margin=layout_config.get('margin', {}),
            height=layout_config.get('height', 450),
        )
        return fig
    
    def create_summary_metrics(self, metrics_data, columns: int = 4):
        """Create unified style metrics display"""
        st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
        
        # Handle different types of input data
        if isinstance(metrics_data, dict):
            items = list(metrics_data.items())
        elif isinstance(metrics_data, list):
            # If it's a list, check element type
            if metrics_data and isinstance(metrics_data[0], tuple) and len(metrics_data[0]) == 2:
                # If it's a tuple list, use directly
                items = metrics_data
            else:
                # If it's a regular list, convert to key-value pairs
                items = [(f"Metric{i+1}", item) for i, item in enumerate(metrics_data)]
        else:
            st.error("metrics_data must be a dictionary or list type")
            return
        
        cols = st.columns(columns)
        for i, item in enumerate(items):
            with cols[i % columns]:
            # Ensure item is a tuple containing two elements
                if isinstance(item, tuple) and len(item) == 2:
                    key, value = item
                    # Ensure key and value are of correct types
                    key_str = str(key)
                    if isinstance(value, dict) and 'value' in value:
                        st.metric(
                            label=value.get('label', key_str),
                            value=value['value'],
                            delta=value.get('delta', None)
                        )
                    else:
                        # Ensure value is of acceptable type
                        if isinstance(value, (int, float, str)) or value is None:
                            st.metric(label=key_str, value=value)
                        else:
                            st.metric(label=key_str, value=str(value))
                else:
                    # If not in correct tuple format, show error
                    st.error(f"Invalid metric data format: {item}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def create_data_table(self, data: pd.DataFrame, title: str = "Data Details"):
        """Create unified style data table"""
        st.markdown(f"### 📋 {title}")
        st.dataframe(data, use_container_width=True, hide_index=True)

# Create global style manager instance
style_manager = StreamlitStyleManager()

def create_chart(data, chart_type: str = 'bar', title: str = '', 
                custom_order: List[str] = None, preserve_order: bool = False,
                filter_threshold: float = 0.0) -> go.Figure:
    """Convenient chart creation function, supports dictionary and pandas Series"""
    # If it's pandas Series, convert to dictionary
    if hasattr(data, 'to_dict'):
        data = data.to_dict()
    
    return style_manager.create_standardized_chart(
        data=data, 
        chart_type=chart_type, 
        title=title,
        custom_order=custom_order,
        preserve_order=preserve_order,
        filter_threshold=filter_threshold
    )

def apply_page_style():
    """Apply page styles"""
    style_manager.apply_custom_css()

def create_metrics(metrics_data, columns: int = 4):
    """Create metrics display - supports dictionary and tuple list"""
    style_manager.create_summary_metrics(metrics_data, columns)

def create_table(data: pd.DataFrame, title: str = "Data Details"):
    """Create data table"""
    style_manager.create_data_table(data, title)
    
    def create_horizontal_bar_chart(self, labels, values, title="Horizontal Bar Chart", color_scale="Viridis"):
        """
        Create standard horizontal bar chart with automatic label wrapping, highest value at top
        """
        def wrap_label(label, max_length=15):
            label_str = str(label)
            if len(label_str) <= max_length:
                return label_str
            words = label_str.split(' ')
            lines = []
            current_line = ""
            for word in words:
                if len(current_line) + len(word) + 1 <= max_length:
                    current_line += (" " if current_line else "") + word
                else:
                    lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)
            return "<br>".join(lines)

        # Reverse order, highest at top
        labels = labels[::-1]
        values = values[::-1]
        wrapped_labels = [wrap_label(label, 15) for label in labels]

        import plotly.express as px
        fig = px.bar(
            x=values,
            y=wrapped_labels,
            orientation='h',
            color=values,
            color_continuous_scale=color_scale
        )
        fig.update_layout(
            title=title,
            xaxis_title="Count",
            yaxis_title="Category",
            coloraxis_colorbar=dict(title="Count")
        )
        return fig
