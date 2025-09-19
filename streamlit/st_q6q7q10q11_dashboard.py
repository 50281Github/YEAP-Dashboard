import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from typing import Dict, Any, List

# 标准化颜色配置
STANDARD_COLORS = [
    '#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6',
    '#1abc9c', '#34495e', '#e67e22', '#95a5a6', '#f1c40f',
    '#8e44ad', '#16a085', '#2c3e50', '#d35400', '#7f8c8d'
]

class Q6Q7Q10Q11DataProcessor:
    """Q6Q7Q10Q11 Data Processor - responsible for loading and preprocessing analyzed data"""
    
    def __init__(self, base_path: str = None):
        """Initialize data processor"""
        self.base_path = base_path or "."
        self.cpo_glo_data = None
        self.works_count_data = None
        self.frequency_data = None
        self.works_list_data = None
        self.special_fields_data = None
        self._load_all_data()
    
    def _load_all_data(self):
        """Load all data files"""
        try:
            # Load CPO/GLO code analysis results
            cpo_glo_path = os.path.join(self.base_path, 'result/q6q7q10q11_cpo_glo_analysis_results.csv')
            if os.path.exists(cpo_glo_path):
                self.cpo_glo_data = pd.read_csv(cpo_glo_path, encoding='utf-8')
            else:
                self.cpo_glo_data = pd.DataFrame()
            
            # Load works count analysis results
            works_count_path = os.path.join(self.base_path, 'result/q6q7q10q11_works_count_analysis_results.csv')
            if os.path.exists(works_count_path):
                self.works_count_data = pd.read_csv(works_count_path, encoding='utf-8')
            else:
                self.works_count_data = pd.DataFrame()
            
            # Load frequency analysis results
            frequency_path = os.path.join(self.base_path, 'result/q6q7q10q11_frequency_analysis_results.csv')
            if os.path.exists(frequency_path):
                self.frequency_data = pd.read_csv(frequency_path, encoding='utf-8')
            else:
                self.frequency_data = pd.DataFrame()
            
            # Load works name list
            works_list_path = os.path.join(self.base_path, 'result/q6q7q10q11_works_list.csv')
            if os.path.exists(works_list_path):
                self.works_list_data = pd.read_csv(works_list_path, encoding='utf-8')
            else:
                self.works_list_data = pd.DataFrame()
            
            # Load special fields analysis results
            special_fields_path = os.path.join(self.base_path, 'result/q6q7q10q11_special_fields_analysis_results.csv')
            if os.path.exists(special_fields_path):
                self.special_fields_data = pd.read_csv(special_fields_path, encoding='utf-8')
            else:
                self.special_fields_data = pd.DataFrame()
            
        except Exception as e:
            st.error(f"Data loading error: {e}")
            # Create empty DataFrames as backup
            self.cpo_glo_data = pd.DataFrame()
            self.works_count_data = pd.DataFrame()
            self.frequency_data = pd.DataFrame()
            self.works_list_data = pd.DataFrame()
            self.special_fields_data = pd.DataFrame()
    
    def get_summary_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get summary statistics data"""
        try:
            # Q6, Q7, Q10, Q11 - 4 questions
            questions_count = 4
            
            # Calculate participant instances and total works from works count analysis results file
            total_participant_instances = 0
            total_works = 0
            
            if not self.works_count_data.empty:
                # Filter out Q9 data, only keep Q6, Q7, Q10, Q11
                filtered_works_data = self.works_count_data[self.works_count_data['Question'].isin(['Q6', 'Q7', 'Q10', 'Q11'])]
                # Calculate total participant instances (sum of participants for each question)
                total_participant_instances = filtered_works_data['Users with Related Works'].sum()
                # Calculate total works count
                total_works = filtered_works_data['Total Works Count'].sum()
            
            # Calculate unique user ID count (actual participant count)
            unique_participants = 0
            if not self.works_list_data.empty:
                user_id_col = 'User ID' if 'User ID' in self.works_list_data.columns else 'User ID'
                unique_participants = self.works_list_data[user_id_col].nunique()
            
            # Calculate averages
            avg_projects_per_question = total_works / questions_count if questions_count > 0 else 0
            avg_works_per_participant = total_works / total_participant_instances if total_participant_instances > 0 else 0
            
            return {
                "stat1": {"value": questions_count, "label": "Questions Analyzed"},
                "stat2": {"value": unique_participants, "label": "Participants with Outputs"},
                "stat3": {"value": f"{avg_projects_per_question:.1f}", "label": "Avg Outputs/Question"},
                "stat4": {"value": f"{avg_works_per_participant:.1f}", "label": "Avg Outputs/Participant"}
            }
        except Exception as e:
            st.error(f"Get summary statistics error: {e}")
            return {
                "stat1": {"value": "N/A", "label": "Questions Analyzed"},
                "stat2": {"value": "N/A", "label": "Participants"},
                "stat3": {"value": "N/A", "label": "Avg Projects/Question"},
                "stat4": {"value": "N/A", "label": "Avg Outputs/Participant"}
            }
    
    def get_works_count_data(self) -> Dict[str, Dict[str, Any]]:
        """Get works count statistics data"""
        try:
            if self.works_count_data.empty:
                return {}
            
            # Filter to only include Q6, Q7, Q10, Q11
            filtered_data = self.works_count_data[self.works_count_data['Question'].isin(['Q6', 'Q7', 'Q10', 'Q11'])]
            
            result = {}
            for _, row in filtered_data.iterrows():
                question = row['Question']
                result[question] = {
                    'users_with_works': int(row['Users with Related Works']),
                    'total_works': int(row['Total Works Count']),
                    'avg_works_per_user': float(row['Average Works per User'])
                }
            
            return result
        except Exception as e:
            st.error(f"Get works count data error: {e}")
            return {}
    
    def get_frequency_data(self, question: str = None) -> Dict[str, Any]:
        """Get frequency analysis data"""
        try:
            if self.frequency_data.empty:
                return {}
            
            if question:
                question_data = self.frequency_data[self.frequency_data['Question'] == question]
            else:
                question_data = self.frequency_data
            
            result = {}
            for _, row in question_data.iterrows():
                key = f"{row['Question']} - {row['Variable']}"
                if row['Value'] not in result:
                    result[row['Value']] = 0
                result[row['Value']] += int(row['Frequency'])
            
            return result
        except Exception as e:
            st.error(f"Get frequency data error: {e}")
            return {}

def create_chart(data: pd.DataFrame, chart_type: str = 'bar', title: str = '') -> go.Figure:
    """Create standardized chart with consistent styling"""
    if data.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color="#7f8c8d")
        )
        fig.update_layout(
            title=title,
            title_font_size=20,
            title_x=0.5,
            title_xanchor='center',
            height=500,
            paper_bgcolor='white',
            plot_bgcolor='white',
            font_family="Arial"
        )
        return fig

    if chart_type == 'pie':
        # 使用标准化颜色
        colors = STANDARD_COLORS[:len(data)]
        
        fig = go.Figure(data=[go.Pie(
            labels=data.index if hasattr(data, 'index') else data.iloc[:, 0],
            values=data.values if len(data.shape) == 1 else data.iloc[:, -1],
            hole=.3,
            marker=dict(colors=colors, line=dict(color='#FFFFFF', width=2)),
            textinfo='label+percent',
            textposition='auto',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )])
        
        fig.update_layout(
            title=title,
            title_font_size=20,
            title_x=0.5,
            title_xanchor='center',
            height=500,
            paper_bgcolor='white',
            plot_bgcolor='white',
            font_family="Arial",
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.05
            )
        )
    
    elif chart_type == 'horizontal_bar':
        # 水平柱状图
        if len(data.shape) == 1:
            x_values = data.values
            y_values = data.index
        else:
            x_values = data.iloc[:, -1]
            y_values = data.iloc[:, 0] if data.shape[1] > 1 else data.index
        
        fig = go.Figure(data=[go.Bar(
            x=x_values,
            y=y_values,
            orientation='h',
            marker=dict(color=STANDARD_COLORS[0], line=dict(color='#FFFFFF', width=1)),
            hovertemplate='<b>%{y}</b><br>Count: %{x}<extra></extra>'
        )])
        
        fig.update_layout(
            title=title,
            title_font_size=20,
            title_x=0.5,
            title_xanchor='center',
            height=max(400, len(data) * 30),
            paper_bgcolor='white',
            plot_bgcolor='white',
            font_family="Arial",
            xaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
            yaxis=dict(showgrid=False)
        )
    
    else:  # 默认垂直柱状图
        if len(data.shape) == 1:
            x_values = data.index
            y_values = data.values
        else:
            x_values = data.iloc[:, 0] if data.shape[1] > 1 else data.index
            y_values = data.iloc[:, -1]
        
        fig = go.Figure(data=[go.Bar(
            x=x_values,
            y=y_values,
            marker=dict(color=STANDARD_COLORS[0], line=dict(color='#FFFFFF', width=1)),
            hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
        )])
        
        fig.update_layout(
            title=title,
            title_font_size=20,
            title_x=0.5,
            title_xanchor='center',
            height=500,
            paper_bgcolor='white',
            plot_bgcolor='white',
            font_family="Arial",
            xaxis=dict(showgrid=False, tickangle=-45),
            yaxis=dict(showgrid=True, gridcolor='#f0f0f0')
        )
    
    return fig

def create_layout():
    st.header("Youth employment 2024 outputs analysis")
    st.markdown("Analysis of Q6, Q7, Q10, Q11 survey responses with interactive visualization")

    # 添加区域过滤功能
    st.sidebar.header("Filters")
    
    # 检查是否有区域数据
    has_region_data = False
    selected_region = 'All'
    try:
        # 尝试加载区域数据
        region_files = [
            "orignaldata/q6_option_other.csv",
            "orignaldata/q7_option_other.csv", 
            "orignaldata/q10_option_other.csv",
            "orignaldata/q11_option_other.csv"
        ]
        
        regions_set = set()
        for file_path in region_files:
            try:
                if os.path.exists(file_path):
                    df = pd.read_csv(file_path, header=2)
                    if 'Department/Region' in df.columns:
                        regions_set.update(df['Department/Region'].dropna().unique())
                        has_region_data = True
            except:
                continue
        
        if has_region_data and regions_set:
            regions = ['All'] + sorted(list(regions_set))
            selected_region = st.sidebar.selectbox("Select Organizational Unit", regions)
        else:
            st.sidebar.info("Regional filtering not available - no region data found.")
    except:
        st.sidebar.info("Regional filtering not available - data files not found.")

    data_processor = Q6Q7Q10Q11DataProcessor()
    
    # 根据区域过滤数据处理器
    if has_region_data and selected_region != 'All':
        try:
            # 创建区域过滤的数据处理器
            filtered_processor = Q6Q7Q10Q11DataProcessor()
            
            # 获取选定区域的用户ID
            region_users = set()
            for file_path in region_files:
                try:
                    if os.path.exists(file_path):
                        df = pd.read_csv(file_path, header=2)
                        if 'Department/Region' in df.columns:
                            region_df = df[df['Department/Region'] == selected_region]
                            if 'UserId' in region_df.columns:
                                region_users.update(region_df['UserId'].dropna().unique())
                except:
                    continue
            
            if region_users:
                # 过滤数据处理器中的数据
                if not filtered_processor.cpo_glo_data.empty and 'UserId' in filtered_processor.cpo_glo_data.columns:
                    filtered_processor.cpo_glo_data = filtered_processor.cpo_glo_data[
                        filtered_processor.cpo_glo_data['UserId'].isin(region_users)
                    ]
                
                if not filtered_processor.works_count_data.empty and 'UserId' in filtered_processor.works_count_data.columns:
                    filtered_processor.works_count_data = filtered_processor.works_count_data[
                        filtered_processor.works_count_data['UserId'].isin(region_users)
                    ]
                
                if not filtered_processor.frequency_data.empty and 'UserId' in filtered_processor.frequency_data.columns:
                    filtered_processor.frequency_data = filtered_processor.frequency_data[
                        filtered_processor.frequency_data['UserId'].isin(region_users)
                    ]
                
                if not filtered_processor.works_list_data.empty and 'UserId' in filtered_processor.works_list_data.columns:
                    filtered_processor.works_list_data = filtered_processor.works_list_data[
                        filtered_processor.works_list_data['UserId'].isin(region_users)
                    ]
                
                data_processor = filtered_processor
                st.info(f"Showing data for: {selected_region} ({len(region_users)} users)")
            else:
                st.warning(f"No users found for region: {selected_region}")
        except Exception as e:
            st.warning(f"Region filtering encountered an issue: {str(e)}. Showing all data.")
    
    # Check if data is available
    if (data_processor.works_count_data.empty and 
        data_processor.frequency_data.empty and 
        data_processor.works_list_data.empty):
        st.warning("No data available to display. Please ensure the result files are in the correct location.")
        return

    # Display summary statistics
    summary_stats = data_processor.get_summary_stats()
    if summary_stats:
        st.subheader("📊 Summary Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(summary_stats["stat1"]["label"], summary_stats["stat1"]["value"])
        with col2:
            st.metric(summary_stats["stat2"]["label"], summary_stats["stat2"]["value"])
        with col3:
            st.metric(summary_stats["stat3"]["label"], summary_stats["stat3"]["value"])
        with col4:
            st.metric(summary_stats["stat4"]["label"], summary_stats["stat4"]["value"])

    # Works count statistics
    st.subheader("📈 Outputs Count Statistics")
    works_count_data = data_processor.get_works_count_data()
    
    if works_count_data:
        # Create works count chart
        questions = list(works_count_data.keys())
        total_works = [works_count_data[q]['total_works'] for q in questions]
        users_with_works = [works_count_data[q]['users_with_works'] for q in questions]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Total Works',
            x=questions,
            y=total_works,
            marker_color='#3498db'
        ))
        fig.add_trace(go.Bar(
            name='Users with Works',
            x=questions,
            y=users_with_works,
            marker_color='#e74c3c'
        ))
        
        fig.update_layout(
            title='Outputs Count by Question',
            title_font_size=20,
            title_x=0.5,
            title_xanchor='center',
            xaxis_title='Question',
            yaxis_title='Count',
            barmode='group',
            height=400,
            paper_bgcolor='white',
            plot_bgcolor='white',
            font_family="Arial"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Display data table
        st.subheader("📋 Detailed Statistics")
        df_display = pd.DataFrame([
            {
                'Question': q,
                'Total Works': data['total_works'],
                'Users with Works': data['users_with_works'],
                'Avg Works per User': f"{data['avg_works_per_user']:.2f}"
            }
            for q, data in works_count_data.items()
        ])
        st.dataframe(df_display, use_container_width=True)
    else:
        st.info("No works count data available.")

    # Frequency analysis
    st.subheader("📊 Frequency Analysis")
    frequency_data = data_processor.get_frequency_data()
    
    if frequency_data:
        # Show top 15 most frequent items
        sorted_freq = dict(sorted(frequency_data.items(), key=lambda x: x[1], reverse=True)[:15])
        
        if sorted_freq:
            # 添加图表类型选择
            col1, col2 = st.columns([3, 1])
            with col2:
                freq_chart_type = st.selectbox("Chart Type", ['horizontal_bar', 'bar', 'pie'], key='freq_type')
            
            # 转换数据格式为DataFrame
            freq_df = pd.DataFrame(list(sorted_freq.items()), columns=['Category', 'Count'])
            freq_df = freq_df.sort_values('Count', ascending=False)
            
            with col1:
                fig = create_chart(freq_df.set_index('Category')['Count'], freq_chart_type, 'Top Frequency Analysis Results')
                st.plotly_chart(fig, use_container_width=True)
            
            # Display frequency data table
            st.subheader("📋 Frequency Data")
            freq_df['Percentage'] = (freq_df['Count'] / freq_df['Count'].sum() * 100).round(1)
            st.dataframe(freq_df, use_container_width=True)
        else:
            st.info("No frequency data to display.")
    else:
        st.info("No frequency analysis data available.")

    # Works detail list
    if not data_processor.works_list_data.empty:
        st.subheader("📋 Outputs Detail List")
        
        # Filter and display works list
        works_df = data_processor.works_list_data.copy()
        
        # Show basic information about the works
        if not works_df.empty:
            st.write(f"Total outputs: {len(works_df)}")
            
            # Display sample of works (first 100 rows to avoid performance issues)
            display_df = works_df.head(100)
            
            # Select relevant columns for display
            display_columns = []
            for col in ['Question', 'Work Name', 'Department/Region', 'User ID']:
                if col in display_df.columns:
                    display_columns.append(col)
            
            if display_columns:
                st.dataframe(display_df[display_columns], use_container_width=True)
                
                if len(works_df) > 100:
                    st.info(f"Showing first 100 of {len(works_df)} total outputs.")
            else:
                st.dataframe(display_df, use_container_width=True)
        else:
            st.info("No works detail data available.")
    else:
        st.info("No works detail list available.")