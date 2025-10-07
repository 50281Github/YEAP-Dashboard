import streamlit as st
import pandas as pd
import os
import re
import sys
import base64
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any

# Try to import unified style module
try:
    from st_styles import style_manager, create_chart, apply_page_style, create_table
    STYLES_AVAILABLE = True
except ImportError:
    STYLES_AVAILABLE = False
    # Backup color  configuration
    STANDARD_COLORS = [
        '#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6',
        '#1abc9c', '#34495e', '#e67e22', '#95a5a6', '#f1c40f',
        '#8e44ad', '#16a085', '#2c3e50', '#d35400', '#7f8c8d'
    ]

def safe_read_csv(file_path, **kwargs):
    """
    Safely read CSV file with automatic encoding detection
    """
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            return pd.read_csv(file_path, encoding=encoding, **kwargs)
        except UnicodeDecodeError:
            continue
    
    # If all encodings fail, try without specifying encoding
    try:
        return pd.read_csv(file_path, **kwargs)
    except Exception as e:
        st.error(f"Failed to read {file_path}: {str(e)}")
        return pd.DataFrame()

# Import original modules from local streamlit directory
try:
    from data_handler import DataHandler
    from visualizer import visualizer
    ORIGINAL_MODULES_AVAILABLE = True
except ImportError:
    ORIGINAL_MODULES_AVAILABLE = False
    # If unable to import original modules, create simplified versions
    class DataHandler:
        def import_data_from_external(self, file_path, file_type):
            try:
                if file_type == 'csv':
                    df = safe_read_csv(file_path)
                    # Simplified data processing logic
                    questions_data = {}
                    for _, row in df.iterrows():
                        question = row.get('Question', '')
                        option = row.get('Option', '')
                        count = row.get('Count', 0)
                        if question not in questions_data:
                            questions_data[question] = {}
                        questions_data[question][option] = count
                    return questions_data
                return {}
            except Exception:
                return {}
    
    class StyleManager:
        def get_theme_colors(self):
            return {
                'primary': '#3498DB',
                'secondary': '#F39C12',
                'success': '#2ECC71',
                'danger': '#E74C3C',
                'warning': '#F1C40F',
                'info': '#17A2B8',
                'light': '#F8F9FA',
                'dark': '#343A40',
                'background': '#FFFFFF',
                'text': '#2C3E50',
                'border': '#DEE2E6'
            }
        
        def get_chart_colors(self):
            return STANDARD_COLORS
    
    # If unable to import original visualizer, create simplified version
    class Visualizer:
        def create_chart(self, data, chart_type, title):
            fig = go.Figure()
            if data and isinstance(data, dict):
                categories = list(data.keys())
                values = list(data.values())
                
                if chart_type == 'pie':
                    fig.add_trace(go.Pie(
                        labels=categories,
                        values=values,
                        marker_colors=STANDARD_COLORS[:len(categories)]
                    ))
                else:
                    fig.add_trace(go.Bar(
                        x=categories,
                        y=values,
                        marker_color=STANDARD_COLORS[0]
                    ))
                
                fig.update_layout(
                    title=title,
                    title_font_size=20,
                    title_x=0.5,
                    title_xanchor='center',
                    height=500,
                    paper_bgcolor='white',
                    plot_bgcolor='white'
                )
            
            return fig
        
        def auto_select_chart_type(self, data):
            """Automatically select appropriate chart type"""
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
    
    visualizer = Visualizer()

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

