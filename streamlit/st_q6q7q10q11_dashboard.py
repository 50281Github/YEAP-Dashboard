import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys
import base64
from typing import Dict, Any, List

# Import unified style   module
try:
    from st_styles import style_manager, create_chart, apply_page_style, create_metrics, create_table, create_standardized_chart
    STYLES_AVAILABLE = True
except ImportError:
    STYLES_AVAILABLE = False
    # Define backup colors
    STANDARD_COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

def safe_read_csv(file_path: str, **kwargs) -> pd.DataFrame:
    """Safely read CSV file with multiple encoding attempts"""
    encodings_to_try = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    
    for encoding in encodings_to_try:
        try:
            return pd.read_csv(file_path, encoding=encoding, **kwargs)
        except UnicodeDecodeError:
            continue
    
    # If all encodings fail, try without specifying encoding
    return pd.read_csv(file_path, **kwargs)

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

class Q6Q7Q10Q11DataProcessor:
    """Q6Q7Q10Q11 Data Processor - responsible for loading and preprocessing original data"""
    
    def __init__(self, base_path: str = None):
        """Initialize data processor"""
        self.base_path = base_path or "."
        self.q6_data = None
        self.q7_data = None
        self.q10_data = None
        self.q11_data = None
        self.combined_data = None
        self._load_all_data()
    
    def _load_all_data(self):
        """Load all original data files"""
        try:
            # Get absolute path of project root directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)
            
            # Original data file paths
            data_files = {
                'q6': os.path.join(project_root, 'orignaldata', 'PART3_base_dataQ6.csv'),
                'q7': os.path.join(project_root, 'orignaldata', 'PART3_base_dataQ7.csv'),
                'q10': os.path.join(project_root, 'orignaldata', 'PART3_base_dataQ10.csv'),
                'q11': os.path.join(project_root, 'orignaldata', 'PART3_base_dataQ11.csv')
            }
            
            # Load Q6 data
            self.q6_data = self._load_data_file(data_files['q6'])
            if not self.q6_data.empty:
                self.q6_data['Question'] = 'Q6'
            
            # Load Q7 data
            self.q7_data = self._load_data_file(data_files['q7'])
            if not self.q7_data.empty:
                self.q7_data['Question'] = 'Q7'
            
            # Load Q10 data
            self.q10_data = self._load_data_file(data_files['q10'])
            if not self.q10_data.empty:
                self.q10_data['Question'] = 'Q10'
            
            # Load Q11 data
            self.q11_data = self._load_data_file(data_files['q11'])
            if not self.q11_data.empty:
                self.q11_data['Question'] = 'Q11'
            
            # Combine all data for unified processing
            self._combine_data()
            
        except Exception as e:
            st.error(f"Data loading error: {e}")
            # Create empty DataFrames as backup
            self._initialize_empty_dataframes()
    
    def _combine_data(self):
        """Combine all question data into a single DataFrame"""
        dataframes = []
        
        for df in [self.q6_data, self.q7_data, self.q10_data, self.q11_data]:
            if df is not None and not df.empty:
                # More lenient filtering: keep rows with UserId and year
                # This ensures we don't lose records that might have partial data
                basic_filter = (
                    df['UserId'].notna() & 
                    (df['UserId'].astype(str).str.strip() != '') &
                    (df['UserId'].astype(str).str.strip() != 'nan')
                )
                
                # Also keep rows that have year information
                if 'year' in df.columns:
                    year_filter = (
                        df['year'].notna() & 
                        (df['year'].astype(str).str.strip() != '') &
                        (df['year'].astype(str).str.strip() != 'nan')
                    )
                    basic_filter = basic_filter & year_filter
                elif 'YEAR' in df.columns:
                    year_filter = (
                        df['YEAR'].notna() & 
                        (df['YEAR'].astype(str).str.strip() != '') &
                        (df['YEAR'].astype(str).str.strip() != 'nan')
                    )
                    basic_filter = basic_filter & year_filter
                
                df_filtered = df[basic_filter].copy()
                if not df_filtered.empty:
                    dataframes.append(df_filtered)
        
        if dataframes:
            self.combined_data = pd.concat(dataframes, ignore_index=True, sort=False)
        else:
            self.combined_data = pd.DataFrame()
    
    def _load_data_file(self, file_path: str) -> pd.DataFrame:
        """Load data file with year filtering"""
        try:
            full_path = os.path.join(self.base_path, file_path)
            if os.path.exists(full_path):
                df = safe_read_csv(full_path)
                
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
                
                return df
            else:
                st.warning(f"File not found: {full_path}")
                return pd.DataFrame()
        except Exception as e:
            st.error(f"Error loading file {file_path}: {e}")
            return pd.DataFrame()
    
    def _initialize_empty_dataframes(self):
        """Initialize empty DataFrames as backup"""
        self.q6_data = pd.DataFrame()
        self.q7_data = pd.DataFrame()
        self.q10_data = pd.DataFrame()
        self.q11_data = pd.DataFrame()
        self.combined_data = pd.DataFrame()
    
    def _recalculate_works_count_stats(self):
        """Recalculate works_count statistics from raw data"""
        try:
            if self.combined_data is None or self.combined_data.empty:
                return pd.DataFrame()
            
            # Recalculate statistics for each question
            questions = ['Q6', 'Q7', 'Q10', 'Q11']
            new_works_count_data = []
            
            for question in questions:
                # Filter data for this question
                question_data = self.combined_data[self.combined_data['Question'] == question]
                
                if not question_data.empty:
                    # Total works count: all records (including empty rows)
                    total_works = len(question_data)
                    
                    # Filtered works count: valid works (excluding empty rows)
                    # Check if work name columns have values
                    work_name_columns = [col for col in question_data.columns if 'name' in col.lower() or 'work' in col.lower()]
                    if work_name_columns:
                        # Calculate rows with at least one work name column not null and not empty string
                        valid_mask = question_data[work_name_columns].notna().any(axis=1)
                        # Further filter empty strings
                        for col in work_name_columns:
                            if col in question_data.columns:
                                valid_mask = valid_mask & (question_data[col].astype(str).str.strip() != '')
                        valid_works = valid_mask.sum()
                    else:
                        # If no work name columns found, check all non-ID and non-region columns
                        exclude_cols = ['UserId', 'User ID', 'Region', 'Question']
                        content_cols = [col for col in question_data.columns if col not in exclude_cols]
                        if content_cols:
                            valid_works = question_data[content_cols].notna().any(axis=1).sum()
                        else:
                            valid_works = 0
                    
                    # Get unique user IDs - count only users with valid content
                    user_id_col = 'UserId' if 'UserId' in question_data.columns else 'User ID'
                    if user_id_col in question_data.columns:
                        # Count only users with valid work content
                        if work_name_columns:
                            # Use the same filtering logic as valid_works
                            valid_mask = question_data[work_name_columns].notna().any(axis=1)
                            for col in work_name_columns:
                                if col in question_data.columns:
                                    valid_mask = valid_mask & (question_data[col].astype(str).str.strip() != '')
                            users_with_valid_works = question_data[valid_mask][user_id_col].nunique()
                        else:
                            # If no work name columns found, check all content columns
                            exclude_cols = ['UserId', 'User ID', 'Region', 'Question']
                            content_cols = [col for col in question_data.columns if col not in exclude_cols]
                            if content_cols:
                                valid_mask = question_data[content_cols].notna().any(axis=1)
                                users_with_valid_works = question_data[valid_mask][user_id_col].nunique()
                            else:
                                users_with_valid_works = 0
                    else:
                        users_with_valid_works = 0
                    
                    new_works_count_data.append({
                        'Question': question,
                        'Total_Works': total_works,  # Total works count
                        'Valid_Works': valid_works,  # Filtered works count
                        'Unique_Users': users_with_valid_works,  # Number of users with valid content
                        'Total_Outputs': total_works,  # Maintain compatibility
                        'Valid_Outputs': valid_works   # Maintain compatibility
                    })
            
            return pd.DataFrame(new_works_count_data)
                
        except Exception as e:
            st.warning(f"Error recalculating works count stats: {str(e)}")
            return pd.DataFrame()
    
    def _load_analysis_results(self):
        """Load pre-computed analysis results (deprecated, kept for compatibility)"""
        # This method is no longer used as we now calculate directly from original data
        pass

    def get_summary_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get summary statistics for all questions"""
        try:
            # Recalculate from raw data
            works_count_stats = self._recalculate_works_count_stats()
            
            if works_count_stats.empty:
                return {}
            
            summary = {}
            for _, row in works_count_stats.iterrows():
                question = row['Question']
                summary[question] = {
                    'total_works': int(row['Total_Works']),  # Total works count
                    'valid_works': int(row['Valid_Works']),  # Filtered works count
                    'unique_users': int(row['Unique_Users']),  # Unique user count
                    'avg_works_per_user': round(row['Valid_Works'] / row['Unique_Users'], 2) if row['Unique_Users'] > 0 else 0,
                    # Maintain compatibility
                    'total_outputs': int(row['Total_Works']),
                    'valid_outputs': int(row['Valid_Works']),
                    'completion_rate': (row['Valid_Works'] / row['Total_Works'] * 100) if row['Total_Works'] > 0 else 0
                }
            
            return summary
            
        except Exception as e:
            st.error(f"Get summary stats error: {e}")
            return {}
    
    def get_works_count_data(self) -> Dict[str, Dict[str, Any]]:
        """Get works count data for visualization"""
        try:
            # Recalculate from raw data
            works_count_stats = self._recalculate_works_count_stats()
            
            if works_count_stats.empty:
                return {}
            
            # Prepare chart data
            chart_data = {}
            for _, row in works_count_stats.iterrows():
                question = row['Question']
                chart_data[question] = {
                    'total_works': row['Total_Works'],      # Total works count
                    'valid_works': row['Valid_Works'],      # Filtered works count
                    'unique_users': row['Unique_Users'],    # Unique user count
                    # Maintain compatibility
                    'users_with_works': row['Unique_Users'],
                    'avg_works_per_user': (row['Valid_Works'] / row['Unique_Users']) if row['Unique_Users'] > 0 else 0
                }
            
            return chart_data
            
        except Exception as e:
            st.error(f"Get works count data error: {e}")
            return {}
    
    def get_frequency_data(self, question: str = None) -> Dict[str, Any]:
        """Get frequency analysis data"""
        try:
            # Recalculate from raw data
            frequency_stats = self._recalculate_frequency_stats()
            
            if frequency_stats.empty:
                return {}
            
            # If question is specified, filter data
            if question:
                question_data = frequency_stats[frequency_stats['Question'] == question]
            else:
                question_data = frequency_stats
            
            result = {}
            for _, row in question_data.iterrows():
                value = row['Value']
                if value not in result:
                    result[value] = 0
                result[value] += int(row['Frequency'])
            
            return result
            
        except Exception as e:
            st.error(f"Get frequency data error: {e}")
            return {}
    
    def get_special_fields_data(self, question: str, variable: str = None) -> Dict[str, int]:
        """Get special fields analysis data for specified question and variable"""
        try:
            # Recalculate from raw data
            frequency_stats = self._recalculate_frequency_stats()
            
            if frequency_stats.empty:
                return {}
            
            # Filter data for specified question
            question_data = frequency_stats[frequency_stats['Question'] == question]
            if question_data.empty:
                return {}
            
            # If variable is specified, further filter
            if variable:
                question_data = question_data[question_data['Field'] == variable]
            
            result = {}
            for _, row in question_data.iterrows():
                value = str(row['Value'])[:80]  # Limit length to display complete labels
                frequency = int(row['Frequency'])
                result[value] = frequency
            
            return result
            
        except Exception as e:
            st.error(f"Get special fields data error: {e}")
            return {}
    
    def get_special_fields_variables(self, question: str) -> List[str]:
        """Get all special field variable names for specified question"""
        try:
            # Recalculate from raw data
            frequency_stats = self._recalculate_frequency_stats()
            
            if frequency_stats.empty:
                return []
            
            question_data = frequency_stats[frequency_stats['Question'] == question]
            variables = question_data['Field'].unique().tolist()
            return variables
        except Exception as e:
            st.error(f"Get special field variables error: {e}")
            return []
    
    def get_cpo_glo_distribution(self, question: str) -> Dict[str, int]:
        """Get CPO/GLO code distribution for specified question"""
        try:
            # Recalculate from raw data
            cpo_glo_stats = self._recalculate_cpo_glo_stats()
            
            if cpo_glo_stats.empty:
                return {}
            
            question_data = cpo_glo_stats[cpo_glo_stats['Question'] == question]
            if question_data.empty:
                return {}
            
            # Take top 10 most frequent codes
            top_data = question_data.head(10)
            result = {}
            for _, row in top_data.iterrows():
                region = row['Region']
                count = row['Count']
                result[region] = count
            
            return result
        except Exception as e:
            st.error(f"Get CPO/GLO distribution error: {e}")
            return {}
    
    def get_field_distribution(self, question: str, field_name: str) -> Dict[str, int]:
        """Get distribution of values for a specific field in a question"""
        try:
            # Use filtered combined_data to ensure response region filtering
            if self.combined_data is None or self.combined_data.empty:
                st.warning(f"No combined data available for {question}")
                return {}
            
            # Get data for specified question from filtered data
            question_data = self.combined_data[self.combined_data['Question'] == question]
            
            if question_data.empty:
                st.info(f"No data found for question {question}")
                return {}
            
            # Check if field exists
            if field_name not in question_data.columns:
                st.warning(f"Field '{field_name}' not found in {question} data. Available columns: {list(question_data.columns)}")
                return {}
            
            # Data standardization processing
            field_data = question_data[field_name].copy()
            
            # More lenient null value handling - only remove truly empty values
            field_data = field_data.dropna()
            field_data = field_data[field_data.astype(str).str.strip() != '']
            field_data = field_data[field_data.astype(str).str.strip() != 'nan']
            
            if field_data.empty:
                st.info(f"No valid data found for field '{field_name}' in {question} after filtering")
                return {}
            
            # Standardization processing: remove extra spaces, unify case format
            field_data = field_data.astype(str).str.strip()  # Remove leading and trailing spaces
            field_data = field_data.str.replace(r'\s+', ' ', regex=True)  # Replace multiple spaces with single space
            
            # Standardize common value formats
            standardization_map = {
                # Funding source standardization
                'extrabudgetary': 'Extrabudgetary',
                'extra budgetary': 'Extrabudgetary', 
                'extra-budgetary': 'Extrabudgetary',
                'EXTRABUDGETARY': 'Extrabudgetary',
                'regular budget': 'Regular Budget',
                'regularbudget': 'Regular Budget',
                'REGULAR BUDGET': 'Regular Budget',
                
                # Publication type standardization
                'technical report': 'Technical Report',
                'Technical report': 'Technical Report',
                'TECHNICAL REPORT': 'Technical Report',
                'working paper': 'Working Paper',
                'Working paper': 'Working Paper',
                'WORKING PAPER': 'Working Paper',
                'guidance/tools': 'Guidance/Tools',
                'Guidance/tools': 'Guidance/Tools',
                'GUIDANCE/TOOLS': 'Guidance/Tools',
                'evaluation': 'Evaluation',
                'EVALUATION': 'Evaluation',
                'data/database': 'Data/Database',
                'Data/database': 'Data/Database',
                'DATA/DATABASE': 'Data/Database',
                'best practices/lessons learned': 'Best Practices/Lessons Learned',
                'Best practices/lessons learned': 'Best Practices/Lessons Learned',
                'BEST PRACTICES/LESSONS LEARNED': 'Best Practices/Lessons Learned',
                
                # Youth-related standardization
                'youth only': 'Youth Only',
                'YOUTH ONLY': 'Youth Only',
                'youth is one of the target groups': 'Youth Is One Of The Target Groups',
                'YOUTH IS ONE OF THE TARGET GROUPS': 'Youth Is One Of The Target Groups',
                
                # Geographic focus standardization
                'global': 'Global',
                'GLOBAL': 'Global',
                'regional': 'Regional',
                'REGIONAL': 'Regional',
                'national/local': 'National/Local',
                'NATIONAL/LOCAL': 'National/Local',
                
                # Certification standardization
                'yes': 'Yes',
                'YES': 'Yes',
                'no': 'No',
                'NO': 'No',
                
                # Delivery mode standardization
                'in person': 'In Person',
                'IN PERSON': 'In Person',
                'online': 'Online',
                'ONLINE': 'Online',
                'both': 'Both',
                'BOTH': 'Both'
            }
            
            # Apply standardization mapping
            for old_value, new_value in standardization_map.items():
                field_data = field_data.str.replace(old_value, new_value, case=False, regex=False)
            
            # Calculate field value distribution
            field_counts = field_data.value_counts()
            
            return field_counts.to_dict()
            
        except Exception as e:
            st.error(f"Get field distribution error for {question} - {field_name}: {e}")
            return {}

def create_theme_count_chart(works_count_data, current_theme=None):
    """Create count chart with transparency effect for non-current themes"""
    if not works_count_data:
        return None
    
    question_labels = {
        'Q6': 'Knowledge development & dissemination',
        'Q7': 'Technical assistance', 
        'Q10': 'Capacity building',
        'Q11': 'Advocacy & partnerships'
    }
    
    # Filter Q6, Q7, Q10, Q11 data (consistent with Dash version)
    all_questions = ['Q6', 'Q7', 'Q10', 'Q11']
    
    # Prepare data - ensure all questions have data, fill with 0 if missing
    questions = all_questions
    question_display_labels = [question_labels.get(q, q) for q in questions]
    unique_users = []
    total_works = []
    
    for q in questions:
        if q in works_count_data:
            unique_users.append(works_count_data[q]['unique_users'])
            total_works.append(works_count_data[q]['valid_works'])
        else:
            unique_users.append(0)
            total_works.append(0)
    
    # Create chart with transparency effect
    colors = STANDARD_COLORS[:2] if not STYLES_AVAILABLE else style_manager.get_chart_colors()[:2]
    
    # Apply transparency to non-current themes
    user_colors = []
    work_colors = []
    
    for i, q in enumerate(questions):
        if current_theme and q != current_theme:
            # Make non-current themes semi-transparent
            user_colors.append(f"rgba({int(colors[0][1:3], 16)}, {int(colors[0][3:5], 16)}, {int(colors[0][5:7], 16)}, 0.3)")
            work_colors.append(f"rgba({int(colors[1][1:3], 16)}, {int(colors[1][3:5], 16)}, {int(colors[1][5:7], 16)}, 0.3)")
        else:
            # Keep current theme fully opaque
            user_colors.append(colors[0])
            work_colors.append(colors[1])
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='Number of staff reporting',
        x=question_display_labels,
        y=unique_users,
        marker_color=user_colors,
        hovertemplate='<b>%{x}</b><br>Number of staff reporting: %{y}<extra></extra>',
        hoverlabel=dict(bgcolor='rgba(255,255,255,0.9)', bordercolor='rgba(0,0,0,0.2)', font_color='black')
    ))
    fig.add_trace(go.Bar(
        name='Number of outputs delivered',
        x=question_display_labels,
        y=total_works,
        marker_color=work_colors,
        hovertemplate='<b>%{x}</b><br>Number of outputs delivered: %{y}<extra></extra>',
        hoverlabel=dict(bgcolor='rgba(255,255,255,0.9)', bordercolor='rgba(0,0,0,0.2)', font_color='black')
    ))
    
    # Create line-wrapped labels
    wrapped_labels = []
    for label in question_display_labels:
        # Split long labels into two lines
        if len(label) > 15:
            words = label.split(' ')
            mid = len(words) // 2
            line1 = ' '.join(words[:mid])
            line2 = ' '.join(words[mid:])
            wrapped_labels.append(f"{line1}<br>{line2}")
        else:
            wrapped_labels.append(label)
    
    # Apply style configuration
    if STYLES_AVAILABLE:
        layout_config = style_manager.get_global_chart_config('layout')
        fig.update_layout(
            xaxis_title='',  # Hide x-axis title
            yaxis_title='',  # Hide y-axis title
            barmode='group',
            height=500,
            margin=dict(b=120),
            xaxis=dict(
                tickangle=0,
                tickmode='array',
                tickvals=list(range(len(question_display_labels))),
                ticktext=wrapped_labels,
                tickfont=dict(size=10),
                side='bottom'
            ),
            **layout_config
        )
    else:
        fig.update_layout(
            title='Outputs Count by Question',
            title_font_size=20,
            title_x=0.5,
            title_xanchor='center',
            xaxis_title='',  # Hide x-axis title
            yaxis_title='',  # Hide y-axis title
            barmode='group',
            height=500,
            margin=dict(b=120),
            paper_bgcolor='white',
            plot_bgcolor='white',
            font_family="Arial",
            xaxis=dict(
                tickangle=0,
                tickmode='array',
                tickvals=list(range(len(question_display_labels))),
                ticktext=wrapped_labels,
                tickfont=dict(size=10),
                side='bottom'
            )
        )
    
    return fig

def create_theme_detail_list(data_processor, question):
    """Create detail list for specific question/theme"""
    if data_processor.combined_data is None or data_processor.combined_data.empty:
        return None
    
    # Filter data for specific question
    works_df = data_processor.combined_data[data_processor.combined_data['Question'] == question].copy()
    
    if works_df.empty:
        return None
    
    # Project name column mapping
    project_name_mapping = {
        'Q6': 'Initiative/output\'s name??',
        'Q7': 'Initiative/programme/project\'s name??',
        'Q10': 'Course/programme/project\'s name??',
        'Q11': 'Output/initiative/programme/project\'s name??'
    }
    
    project_col = project_name_mapping.get(question)
    
    # Filter to only show records that have a valid project name
    if project_col and project_col in works_df.columns:
        has_project_name = (
            works_df[project_col].notna() & 
            (works_df[project_col].astype(str).str.strip() != '') & 
            (works_df[project_col].astype(str).str.strip() != 'None') &
            (works_df[project_col].astype(str).str.strip() != 'nan') &
            (works_df[project_col].astype(str).str.lower().str.strip() != 'none')
        )
        works_df = works_df[has_project_name].copy()
    
    if works_df.empty:
        return None
    
    # Select relevant columns for display
    display_columns = ['Question', 'UserId']
    
    # Add Department/Region if available
    if 'Department/Region' in works_df.columns:
        display_columns.append('Department/Region')
    
    # Add project name column
    if project_col and project_col in works_df.columns:
        display_columns.append(project_col)
    
    # Create final display dataframe
    display_df = works_df[display_columns].copy()
    
    # Rename project column to unified name
    if project_col and project_col in display_df.columns:
        display_df = display_df.rename(columns={project_col: 'Project Name'})
    
    return display_df
    """Legacy chart creation function - deprecated, use unified style create_chart function"""
    if STYLES_AVAILABLE:
        # Convert data format to dictionary
        if hasattr(data, 'index'):
            # Series data
            chart_data = dict(zip(data.index, data.values))
        else:
            # DataFrame data
            if len(data.columns) >= 2:
                chart_data = dict(zip(data.iloc[:, 0], data.iloc[:, 1]))
            else:
                chart_data = dict(zip(data.index, data.iloc[:, 0]))
        
        # Use unified style to create chart
        return create_chart(chart_data, chart_type, title)
    else:
        # Fallback chart creation logic
        colors = STANDARD_COLORS
        
        if hasattr(data, 'index'):
            # Series data
            categories = data.index.tolist()
            values = data.values.tolist()
        else:
            # DataFrame data
            if len(data.columns) >= 2:
                categories = data.iloc[:, 0].tolist()
                values = data.iloc[:, 1].tolist()
            else:
                categories = data.index.tolist()
                values = data.iloc[:, 0].tolist()
        
        fig = go.Figure()
        
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
            title=title,
            title_font_size=20,
            title_x=0.5,
            title_xanchor='center',
            height=400,
            paper_bgcolor='white',
            plot_bgcolor='white',
            font_family="Arial"
        )
        
        return fig


def apply_region_filter_to_processor(data_processor, filtered_user_ids):
    """Filter data in data processor based on filtered user IDs"""
    try:
        # Filter data in combined_data
        if data_processor.combined_data is not None and not data_processor.combined_data.empty:
            # Assume combined_data has UserId or User ID column
            if 'UserId' in data_processor.combined_data.columns:
                data_processor.combined_data = data_processor.combined_data[
                    data_processor.combined_data['UserId'].isin(filtered_user_ids)
                ]
            elif 'User ID' in data_processor.combined_data.columns:
                data_processor.combined_data = data_processor.combined_data[
                    data_processor.combined_data['User ID'].isin(filtered_user_ids)
                ]
        
        # Recalculate statistics
        data_processor._recalculate_works_count_stats()
        
    except Exception as e:
        st.warning(f"Error applying region filter: {str(e)}")
    
    return data_processor

def create_layout():
    """Create the main Streamlit layout with theme-based organization"""
    # Add unified header first
    create_unified_header()
    
    # Apply page styles
    if STYLES_AVAILABLE:
        apply_page_style()
    else:
        st.set_page_config(
            page_title="Q6Q7Q10Q11 Analysis Dashboard",
            page_icon="📊",
            layout="wide"
        )
    
    # Define base_path
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    st.title("📊 Specialized Analysis")
    st.markdown("**Outputs statistics and frequency analysis across areas**")
    st.markdown("---")

    # Add region filtering functionality - moved before data processor initialization
    
    # Check if region data exists
    has_region_data = False
    selected_region = 'All'
    regions_set = set()
    original_data = pd.DataFrame()
    filtered_user_ids = None
    
    try:
        # If global shared selection exists, reuse it
        if 'selected_region' in st.session_state and 'regions_options' in st.session_state:
            selected_region = st.session_state['selected_region']
            regions = st.session_state['regions_options']
            has_region_data = True
            selected_year = st.session_state.get('selected_year', 'All')
            # Build original_data from PART3 files still needed for filtering and counts
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)
            data_files = [
                os.path.join(project_root, 'orignaldata', 'PART3_base_dataQ6.csv'),
                os.path.join(project_root, 'orignaldata', 'PART3_base_dataQ7.csv'),
                os.path.join(project_root, 'orignaldata', 'PART3_base_dataQ10.csv'),
                os.path.join(project_root, 'orignaldata', 'PART3_base_dataQ11.csv')
            ]
            combined_original_data = []
            for file_path in data_files:
                if os.path.exists(file_path):
                    df = safe_read_csv(file_path)
                    # Apply YEAR filter if available
                    try:
                        if selected_year != 'All':
                            # Check for both 'YEAR' and 'year' columns
                            if 'YEAR' in df.columns:
                                df = df[df['YEAR'].astype(str).str.strip() == str(selected_year)]
                            elif 'year' in df.columns:
                                df = df[df['year'].astype(str).str.strip() == str(selected_year)]
                    except Exception:
                        pass
                    if 'Department/Region' in df.columns:
                        combined_original_data.append(df)
            if combined_original_data:
                original_data = pd.concat(combined_original_data, ignore_index=True, sort=False)
            else:
                original_data = pd.DataFrame()
        else:
            # Fallback to local construction (original logic)
            # Get absolute path of project root directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)
            
            data_files = [
                os.path.join(project_root, 'orignaldata', 'PART3_base_dataQ6.csv'),
                os.path.join(project_root, 'orignaldata', 'PART3_base_dataQ7.csv'),
                os.path.join(project_root, 'orignaldata', 'PART3_base_dataQ10.csv'),
                os.path.join(project_root, 'orignaldata', 'PART3_base_dataQ11.csv')
            ]
            
            combined_original_data = []
            selected_year = st.session_state.get('selected_year', 'All')
            for file_path in data_files:
                if os.path.exists(file_path):
                    df = safe_read_csv(file_path)
                    # Apply YEAR filter if available
                    try:
                        if selected_year != 'All':
                            # Check for both 'YEAR' and 'year' columns
                            if 'YEAR' in df.columns:
                                df = df[df['YEAR'].astype(str).str.strip() == str(selected_year)]
                            elif 'year' in df.columns:
                                df = df[df['year'].astype(str).str.strip() == str(selected_year)]
                    except Exception:
                        pass
                    if 'Department/Region' in df.columns:
                        regions_set.update(df['Department/Region'].dropna().unique())
                        has_region_data = True
                        combined_original_data.append(df)
                    elif 'Department/Region' in df.columns:  # Chinese column name
                        regions_set.update(df['Department/Region'].dropna().unique())
                        has_region_data = True
                        combined_original_data.append(df)
            
            # Combine all original data
            if combined_original_data:
                original_data = pd.concat(combined_original_data, ignore_index=True, sort=False)
            else:
                original_data = pd.DataFrame()
            
            if has_region_data and regions_set:
                regions = ['All'] + sorted(list(regions_set))

                # Improve display: insert soft wrap opportunities so long texts can wrap gracefully
                def _wrap_label(s):
                    s = str(s)
                    # Insert zero-width space after common separators to allow wrapping
                    for ch in ['/', '\\', '-', '—', '–', '_', ' ', '（', '）', '(', ')', ':', '：', ',', '·']:
                        s = s.replace(ch, ch + '\u200B')
                    return s

                selected_region = st.sidebar.selectbox(
                    "Select Organizational Unit",
                    regions,
                    format_func=_wrap_label
                )
            elif has_region_data and not regions_set:
                st.sidebar.info("Regional filtering not available - no region data found.")
            else:
                st.sidebar.info("Regional filtering not available - data file not found.")
    except Exception as e:
        st.sidebar.info(f"Regional filtering not available - error: {str(e)}")
    
    # Apply region filtering (similar to Dash version logic)
    filtered_data = original_data
    if has_region_data and selected_region != 'All' and not original_data.empty:
        try:
            if 'Department/Region' in original_data.columns:
                filtered_data = original_data[original_data['Department/Region'] == selected_region]
            elif 'Department/Region' in original_data.columns:  # Chinese column name
                filtered_data = original_data[original_data['Department/Region'] == selected_region]
            
            if not filtered_data.empty:
                st.info(f"Showing data for: {selected_region} ({len(filtered_data)} records)")
                # Get filtered user IDs
                if 'UserId' in filtered_data.columns:
                    filtered_user_ids = filtered_data['UserId'].unique()
            else:
                st.warning(f"No data found for region: {selected_region}. Showing all data.")
                filtered_data = original_data
        except Exception as e:
            st.warning(f"Region filtering encountered an issue: {str(e)}. Showing all data.")
            filtered_data = original_data
    
    # Initialize data processor (after filtering logic)
    data_processor = Q6Q7Q10Q11DataProcessor(base_path)
    
    # If there are filtering conditions, apply to data processor
    if filtered_user_ids is not None:
        data_processor = apply_region_filter_to_processor(data_processor, filtered_user_ids)
    
    # Check if data is available
    if (data_processor.combined_data is None or data_processor.combined_data.empty):
        st.warning("No data available to display. Please ensure the data files are in the correct location.")
        return


    # Get works count data for all themes
    works_count_data = data_processor.get_works_count_data()
    
    # Define theme information
    themes = {
        'Q6': {
            'title': '📚 Knowledge Development & Dissemination',
            'color': '#f0f8ff',
            'charts': [
                ('Funding source (Options: regular budget or extrabudgetary)', 'pie', 'Funding Source Of Knowledge Development And Dissemination Outputs In 2024'),
                ('Focus (Options: Youth only or Youth is one of the target groups)', 'pie', 'Target Group Of Knowledge Development And Dissemination Outputs In 2024'),
                ('Type of publication (Options: Evaluation, or Guidance/tools, or Technical Report, or Working paper, or Data/Database) ', 'bar', 'Types Of Knowledge Development And Dissemination Outputs Delivered In 2024')
            ]
        },
        'Q7': {
            'title': '🔧 Technical Assistance',
            'color': '#f0fff0',
            'charts': [
                ('Funding source (Options: regular budget or extrabudgetary)', 'pie', 'Funding Source Of Technical Assistance Outputs In 2024'),
                ('Focus \n(Options: Youth only or Youth is one of the target groups)', 'pie', 'Target Group Of Technical Assistance Outputs In 2024'),
                ('Country or Region', 'bar', 'Technical Assistance Outputs Across Regions')
            ]
        },
        'Q10': {
            'title': '🎓 Capacity Development',
            'color': '#fff8f0',
            'charts': [
                ('In person or online or both', 'pie', 'Delivery Mode Of Capacity Development Outputs In 2024'),
                ('Funding source (Options: regular budget or extrabudgetary)', 'pie', 'Funding Source For Capacity Development Outputs In 2024'),
                ('With certification (Yes or No)', 'pie', 'Capacity Development Outputs & Certification'),
                ('Focus (Options: Youth only or Youth is one of the target groups)', 'pie', 'Target Group Of Capacity Development Outputs In 2024')
            ]
        },
        'Q11': {
            'title': '🤝 Advocacy & Partnerships',
            'color': '#fdf0ff',
            'charts': [
                ('Type of partnership\n(Options: UN interagency initiative; or multistakeholder initiative; or bilateral partnership; or event; or campaign; or challenge)', 'bar', 'Types Of Advocacy Or Partnership Outputs In 2024'),
                ('Focus\n (Options: Youth only or Youth is one of the target groups)', 'pie', 'Target Group For Advocacy & Partnerships Outputs In 2024'),
                ('Specify name of the Region/country', 'bar', 'Advocacy & Partnership Outputs Across Regions'),
                ('Funding source (Options: regular budget or extrabudgetary)', 'pie', 'Funding Source For Advocacy & Partnerships Related Outputs In 2024'),
                ('Geographical focus (Global, Regional  or National/local)', 'pie', 'Geographical Focus Of Advocacy And Partnerships Outputs')
            ]
        }
    }
    
    # Add section filter selectbox
    st.markdown("### 📋 Select Analysis Section")
    section_options = [
        "Outputs Count Statistics",
        "📚 Knowledge Development & Dissemination", 
        "🔧 Technical Assistance",
        "🎓 Capacity Development",
        "🤝 Advocacy & Partnerships"
    ]
    
    selected_section = st.selectbox(
        "Choose the section to analyze:",
        section_options,
        index=0
    )
    
    st.markdown("---")
    
    # Display content based on selected section
    if selected_section == "Outputs Count Statistics":
        # Section 1: Outputs Count Statistics only
        st.markdown("""
        <div style="background-color: #e8f4fd; padding: 15px; border-radius: 10px; margin: 20px 0;">
            <h2 style="color: #2c3e50; margin: 0;">📊 Outputs Count Statistics</h2>
        </div>
        """, unsafe_allow_html=True)
        
        if works_count_data:
            count_fig = create_theme_count_chart(works_count_data, current_theme=None)
            if count_fig:
                st.plotly_chart(count_fig, use_container_width=True)
            else:
                st.info("No count statistics data available.")
        else:
            st.info("No count statistics data available.")
    
    else:
        # Find the corresponding theme for the selected section
        theme_mapping = {
            "📚 Knowledge Development & Dissemination": "Q6",
            "🔧 Technical Assistance": "Q7", 
            "🎓 Capacity Development": "Q10",
            "🤝 Advocacy & Partnerships": "Q11"
        }
        
        question = theme_mapping[selected_section]
        theme_info = themes[question]
        
        # Theme header
        st.markdown(f"""
        <div style="background-color: {theme_info['color']}; padding: 15px; border-radius: 10px; margin: 20px 0;">
            <h2 style="color: #2c3e50; margin: 0;">{theme_info['title']}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Section 2: Frequency Analysis
        st.subheader("📊 Frequency Analysis")
        
        for field_name, chart_type, chart_title in theme_info['charts']:
            field_data = data_processor.get_field_distribution(question, field_name)
            if field_data:
                # Special handling for Q7 and Q11 region data (top 10)
                if 'Region' in chart_title or 'Regions' in chart_title:
                    sorted_data = dict(sorted(field_data.items(), key=lambda x: x[1], reverse=True)[:10])
                    field_data = sorted_data
                
                # Special handling for Q11 partnership types with custom order
                if question == 'Q11' and 'Type of partnership' in field_name:
                    custom_order = [
                        'multistakeholder initiative',
                        'bilateral partnership',
                        'UN interagency initiative',
                        'campaign',
                        'event',
                        'challenge'
                    ]
                    
                    ordered_data = {}
                    for item in custom_order:
                        if item in field_data:
                            ordered_data[item] = field_data[item]
                    
                    for key, value in field_data.items():
                        if key not in ordered_data:
                            ordered_data[key] = value
                    
                    field_data = ordered_data
                    preserve_order = True
                else:
                    preserve_order = False
                
                fig = create_chart(pd.Series(field_data), chart_type, chart_title, preserve_order=preserve_order)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info(f"No data available for {chart_title.lower()}")
        
        # Section 3: Outputs Detail List
        st.subheader("📋 Outputs Detail List")
        
        detail_df = create_theme_detail_list(data_processor, question)
        if detail_df is not None and not detail_df.empty:
            total_records = len(detail_df)
            
            # Initialize session state for current page if not exists
            page_key = f'outputs_current_page_{question}'
            if page_key not in st.session_state:
                st.session_state[page_key] = 1
            
            # Get current page data
            items_per_page = st.session_state.get('items_per_page', 50)
            total_pages = (total_records - 1) // items_per_page + 1
            
            # Calculate display range
            start_idx = (st.session_state[page_key] - 1) * items_per_page
            end_idx = min(start_idx + items_per_page, total_records)
            
            # Get current page data
            display_df = detail_df.iloc[start_idx:end_idx].copy()
            
            st.dataframe(display_df, use_container_width=True)
            
            # Compact pagination controls
            st.markdown("<br>", unsafe_allow_html=True)
            
            # First row: Page info centered at the top
            st.markdown(
                f"<div style='text-align: center; margin: 10px 0;'>"
                f"<strong>Page {st.session_state[page_key]} of {total_pages}</strong> | "
                f"Showing {start_idx + 1}-{end_idx} of {total_records} records"
                f"</div>", 
                unsafe_allow_html=True
            )
            
            # Second row: Items per page and Jump to page side by side
            control_col1, control_col2 = st.columns([1, 1])
            
            with control_col1:
                # Items per page
                new_items_per_page = st.selectbox(
                    "Items per page:",
                    options=[10, 25, 50, 100, 200],
                    index=[10, 25, 50, 100, 200].index(items_per_page) if items_per_page in [10, 25, 50, 100, 200] else 2,
                    key=f"items_per_page_{question}"
                )
                
                if new_items_per_page != items_per_page:
                    st.session_state.items_per_page = new_items_per_page
                    st.session_state[page_key] = 1
                    st.rerun()
            
            with control_col2:
                # Jump to page
                new_page = st.number_input(
                    "Jump to page:",
                    min_value=1,
                    max_value=total_pages,
                    value=st.session_state[page_key],
                    key=f"page_input_{question}"
                )
                if new_page != st.session_state[page_key]:
                    st.session_state[page_key] = new_page
                    st.rerun()
            
            # Third row: Navigation buttons
            nav_col1, nav_col2 = st.columns([1, 1])
            
            with nav_col1:
                # Previous page
                if st.button("◀ Previous", key=f"prev_{question}", disabled=(st.session_state[page_key] <= 1), use_container_width=True):
                    st.session_state[page_key] = max(1, st.session_state[page_key] - 1)
                    st.rerun()
            
            with nav_col2:
                # Next page
                if st.button("Next ▶", key=f"next_{question}", disabled=(st.session_state[page_key] >= total_pages), use_container_width=True):
                    st.session_state[page_key] = min(total_pages, st.session_state[page_key] + 1)
                    st.rerun()
        else:
            st.info(f"No detail data available for {theme_info['title']}")

if __name__ == "__main__":
    create_layout()