import streamlit as st
import pandas as pd
import os
import re
import sys
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any

# Import original modules from main directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_handler import DataHandler
from styles import style_manager
from visualizer import visualizer

class GeneralDataProcessor:
    def __init__(self, csv_file_path="orignaldata/question_response_count_statistics.csv"):
        self.csv_file_path = csv_file_path
        self.questions_data = {}
        self.analysis_results = None
        self.unique_users_count = 0
        self.load_data()
        self._load_user_data()

    def load_data(self):
        """Load survey data using DataHandler (same as original Dash version)"""
        try:
            # Import DataHandler from the main directory
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from data_handler import DataHandler
            
            # Use DataHandler to load data (same as original Dash version)
            data_handler = DataHandler()
            self.questions_data = data_handler.import_data_from_external(self.csv_file_path, 'csv')
            
            if self.questions_data:
                st.success(f"Successfully loaded {len(self.questions_data)} questions")
                print(f"General Survey Data loaded: {len(self.questions_data)} questions")
                
                self._merge_other_options()
                self._process_analysis_results()
            else:
                st.error("No valid data found in the file")
                print("General Survey Data loading failed: No data")
                self.questions_data = {}
                self.analysis_results = None
                
        except Exception as e:
            st.error(f"Error loading data: {e}")
            print(f"General Survey Data loading failed: {e}")
            self.questions_data = {}
            self.analysis_results = None

    def _process_analysis_results(self):
        if not self.questions_data:
            self.analysis_results = None
            return
        
        total_questions = len(self.questions_data)
        total_responses = 0
        max_responses = 0
        avg_responses = 0
        
        for question, options_data in self.questions_data.items():
            if isinstance(options_data, dict):
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

    def _merge_other_options(self):
        if not self.questions_data:
            return
        
        for question_key, options_data in self.questions_data.items():
            if ('Q4:' in question_key or 'Q5:' in question_key) and isinstance(options_data, dict):
                other_count = options_data.get('Other', 0)
                other_elaborated_count = options_data.get('Other (elaborated answ)', 0)
                
                if other_count > 0 or other_elaborated_count > 0:
                    if 'Other' in options_data: del options_data['Other']
                    if 'Other (elaborated answ)' in options_data: del options_data['Other (elaborated answ)']
                    options_data['Other'] = other_count + other_elaborated_count

    def _load_user_data(self):
        try:
            unique_users = set()
            q8q9_path = "orignaldata/Q8Q9_basic_data.csv"
            if os.path.exists(q8q9_path):
                q8q9_df = pd.read_csv(q8q9_path, encoding='utf-8', skiprows=2)
                if len(q8q9_df.columns) > 0:
                    user_ids = q8q9_df.iloc[:, 0].dropna().unique()
                    unique_users.update(user_ids)
            
            q6q7q10q11_path = "orignaldata/Q6Q7Q10Q11_basic_data.csv"
            if os.path.exists(q6q7q10q11_path):
                q6q7q10q11_df = pd.read_csv(q6q7q10q11_path, encoding='utf-8')
                if 'UserId' in q6q7q10q11_df.columns:
                    unique_users.update(q6q7q10q11_df['UserId'].dropna().unique())
            
            self.unique_users_count = len(unique_users)
        except Exception as e:
            self.unique_users_count = 0

    def _extract_question_number(self, question_text: str) -> int:
        match = re.match(r'^[Qq](\d+):', question_text)
        if match:
            return int(match.group(1))
        return 999

def create_chart(data, chart_type, title):
    """Create chart using original visualizer with proper styling"""
    try:
        # Use the visualizer's create_chart method with proper chart type mapping
        if chart_type == 'bar':
            fig = visualizer.create_chart(data, 'bar', title)
        elif chart_type == 'pie':
            fig = visualizer.create_chart(data, 'pie', title)
        elif chart_type == 'horizontal_bar':
            fig = visualizer.create_chart(data, 'horizontal_bar', title)
        else:
            fig = visualizer.create_chart(data, 'bar', title)
            
        return fig
        
    except Exception as e:
        st.error(f"Error creating chart: {str(e)}")
        # Fallback to simple chart with original styling
        fig = go.Figure()
        if data and isinstance(data, dict):
            colors = style_manager.get_chart_colors()
            fig.add_trace(go.Bar(
                x=list(data.keys()), 
                y=list(data.values()),
                marker_color=colors[0]
            ))
        fig.update_layout(
            title=title,
            title_font_size=20,
            title_x=0.5,
            title_xanchor='center',
            paper_bgcolor='white',
            plot_bgcolor='white'
        )
        return fig

