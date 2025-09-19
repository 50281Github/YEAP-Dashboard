import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# 标准化颜色配置
STANDARD_COLORS = [
    '#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6',
    '#1abc9c', '#34495e', '#e67e22', '#95a5a6', '#f1c40f',
    '#8e44ad', '#16a085', '#2c3e50', '#d35400', '#7f8c8d'
]

def create_layout():
    st.title("Overview of 2024 outputs")

    # Load data
    try:
        data = pd.read_csv("result/q345_analysis_results.csv")
    except FileNotFoundError:
        st.error("The data file 'q345_analysis_results.csv' was not found in the 'result' directory.")
        return

    # 添加区域过滤功能
    st.sidebar.header("Filters")
    
    # 检查是否有区域数据
    has_region_data = False
    try:
        other_data = pd.read_csv("orignaldata/q345_option_other.csv", header=2)
        if 'Department/Region' in other_data.columns:
            regions = ['All'] + sorted(other_data['Department/Region'].dropna().unique().tolist())
            selected_region = st.sidebar.selectbox("Select Organizational Unit", regions)
            has_region_data = True
        else:
            st.sidebar.info("Regional filtering not available - no region data found.")
            selected_region = 'All'
    except:
        st.sidebar.info("Regional filtering not available - data file not found.")
        selected_region = 'All'

    def create_standardized_chart(data: pd.DataFrame, group: str, chart_type: str = 'pie') -> go.Figure:
        """Create standardized chart with consistent styling"""
        if data.empty:
            fig = go.Figure()
            fig.add_annotation(
                text=f"No data available for {group}",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=16, color="#7f8c8d")
            )
            fig.update_layout(
                title=f"{group} Response Distribution",
                title_font_size=20,
                title_x=0.5,
                title_xanchor='center',
                height=500,
                paper_bgcolor='white',
                plot_bgcolor='white'
            )
            return fig

        # Convert data format to dictionary
        if 'option' in data.columns and 'count' in data.columns:
            # Filter out zero counts
            filtered_data = data[data['count'] > 0]
            if filtered_data.empty:
                fig = go.Figure()
                fig.add_annotation(
                    text=f"No responses for {group}",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5,
                    showarrow=False,
                    font=dict(size=16, color="#7f8c8d")
                )
                fig.update_layout(
                    title=f"{group} Response Distribution",
                    title_font_size=20,
                    title_x=0.5,
                    title_xanchor='center',
                    height=500,
                    paper_bgcolor='white',
                    plot_bgcolor='white'
                )
                return fig
            data_dict = dict(zip(filtered_data['option'], filtered_data['count']))
        else:
            fig = go.Figure()
            fig.add_annotation(
                text=f"Invalid data structure for {group}",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=16, color="#7f8c8d")
            )
            fig.update_layout(
                title=f"{group} Response Distribution",
                title_font_size=20,
                title_x=0.5,
                title_xanchor='center',
                height=500,
                paper_bgcolor='white',
                plot_bgcolor='white'
            )
            return fig

        labels = list(data_dict.keys())
        values = list(data_dict.values())

        # 创建图表
        if chart_type == 'pie':
            # 使用标准化颜色
            colors = STANDARD_COLORS[:len(labels)]
            
            fig = go.Figure(data=[go.Pie(
                labels=labels, 
                values=values, 
                hole=.3,
                marker=dict(colors=colors, line=dict(color='#FFFFFF', width=2)),
                textinfo='label+percent',
                textposition='auto',
                hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
            )])
            
            fig.update_layout(
                title=f"{group} Response Distribution",
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
        else:  # bar chart
            df = pd.DataFrame({'Category': labels, 'Count': values})
            df = df.sort_values('Count', ascending=False)
            
            fig = px.bar(
                df, 
                x='Category', 
                y='Count', 
                title=f"{group} Response Distribution",
                color_discrete_sequence=STANDARD_COLORS
            )
            
            fig.update_layout(
                title_font_size=20,
                title_x=0.5,
                title_xanchor='center',
                height=500,
                paper_bgcolor='white',
                plot_bgcolor='white',
                font_family="Arial",
                xaxis_tickangle=-45
            )
        
        return fig

    # 根据区域过滤数据
    filtered_data = data.copy()
    if has_region_data and selected_region != 'All':
        try:
            # 获取选定区域的用户ID
            region_users = other_data[other_data['Department/Region'] == selected_region]['UserId'].unique()
            
            if len(region_users) > 0:
                # 过滤主数据，只显示选定区域的数据
                # 假设主数据中有UserId字段或者可以通过某种方式关联
                # 如果没有直接的UserId字段，我们需要重新生成分析结果
                st.info(f"Showing data for: {selected_region} ({len(region_users)} users)")
                
                # 重新分析选定区域的数据
                filtered_other_data = other_data[other_data['Department/Region'] == selected_region]
                
                # 重新计算Q3, Q4, Q5的统计数据
                q3_columns = [col for col in filtered_other_data.columns if 'Q3:' in col and col != 'Q3:Please indicate the cluster(s) of the implementation framework relevant to your work on youth employment. ']
                q4_columns = [col for col in filtered_other_data.columns if 'Q4:' in col and col != 'Q4:Please indicate the policy areas relevant to your work on youth employment. ']
                q5_columns = [col for col in filtered_other_data.columns if 'Q5:' in col and col != 'Q5:Please mark the youth groups targeted in your work on youth employment. ']
                
                # 创建过滤后的数据
                filtered_results = []
                
                # 处理Q3数据
                for col in q3_columns:
                    if col in filtered_other_data.columns:
                        col_data = filtered_other_data[col].dropna()
                        yes_count = (col_data == 'YES').sum()
                        if yes_count > 0:
                            # 提取选项名称
                            option_name = col.split('Q3:Please indicate the cluster(s) of the implementation framework relevant to your work on youth employment. ')[0].strip()
                            if not option_name:
                                # 从列名中提取选项
                                if 'Knowledge development' in col:
                                    option_name = 'Knowledge development and dissemination'
                                elif 'Technical assistance' in col:
                                    option_name = 'Technical assistance and capacity-building'
                                elif 'Advocacy' in col:
                                    option_name = 'Advocacy and partnerships'
                            filtered_results.append({'group': 'Q3', 'option': option_name, 'count': yes_count})
                
                # 处理Q4数据
                for col in q4_columns:
                    if col in filtered_other_data.columns:
                        col_data = filtered_other_data[col].dropna()
                        yes_count = (col_data == 'YES').sum()
                        if yes_count > 0:
                            option_name = col.split('Q4:Please indicate the policy areas relevant to your work on youth employment. ')[0].strip()
                            if not option_name:
                                if 'Employment and economic' in col:
                                    option_name = 'Employment and economic policies'
                                elif 'Employability' in col:
                                    option_name = 'Employability – Education, training and skills'
                                elif 'Labour market' in col:
                                    option_name = 'Labour market policies'
                                elif 'Youth entrepreneurship' in col:
                                    option_name = 'Youth entrepreneurship and self-employment'
                                elif 'Rights for young' in col:
                                    option_name = 'Rights for young people'
                            filtered_results.append({'group': 'Q4', 'option': option_name, 'count': yes_count})
                
                # 处理Q5数据
                for col in q5_columns:
                    if col in filtered_other_data.columns:
                        col_data = filtered_other_data[col].dropna()
                        yes_count = (col_data == 'YES').sum()
                        if yes_count > 0:
                            option_name = col.split('Q5:Please mark the youth groups targeted in your work on youth employment. ')[0].strip()
                            if not option_name:
                                if 'Young women' in col:
                                    option_name = 'Young women'
                                elif 'NEET' in col:
                                    option_name = 'Young people not in employment, education or training (NEET)'
                                elif 'migrant' in col:
                                    option_name = 'Young migrant workers'
                                elif 'refugees' in col:
                                    option_name = 'Young refugees'
                                elif 'disabilities' in col:
                                    option_name = 'Young people with disabilities'
                                elif 'rural' in col:
                                    option_name = 'Young rural workers'
                                elif 'indigenous' in col:
                                    option_name = 'Young indigenous people'
                            filtered_results.append({'group': 'Q5', 'option': option_name, 'count': yes_count})
                
                if filtered_results:
                    filtered_data = pd.DataFrame(filtered_results)
                else:
                    st.warning(f"No data found for region: {selected_region}")
                    filtered_data = pd.DataFrame(columns=['group', 'option', 'count'])
            else:
                st.warning(f"No users found for region: {selected_region}")
                filtered_data = pd.DataFrame(columns=['group', 'option', 'count'])
        except Exception as e:
            st.warning(f"Region filtering encountered an issue: {str(e)}. Showing all data.")
            filtered_data = data.copy()

    # Q3 Chart
    st.header("Distribution Of Outputs Across The Clusters Of The Implementation Framework")
    q3_data = filtered_data[filtered_data['group'] == 'Q3']
    
    # 添加图表类型选择
    col1, col2 = st.columns([3, 1])
    with col2:
        q3_chart_type = st.selectbox("Chart Type", ['pie', 'bar'], key='q3_type')
    
    with col1:
        st.plotly_chart(create_standardized_chart(q3_data, 'Q3', q3_chart_type), use_container_width=True)

    # Q4 Chart
    st.header("Distribution Of Outputs Across The Pillars Of The Call For Action On Youth Employment")
    q4_data = filtered_data[filtered_data['group'] == 'Q4']
    
    col1, col2 = st.columns([3, 1])
    with col2:
        q4_chart_type = st.selectbox("Chart Type", ['pie', 'bar'], key='q4_type')
    
    with col1:
        st.plotly_chart(create_standardized_chart(q4_data, 'Q4', q4_chart_type), use_container_width=True)

    # Q5 Chart
    st.header("Distribution Of Outputs Across Target Youth Groups, When Applicable")
    q5_data = filtered_data[filtered_data['group'] == 'Q5']
    
    col1, col2 = st.columns([3, 1])
    with col2:
        q5_chart_type = st.selectbox("Chart Type", ['pie', 'bar'], key='q5_type')
    
    with col1:
        st.plotly_chart(create_standardized_chart(q5_data, 'Q5', q5_chart_type), use_container_width=True)