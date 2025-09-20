import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys
from typing import Dict, Any, List

# Import unified style module
try:
    from st_styles import style_manager, create_chart, apply_page_style, create_metrics, create_table, create_standardized_chart
    STYLES_AVAILABLE = True
except ImportError:
    STYLES_AVAILABLE = False
    # Define backup colors
    STANDARD_COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

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
                # Keep all rows that have meaningful data in any column
                # Check if row has any non-null, non-empty content (excluding just UserId)
                meaningful_columns = [col for col in df.columns if col not in ['UserId']]
                
                if meaningful_columns:
                    # Check if any meaningful column has content
                    has_content = pd.Series([False] * len(df), index=df.index)
                    
                    for col in meaningful_columns:
                        if col in df.columns:
                            # Check for non-null and non-empty string values
                            col_has_content = (
                                df[col].notna() & 
                                (df[col].astype(str).str.strip() != '') & 
                                (df[col].astype(str).str.strip() != 'nan')
                            )
                            has_content = has_content | col_has_content
                    
                    df_filtered = df[has_content].copy()
                    if not df_filtered.empty:
                        dataframes.append(df_filtered)
                else:
                    # If no meaningful columns found, keep all rows with UserId
                    if 'UserId' in df.columns:
                        df_filtered = df[df['UserId'].notna()].copy()
                        if not df_filtered.empty:
                            dataframes.append(df_filtered)
        
        if dataframes:
            self.combined_data = pd.concat(dataframes, ignore_index=True, sort=False)
        else:
            self.combined_data = pd.DataFrame()
    
    def _load_data_file(self, file_path: str) -> pd.DataFrame:
        """Load data file"""
        try:
            full_path = os.path.join(self.base_path, file_path)
            if os.path.exists(full_path):
                df = pd.read_csv(full_path, encoding='utf-8')
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
                    
                    # Get unique user IDs - 只统计有有效内容的用户
                    user_id_col = 'UserId' if 'UserId' in question_data.columns else 'User ID'
                    if user_id_col in question_data.columns:
                        # 只统计有有效工作内容的用户
                        if work_name_columns:
                            # 使用与valid_works相同的过滤逻辑
                            valid_mask = question_data[work_name_columns].notna().any(axis=1)
                            for col in work_name_columns:
                                if col in question_data.columns:
                                    valid_mask = valid_mask & (question_data[col].astype(str).str.strip() != '')
                            users_with_valid_works = question_data[valid_mask][user_id_col].nunique()
                        else:
                            # 如果没有工作名称列，检查所有内容列
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
                        'Unique_Users': users_with_valid_works,  # 有有效内容的用户数量
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
                return {}
            
            # Get data for specified question from filtered data
            question_data = self.combined_data[self.combined_data['Question'] == question]
            
            if question_data.empty:
                return {}
            
            # Check if field exists
            if field_name not in question_data.columns:
                return {}
            
            # Data standardization processing
            field_data = question_data[field_name].copy()
            
            # Remove null values and NaN
            field_data = field_data.dropna()
            
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

