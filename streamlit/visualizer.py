import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, Any, List, Callable

# Try to import local style module
try:
    from st_styles import style_manager
except ImportError:
    # If unable to import,  create simplified version
    class StyleManager:
        def get_chart_colors(self):
            return ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']
        
        def get_theme_colors(self):
            return {
                'primary': '#3498DB',
                'light': '#F8F9FA',
                'text': '#2C3E50'
            }
        
        def create_plotly_theme(self):
            return {'layout': {'paper_bgcolor': 'white', 'plot_bgcolor': 'white'}}
        
        def get_global_chart_config(self, config_type):
            return {'title': {'text': ''}}
        
        def _wrap_title(self, title):
            return title
        
        def create_standardized_chart(self, data, chart_type, title):
            # Simplified chart creation
            fig = go.Figure()
            if data and isinstance(data, dict):
                if chart_type == 'pie':
                    fig.add_trace(go.Pie(
                        labels=list(data.keys()),
                        values=list(data.values()),
                        marker_colors=self.get_chart_colors()[:len(data)]
                    ))
                else:
                    fig.add_trace(go.Bar(
                        x=list(data.keys()),
                        y=list(data.values()),
                        marker_color=self.get_chart_colors()[0]
                    ))
                fig.update_layout(title=title, height=400)
            return fig
    
    style_manager = StyleManager()