class GeneralDataProcessor:
    def __init__(self, csv_file_path=None):
        # Get absolute path of project root directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        
        if csv_file_path is None:
            csv_file_path = os.path.join(project_root, 'orignaldata', 'PART1_base_dataQ2-5.csv')
        
        self.csv_file_path = csv_file_path
        self.questions_data = {}
        self.unique_users_count = 0
        self.load_data()
        self._load_user_data()

    def load_data(self):
        """Load survey data using DataHandler (same as original Dash version)"""
        try:
            # Read new format CSV file directly
            df = safe_read_csv(self.csv_file_path)
            
            # Apply global YEAR filter if available
            try:
                selected_year = st.session_state.get('selected_year', 'All')
                if selected_year != 'All':
                    # Check for both 'YEAR' and 'year' columns
                    if 'YEAR' in df.columns:
                        df = df[df['YEAR'].astype(str).str.strip() == str(selected_year)]
                    elif 'year' in df.columns:
                        df = df[df['year'].astype(str).str.strip() == str(selected_year)]
            except Exception:
                pass
            
            # Check if necessary columns exist
            if 'question' not in df.columns or 'option' not in df.columns or 'count' not in df.columns:
                st.error("CSV file must contain 'question', 'option', and 'count' columns")
                self.questions_data = {}
                self.analysis_results = None
                return
            
            # Convert data format to expected dictionary structure
            self.questions_data = {}
            for _, row in df.iterrows():
                question = str(row['question']).strip()
                option = str(row['option']).strip()
                count = int(row['count']) if pd.notna(row['count']) else 0
                
                if question not in self.questions_data:
                    self.questions_data[question] = {}
                self.questions_data[question][option] = count
            
            if self.questions_data:
                st.success(f"Successfully loaded {len(self.questions_data)} questions")
                print(f"General Survey Data loaded: {len(self.questions_data)} questions")
                
                self._merge_other_options()
            else:
                st.error("No valid data found in the file")
                print("General Survey Data loading failed: No data")
                self.questions_data = {}
                
        except Exception as e:
            st.error(f"Error loading data: {e}")
            print(f"General Survey Data loading failed: {e}")
            self.questions_data = {}

    def _process_analysis_results(self):
        """This method is no longer needed as we don't display summary statistics"""
        pass

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
            # Get absolute path of project root directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)
            
            unique_users = set()
            q8q9_path = os.path.join(project_root, 'orignaldata', 'Q8Q9_basic_data.csv')
            if os.path.exists(q8q9_path):
                q8q9_df = safe_read_csv(q8q9_path, skiprows=2)
                if len(q8q9_df.columns) > 0:
                    user_ids = q8q9_df.iloc[:, 0].dropna().unique()
                    unique_users.update(user_ids)
            
            q6q7q10q11_path = os.path.join(project_root, 'orignaldata', 'Q6Q7Q10Q11_basic_data.csv')
            if os.path.exists(q6q7q10q11_path):
                q6q7q10q11_df = safe_read_csv(q6q7q10q11_path)
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

def process_title_for_display(title):
    """Process title for better display - add line breaks for long titles"""
    if not title:
        return title
    
    # For Q2 and Q3 questions, apply smart line breaking
    if 'Q2:' in title or 'Q3:' in title:
        # Split at the colon first
        if ':' in title:
            parts = title.split(':', 1)
            question_part = parts[0] + ':'
            content_part = parts[1].strip()
            
            # Check if the combined length is reasonable for one line
            combined_length = len(question_part) + len(content_part) + 1
            
            # If total length is reasonable (< 80 characters), keep on one line
            if combined_length <= 80:
                return title
            
            # If too long, break intelligently at natural points
            # Try to find a good breaking point in the content
            words = content_part.split(' ')
            if len(words) > 1:
                # Find a good midpoint for breaking
                mid_point = len(words) // 2
                first_part = ' '.join(words[:mid_point])
                second_part = ' '.join(words[mid_point:])
                
                # Keep question part with first part of content
                return question_part + ' ' + first_part + '<br>' + second_part
            else:
                # If content is just one long word, break after question part
                return question_part + '<br>' + content_part
    
    # For other titles, apply general line breaking if needed
    max_length = 50  # Maximum length per line for other titles
    
    # If title is short enough, return as is
    if len(title) <= max_length:
        return title
    
    # For other long titles, apply general line breaking
    words = title.split(' ')
    lines = []
    current_line = ""
    
    for word in words:
        if len(current_line) + len(word) + 1 <= max_length:
            current_line += (" " if current_line else "") + word
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    
    if current_line:
        lines.append(current_line)
    
    return "<br>".join(lines)