def create_chart_old(data: pd.DataFrame, chart_type: str = 'bar', title: str = '') -> go.Figure:
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
    """Create the main Streamlit layout"""
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
    st.sidebar.header("Filters")
    
    # Check if region data exists
    has_region_data = False
    selected_region = 'All'
    regions_set = set()
    original_data = pd.DataFrame()
    filtered_user_ids = None
    
    try:
        # Load original data for region filtering from actual data files
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
        for file_path in data_files:
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
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
            selected_region = st.sidebar.selectbox("Select Organizational Unit", regions)
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



    # Works count statistics - unified title and data source mapping
    st.subheader("✅ Outputs Count Statistics")
    works_count_data = data_processor.get_works_count_data()
    
    if works_count_data:
        # Create question label mapping consistent with Dash version - optimized line break display
        question_labels = {
            'Q6': 'Knowledge development & dissemination',
            'Q7': 'Technical assistance', 
            'Q10': 'Capacity building',
            'Q11': 'Advocacy & partnerships'
        }
        
        # Filter Q6, Q7, Q10, Q11 data (consistent with Dash version)
        # Ensure all questions are displayed, even if data is 0
        all_questions = ['Q6', 'Q7', 'Q10', 'Q11']
        
        # Prepare data - ensure all questions have data, fill with 0 if missing
        questions = all_questions
        question_display_labels = [question_labels.get(q, q) for q in questions]
        unique_users = []
        total_works = []
        
        for q in questions:
            if q in works_count_data:
                unique_users.append(works_count_data[q]['unique_users'])
                total_works.append(works_count_data[q]['valid_works'])  # 使用valid_works而不是total_works
            else:
                # If no data, fill with 0
                unique_users.append(0)
                total_works.append(0)
            
        # Create chart - display unique user count and total works count
        colors = STANDARD_COLORS[:2] if not STYLES_AVAILABLE else style_manager.get_chart_colors()[:2]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Number of staff reporting',
            x=question_display_labels,
            y=unique_users,
            marker_color=colors[0],
            hovertemplate='<b>%{x}</b><br>Number of staff reporting: %{y}<extra></extra>',
            hoverlabel=dict(bgcolor='rgba(255,255,255,0.9)', bordercolor='rgba(0,0,0,0.2)', font_color='black')
        ))
        fig.add_trace(go.Bar(
            name='Number of outputs delivered',
            x=question_display_labels,
            y=total_works,
            marker_color=colors[1],
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
                xaxis_title='Question',
                yaxis_title='Count',
                barmode='group',
                height=500,  # Increase height to accommodate line-wrapped labels
                margin=dict(b=120),  # Increase bottom margin
                xaxis=dict(
                    tickangle=0,  # Set labels to display horizontally
                    tickmode='array',
                    tickvals=list(range(len(question_display_labels))),
                    ticktext=wrapped_labels,
                    tickfont=dict(size=10),  # Adjust font size
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
                xaxis_title='Question',
                yaxis_title='Count',
                barmode='group',
                height=500,  # Increase height to accommodate line-wrapped labels
                margin=dict(b=120),  # Increase bottom margin
                paper_bgcolor='white',
                plot_bgcolor='white',
                font_family="Arial",
                xaxis=dict(
                    tickangle=0,  # Set labels to display horizontally
                    tickmode='array',
                    tickvals=list(range(len(question_display_labels))),
                    ticktext=wrapped_labels,
                    tickfont=dict(size=10),  # Adjust font size
                    side='bottom'
                )
            )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No works count data available.")
    
    # Detailed Analysis by Question
    st.header("📊 Frequency Analysis")
    
    # Q6 Analysis
    st.subheader("Q6 - Knowledge Development & Dissemination")
    
    # Funding Source of Knowledge Development & Dissemination Outputs
    q6_funding_data = data_processor.get_field_distribution('Q6', 'Funding source (Options: regular budget or extrabudgetary)')
    if q6_funding_data:
        fig = create_chart(pd.Series(q6_funding_data), 'pie', 'Funding Source Of Knowledge Development And Dissemination Outputs In 2024')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No funding source data available for Q6")
    
    # Target Group of Knowledge Development & Dissemination Outputs
    q6_focus_data = data_processor.get_field_distribution('Q6', 'Focus (Options: Youth only or Youth is one of the target groups)')
    if q6_focus_data:
        fig = create_chart(pd.Series(q6_focus_data), 'pie', 'Target Group Of Knowledge Development And Dissemination Outputs In 2024')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No target group data available for Q6")
    
    # Types of Knowledge Development & Dissemination Outputs
    q6_type_data = data_processor.get_field_distribution('Q6', 'Type of publication (Options: Evaluation, or Guidance/tools, or Technical Report, or Working paper, or Data/Database) ')
    if q6_type_data:
        fig = create_chart(pd.Series(q6_type_data), 'bar', 'Types Of Knowledge Development And Dissemination Outputs Delivered In 2024')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No publication type data available for Q6")

    # Q7 Analysis
    st.subheader("Q7 - Technical Assistance")
    
    # Funding Source of Technical Assistance Outputs
    q7_funding_data = data_processor.get_field_distribution('Q7', 'Funding source (Options: regular budget or extrabudgetary)')
    if q7_funding_data:
        fig = create_chart(pd.Series(q7_funding_data), 'pie', 'Funding Source Of Technical Assistance Outputs In 2024')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No funding source data available for Q7")
    
    # Target Group of Technical Assistance Outputs
    q7_focus_data = data_processor.get_field_distribution('Q7', 'Focus \n(Options: Youth only or Youth is one of the target groups)')
    if q7_focus_data:
        fig = create_chart(pd.Series(q7_focus_data), 'pie', 'Target Group Of Technical Assistance Outputs In 2024')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No target group data available for Q7")
    
    # Technical Assistance Outputs Across Regions
    q7_region_data = data_processor.get_field_distribution('Q7', 'Country or Region')
    if q7_region_data:
        # Take top 10 regions
        sorted_region_data = dict(sorted(q7_region_data.items(), key=lambda x: x[1], reverse=True)[:10])
        fig = create_chart(pd.Series(sorted_region_data), 'bar', 'Technical Assistance Outputs Across Regions')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No region data available for Q7")
    
    # Q10 Analysis
    st.subheader("Q10 - Capacity Development")
    
    # Delivery Mode of Capacity Development Outputs
    q10_delivery_data = data_processor.get_field_distribution('Q10', 'In person or online or both')
    if q10_delivery_data:
        fig = create_chart(pd.Series(q10_delivery_data), 'pie', 'Delivery Mode Of Capacity Development Outputs In 2024')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No delivery mode data available for Q10")
    
    # Funding Source for Capacity Development Outputs
    q10_funding_data = data_processor.get_field_distribution('Q10', 'Funding source (Options: regular budget or extrabudgetary)')
    if q10_funding_data:
        fig = create_chart(pd.Series(q10_funding_data), 'pie', 'Funding Source For Capacity Development Outputs In 2024')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No funding source data available for Q10")
    
    # Capacity Development Outputs & Certification
    q10_cert_data = data_processor.get_field_distribution('Q10', 'With certification (Yes or No)')
    if q10_cert_data:
        fig = create_chart(pd.Series(q10_cert_data), 'pie', 'Capacity Development Outputs & Certification')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No certification data available for Q10")
    
    # Target Group of Capacity Development Outputs
    q10_focus_data = data_processor.get_field_distribution('Q10', 'Focus (Options: Youth only or Youth is one of the target groups)')
    if q10_focus_data:
        fig = create_chart(pd.Series(q10_focus_data), 'pie', 'Target Group Of Capacity Development Outputs In 2024')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No target group data available for Q10")

    # Q11 Analysis
    st.subheader("Q11 - Advocacy & Partnerships")
    
    # Types of Advocacy & Partnership Outputs
    q11_type_data = data_processor.get_field_distribution('Q11', 'Type of partnership\n(Options: UN interagency initiative; or multistakeholder initiative; or bilateral partnership; or event; or campaign; or challenge)')
    
    if q11_type_data:
        # Custom sorting order - by expected display order
        custom_order = [
            'multistakeholder initiative', # 1
            'bilateral partnership',       # 2  
            'UN interagency initiative',  # 3
            'campaign',                   # 4
            'event',                      # 5
            'challenge'                   # 6
        ]
        
        # Reorder data according to custom order
        ordered_data = {}
        
        # First add data according to custom order
        for item in custom_order:
            if item in q11_type_data:
                ordered_data[item] = q11_type_data[item]
        
        # Add any items not in custom order
        for key, value in q11_type_data.items():
            if key not in ordered_data:
                ordered_data[key] = value
        
        fig = create_chart(pd.Series(ordered_data), 'bar', 'Types Of Advocacy Or Partnership Outputs In 2024', preserve_order=True)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No partnership type data available for Q11")
    
    # Target Group for Advocacy & Partnerships Outputs
    q11_focus_data = data_processor.get_field_distribution('Q11', 'Focus\n (Options: Youth only or Youth is one of the target groups)')
    if q11_focus_data:
        fig = create_chart(pd.Series(q11_focus_data), 'pie', 'Target Group For Advocacy & Partnerships Outputs In 2024')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No target group data available for Q11")
    
    # Advocacy & Partnership Outputs Across Regions
    q11_region_data = data_processor.get_field_distribution('Q11', 'Specify name of the Region/country')
    if q11_region_data:
        # Take top 10 regions/countries
        sorted_region_data = dict(sorted(q11_region_data.items(), key=lambda x: x[1], reverse=True)[:10])
        fig = create_chart(pd.Series(sorted_region_data), 'bar', 'Advocacy & Partnership Outputs Across Regions')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No region data available for Q11")
    
    # Funding Source for Advocacy & Partnerships Related Outputs
    q11_funding_data = data_processor.get_field_distribution('Q11', 'Funding source (Options: regular budget or extrabudgetary)')
    if q11_funding_data:
        fig = create_chart(pd.Series(q11_funding_data), 'pie', 'Funding Source For Advocacy & Partnerships Related Outputs In 2024')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No funding source data available for Q11")
    
    # Geographical Focus of Advocacy and Partnerships Outputs
    q11_geo_data = data_processor.get_field_distribution('Q11', 'Geographical focus (Global, Regional  or National/local)')
    if q11_geo_data:
        fig = create_chart(pd.Series(q11_geo_data), 'pie', 'Geographical Focus Of Advocacy And Partnerships Outputs')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No geographical focus data available for Q11")
    
    # Note: Data table has been removed as requested - keeping only charts

    # Works detail list
    if data_processor.combined_data is not None and not data_processor.combined_data.empty:
        st.subheader("📋 Outputs Detail List")
        
        # Filter and display works list - only show records with project names
        works_df = data_processor.combined_data.copy()
        
        # Project name columns for different questions
        project_name_columns = [
            'Initiative/output\'s name??',  # Q6
            'Initiative/programme/project\'s name??',  # Q7
            'Course/programme/project\'s name??',  # Q10
            'Output/initiative/programme/project\'s name??'  # Q11
        ]
        
        # Filter to only show records that have a valid project name
        if not works_df.empty:
            has_project_name = pd.Series([False] * len(works_df), index=works_df.index)
            
            # 为每个问题使用正确的project name列
            for question in ['Q6', 'Q7', 'Q10', 'Q11']:
                question_mask = works_df['Question'] == question
                question_data = works_df[question_mask]
                
                if not question_data.empty:
                    # 根据问题类型选择正确的project name列
                    if question == 'Q6':
                        project_col = 'Initiative/output\'s name??'
                    elif question == 'Q7':
                        project_col = 'Initiative/programme/project\'s name??'
                    elif question == 'Q10':
                        project_col = 'Course/programme/project\'s name??'
                    elif question == 'Q11':
                        project_col = 'Output/initiative/programme/project\'s name??'
                    
                    if project_col in works_df.columns:
                        # Check for non-null, non-empty, and not 'None' values
                        col_has_name = (
                            works_df[project_col].notna() & 
                            (works_df[project_col].astype(str).str.strip() != '') & 
                            (works_df[project_col].astype(str).str.strip() != 'None') &
                            (works_df[project_col].astype(str).str.strip() != 'nan') &
                            (works_df[project_col].astype(str).str.lower().str.strip() != 'none')
                        )
                        
                        # 只对当前问题的记录应用过滤
                        question_has_name = question_mask & col_has_name
                        has_project_name = has_project_name | question_has_name
            
            # Only keep records with valid project names
            works_df = works_df[has_project_name].copy()
        
        # Show basic information about the works
        if not works_df.empty:
            total_records = len(works_df)
            
            # Initialize session state for current page if not exists
            if 'outputs_current_page' not in st.session_state:
                st.session_state.outputs_current_page = 1
            
            # Get current page data (using default 50 items per page initially)
            items_per_page = st.session_state.get('items_per_page', 50)
            total_pages = (total_records - 1) // items_per_page + 1
            
            # Calculate display range
            start_idx = (st.session_state.outputs_current_page - 1) * items_per_page
            end_idx = min(start_idx + items_per_page, total_records)
            
            # Get current page data
            display_df = works_df.iloc[start_idx:end_idx].copy()
            
            # Select relevant columns for display - focus on core information including project names
            display_columns = []
            
            # Core columns with actual data (ordered by importance)
            core_columns = [
                'Question',  # Question type
                'UserId',    # User ID  
                'Department/Region',  # Department/Region (注意：Q11文件中此列缺失)
            ]
            
            # Project name columns for different questions (实际列名)
            project_name_columns = [
                'Initiative/output\'s name??',  # Q6
                'Initiative/programme/project\'s name??',  # Q7
                'Course/programme/project\'s name??',  # Q10
                'Output/initiative/programme/project\'s name??'  # Q11
            ]
            
            # Add existing core columns that have data
            for col in core_columns:
                if col in display_df.columns:
                    # 特殊处理：Q11文件缺少Department/Region列
                    if col == 'Department/Region':
                        # 检查是否有Q11数据且该列不存在
                        q11_data = display_df[display_df['Question'] == 'Q11']
                        if not q11_data.empty and col not in q11_data.columns:
                            continue
                    
                    # Check if column has meaningful data (not all None/empty)
                    if not display_df[col].isna().all() and not (display_df[col] == 'None').all():
                        display_columns.append(col)
            
            # Add project name column based on question type
            for question in ['Q6', 'Q7', 'Q10', 'Q11']:
                question_data = display_df[display_df['Question'] == question]
                if not question_data.empty:
                    # 根据问题类型选择正确的project name列
                    if question == 'Q6':
                        project_col = 'Initiative/output\'s name??'
                    elif question == 'Q7':
                        project_col = 'Initiative/programme/project\'s name??'
                    elif question == 'Q10':
                        project_col = 'Course/programme/project\'s name??'
                    elif question == 'Q11':
                        project_col = 'Output/initiative/programme/project\'s name??'
                    
                    if project_col in display_df.columns and project_col not in display_columns:
                        display_columns.append(project_col)
            
            # If no meaningful columns found, show basic info
            if not display_columns:
                display_columns = ['Question', 'UserId'] if 'Question' in display_df.columns and 'UserId' in display_df.columns else list(display_df.columns)[:3]
            
            # Display data table
            if display_columns:
                # Create a unified project name column
                display_df_final = display_df[display_columns].copy()
                
                # Create unified Project Name column
                if any(col in display_df_final.columns for col in project_name_columns):
                    display_df_final['Project Name'] = ''
                    for question in ['Q6', 'Q7', 'Q10', 'Q11']:
                        question_mask = display_df_final['Question'] == question
                        if question_mask.any():
                            if question == 'Q6' and 'Initiative/output\'s name??' in display_df_final.columns:
                                display_df_final.loc[question_mask, 'Project Name'] = display_df_final.loc[question_mask, 'Initiative/output\'s name??']
                            elif question == 'Q7' and 'Initiative/programme/project\'s name??' in display_df_final.columns:
                                display_df_final.loc[question_mask, 'Project Name'] = display_df_final.loc[question_mask, 'Initiative/programme/project\'s name??']
                            elif question == 'Q10' and 'Course/programme/project\'s name??' in display_df_final.columns:
                                display_df_final.loc[question_mask, 'Project Name'] = display_df_final.loc[question_mask, 'Course/programme/project\'s name??']
                            elif question == 'Q11' and 'Output/initiative/programme/project\'s name??' in display_df_final.columns:
                                display_df_final.loc[question_mask, 'Project Name'] = display_df_final.loc[question_mask, 'Output/initiative/programme/project\'s name??']
                    
                    # Remove original project name columns
                    for col in project_name_columns:
                        if col in display_df_final.columns:
                            display_df_final = display_df_final.drop(columns=[col])
                
                st.dataframe(display_df_final, use_container_width=True)
                
                # Compact pagination controls
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Single row with all controls - more compact layout
                col1, col2, col3, col4, col5 = st.columns([1.5, 2.5, 2, 2, 1])
                
                with col1:
                    # Items per page - more compact
                    new_items_per_page = st.selectbox(
                        "Per page:",
                        options=[10, 25, 50, 100, 200],
                        index=[10, 25, 50, 100, 200].index(items_per_page) if items_per_page in [10, 25, 50, 100, 200] else 2,
                        key="items_per_page",
                        label_visibility="collapsed"
                    )
                    st.caption("Items per page")
                    
                    # Update session state and recalculate if items per page changed
                    if new_items_per_page != items_per_page:
                        st.session_state.items_per_page = new_items_per_page
                        # Reset to first page when changing items per page
                        st.session_state.outputs_current_page = 1
                        st.rerun()
                
                with col2:
                    # Navigation buttons - more compact
                    nav_col1, nav_col2, nav_col3, nav_col4 = st.columns([1, 1, 1, 1])
                    
                    with nav_col1:
                        if st.button("⏮️", disabled=(st.session_state.outputs_current_page == 1), help="First page"):
                            st.session_state.outputs_current_page = 1
                            st.rerun()
                    
                    with nav_col2:
                        if st.button("◀️", disabled=(st.session_state.outputs_current_page == 1), help="Previous page"):
                            st.session_state.outputs_current_page = max(1, st.session_state.outputs_current_page - 1)
                            st.rerun()
                    
                    with nav_col3:
                        if st.button("▶️", disabled=(st.session_state.outputs_current_page == total_pages), help="Next page"):
                            st.session_state.outputs_current_page = min(total_pages, st.session_state.outputs_current_page + 1)
                            st.rerun()
                    
                    with nav_col4:
                        if st.button("⏭️", disabled=(st.session_state.outputs_current_page == total_pages), help="Last page"):
                            st.session_state.outputs_current_page = total_pages
                            st.rerun()
                
                with col3:
                    # Current page info - compact text
                    st.markdown(f"**Page:** {st.session_state.outputs_current_page} / {total_pages}")
                
                with col4:
                    # Records info - compact text
                    st.markdown(f"**Records:** {start_idx + 1}-{end_idx} of {total_records}")
                
                with col5:
                    # Empty column for balance
                    st.write("")
                        
            else:
                st.dataframe(display_df, use_container_width=True)
        else:
            st.info("No works detail data available.")
    else:
        st.info("No works detail list available.")


if __name__ == "__main__":
    create_layout()