class Visualizer:
    """Visualization layer - responsible for chart generation and style application"""
    
    def __init__(self):
        self.chart_registry = {}
        self.style_manager = style_manager
        self._register_default_charts()
    
    def _register_default_charts(self):
        """Register default chart types"""
        self.chart_registry['pie'] = self._create_pie_chart
        self.chart_registry['bar'] = self._create_bar_chart
        self.chart_registry['horizontal_bar'] = self._create_horizontal_bar_chart
        self.chart_registry['table'] = self._create_table
        self.chart_registry['summary_cards'] = self._create_summary_cards
    
    def register_external_chart(self, chart_name: str, chart_func: Callable):
        """Register external chart generation function"""
        self.chart_registry[chart_name] = chart_func
        print(f"Registered external chart type: {chart_name}")
    
    def load_external_style(self, style_config: Dict[str, Any]):
        """Load external style configuration, override default theme"""
        return self.style_manager.load_external_style(style_config)
    
    def create_chart(self, data: Dict[str, int], chart_type: str = 'bar', 
                    title: str = '', **kwargs) -> go.Figure:
        """Unified interface for creating charts"""
        # Prioritize using global standardized styles
        if chart_type in ['pie', 'bar', 'horizontal_bar'] and kwargs.get('use_global_style', True):
            return self.style_manager.create_standardized_chart(data, chart_type, title)
        
        # Compatible with original chart creation method
        if chart_type not in self.chart_registry:
            raise ValueError(f"Unsupported chart type: {chart_type}")
        
        chart_func = self.chart_registry[chart_type]
        fig = chart_func(data, title, **kwargs)
        
        # Apply theme styles
        self._apply_theme_to_figure(fig)
        return fig
    
    def _create_pie_chart(self, data: Dict[str, int], title: str = '', **kwargs) -> go.Figure:
        """Create pie chart"""
        if not data:
            fig = go.Figure()
            fig.add_annotation(
                text="No data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False, font_size=14
            )
            # Use _wrap_title to handle title line wrapping
            layout_config = self.style_manager.get_global_chart_config('layout')
            title_config = layout_config.get('title', {})
            title_config['text'] = self.style_manager._wrap_title(title)
            layout_config_copy = layout_config.copy()
            layout_config_copy['title'] = title_config
            fig.update_layout(**layout_config_copy)
            return fig
        
        # Sort data by values in descending order (left high, right low)
        sorted_data = dict(sorted(data.items(), key=lambda x: x[1], reverse=True))
        labels = list(sorted_data.keys())
        values = list(sorted_data.values())
        colors = self.style_manager.get_chart_colors()
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=kwargs.get('hole', 0.3),
            marker_colors=colors[:len(labels)]
        )])
        
        fig.update_layout(
            title=title,
            showlegend=True,
            height=kwargs.get('height', 400)
        )
        
        return fig
    
    def _create_bar_chart(self, data: Dict[str, int], title: str = '', **kwargs) -> go.Figure:
        """Create bar chart"""
        if not data:
            fig = go.Figure()
            fig.add_annotation(
                text="No data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False, font_size=14
            )
            # Use _wrap_title to handle title line wrapping
            layout_config = self.style_manager.get_global_chart_config('layout')
            title_config = layout_config.get('title', {})
            title_config['text'] = self.style_manager._wrap_title(title)
            layout_config_copy = layout_config.copy()
            layout_config_copy['title'] = title_config
            fig.update_layout(**layout_config_copy)
            return fig
        
        labels = list(data.keys())
        values = list(data.values())
        colors = self.style_manager.get_chart_colors()
        
        fig = go.Figure(data=[go.Bar(
            x=labels,
            y=values,
            marker_color=colors[0],
            text=values,
            textposition='auto'
        )])
        
        fig.update_layout(
            title=title,
            xaxis_title=kwargs.get('x_title', 'Options'),
            yaxis_title=kwargs.get('y_title', 'Count'),
            height=kwargs.get('height', 400)
        )
        
        # If labels are too long, rotate display
        max_label_length = max(len(str(label)) for label in labels) if labels else 0
        if max_label_length > 10:
            fig.update_layout(xaxis_tickangle=-45)
        
        return fig
    
    def _create_horizontal_bar_chart(self, data: Dict[str, int], title: str = '', **kwargs) -> go.Figure:
        """Create horizontal bar chart"""
        if not data:
            fig = go.Figure()
            fig.add_annotation(
                text="No data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False, font_size=14
            )
            # Use _wrap_title to handle title line wrapping
            layout_config = self.style_manager.get_global_chart_config('layout')
            title_config = layout_config.get('title', {})
            title_config['text'] = self.style_manager._wrap_title(title)
            layout_config_copy = layout_config.copy()
            layout_config_copy['title'] = title_config
            fig.update_layout(**layout_config_copy)
            return fig
        
        # Sort by value in descending order, then reverse for horizontal display (highest at top)
        sorted_data = dict(sorted(data.items(), key=lambda x: x[1], reverse=True))
        labels = list(reversed(list(sorted_data.keys())))
        values = list(reversed(list(sorted_data.values())))
        colors = self.style_manager.get_chart_colors()
        
        fig = go.Figure(data=[go.Bar(
            x=values,
            y=labels,
            orientation='h',
            marker_color=colors[0],
            text=values,
            textposition='auto'
        )])
        
        fig.update_layout(
            title=title,
            xaxis_title=kwargs.get('x_title', 'Count'),
            yaxis_title=kwargs.get('y_title', 'Options'),
            height=max(400, len(labels) * 30)
        )
        
        return fig
    
    def _create_table(self, data: Dict[str, int], title: str = '', **kwargs) -> go.Figure:
        """Create table"""
        if not data:
            return go.Figure()
        
        # Calculate percentages
        total = sum(data.values())
        percentages = [f"{(value/total)*100:.1f}%" if total > 0 else "0%" for value in data.values()]
        
        fig = go.Figure(data=[go.Table(
            header=dict(
                values=['Options', 'Count', 'Percentage'],
                fill_color=self.style_manager.get_theme_colors()['primary'],
                font=dict(color='white', size=14),
                align='center'
            ),
            cells=dict(
                values=[list(data.keys()), list(data.values()), percentages],
                fill_color=self.style_manager.get_theme_colors()['light'],
                font=dict(color=self.style_manager.get_theme_colors()['text'], size=12),
                align='center'
            )
        )])
        
        fig.update_layout(
            title=title,
            height=kwargs.get('height', min(600, len(data) * 40 + 100))
        )
        
        return fig
    
    def _create_summary_cards(self, data: Dict[str, int], title: str = '', **kwargs) -> Dict[str, Any]:
        """Create summary card data (returns data instead of chart)"""
        if not data:
            return {}
        
        total_responses = sum(data.values())
        most_common = max(data.items(), key=lambda x: x[1]) if data else ('None', 0)
        
        return {
            'total_responses': total_responses,
            'total_options': len(data),
            'most_common_option': most_common[0],
            'most_common_count': most_common[1],
            'response_rate': f"{(most_common[1]/total_responses)*100:.1f}%" if total_responses > 0 else "0%"
        }
    
    def _apply_theme_to_figure(self, fig: go.Figure):
        """Apply theme styles to chart"""
        theme = self.style_manager.create_plotly_theme()
        fig.update_layout(**theme['layout'])
    
    def create_multi_question_dashboard(self, questions_data: Dict[str, Dict[str, int]], 
                                      chart_type: str = 'bar') -> List[go.Figure]:
        """Create dashboard charts for multiple questions - using global standard styles"""
        figures = []
        
        for question, data in questions_data.items():
            # Truncate overly long question titles
            short_title = question[:80] + '...' if len(question) > 80 else question
            
            # Automatically select chart type
            auto_type = self.auto_select_chart_type(data)
            selected_type = chart_type if chart_type != 'auto' else auto_type
            
            # Create charts using global standardized styles
            if selected_type in ['pie', 'bar', 'horizontal_bar']:
                fig = self.style_manager.create_standardized_chart(data, selected_type, title=short_title)
            else:
                # Compatible with other chart types
                fig = self.create_chart(data, selected_type, title=short_title, use_global_style=False)
            
            figures.append(fig)
        
        return figures
    
    def get_available_chart_types(self) -> List[str]:
        """Get list of available chart types"""
        return list(self.chart_registry.keys())
    
    def auto_select_chart_type(self, data: Dict[str, int]) -> str:
        """Automatically select appropriate chart type based on data characteristics"""
        if not data:
            return 'table'
        
        num_options = len(data)
        max_label_length = max(len(str(label)) for label in data.keys())
        
        # Select chart type based on number of options and label length
        if num_options <= 5:
            return 'pie'
        elif max_label_length > 20 or num_options > 10:
            return 'horizontal_bar'
        else:
            return 'bar'

# Global visualizer instance
visualizer = Visualizer()