def create_chart_unified(data, chart_type, title):
    """Create chart using unified styling system"""
    try:
        # Validate input data
        if not data or not isinstance(data, dict):
            raise ValueError("Invalid data: expected non-empty dictionary")
        
        # Clean and validate data
        clean_data = {}
        for key, value in data.items():
            if key is not None and value is not None:
                clean_key = str(key) if key else "Unknown"
                try:
                    clean_value = float(value) if isinstance(value, (int, float)) else 0
                    if clean_value >= 0:  # Only include non-negative values
                        clean_data[clean_key] = clean_value
                except (ValueError, TypeError):
                    continue  # Skip invalid values
        
        if not clean_data:
            raise ValueError("No valid data points found")
        
        # Process title for better display - add line breaks for long titles
        processed_title = process_title_for_display(title)
        
        # Use unified styling to create chart
        if STYLES_AVAILABLE:
            return create_chart(clean_data, chart_type, processed_title)
        else:
            # Backup chart creation logic
            fig = go.Figure()
            colors = STANDARD_COLORS
            categories = list(clean_data.keys())
            values = list(clean_data.values())
            
            if chart_type == 'pie':
                fig.add_trace(go.Pie(
                    labels=categories,
                    values=values,
                    marker_colors=colors[:len(categories)],
                    hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
                ))
            elif chart_type == 'horizontal_bar':
                fig.add_trace(go.Bar(
                    x=values,
                    y=categories,
                    orientation='h',
                    marker_color=colors[0],
                    hovertemplate='<b>%{y}</b><br>Count: %{x}<extra></extra>'
                ))
                fig.update_layout(
                    xaxis_title='Count',
                    yaxis_title='Category'
                )
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
                title=processed_title,
                title_font_size=20,
                title_x=0.5,
                title_xanchor='center',
                height=500,
                paper_bgcolor='white',
                plot_bgcolor='white',
                font_family="Arial"
            )
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating chart: {str(e)}")
        # Create error chart
        fig = go.Figure()
        fig.add_annotation(
            text=f"Chart Error: {str(e)}<br>Please try selecting a different question or chart type.",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=14, color="#e74c3c"),
            align="center"
        )
        fig.update_layout(
            title=title or "Chart Error",
            title_font_size=20,
            title_x=0.5,
            title_xanchor='center',
            height=400,
            paper_bgcolor='white',
            plot_bgcolor='white',
            showlegend=False
        )
        return fig

