import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
import base64

# Import unified style  module
try:
    from st_styles import style_manager, create_chart, apply_page_style, create_metrics, create_table
    STYLES_AVAILABLE = True
except ImportError:
    STYLES_AVAILABLE = False
    # Standardized color configuration
    STANDARD_COLORS = [
        '#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6',
        '#1abc9c', '#34495e', '#e67e22', '#95a5a6', '#f1c40f',
        '#8e44ad', '#16a085', '#2c3e50', '#d35400', '#7f8c8d'
    ]

def safe_read_csv(file_path):
    """
    Safely read CSV file with automatic encoding detection
    """
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            return pd.read_csv(file_path, encoding=encoding)
        except UnicodeDecodeError:
            continue
    
    # If all encodings fail, try without specifying encoding
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        st.error(f"Failed to read {file_path}: {str(e)}")
        return pd.DataFrame()

def get_base64_image(image_path):
    """Convert image to base64 string for embedding in HTML"""
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

def create_unified_header():
    """Create unified header with logo and title for all pages"""
    # Resolve logo path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    logo_path = os.path.join(project_root, 'orignaldata', 'logo.png')

    # Determine year-aware title
    selected_year = st.session_state.get('selected_year', None)
    year_text = None
    if selected_year and str(selected_year).lower() != 'all':
        year_text = str(selected_year)
    title = f"{year_text} YEAP Survey Analysis" if year_text else "YEAP Survey Analysis"

    # Create a unified blue background container for both logo and title
    st.markdown(f"""
    <div style="
        background-color: rgb(33, 45, 183);
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 15px;
        height: 120px;
    ">
        <div style="flex: 1; max-width: 180px; display: flex; align-items: center; justify-content: center;">
              <img src="data:image/png;base64,{get_base64_image(logo_path)}" 
                   style="width: 100%; height: auto; display: block;">
          </div>
        <div style="
            flex: 3;
            color: white;
            text-align: center;
            font-size: 2.2rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            justify-content: center;
        ">
            {title}
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_layout():
    # Add unified header first
    create_unified_header()
    
    # Apply page styling
    if STYLES_AVAILABLE:
        apply_page_style()
    else:
        st.set_page_config(
            page_title="Q3-Q4-Q5 Analysis",
            page_icon="📊",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    st.title("📊 Specialized Analysis")
    st.markdown("**In-depth analysis focused on implementation frameworks, policy areas, and target groups**")
    st.markdown("---")

    # Add region filtering functionality
    
    # Read original data files directly
    try:
        # Get absolute path of project root directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        
        # Read Q3 data
        q3_data = safe_read_csv(os.path.join(project_root, 'orignaldata', 'PART2_base_dataQ3.csv'))
        # Read Q4 data  
        q4_data = safe_read_csv(os.path.join(project_root, 'orignaldata', 'PART2_base_dataQ4.csv'))
        # Read Q5 data
        q5_data = safe_read_csv(os.path.join(project_root, 'orignaldata', 'PART2_base_dataQ5.csv'))
        
        # Apply global YEAR filter if available
        try:
            selected_year = st.session_state.get('selected_year', 'All')
            if selected_year != 'All':
                # Filter Q3 data
                if 'YEAR' in q3_data.columns:
                    q3_data = q3_data[q3_data['YEAR'].astype(str).str.strip() == str(selected_year)]
                elif 'year' in q3_data.columns:
                    q3_data = q3_data[q3_data['year'].astype(str).str.strip() == str(selected_year)]
                
                # Filter Q4 data
                if 'YEAR' in q4_data.columns:
                    q4_data = q4_data[q4_data['YEAR'].astype(str).str.strip() == str(selected_year)]
                elif 'year' in q4_data.columns:
                    q4_data = q4_data[q4_data['year'].astype(str).str.strip() == str(selected_year)]
                
                # Filter Q5 data
                if 'YEAR' in q5_data.columns:
                    q5_data = q5_data[q5_data['YEAR'].astype(str).str.strip() == str(selected_year)]
                elif 'year' in q5_data.columns:
                    q5_data = q5_data[q5_data['year'].astype(str).str.strip() == str(selected_year)]
        except Exception:
            pass
        
        # Check if region data exists
        has_region_data = False
        if 'selected_region' in st.session_state and 'regions_options' in st.session_state:
            # Use globally shared selection
            regions = st.session_state['regions_options']
            selected_region = st.session_state['selected_region']
            has_region_data = True
        elif 'Department/Region' in q3_data.columns:
            regions = ['All'] + sorted(q3_data['Department/Region'].dropna().unique().tolist())
            selected_region = st.sidebar.selectbox("Select Organizational Unit", regions)
            has_region_data = True
        else:
            st.sidebar.info("Regional filtering not available - no region data found.")
            selected_region = 'All'
            
    except FileNotFoundError as e:
        st.error(f"Data files not found: {str(e)}")
        return

    def create_standardized_chart(data_dict: dict, group: str, chart_type: str = 'pie') -> go.Figure:
        """Create standardized chart with consistent styling"""
        if not data_dict or all(v == 0 for v in data_dict.values()):
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

        # Set corresponding title based on group
        title_mapping = {
            'Q3': 'Distribution Of Outputs Across The Clusters Of The Implementation Framework',
            'Q4': 'Distribution Of Outputs Across The Pillars Of The Call For Action On Youth Employment',
            'Q5': 'Distribution Of Outputs Across Target Youth Groups, When Applicable'
        }
        chart_title = title_mapping.get(group, f"{group} Response Distribution")

        # Use unified styling to create chart
        if STYLES_AVAILABLE:
            return create_chart(data_dict, chart_type, chart_title)
        else:
            # Backup chart creation logic
            colors = STANDARD_COLORS
            categories = list(data_dict.keys())
            values = list(data_dict.values())
            
            fig = go.Figure()
            
            if chart_type == 'pie':
                fig.add_trace(go.Pie(
                    labels=categories,
                    values=values,
                    marker_colors=colors[:len(categories)],
                    hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
                ))
            else:  # bar chart
                fig.add_trace(go.Bar(
                    x=categories,
                    y=values,
                    marker_color=colors[0],
                    hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
                ))
                fig.update_layout(
                    xaxis_title='Category',
                    yaxis_title='Count'
                )
            
            fig.update_layout(
                title=chart_title,
                title_font_size=20,
                title_x=0.5,
                title_xanchor='center',
                height=500,
                paper_bgcolor='white',
                plot_bgcolor='white',
                font_family="Arial"
            )
            
            return fig

    # Data processing and analysis functions
    def process_question_data(data, question_columns, group_name):
        """Process question data and return statistical results"""
        results = {}
        for col in question_columns:
            if col in data.columns:
                yes_count = (data[col] == 'YES').sum()
                if yes_count > 0:
                    # Clean column name, remove trailing spaces and periods
                    clean_name = col.strip().rstrip('.')
                    results[clean_name] = yes_count
        return results

    # Define question column mapping
    q3_columns = [
        'Knowledge development and dissemination. ',
        'Technical assistance and capacity-building of constituents. ',
        'Advocacy and partnerships. '
    ]
    
    q4_columns = [
        'Employment and economic policies for youth employment. ',
        'Employability – Education, training and skills, and the school-to-work transition. ',
        'Labour market policies. ',
        'Youth entrepreneurship and self-employment. ',
        'Rights for young people. '
    ]
    
    q5_columns = [
        'Young women',
        'Young people not in employment, education or training (NEET) ',
        'Young migrant workers ',
        'Young refugees ',
        'Young people - sexual orientation and gender identity ',
        'Young people with disabilities ',
        'Young rural workers  ',
        'Young indigenous people '
    ]

    # Filter data based on region
    if has_region_data and selected_region != 'All':
        st.info(f"Showing data for: {selected_region}")
        
        # Filter data
        filtered_q3 = q3_data[q3_data['Department/Region'] == selected_region]
        filtered_q4 = q4_data[q4_data['Department/Region'] == selected_region]
        filtered_q5 = q5_data[q5_data['Department/Region'] == selected_region]
        
        # Process data
        q3_results = process_question_data(filtered_q3, q3_columns, 'Q3')
        q4_results = process_question_data(filtered_q4, q4_columns, 'Q4')
        q5_results = process_question_data(filtered_q5, q5_columns, 'Q5')
    else:
        # Process all data
        q3_results = process_question_data(q3_data, q3_columns, 'Q3')
        q4_results = process_question_data(q4_data, q4_columns, 'Q4')
        q5_results = process_question_data(q5_data, q5_columns, 'Q5')

    # Q3 Chart
    # Automatically select chart type: bar chart for 5+ items, pie chart for less than 5
    q3_chart_type = 'bar' if len(q3_results) >= 5 else 'pie'
    st.plotly_chart(create_standardized_chart(q3_results, 'Q3', q3_chart_type), use_container_width=True)

    # Q4 Chart
    # Automatically select chart type: bar chart for 5+ items, pie chart for less than 5
    q4_chart_type = 'bar' if len(q4_results) >= 5 else 'pie'
    st.plotly_chart(create_standardized_chart(q4_results, 'Q4', q4_chart_type), use_container_width=True)

    # Q5 Chart
    # Automatically select chart type: bar chart for 5+ items, pie chart for less than 5
    q5_chart_type = 'bar' if len(q5_results) >= 5 else 'pie'
    st.plotly_chart(create_standardized_chart(q5_results, 'Q5', q5_chart_type), use_container_width=True)

if __name__ == "__main__":
    create_layout()