def create_layout():
    """Create the main layout using original styles"""
    # Apply original styles using theme colors
    theme_colors = style_manager.get_theme_colors()
    chart_colors = style_manager.get_chart_colors()
    
    # Create custom CSS based on original styles
    custom_css = f"""
    <style>
    /* 使用原始配色方案 */
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
    
    /* 主容器样式 */
    .main .block-container {{
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    
    /* 指标容器样式 */
    .metrics-container {{
        background-color: var(--light-color);
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
        border: 1px solid var(--border-color);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    
    /* 数据表格样式 */
    .data-table {{
        background-color: var(--background-color);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    
    /* 选择框样式 */
    .stSelectbox > div > div {{
        background-color: var(--background-color);
        border: 1px solid var(--border-color);
        border-radius: 4px;
    }}
    
    /* 标题样式 */
    .main-title {{
        color: var(--primary-color);
        text-align: center;
        margin-bottom: 30px;
    }}
    
    /* 图表容器样式 */
    .js-plotly-plot {{
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }}
    
    /* 指标卡片样式 */
    [data-testid="metric-container"] {{
        background-color: var(--background-color);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }}
    
    /* 分隔线样式 */
    hr {{
        border: none;
        height: 2px;
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        margin: 20px 0;
    }}
    </style>
    """
    
    st.markdown(custom_css, unsafe_allow_html=True)
    
    st.title("📊 General Survey Analysis")
    st.markdown("---")
    
    # Initialize data processor
    data_processor = GeneralDataProcessor()
    questions_data = data_processor.questions_data
    
    if not questions_data:
        st.error("❌ No data available. Please check the data files.")
        return
    
    # Display summary statistics using original style
    if data_processor.analysis_results:
        # Create styled metrics container
        st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Questions", data_processor.analysis_results['total_questions'])
        with col2:
            st.metric("Total Responses", data_processor.analysis_results['total_responses'])
        with col3:
            st.metric("Avg Responses/Question", f"{data_processor.analysis_results['avg_responses']:.1f}")
        with col4:
            st.metric("Total Participants", data_processor.unique_users_count)
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("---")
    
    # Filter questions to only show Q1-Q5 (matching original dashboard)
    sorted_questions = sorted(questions_data.keys(), key=lambda x: data_processor._extract_question_number(x))
    filtered_questions = [q for q in sorted_questions if data_processor._extract_question_number(q) <= 5]

    if not filtered_questions:
        st.warning("No questions available for analysis.")
        return

    # Question selection and chart controls
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_question = st.selectbox(
            "Select Question to Analyze:",
            filtered_questions,
            key="question_selector"
        )
    
    # Auto-select chart type based on data characteristics
    if selected_question and selected_question in questions_data:
        question_data = questions_data[selected_question]
        auto_chart_type = visualizer.auto_select_chart_type(question_data)
        
        # Map auto-selected type to display names
        chart_type_mapping = {
            'pie': 'Pie Chart',
            'bar': 'Bar Chart', 
            'horizontal_bar': 'Horizontal Bar'
        }
        
        # Get default index based on auto-selection
        chart_options = ["Bar Chart", "Pie Chart", "Horizontal Bar"]
        default_chart = chart_type_mapping.get(auto_chart_type, 'Bar Chart')
        default_index = chart_options.index(default_chart) if default_chart in chart_options else 0
        
        with col2:
            chart_type = st.selectbox(
                "Chart Type:",
                chart_options,
                index=default_index,
                key="chart_type_selector",
                help=f"Auto-selected: {default_chart} (based on {len(question_data) if question_data else 0} options)"
            )
    else:
        with col2:
            chart_type = st.selectbox(
                "Chart Type:",
                ["Bar Chart", "Pie Chart", "Horizontal Bar"],
                key="chart_type_selector"
            )
    
    if selected_question and selected_question in questions_data:
        question_data = questions_data[selected_question]
        
        # Apply filtering for Q4 and Q5 questions (matching original dashboard logic)
        if ('Q4:' in selected_question or 'Q5:' in selected_question) and isinstance(question_data, dict):
            total_count = sum(question_data.values()) if question_data else 0
            if total_count > 0:
                # Filter out options with less than 5% of total responses
                filtered_data = {k: v for k, v in question_data.items() 
                               if 'other' not in k.lower() and (v/total_count) >= 0.05}
                # Always include "Other" if it exists
                if 'Other' in question_data:
                    filtered_data['Other'] = question_data['Other']
            else:
                filtered_data = question_data
        else:
            filtered_data = question_data
        
        # Create chart using original visualizer
        if chart_type == "Bar Chart":
            chart_type_key = "bar"
        elif chart_type == "Pie Chart":
            chart_type_key = "pie"
        else:
            chart_type_key = "horizontal_bar"
            
        fig = create_chart(filtered_data, chart_type_key, selected_question)
        
        # Display chart
        st.plotly_chart(fig, use_container_width=True)
        
        # Display data table with original styling
        st.markdown("### 📋 Response Details")
        
        if filtered_data:
            df = pd.DataFrame(list(filtered_data.items()), columns=['Option', 'Count'])
            df = df.sort_values('Count', ascending=False)
            df['Percentage'] = (df['Count'] / df['Count'].sum() * 100).round(1)
            df['Percentage'] = df['Percentage'].astype(str) + '%'
            
            # Apply table styling
            st.markdown('<div class="data-table">', unsafe_allow_html=True)
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No response data available for this question.")
    else:
        st.info("Please select a question to view the analysis.")