def create_layout():
    """Create the main layout using unified styling system"""
    # Add unified header first
    create_unified_header()
    
    # Use unified styling system
    if STYLES_AVAILABLE:
        apply_page_style()
        # When using unified styling system, no additional CSS needed
        custom_css = ""
    else:
        # Backup page styling
        st.set_page_config(
            page_title="General Survey Dashboard",
            page_icon="📊",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Apply original styles using theme colors
        if ORIGINAL_MODULES_AVAILABLE:
            # Use local visualizer's style manager
            theme_colors = visualizer.style_manager.get_theme_colors()
            chart_colors = visualizer.style_manager.get_chart_colors()
        else:
            # Use backup styling
            style_manager = StyleManager()
            theme_colors = style_manager.get_theme_colors()
            chart_colors = style_manager.get_chart_colors()
        
        # Create custom CSS based on original styles
        custom_css = f"""
        <style>
        /* Use original color scheme */
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
        
        /* Main container styling */
        .main .block-container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        
        /* Metrics container styling */
        .metrics-container {{
            background-color: var(--light-color);
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            border: 1px solid var(--border-color);
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        /* Data table styling */
        .data-table {{
            background-color: var(--background-color);
            border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    
    /* Select box styling */
    .stSelectbox > div > div {{
        background-color: var(--background-color);
        border: 1px solid var(--border-color);
        border-radius: 4px;
    }}
    
    /* Select box main container - prevent truncation */
    .stSelectbox {{
        width: 100% !important;
    }}
    
    /* Select box dropdown options - enable text wrapping and auto height */
    .stSelectbox [data-baseweb="select"] {{
        width: 100% !important;
        min-width: 300px !important;
        max-width: 100% !important;
    }}
    
    /* Main select container - allow multi-line text */
    .stSelectbox [data-baseweb="select"] > div {{
        white-space: normal !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        min-height: 40px !important;
        height: auto !important;
        line-height: 1.4 !important;
        padding: 8px 12px !important;
        overflow: visible !important;
        text-overflow: unset !important;
        display: flex !important;
        align-items: flex-start !important;
    }}
    
    /* Select box dropdown menu container */
    .stSelectbox [data-baseweb="popover"] {{
        max-width: none !important;
        width: auto !important;
        min-width: 400px !important;
        max-width: 90vw !important;
    }}
    
    /* Select box dropdown options in the menu */
    .stSelectbox [data-baseweb="menu"] {{
        max-width: none !important;
        width: auto !important;
        min-width: 400px !important;
        max-width: 90vw !important;
    }}
    
    /* Individual dropdown options - enhanced text wrapping */
    .stSelectbox [data-baseweb="menu"] [role="option"] {{
        white-space: normal !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        min-height: 40px !important;
        height: auto !important;
        line-height: 1.4 !important;
        padding: 12px 16px !important;
        max-width: none !important;
        overflow: visible !important;
        text-overflow: unset !important;
        display: flex !important;
        align-items: flex-start !important;
        word-break: break-word !important;
    }}
    
    /* Selected option display - enhanced for long text */
    .stSelectbox [data-baseweb="select"] [data-baseweb="base-input"] {{
        white-space: normal !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        min-height: 40px !important;
        height: auto !important;
        line-height: 1.4 !important;
        overflow: visible !important;
        text-overflow: unset !important;
        display: flex !important;
        align-items: flex-start !important;
        word-break: break-word !important;
    }}
    
    /* Input container - allow text wrapping */
    .stSelectbox [data-baseweb="select"] [data-baseweb="input"] {{
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: unset !important;
        min-height: 40px !important;
        height: auto !important;
        display: flex !important;
        align-items: flex-start !important;
        word-break: break-word !important;
    }}
    
    /* Value container - enhanced for multi-line display */
    .stSelectbox [data-baseweb="select"] [data-baseweb="input"] > div {{
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: unset !important;
        flex-wrap: wrap !important;
        min-height: 24px !important;
        height: auto !important;
        line-height: 1.4 !important;
        word-break: break-word !important;
        display: flex !important;
        align-items: flex-start !important;
    }}
    
    /* Additional styling for better text display */
    .stSelectbox [data-baseweb="select"] [data-baseweb="input"] [data-baseweb="input-container"] {{
        min-height: 40px !important;
        height: auto !important;
        display: flex !important;
        align-items: flex-start !important;
    }}
    
    /* Ensure dropdown arrow doesn't interfere with text */
    .stSelectbox [data-baseweb="select"] [data-baseweb="select-arrow"] {{
        align-self: flex-start !important;
        margin-top: 8px !important;
    }}
    
    /* Title styling */
    .main-title {{
        color: var(--primary-color);
        text-align: center;
        margin-bottom: 30px;
    }}
    
    /* Chart container styling */
    .js-plotly-plot {{
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }}
    
    /* Metric card styling */
    [data-testid="metric-container"] {{
        background-color: var(--background-color);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }}
    
    /* Separator line styling */
    hr {{
        border: none;
        height: 2px;
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        margin: 20px 0;
    }}
    </style>
    """
    
    # Only apply custom CSS when needed
    if custom_css:
        st.markdown(custom_css, unsafe_allow_html=True)
    
    st.title("📊 General Survey Analysis")
    st.markdown("**Supports visual analysis of all questions with multiple chart types and interactive features**")
    st.markdown("---")
    
    # Initialize data processor
    data_processor = GeneralDataProcessor()
    questions_data = data_processor.questions_data
    
    if not questions_data:
        st.error("❌ No data available. Please check the data files.")
        return
    
    # Filter questions to only show Q1-Q5 (matching original dashboard)
    sorted_questions = sorted(questions_data.keys(), key=lambda x: data_processor._extract_question_number(x))
    filtered_questions = [q for q in sorted_questions if data_processor._extract_question_number(q) <= 5]

    if not filtered_questions:
        st.warning("No questions available for analysis.")
        return

    # Question selection and chart controls
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
        
        chart_type = st.selectbox(
            "Chart Type:",
            chart_options,
            index=default_index,
            key="chart_type_selector",
            help=f"Auto-selected: {default_chart} (based on {len(question_data) if question_data else 0} options)"
        )
    else:
        chart_type = st.selectbox(
            "Chart Type:",
            ["Bar Chart", "Pie Chart", "Horizontal Bar"],
            key="chart_type_selector"
        )
    
    if selected_question and selected_question in questions_data:
        question_data = questions_data[selected_question]
        
        # Apply filtering for Q4 and Q5 questions (matching original dashboard logic)
        # Q2 questions (YES/NO) should not be filtered by percentage threshold
        if ('Q4:' in selected_question or 'Q5:' in selected_question) and isinstance(question_data, dict):
            total_count = sum(question_data.values()) if question_data else 0
            if total_count > 0:
                # Only remove "other" options, but keep all percentage levels
                filtered_data = {k: v for k, v in question_data.items() 
                               if 'other' not in k.lower()}
            else:
                filtered_data = question_data
        elif 'Q2:' in selected_question and isinstance(question_data, dict):
            # Q2 questions are YES/NO questions - do not apply percentage filtering
            # Keep all options regardless of percentage
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
            
        fig = create_chart_unified(filtered_data, chart_type_key, selected_question)
        
        # Display chart
        st.plotly_chart(fig, use_container_width=True)
        
        # Display data table with unified styling
        if filtered_data and isinstance(filtered_data, dict):
            try:
                # Validate data before creating DataFrame
                valid_items = []
                for key, value in filtered_data.items():
                    if key is not None and value is not None:
                        # Ensure key is string and value is numeric
                        clean_key = str(key) if key else "Unknown"
                        clean_value = float(value) if isinstance(value, (int, float)) else 0
                        valid_items.append((clean_key, clean_value))
                
                if valid_items:
                    df = pd.DataFrame(valid_items, columns=['Option', 'Count'])
                    df = df.sort_values('Count', ascending=False)
                    
                    # Calculate percentage safely
                    total_count = df['Count'].sum()
                    if total_count > 0:
                        df['Percentage'] = (df['Count'] / total_count * 100).round(1)
                        df['Percentage'] = df['Percentage'].astype(str) + '%'
                    else:
                        df['Percentage'] = '0%'
                    
                    # Use unified styling to create table
                    if STYLES_AVAILABLE:
                        create_table(df)
                    else:
                        # Backup table styling
                        st.markdown('<div class="data-table">', unsafe_allow_html=True)
                        st.dataframe(df, use_container_width=True, hide_index=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.info("No valid response data available for this question.")
            except Exception as e:
                st.error(f"Error displaying data table: {str(e)}")
                st.info("Data processing error occurred. Please try selecting a different question.")
        else:
            st.info("No response data available for this question.")
        
    else:
        st.info("Please select a question to view the analysis.")