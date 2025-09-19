#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Q6Q7Q10Q11 Survey Analysis Results Display Module

This module is responsible for displaying analysis results of Q6, Q7, Q10, Q11 questions, including:
- CPO/GLO code distribution analysis
- Outputs count statistical analysis
- Frequency analysis results
- Outputs name list display


"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html, Input, Output, dash_table
import dash
from typing import Dict, Any, List
import os
from styles import style_manager

class Q6Q7Q10Q11DataProcessor:
    """Q6Q7Q10Q11 Data Processor - responsible for loading and preprocessing analyzed data"""
    
    def __init__(self, base_path: str = None):
        """
        Initialize data processor
        
        Args:
            base_path: Base path for data files, defaults to current directory
        """
        self.base_path = base_path or os.path.dirname(os.path.abspath(__file__))
        self.cpo_glo_data = None
        self.works_count_data = None
        self.frequency_data = None
        self.works_list_data = None
        self.special_fields_data = None
        self._load_all_data()
    
    def _load_all_data(self):
        """Load all data files"""
        try:
            # Load CPO/GLO code analysis results (use current available files)
            cpo_glo_path = os.path.join(self.base_path, 'result/q6q7q10q11_cpo_glo_analysis_results.csv')
            if os.path.exists(cpo_glo_path):
                self.cpo_glo_data = pd.read_csv(cpo_glo_path, encoding='utf-8')
            else:
                # Try with Q9 included version if available
                q9_cpo_glo_path = os.path.join(self.base_path, 'result/q6q7q9q10q11_cpo_glo_analysis_results.csv')
                if os.path.exists(q9_cpo_glo_path):
                    self.cpo_glo_data = pd.read_csv(q9_cpo_glo_path, encoding='utf-8')
                else:
                    self.cpo_glo_data = pd.DataFrame()
            
            # Load works count analysis results (use current available files)
            works_count_path = os.path.join(self.base_path, 'result/q6q7q10q11_works_count_analysis_results.csv')
            if os.path.exists(works_count_path):
                self.works_count_data = pd.read_csv(works_count_path, encoding='utf-8')
            else:
                # Try with Q9 included version if available
                q9_works_count_path = os.path.join(self.base_path, 'result/q6q7q9q10q11_works_count_analysis_results.csv')
                if os.path.exists(q9_works_count_path):
                    self.works_count_data = pd.read_csv(q9_works_count_path, encoding='utf-8')
                else:
                    self.works_count_data = pd.DataFrame()
            
            # Load frequency analysis results (use current available files)
            frequency_path = os.path.join(self.base_path, 'result/q6q7q10q11_frequency_analysis_results.csv')
            if os.path.exists(frequency_path):
                self.frequency_data = pd.read_csv(frequency_path, encoding='utf-8')
            else:
                # Try with Q9 included version if available
                q9_frequency_path = os.path.join(self.base_path, 'result/q6q7q9q10q11_frequency_analysis_results.csv')
                if os.path.exists(q9_frequency_path):
                    self.frequency_data = pd.read_csv(q9_frequency_path, encoding='utf-8')
                else:
                    self.frequency_data = pd.DataFrame()
            
            # Load works name list (use current available files)
            works_list_path = os.path.join(self.base_path, 'result/q6q7q10q11_works_list.csv')
            if os.path.exists(works_list_path):
                self.works_list_data = pd.read_csv(works_list_path, encoding='utf-8')
            else:
                # Try with Q9 included version if available
                q9_works_list_path = os.path.join(self.base_path, 'result/q6q7q9q10q11_works_list.csv')
                if os.path.exists(q9_works_list_path):
                    self.works_list_data = pd.read_csv(q9_works_list_path, encoding='utf-8')
                else:
                    self.works_list_data = pd.DataFrame()
            
            # Load special fields analysis results (use current available files)
            special_fields_path = os.path.join(self.base_path, 'result/q6q7q10q11_special_fields_analysis_results.csv')
            if os.path.exists(special_fields_path):
                self.special_fields_data = pd.read_csv(special_fields_path, encoding='utf-8')
            else:
                # Try with Q9 included version if available
                q9_special_fields_path = os.path.join(self.base_path, 'result/q6q7q9q10q11_special_fields_analysis_results.csv')
                if os.path.exists(q9_special_fields_path):
                    self.special_fields_data = pd.read_csv(q9_special_fields_path, encoding='utf-8')
                else:
                    self.special_fields_data = pd.DataFrame()
            
            # Count loaded data information
            loaded_files = []
            if not self.cpo_glo_data.empty:
                loaded_files.append(f"CPO/GLO analysis ({len(self.cpo_glo_data)} records)")
            if not self.works_count_data.empty:
                loaded_files.append(f"Works count statistics ({len(self.works_count_data)} questions)")
            if not self.frequency_data.empty:
                loaded_files.append(f"Frequency analysis ({len(self.frequency_data)} records)")
            if not self.works_list_data.empty:
                unique_regions = self.works_list_data['Department/Region'].nunique() if 'Department/Region' in self.works_list_data.columns else 0
                loaded_files.append(f"Works list ({len(self.works_list_data)} works, {unique_regions} regions)")
            if not self.special_fields_data.empty:
                loaded_files.append(f"Special fields analysis ({len(self.special_fields_data)} records)")
            
            print(f"✓ Q6Q7Q10Q11 module data loading completed: {', '.join(loaded_files)}")
            
        except Exception as e:
            print(f"Data loading error: {e}")
            # Create empty DataFrames as backup
            self.cpo_glo_data = pd.DataFrame()
            self.works_count_data = pd.DataFrame()
            self.frequency_data = pd.DataFrame()
            self.works_list_data = pd.DataFrame()
            self.special_fields_data = pd.DataFrame()
    
    def get_summary_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get summary statistics data"""
        try:
            # Q9 removed, so it's 4 questions: Q6, Q7, Q10, Q11
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
            print(f"Get summary statistics error: {e}")
            return {
                "stat1": {"value": "N/A", "label": "Questions Analyzed"},
                "stat2": {"value": "N/A", "label": "Participants"},
                "stat3": {"value": "N/A", "label": "Avg Projects/Question"},
                "stat4": {"value": "N/A", "label": "Avg Outputs/Participant"}
            }
    
    def get_cpo_glo_distribution(self, question: str) -> Dict[str, int]:
        """Get CPO/GLO code distribution for specified question"""
        try:
            if self.cpo_glo_data.empty:
                return {}
            
            question_data = self.cpo_glo_data[self.cpo_glo_data['Question'] == question]
            if question_data.empty:
                return {}
            
            # Take top 10 most frequent codes
            top_data = question_data.head(10)
            result = {}
            for _, row in top_data.iterrows():
                code = str(row['CPO/GLO Code'])[:50]  # Limit length
                frequency = int(row['Frequency'])
                result[code] = frequency
            
            return result
        except Exception as e:
            print(f"Get CPO/GLO distribution error: {e}")
            return {}
    
    def get_works_count_data(self) -> Dict[str, Dict[str, Any]]:
        """Get works count statistics data"""
        try:
            if self.works_count_data.empty:
                return {}
            
            result = {}
            for _, row in self.works_count_data.iterrows():
                question = row['Question']
                participants = row['Users with Related Works']
                total_works = row['Total Works Count']
                avg_works = row['Average Works Count']
                
                result[question] = {
                    'Participants': int(participants),
                    'Total Works': int(total_works),
                    'Average Works': float(avg_works)
                }
            
            return result
        except Exception as e:
            print(f"Get works count data error: {e}")
            return {}
    
    def get_frequency_data(self, question: str, variable: str = None) -> Dict[str, int]:
        """Get frequency analysis data for specified question"""
        try:
            if self.frequency_data.empty:
                return {}
            
            question_data = self.frequency_data[self.frequency_data['Question'] == question]
            if question_data.empty:
                return {}
            
            # If variable is specified, filter further
            if variable:
                question_data = question_data[question_data['Variable Name'] == variable]
            
            result = {}
            for _, row in question_data.iterrows():
                value = str(row['Variable Value'])[:80]  # Increase length limit to display complete labels
                frequency = int(row['Frequency'])
                result[value] = frequency
            
            return result
        except Exception as e:
            print(f"Get frequency data error: {e}")
            return {}
    
    def get_works_list(self, question: str = None) -> List[Dict[str, str]]:
        """Get works list data with deduplication and region information"""
        try:
            if self.works_list_data.empty:
                return []
            
            data = self.works_list_data
            if question:
                data = data[data['Question'] == question]
            
            # Remove duplicates based on all columns
            data_deduplicated = data.drop_duplicates()
            
            result = []
            for _, row in data_deduplicated.iterrows():
                result.append({
                    'Question': row['Question'],
                    'User ID': row['User ID'],
                    'Department/Region': row.get('Department/Region', 'N/A'),
                    'Work Name': row['Work Name']
                })
            
            return result
        except Exception as e:
            print(f"Get works list error: {e}")
            return []
    
    def get_department_distribution(self) -> Dict[str, int]:
        """Get department/region distribution data"""
        try:
            if self.works_list_data.empty or 'Department/Region' not in self.works_list_data.columns:
                return {}
            
            # Count works by department/region
            dept_counts = self.works_list_data['Department/Region'].value_counts().to_dict()
            return dept_counts
        except Exception as e:
            print(f"Get department distribution error: {e}")
            return {}
    
    def get_frequency_variables(self, question: str) -> List[str]:
        """Get all variable names for specified question"""
        try:
            if self.frequency_data.empty:
                return []
            
            question_data = self.frequency_data[self.frequency_data['Question'] == question]
            variables = question_data['Variable Name'].unique().tolist()
            return variables
        except Exception as e:
            print(f"Get variable names error: {e}")
            return []
    
    def get_special_fields_data(self, question: str, variable: str = None) -> Dict[str, int]:
        """Get special fields analysis data for specified question and variable"""
        try:
            if self.special_fields_data.empty:
                return {}
            
            question_data = self.special_fields_data[self.special_fields_data['Question'] == question]
            if question_data.empty:
                return {}
            
            # If variable is specified, filter further
            if variable:
                question_data = question_data[question_data['Variable Name'] == variable]
            
            result = {}
            for _, row in question_data.iterrows():
                value = str(row['Variable Value'])[:80]  # Increase length limit to display complete labels
                frequency = int(row['Frequency'])
                result[value] = frequency
            
            return result
        except Exception as e:
            print(f"Get special fields data error: {e}")
            return {}
    
    def get_special_fields_variables(self, question: str) -> List[str]:
        """Get all special field variable names for specified question"""
        try:
            if self.special_fields_data.empty:
                return []
            
            question_data = self.special_fields_data[self.special_fields_data['Question'] == question]
            variables = question_data['Variable Name'].unique().tolist()
            return variables
        except Exception as e:
            print(f"Get special field variables error: {e}")
            return []
    
    def get_special_fields_data_from_filtered(self, filtered_data: pd.DataFrame, question: str, variable: str) -> Dict[str, int]:
        """Get special fields analysis data from filtered data for specified question and variable"""
        try:
            if filtered_data.empty or self.special_fields_data.empty:
                return {}
            
            # Get user IDs from filtered data for the specific question
            question_col = 'Question' if 'Question' in filtered_data.columns else 'Question'
            user_id_col = 'User ID' if 'User ID' in filtered_data.columns else 'User ID'
            question_users = filtered_data[filtered_data[question_col] == question][user_id_col].unique()
            if len(question_users) == 0:
                return {}
            
            # Filter special fields data for the question and variable
            special_data = self.special_fields_data[
                (self.special_fields_data['Question'] == question) & 
                (self.special_fields_data['Variable Name'] == variable)
            ]
            
            if special_data.empty:
                return {}
            
            # Calculate ratio based on filtered users vs total users for this question
            works_question_col = 'Question' if 'Question' in self.works_list_data.columns else 'Question'
            works_user_id_col = 'User ID' if 'User ID' in self.works_list_data.columns else 'User ID'
            total_users = len(self.works_list_data[self.works_list_data[works_question_col] == question][works_user_id_col].unique())
            filtered_users_count = len(question_users)
            ratio = filtered_users_count / total_users if total_users > 0 else 0
            
            # Apply ratio to frequency data
            result = {}
            for _, row in special_data.iterrows():
                value = str(row['Variable Value'])
                original_freq = int(row['Frequency'])
                adjusted_freq = max(1, int(original_freq * ratio))  # Ensure at least 1 if original > 0
                
                if value.strip() and adjusted_freq > 0:
                    result[value] = adjusted_freq
            
            return result
            
        except Exception as e:
            print(f"Error getting special fields data from filtered data: {e}")
            return {}
    
    def refresh_data(self):
        """Refresh data - reload all data files"""
        self._load_all_data()
    
    @property
    def original_data(self):
        """Return original data (for compatibility)"""
        return self.works_list_data
    
    def _process_data(self, filtered_data):
        """Process filtered data - support region filtering"""
        if filtered_data is None or filtered_data.empty:
            return self.works_list_data.copy() if not self.works_list_data.empty else pd.DataFrame()
        
        # Return filtered data
        return filtered_data.copy()
    
    def get_frequency_data_from_filtered(self, filtered_data: pd.DataFrame, question: str, variable: str = None) -> Dict[str, int]:
        """Get frequency analysis data based on filtered data"""
        try:
            if filtered_data.empty or self.frequency_data.empty:
                return {}
            
            # Get user ID list for this question in filtered data
            question_col = 'Question' if 'Question' in filtered_data.columns else 'Question'
            user_id_col = 'User ID' if 'User ID' in filtered_data.columns else 'User ID'
            question_users = filtered_data[filtered_data[question_col] == question][user_id_col].unique()
            if len(question_users) == 0:
                return {}
            
            # For Q7 Country or Region, we need to recalculate based on filtered works_list_data
            if question == 'Q7' and variable == 'Country or Region':
                # Filter works_list_data by the filtered user IDs
                filtered_works = self.works_list_data[
                    (self.works_list_data['Question'] == question) & 
                    (self.works_list_data['User ID'].isin(question_users))
                ]
                
                if filtered_works.empty:
                    return {}
                
                # Get the region mapping from Department/Region to standardized region names
                region_mapping = {
                    'Region: Asia and the Pacific': 'Asia and the Pacific',
                    'Region: Africa': 'Africa', 
                    'Region: Arab States': 'Arab States',
                    'Region: Americas': 'Americas',
                    'Region: Europe and Central Asia': 'Europe and Central Asia'
                }
                
                # Count occurrences by region
                region_counts = {}
                for _, row in filtered_works.iterrows():
                    dept_region = row.get('Department/Region', '')
                    # Map department/region to standardized region name
                    region = region_mapping.get(dept_region, dept_region)
                    if region and region != '':
                        region_counts[region] = region_counts.get(region, 0) + 1
                
                return region_counts
            
            # For other cases, use the original logic but properly filter by user IDs
            question_data = self.frequency_data[self.frequency_data['Question'] == question]
            if question_data.empty:
                return {}
            
            # If variable is specified, filter further
            if variable:
                question_data = question_data[question_data['Variable Name'] == variable]
            
            # Adjust frequency based on filtered user count (simplified processing)
            works_question_col = 'Question'
            works_user_id_col = 'User ID'
            total_users_original = len(self.works_list_data[self.works_list_data[works_question_col] == question][works_user_id_col].unique())
            filtered_users_count = len(question_users)
            ratio = filtered_users_count / total_users_original if total_users_original > 0 else 0
            
            result = {}
            for _, row in question_data.iterrows():
                value = str(row['Variable Value'])[:80]   
                frequency = int(row['Frequency'] * ratio)  # Adjust frequency by ratio
                if frequency > 0:  # Only keep items with frequency > 0
                    result[value] = frequency
            
            return result
        except Exception as e:
            print(f"Get filtered frequency data error: {e}")
            return {}

class Q6Q7Q10Q11ComponentFactory:
    """Q6Q7Q10Q11 Component Factory - responsible for creating various UI components"""
    
    def __init__(self, style_manager):
        self.style_manager = style_manager
    
    def create_summary_card(self, icon: str, value: str, title: str, 
                           subtitle: str, footer: str, color: str) -> html.Div:
        """Create summary statistics card"""
        # Get base card style
        base_style = self.style_manager.get_style('card_style')
        
        # Define color-related styles
        color_style = {
            'border': f'2px solid {color}20'
        }
        
        # Merge styles
        card_style = {**base_style, **color_style}
        
        return html.Div([
            html.Div([
                html.I(className=icon, style={
                    'fontSize': '2.5em',
                    'color': color,
                    'marginBottom': '10px'
                }),
                html.H2(value, style={
                    'margin': '0',
                    'color': '#2c3e50',
                    'fontSize': '2.2em',
                    'fontWeight': 'bold'
                }),
                html.P(title, style={
                    'margin': '5px 0',
                    'color': '#34495e',
                    'fontSize': '1.1em',
                    'fontWeight': '600'
                }),
                html.P(subtitle, style={
                    'margin': '0',
                    'color': '#7f8c8d',
                    'fontSize': '0.9em'
                }),
                html.Hr(style={'margin': '10px 0', 'border': f'1px solid {color}'}),
                html.P(footer, style={
                    'margin': '0',
                    'color': color,
                    'fontSize': '0.8em',
                    'fontWeight': '500'
                })
            ], style=card_style)
        ], style={
            'width': '22%',
            'display': 'inline-block',
            'margin': '0 1.5%',
            'verticalAlign': 'top'
        })
    
    def create_chart_container(self, title: str, chart_component, description: str = "") -> html.Div:
        """Create chart container"""
        # Get base container style
        base_style = self.style_manager.get_style('container_style')
        
        # 定义默认样式
        default_style = {
            'marginBottom': '30px'
        }
        
        # 合并样式
        container_style = {**base_style, **default_style}
        
        return html.Div([
            html.H3(title, style={
                'textAlign': 'center',
                'color': '#2c3e50',
                'marginBottom': '10px',
                'fontSize': '1.2em',
                'whiteSpace': 'nowrap',  # 强制单行显示
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
                'lineHeight': '1.3'
            }) if title else None,
            html.P(description, style={
                'textAlign': 'center',
                'color': '#7f8c8d',
                'marginBottom': '20px',
                'fontSize': '0.9em'
            }) if description else None,
            html.Div(chart_component, style={'textAlign': 'center'})
        ], style=container_style)
    
    def create_works_table(self, works_data: List[Dict[str, str]], table_id: str) -> html.Div:
        """Create works detail table with region information"""
        if not works_data:
            return html.Div("No works data available", style={'textAlign': 'center', 'padding': '20px', 'color': '#7f8c8d'})
        
        # Use standard English column names
        english_data = []
        for item in works_data:
            english_data.append({
                'Question': item.get('Question', ''),
                'User ID': item.get('User ID', ''),
                'Region': item.get('Department/Region', 'N/A'),
                'Work Title': item.get('Work Name', '')
            })
        
        return dash_table.DataTable(
            id=table_id,
            columns=[
                {"name": "Question", "id": "Question", "type": "text"},
                {"name": "User ID", "id": "User ID", "type": "text"},
                {"name": "Department/Region", "id": "Region", "type": "text"},
                {"name": "Work Title", "id": "Work Title", "type": "text"}
            ],
            data=english_data,
            filter_action="native",
            sort_action="native",
            page_action="native",
            page_current=0,
            page_size=25,
            style_cell={
                'textAlign': 'left',
                'padding': '12px',
                'fontFamily': 'Arial, sans-serif',
                'fontSize': '14px',
                'border': '1px solid #ddd',
                'whiteSpace': 'normal',
                'height': 'auto',
                'maxWidth': '300px',
                'overflow': 'hidden',
                'text-overflow': 'ellipsis'
            },
            style_cell_conditional=[
                {
                    'if': {'column_id': 'Question'},
                    'width': '12%',
                    'textAlign': 'center'
                },
                {
                    'if': {'column_id': 'User ID'},
                    'width': '15%',
                    'textAlign': 'center'
                },
                {
                    'if': {'column_id': 'Region'},
                    'width': '18%',
                    'textAlign': 'center'
                },
                {
                    'if': {'column_id': 'Work Title'},
                    'width': '55%'
                }
            ],
            style_header={
                'backgroundColor': '#3498db',
                'color': 'white',
                'fontWeight': 'bold',
                'textAlign': 'center'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': '#f8f9fa'
                },
                {
                    'if': {'row_index': 'even'},
                    'backgroundColor': '#ffffff'
                }
            ],
            tooltip_data=[
                {
                    'Work Title': {'value': str(row['Work Title']), 'type': 'markdown'},
                    'Region': {'value': str(row['Region']), 'type': 'markdown'}
                } for row in english_data
            ],
            tooltip_duration=None
        )

class Q6Q7Q10Q11Dashboard:
    """Q6Q7Q10Q11 Main Dashboard Class - Integrates all functional modules"""
    
    def __init__(self, data_path: str = None):
        """
        Initialize dashboard
        
        Args:
            data_path: Data file path, defaults to current directory
        """
        self.data_processor = Q6Q7Q10Q11DataProcessor(data_path)
        self.style_manager = style_manager
        self.component_factory = Q6Q7Q10Q11ComponentFactory(style_manager)
        self.questions = ['Q6', 'Q7', 'Q10', 'Q11']  # Q9 removed from question list
    
    def create_summary_cards(self) -> html.Div:
        """Create summary statistics card area - 只显示 Participants with Outputs 卡片"""
        stats = self.data_processor.get_summary_stats()
        
        # 创建带有ID的卡片容器，以便回调函数更新
        return html.Div(id='summary-cards-container', style={
            'textAlign': 'center', 
            'marginBottom': '30px', 
            'width': '100%',
            'maxWidth': '1200px',
            'margin': '0 auto'
        })
    
    def create_cpo_glo_charts(self) -> html.Div:
        """Create CPO/GLO code distribution charts"""
        charts = []
        
        for question in self.questions:
            data = self.data_processor.get_cpo_glo_distribution(question)
            
            if data:
                fig = self.style_manager.create_standardized_chart(
                    data=data,
                    chart_type='horizontal_bar',
                    title=f'{question} CPO/GLO Code Distribution'
                )
            else:
                fig = go.Figure()
                fig.add_annotation(
                    text="No Data Available",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5, xanchor='center', yanchor='middle',
                    showarrow=False, font_size=14
                )
                # Remove direct title setting to avoid conflicts with standardized chart creation in styles.py
                # fig.update_layout(title=f'{question} CPO/GLO Code Distribution')
            
            chart_container = self.component_factory.create_chart_container(
                title=self.style_manager._wrap_title(f"{question} CPO/GLO Code Distribution", max_length=60),
                chart_component=dcc.Graph(figure=fig, id=f'cpo-glo-chart-{question.lower()}')
            )
            
            # Vertical layout
            charts.append(chart_container)
        
        return html.Div(charts, style={
            'textAlign': 'center',
            'maxWidth': '1200px',
            'margin': '0 auto'
        })
    
    def create_q9_project_names_list(self) -> html.Div:
        """Create Q9 project names list display"""
        q9_data = self.data_processor.get_special_fields_data('Q9', "Initiative/programme/project's name")
        if q9_data:
            # Create list display for Q9 project names
            project_names = list(q9_data.keys())
            list_items = [html.Li(name, style={'margin': '8px 0', 'fontSize': '14px'}) for name in project_names]
            
            q9_list_component = html.Div([
                html.Ol(list_items, style={
                    'textAlign': 'left',
                    'maxWidth': '800px',
                    'margin': '0 auto',
                    'padding': '20px',
                    'backgroundColor': '#f8f9fa',
                    'borderRadius': '8px',
                    'border': '1px solid #dee2e6'
                })
            ], style={'textAlign': 'center'})
            
            chart_container = self.component_factory.create_chart_container(
                title="",
                chart_component=q9_list_component
            )
            return chart_container
        return html.Div()
    
    def create_q11_geographical_charts(self) -> html.Div:
        """Create Q11 geographical analysis charts"""
        charts = []
        
        # Q11 Geographical focus
        q11_geo_data = self.data_processor.get_special_fields_data('Q11', 'Geographical focus (Global, Regional or National/local)')
        if q11_geo_data:
            # Determine chart type based on number of items
            chart_type = 'bar' if len(q11_geo_data) >= 5 else 'pie'
            fig = self.style_manager.create_standardized_chart(
                data=q11_geo_data,
                chart_type=chart_type,
                title="Geographical Focus Of Advocacy And Partnerships Outputs"
            )
            
            chart_container = self.component_factory.create_chart_container(
                title=self.style_manager._wrap_title("Geographical Focus Of Advocacy And Partnerships Outputs", max_length=60),
                chart_component=dcc.Graph(figure=fig, id='special-q11-geo-chart')
            )
            charts.append(chart_container)
        
        # Q11 Region/country names - Bar chart (standardized)
        q11_region_data = self.data_processor.get_special_fields_data('Q11', 'Specify name of the Region/country')
        if q11_region_data:
            # Use standardized chart creation method like other charts with 5+ items
            fig = self.style_manager.create_standardized_chart(
                data=q11_region_data,
                chart_type='bar',
                title="Advocacy & Partnership Outputs Across Regions"
            )
            
            chart_container = self.component_factory.create_chart_container(
                title=self.style_manager._wrap_title("Advocacy & Partnership Outputs Across Regions", max_length=60),
                chart_component=dcc.Graph(figure=fig, id='special-q11-region-chart')
            )
            charts.append(chart_container)
        
        return html.Div(charts, style={
            'textAlign': 'center',
            'maxWidth': '1200px',
            'margin': '0 auto'
        })
    
    def create_works_count_chart(self) -> html.Div:
        """Create works count statistics chart"""
        works_data = self.data_processor.get_works_count_data()
        
        if not works_data:
            fig = go.Figure()
            fig.add_annotation(
                text="No Data Available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False, font_size=14
            )
            # fig.update_layout(title='Works Count Statistics')
        else:
            # Filter out Q9 data, only keep Q6, Q7, Q10, Q11
            filtered_questions = [q for q in works_data.keys() if q in ['Q6', 'Q7', 'Q10', 'Q11']]
            
            # Create display labels mapping with line breaks for better display
            question_labels = {
                'Q6': 'Knowledge development<br>& dissemination',
                'Q7': 'Technical<br>Assistance',
                'Q10': 'Capacity<br>building',
                'Q11': 'Advocacy &<br>Partnerships'
            }
            
            questions = filtered_questions
            question_display_labels = [question_labels.get(q, q) for q in questions]
            participants = [works_data[q]['Participants'] for q in questions]
            total_works = [works_data[q]['Total Works'] for q in questions]
            
            # Use style manager's color configuration to create grouped bar chart
            colors = self.style_manager.get_chart_colors()[:2]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='Number of staff reporting',
                x=question_display_labels,
                y=participants,
                marker_color=colors[0],
                hovertemplate='<b>%{x}</b><br>Number of staff reporting: %{y}<extra></extra>',
                hoverlabel=dict(bgcolor='rgba(255,255,255,0.9)', bordercolor='rgba(0,0,0,0.2)', font_color='black'),
                showlegend=False
            ))
            fig.add_trace(go.Bar(
                name='Number of outputs delivered',
                x=question_display_labels,
                y=total_works,
                marker_color=colors[1],
                hovertemplate='<b>%{x}</b><br>Number of outputs delivered: %{y}<extra></extra>',
                hoverlabel=dict(bgcolor='rgba(255,255,255,0.9)', bordercolor='rgba(0,0,0,0.2)', font_color='black'),
                showlegend=False
            ))
            
            # Apply style manager's layout configuration
            layout_config = self.style_manager.get_global_chart_config('layout')
            # 移除直接的标题设置，避免与 styles.py 中的标准化图表创建冲突
            fig.update_layout(
                xaxis_title='Question',
                yaxis_title='Count',
                barmode='group',
                showlegend=False,
                **layout_config
            )
            
            # 移除全局悬停模板更新，保持每个柱状图的独立悬停设置
        
        chart_container = self.component_factory.create_chart_container(
            title="Outputs Count Statistics",
            chart_component=dcc.Graph(figure=fig, id='works-count-chart')
        )
        
        return html.Div(chart_container, style={'textAlign': 'center', 'width': '100%'})
    
    def create_frequency_charts(self) -> html.Div:
        """Create frequency analysis charts with special fields integrated"""
        charts = []
        
        for question in self.questions:
            # Get all variables for this question
            variables = self.data_processor.get_frequency_variables(question)
            
            if variables:
                # Create chart for each variable
                for variable in variables:
                    # Skip Q7-DC chart if applicable
                    if question == 'Q7' and variable == 'DC code if applicable':
                        continue  # Comment out Q7-DC chart
                    
                    # Skip Q7 - Is it part of a UN Joint Programme (Yes or No)
                    if question == 'Q7' and 'UN Joint Programme' in variable:
                        continue
                    
                    # Skip Q9-DC chart if applicable
                    if question == 'Q9' and variable == 'DC code if applicable':
                        continue  # Comment out Q9-DC chart
                    
                    # Skip Q10 - New or long-standing
                    if question == 'Q10' and 'New or long-standing' in variable:
                        continue
                    
                    # Skip Q10 - For public use or ILO staff only
                    if question == 'Q10' and ('public use' in variable or 'ILO staff' in variable):
                        continue
                    
                    # Skip Q7 - New or long-standing
                    if question == 'Q7' and 'New or long-standing' in variable:
                        continue
                    
                    # Skip Q11 - New or long-standing
                    if question == 'Q11' and 'New or long-standing' in variable:
                        continue
                    
                    # Skip Q6 - Flagship or periodic
                    if question == 'Q6' and 'Flagship or periodic' in variable:
                        continue
                    
                    # Skip Q6 - New or Produced regularly
                    if question == 'Q6' and 'New or Produced regularly' in variable:
                        continue
                    
                    data = self.data_processor.get_frequency_data(question, variable)
                    
                    if data:
                        # Take top 10 most frequent values
                        sorted_data = dict(sorted(data.items(), key=lambda x: x[1], reverse=True)[:10])
                        
                        # Create custom title mapping for specific Q6, Q7, Q10 and Q11 charts
                        title_mapping = {
                            'Q6 Funding source (Options: regular budget or extrabudgetary)': 'Funding Source Of Knowledge Development And Dissemination Outputs In 2024',
        'Q6 Focus (Options: Youth only or Youth is one of the target groups)': 'Target Group Of Knowledge Development And Dissemination Outputs In 2024',
        'Q6 Type of publication (Options: Evaluation, or Guidance/tools, or Technical Report, or Working paper, or Data/Database)': 'Types Of Knowledge Development And Dissemination Outputs Delivered In 2024',
        'Q7 Funding source (Options: regular budget or extrabudgetary)': 'Funding Source Of Technical Assistance Outputs In 2024',
        'Q7 Focus \n(Options: Youth only or Youth is one of the target groups)': 'Target Group Of Technical Assistance Outputs In 2024',
        'Q7 Country or Region': 'Technical Assistance Outputs Across Regions',
                            'Q10 In person or online or both': 'Delivery Mode Of Capacity Development Outputs In 2024',
        'Q10 With certification (Yes or No)': 'Capacity Development Outputs & Certification',
        'Q10 Funding source (Options: regular budget or extrabudgetary)': 'Funding Source For Capacity Development Outputs In 2024',
        'Q10 Focus (Options: Youth only or Youth is one of the target groups)': 'Target Group Of Capacity Development Outputs In 2024',
                            'Q11 Type of partnership\n(Options: UN interagency initiative; or multistakeholder initiative; or bilateral partnership; or event; or campaign; or challenge)': 'Types Of Advocacy Or Partnership Outputs In 2024',
        'Q11 Funding source (Options: regular budget or extrabudgetary)': 'Funding Source For Advocacy & Partnerships Related Outputs In 2024',
                            'Q11 Focus\n (Options: Youth only or Youth is one of the target groups)': 'Target Group For Advocacy & Partnerships Outputs In 2024'
                        }
                        
                        # Use custom title if available, otherwise use default format
                        chart_title_key = f'{question} {variable}'
                        chart_title = title_mapping.get(chart_title_key, chart_title_key)
                        container_title = title_mapping.get(chart_title_key, f"{question} - {variable}")
                        
                        # Skip creating original chart for Types Of Advocacy Or Partnership Outputs In 2024
                        # Only create custom sorted version for this specific chart
                        if chart_title != 'Types Of Advocacy Or Partnership Outputs In 2024':
                            # Determine chart type based on number of items
                            chart_type = 'bar' if len(sorted_data) >= 5 else 'pie'
                            
                            fig = self.style_manager.create_standardized_chart(
                                data=sorted_data,
                                chart_type=chart_type,
                                title=chart_title
                            )
                            
                            chart_container = self.component_factory.create_chart_container(
                                 title=self.style_manager._wrap_title(container_title, max_length=200),
                                 chart_component=dcc.Graph(figure=fig, id=f'frequency-chart-{question.lower()}-{hash(variable)}')
                             )
                            
                            # Vertical layout
                            charts.append(chart_container)
                        
                        # Add custom sorted bar chart for Types Of Advocacy Or Partnership Outputs In 2024
                        if chart_title == 'Types Of Advocacy Or Partnership Outputs In 2024':
                            # Create a new bar chart with custom ordering
                            custom_sorted_data = {}
                            custom_order_list = ['multistakeholder initiative', 'UN interagency initiative', 'bilateral partnership']
                            
                            # Add items in custom order (case-insensitive matching)
                            for item in custom_order_list:
                                # Try exact match first
                                if item in sorted_data:
                                    custom_sorted_data[item] = sorted_data[item]
                                else:
                                    # Try case-insensitive match
                                    for key in sorted_data.keys():
                                        if key.lower() == item.lower():
                                            custom_sorted_data[key] = sorted_data[key]
                                            break
                            
                            # Add remaining items sorted by value
                            remaining_items = {k: v for k, v in sorted_data.items() if k not in custom_order_list}
                            remaining_sorted = dict(sorted(remaining_items.items(), key=lambda x: x[1], reverse=True))
                            custom_sorted_data.update(remaining_sorted)
                            
                            # Create the custom bar chart
                            custom_fig = self.style_manager.create_standardized_chart(
                                data=custom_sorted_data,
                                chart_type='bar',  # Force bar chart
                                title=chart_title,  # Remove Chinese text from title
                                custom_order=None,  # Don't apply custom order again since we already sorted
                                preserve_order=True  # Add flag to preserve the order we already set
                            )
                            
                            custom_chart_container = self.component_factory.create_chart_container(
                                title=self.style_manager._wrap_title(container_title, max_length=200),  # Remove Chinese text from container title
                                chart_component=dcc.Graph(figure=custom_fig, id=f'custom-frequency-chart-{question.lower()}-{hash(variable)}')
                            )
                            
                            charts.append(custom_chart_container)
                        
                        # Add treemap for Q9 Country or Region - commented out as requested
                        # if question == 'Q9' and variable == 'Country or Region':
                        #     # Get top 20 countries/regions for treemap
                        #     sorted_treemap_data = dict(sorted(data.items(), key=lambda x: x[1], reverse=True)[:20])
                        #     
                        #     if sorted_treemap_data:
                        #         treemap_fig = go.Figure(go.Treemap(
                        #             labels=list(sorted_treemap_data.keys()),
                        #             values=list(sorted_treemap_data.values()),
                        #             parents=[""] * len(sorted_treemap_data),
                        #             textinfo="label+value",
                        #             textfont_size=12,
                        #             marker_colorscale='Viridis'
                        #         ))
                        #         
                        #         layout_config = self.style_manager.get_global_chart_config('layout')
                        #         treemap_fig.update_layout(
                        #             title=f'Q9 Country/Region Distribution (Treemap)',
                        #             **layout_config
                        #         )
                        #         
                        #         treemap_container = self.component_factory.create_chart_container(
                        #             title="Q9 - Country/Region Distribution (Treemap)",
                        #             chart_component=dcc.Graph(figure=treemap_fig, id=f'q9-country-treemap')
                        #         )
                        #         
                        #         charts.append(treemap_container)
            else:
                # If no variable data, show empty state
                fig = go.Figure()
                fig.add_annotation(
                    text="No Data Available",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5, xanchor='center', yanchor='middle',
                    showarrow=False, font_size=14
                )
                # fig.update_layout(title=f'{question} Frequency Analysis')
                
                chart_container = self.component_factory.create_chart_container(
                     title=f"{question} Frequency Analysis",
                     chart_component=dcc.Graph(figure=fig, id=f'frequency-chart-{question.lower()}')
                 )
                
                # Vertical layout
                charts.append(chart_container)
            
            # Add special fields for specific questions
            if question == 'Q9':
                # Add Q9 project names list
                q9_chart = self.create_q9_project_names_list()
                if q9_chart.children:  # Only add if there's content
                    charts.append(q9_chart)
            
            elif question == 'Q11':
                # Add Q11 geographical charts
                q11_charts = self.create_q11_geographical_charts()
                if q11_charts.children:  # Only add if there's content
                    charts.extend(q11_charts.children)
        
        return html.Div(charts, style={
            'textAlign': 'center',
            'maxWidth': '1200px',
            'margin': '0 auto'
        })
    
    def create_works_table_section(self) -> html.Div:
        """Create works detail table section"""
        works_data = self.data_processor.get_works_list()
        
        table = self.component_factory.create_works_table(works_data, 'works-detail-table')
        
        return html.Div([self.component_factory.create_chart_container(
                title="",
                chart_component=table
            )
        ], style={'margin': '0 auto', 'maxWidth': '1200px', 'textAlign': 'center', 'width': '100%'})
    
    def get_layout(self) -> html.Div:
        """Get complete dashboard layout"""
        return html.Div([
            # Back button
            html.Div([
                html.Button(
                    "← Back to Home",
                    id="btn-back-to-home",
                    style={
                        'backgroundColor': '#95a5a6',
                        'color': 'white',
                        'border': 'none',
                        'padding': '10px 20px',
                        'borderRadius': '5px',
                        'cursor': 'pointer',
                        'fontSize': '14px',
                        'marginBottom': '20px'
                    }
                )
            ], style={'textAlign': 'left'}),
            
            # Page title
            html.Div([
                html.H1(
                    "Youth employment 2024 outputs analysis",
                    style={
                        'textAlign': 'center',
                        'color': '#2c3e50',
                        'marginBottom': '10px',
                        'fontSize': '28px',
            'fontWeight': 'bold'
                    }
                )
            ], style={'textAlign': 'center'}),
            
            # Summary statistics cards
            html.Div([
                html.H2("📊 Summary Statistics", style={'color': '#2c3e50', 'marginBottom': '20px', 'textAlign': 'center'}),
                self.create_summary_cards()
            ], style={'marginBottom': '40px', 'textAlign': 'center'}),
            
            # Region filter component
            html.Div([
                html.H3("Display Options", style={
                    'color': '#2c3e50',
                    'marginBottom': '20px',
                    'textAlign': 'center'
                }),
                html.Div([
                    self.style_manager.create_region_filter_component('q6q7q10q11-region-filter')
                ], style={'maxWidth': '400px', 'margin': '0 auto', 'marginBottom': '30px'})
            ], style={'textAlign': 'center', 'marginBottom': '30px'}),
            
            # CPO/GLO code distribution charts - temporarily commented out
            # html.Div([
            #     html.H2("🏷️ CPO/GLO Code Distribution", style={'color': '#2c3e50', 'marginBottom': '20px', 'textAlign': 'center'}),
            #     self.create_cpo_glo_charts()
            # ], style={'marginBottom': '40px', 'textAlign': 'center'}),
            
            # Works count statistics
            html.Div([
                html.H2("📈 Outputs Count Statistics", style={'color': '#2c3e50', 'marginBottom': '20px', 'textAlign': 'center'}),
                self.create_works_count_chart()
            ], style={'marginBottom': '40px', 'textAlign': 'center'}),
            
            # Frequency analysis charts (with integrated special fields)
            html.Div([
                html.H2("📊 Frequency Analysis", style={'color': '#2c3e50', 'marginBottom': '20px', 'textAlign': 'center'}),
                self.create_frequency_charts()
            ], style={'marginBottom': '40px', 'textAlign': 'center'}),
            
            # Works detail table
            html.Div([
                html.H2("📋 Outputs Detail List", style={'color': '#2c3e50', 'marginBottom': '20px', 'textAlign': 'center'}),
                self.create_works_table_section()
            ], style={'marginBottom': '40px', 'textAlign': 'center'})
            
        ], style={
            'maxWidth': '1400px',
            'margin': '0 auto',
            'padding': '20px',
            'fontFamily': 'Arial, sans-serif',
            'backgroundColor': '#f8f9fa',
            'minHeight': '100vh',
            'textAlign': 'center'
        })
    
    def setup_callbacks(self, app):
        """Setup callback functions"""
        # Back to home button callback
        @app.callback(
            Output('main-url', 'pathname', allow_duplicate=True),
            [Input('btn-back-to-home', 'n_clicks')],
            prevent_initial_call=True
        )
        def navigate_back_to_home(n_clicks):
            if n_clicks:
                return '/'
            return dash.no_update
        
        # Main callback function - update all charts and components
        @app.callback(
            [Output('works-count-chart', 'figure'),
             Output('works-detail-table', 'data'),
             Output('summary-cards-container', 'children')],
            [Input('q6q7q10q11-region-filter', 'value')],
            prevent_initial_call=False
        )
        def update_charts_with_region_filter(region_filter):
            """Update works count chart, data table and summary cards based on region filter"""
            try:
                # Get original data (no need to refresh every time)
                original_data = self.data_processor.original_data
            
                # Apply region filter
                if region_filter and region_filter != 'all' and not original_data.empty:
                    if 'Department/Region' in original_data.columns:
                        filtered_data = original_data[original_data['Department/Region'] == region_filter]
                    elif '部门/区域' in original_data.columns:  # Chinese column name: Department/Region
                         filtered_data = original_data[original_data['部门/区域'] == region_filter]
                    else:
                        filtered_data = original_data
                else:
                    filtered_data = original_data
                
                # Process filtered data
                processed_data = self.data_processor._process_data(filtered_data)
                
                # Recalculate works count statistics based on filtered data
                title_suffix = f" ({region_filter})" if region_filter and region_filter != 'all' else ""
                
                # If there is region filter, recalculate statistics from filtered data
                if region_filter and region_filter != 'all' and not processed_data.empty:
                    works_data = self._calculate_works_count_from_filtered_data(processed_data)
                else:
                    # Use original data when no region filter or when processed_data is empty
                    works_data = self.data_processor.get_works_count_data()
                
                if not works_data:
                    works_fig = go.Figure()
                    works_fig.add_annotation(
                        text="No Data Available",
                        xref="paper", yref="paper",
                        x=0.5, y=0.5, xanchor='center', yanchor='middle',
                        showarrow=False, font_size=14
                    )
                    # 移除直接的标题设置，避免与 styles.py 中的标准化图表创建冲突
                    # works_fig.update_layout(title=f'Works Count Statistics{title_suffix}')
                else:
                    # Filter out Q9 data, only keep Q6, Q7, Q10, Q11
                    filtered_questions = [q for q in works_data.keys() if q in ['Q6', 'Q7', 'Q10', 'Q11']]
                    
                    # Create display labels mapping with line breaks for better display
                    question_labels = {
                        'Q6': 'Knowledge development<br>& dissemination',
                        'Q7': 'Technical<br>assistance',
                        'Q10': 'Capacity<br>building',
                        'Q11': 'Advocacy &<br>partnerships'
                    }
                    
                    questions = filtered_questions
                    question_display_labels = [question_labels.get(q, q) for q in questions]
                    participants = [works_data[q]['Participants'] for q in questions]
                    total_works = [works_data[q]['Total Works'] for q in questions]
                    
                    colors = self.style_manager.get_chart_colors()[:2]
                    works_fig = go.Figure()
                    works_fig.add_trace(go.Bar(
                        name='Number of staff reporting',
                        x=question_display_labels,
                        y=participants,
                        marker_color=colors[0],
                        hovertemplate='<b>%{x}</b><br>Number of staff reporting: %{y}<extra></extra>',
                        hoverlabel=dict(bgcolor='rgba(255,255,255,0.9)', bordercolor='rgba(0,0,0,0.2)', font_color='black')
                    ))
                    works_fig.add_trace(go.Bar(
                        name='Number of outputs delivered',
                        x=question_display_labels,
                        y=total_works,
                        marker_color=colors[1],
                        hovertemplate='<b>%{x}</b><br>Number of outputs delivered: %{y}<extra></extra>',
                        hoverlabel=dict(bgcolor='rgba(255,255,255,0.9)', bordercolor='rgba(0,0,0,0.2)', font_color='black')
                    ))
                    
                    layout_config = self.style_manager.get_global_chart_config('layout')
                    works_fig.update_layout(
                        xaxis_title='Question',
                        yaxis_title='Count',
                        barmode='group',
                        **layout_config
                    )
                
                # Update data table - based on filtered data with deduplication and region info
                if not processed_data.empty:
                    # Remove duplicates from processed data
                    processed_data_deduplicated = processed_data.drop_duplicates()
                    table_data = []
                    for _, row in processed_data_deduplicated.iterrows():
                        # Use standard English column names
                        question = row.get('Question', '')
                        user_id = row.get('User ID', '')
                        region = row.get('Department/Region', 'N/A')
                        work_title = row.get('Work Name', '')
                        
                        table_data.append({
                            'Question': question,
                            'User ID': user_id,
                            'Region': region,
                            'Work Title': work_title
                        })
                else:
                    works_list = self.data_processor.get_works_list()
                    table_data = []
                    for item in works_list:
                        table_data.append({
                            'Question': item.get('Question', ''),
                            'User ID': item.get('User ID', ''),
                            'Region': item.get('Department/Region', 'N/A'),
                            'Work Title': item.get('Work Name', '')
                        })
                
                # Update summary cards based on filtered data
                if not processed_data.empty:
                    # Calculate unique participants from filtered data
                    unique_participants = len(processed_data['User ID'].unique())
                    stats = {"stat2": {"value": str(unique_participants), "label": "Participants with Outputs"}}
                else:
                    # Use original stats when no filter applied or no filtered data
                    stats = self.data_processor.get_summary_stats()
                
                # Create summary cards
                if "stat2" in stats:
                    card = self.component_factory.create_summary_card(
                        icon="fas fa-users",
                        value=stats["stat2"]["value"],
                        title=stats["stat2"]["label"],
                        subtitle="",
                        footer="Unique contributors",
                        color="#2ecc71"
                    )
                    summary_cards = [card]
                else:
                    # 如果没有数据，显示占位符
                    summary_cards = [html.Div([
                        html.P("暂无参与者数据", style={
                            'text-align': 'center', 
                            'color': '#7f8c8d',
                            'font-size': '1.2em'
                        })
                    ])]
            
                return works_fig, table_data, summary_cards
                
            except Exception as e:
                print(f"❌ Error in Q6Q7Q10Q11 callback: {str(e)}")
                import traceback
                print(f"❌ Full traceback: {traceback.format_exc()}")
                
                # Return error figure, empty table and error summary cards
                error_fig = go.Figure()
                error_fig.add_annotation(
                    text=f"Error: {str(e)}",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5, xanchor='center', yanchor='middle',
                    showarrow=False, font_size=14, font_color="red"
                )
                # Remove direct title setting to avoid conflicts with standardized chart creation in styles.py
                # error_fig.update_layout(title='Error Loading Data')
                
                error_summary = [html.Div([
                    html.P("数据加载错误", style={
                        'text-align': 'center', 
                        'color': '#e74c3c',
                        'font-size': '1.2em'
                    })
                ])]
                
                return error_fig, [], error_summary
        
        # Create independent callback functions for each frequency analysis chart
        for question in self.questions:
            variables = self.data_processor.get_frequency_variables(question)
            if variables:
                for variable in variables:
                    chart_id = f'frequency-chart-{question.lower()}-{hash(variable)}'
                    custom_chart_id = f'custom-frequency-chart-{question.lower()}-{hash(variable)}'
                    
                    # Create closure to capture current question and variable values
                    def create_frequency_callback(q, var, chart_id):
                        @app.callback(
                            Output(chart_id, 'figure'),
                            [Input('q6q7q10q11-region-filter', 'value')],
                            prevent_initial_call=False
                        )
                        def update_frequency_chart(region_filter):
                            """Update single frequency analysis chart"""
                            title_suffix = f" ({region_filter})" if region_filter and region_filter != 'all' else ""
                            
                            # Get original data and apply region filter
                            original_data = self.data_processor.original_data
                            if region_filter and region_filter != 'all' and not original_data.empty:
                                if 'Department/Region' in original_data.columns:
                                    filtered_data = original_data[original_data['Department/Region'] == region_filter]
                                elif '部门/区域' in original_data.columns:
                                    filtered_data = original_data[original_data['部门/区域'] == region_filter]
                                else:
                                    filtered_data = original_data
                            else:
                                filtered_data = original_data
                            
                            # Use filtered data to get frequency analysis
                            if not filtered_data.empty:
                                data = self.data_processor.get_frequency_data_from_filtered(filtered_data, q, var)
                            else:
                                data = self.data_processor.get_frequency_data(q, var)
                            
                            if data:
                                sorted_data = dict(sorted(data.items(), key=lambda x: x[1], reverse=True)[:10])
                                # Determine chart type based on number of items
                                chart_type = 'bar' if len(sorted_data) >= 5 else 'pie'
                                fig = self.style_manager.create_standardized_chart(
                                    data=sorted_data,
                                    chart_type=chart_type,
                                    title=f'{q} {var[:50]}{title_suffix}'
                                )
                            else:
                                fig = go.Figure()
                                fig.add_annotation(
                                    text="No Data Available",
                                    xref="paper", yref="paper",
                                    x=0.5, y=0.5, xanchor='center', yanchor='middle',
                                    showarrow=False, font_size=14
                                )
                                # Remove direct title setting to avoid conflicts with standardized chart creation in styles.py
                                # fig.update_layout(title=f'{q} {var}{title_suffix}')
                            
                            return fig
                        
                        return update_frequency_chart
                    
                    # Create closure for custom frequency chart (Types Of Advocacy Or Partnership Outputs In 2024)
                    def create_custom_frequency_callback(q, var, custom_chart_id):
                        @app.callback(
                            Output(custom_chart_id, 'figure'),
                            [Input('q6q7q10q11-region-filter', 'value')],
                            prevent_initial_call=False
                        )
                        def update_custom_frequency_chart(region_filter):
                            """Update custom frequency analysis chart with special ordering"""
                            title_suffix = f" ({region_filter})" if region_filter and region_filter != 'all' else ""
                            
                            # Get original data and apply region filter
                            original_data = self.data_processor.original_data
                            if region_filter and region_filter != 'all' and not original_data.empty:
                                if 'Department/Region' in original_data.columns:
                                    filtered_data = original_data[original_data['Department/Region'] == region_filter]
                                elif '部门/区域' in original_data.columns:
                                    filtered_data = original_data[original_data['部门/区域'] == region_filter]
                                else:
                                    filtered_data = original_data
                            else:
                                filtered_data = original_data
                            
                            # Use filtered data to get frequency analysis
                            if not filtered_data.empty:
                                data = self.data_processor.get_frequency_data_from_filtered(filtered_data, q, var)
                            else:
                                data = self.data_processor.get_frequency_data(q, var)
                            
                            if data:
                                sorted_data = dict(sorted(data.items(), key=lambda x: x[1], reverse=True)[:10])
                                
                                # Apply custom ordering for Types Of Advocacy Or Partnership Outputs In 2024
                                if q == 'Q11' and 'Type of partnership' in var:
                                    custom_sorted_data = {}
                                    custom_order_list = ['multistakeholder initiative', 'UN interagency initiative', 'bilateral partnership']
                                    
                                    # Add items in custom order (case-insensitive matching)
                                    for item in custom_order_list:
                                        # Try exact match first
                                        if item in sorted_data:
                                            custom_sorted_data[item] = sorted_data[item]
                                        else:
                                            # Try case-insensitive match
                                            for key in sorted_data.keys():
                                                if key.lower() == item.lower():
                                                    custom_sorted_data[key] = sorted_data[key]
                                                    break
                                    
                                    # Add remaining items sorted by value
                                    remaining_items = {k: v for k, v in sorted_data.items() if k not in custom_order_list}
                                    remaining_sorted = dict(sorted(remaining_items.items(), key=lambda x: x[1], reverse=True))
                                    custom_sorted_data.update(remaining_sorted)
                                    
                                    fig = self.style_manager.create_standardized_chart(
                                        data=custom_sorted_data,
                                        chart_type='bar',
                                        title=f'Types Of Advocacy Or Partnership Outputs In 2024{title_suffix}',
                                        preserve_order=True
                                    )
                                else:
                                    # For other custom charts, use regular sorting
                                    chart_type = 'bar' if len(sorted_data) >= 5 else 'pie'
                                    fig = self.style_manager.create_standardized_chart(
                                        data=sorted_data,
                                        chart_type=chart_type,
                                        title=f'{q} {var[:50]}{title_suffix}'
                                    )
                            else:
                                fig = go.Figure()
                                fig.add_annotation(
                                    text="No Data Available",
                                    xref="paper", yref="paper",
                                    x=0.5, y=0.5, xanchor='center', yanchor='middle',
                                    showarrow=False, font_size=14
                                )
                            
                            return fig
                        
                        return update_custom_frequency_chart
                    
                    # Call closure to create callback function for regular chart
                    create_frequency_callback(question, variable, chart_id)
                    
                    # Call closure to create callback function for custom chart
                    create_custom_frequency_callback(question, variable, custom_chart_id)
        
        # Add callbacks for special fields charts
        # Q9 project names list callback
        @app.callback(
            Output('q9-project-names-list', 'children'),
            [Input('q6q7q10q11-region-filter', 'value')],
            prevent_initial_call=False
        )
        def update_q9_project_names(region_filter):
            """Update Q9 project names list with region information based on region filter"""
            # Get works list data and apply region filter
            works_data = self.data_processor.works_list_data
            if region_filter and region_filter != 'all' and not works_data.empty:
                if 'Department/Region' in works_data.columns:
                    filtered_data = works_data[works_data['Department/Region'] == region_filter]
                else:
                    filtered_data = works_data
            else:
                filtered_data = works_data
            
            # Get Q9 works data with region information
            if not filtered_data.empty:
                # Use standard English column names
                question_col = 'Question'
                q9_works = filtered_data[filtered_data[question_col] == 'Q9']
                
                if not q9_works.empty:
                    # Create list of region + work name combinations
                    region_work_list = []
                    for _, row in q9_works.iterrows():
                        region = row.get('Department/Region', 'Unknown Region')
                        work_name = row.get('Work Name', 'Unknown Work')
                        if work_name.strip() and region.strip():
                            region_work_list.append(f"{region} - {work_name}")
                    
                    # Remove duplicates and sort
                    unique_items = list(set(region_work_list))
                    unique_items.sort()
                    
                    if unique_items:
                        return html.Div([
                            html.H4("Initiative/Programme/Project Names (with Region):", 
                                   style={'color': '#2c3e50', 'marginBottom': '10px'}),
                            html.Ol([
                                html.Li(item, style={'marginBottom': '5px', 'color': '#34495e'}) 
                                for item in unique_items
                            ], style={'textAlign': 'left', 'maxWidth': '800px', 'margin': '0 auto'})
                        ])
                    else:
                        return html.Div([
                            html.H4("Initiative/Programme/Project Names (with Region):", 
                                   style={'color': '#2c3e50', 'marginBottom': '10px'}),
                            html.P("No project data available for selected region", 
                                  style={'color': '#7f8c8d', 'fontStyle': 'italic'})
                        ])
                else:
                    return html.Div([
                        html.H4("Initiative/Programme/Project Names (with Region):", 
                               style={'color': '#2c3e50', 'marginBottom': '10px'}),
                        html.P("No Q9 data available", 
                              style={'color': '#7f8c8d', 'fontStyle': 'italic'})
                    ])
            else:
                return html.Div([
                    html.H4("Initiative/Programme/Project Names (with Region):", 
                           style={'color': '#2c3e50', 'marginBottom': '10px'}),
                    html.P("No data available", 
                          style={'color': '#7f8c8d', 'fontStyle': 'italic'})
                ])
        
        # Q11 geographical focus chart callback (special-q11-geo-chart)
        @app.callback(
            Output('special-q11-geo-chart', 'figure'),
            [Input('q6q7q10q11-region-filter', 'value')],
            prevent_initial_call=False
        )
        def update_special_q11_geo_chart(region_filter):
            """Update Q11 geographical focus chart based on region filter"""
            title_suffix = f" ({region_filter})" if region_filter and region_filter != 'all' else ""
            
            # Get original data and apply region filter
            original_data = self.data_processor.original_data
            if region_filter and region_filter != 'all' and not original_data.empty:
                if 'Department/Region' in original_data.columns:
                    filtered_data = original_data[original_data['Department/Region'] == region_filter]
                else:
                    filtered_data = original_data
            else:
                filtered_data = original_data
            
            # Get Q11 geographical focus data from filtered data
            if not filtered_data.empty:
                geo_focus_data = self.data_processor.get_special_fields_data_from_filtered(filtered_data, 'Q11', "Geographical focus (Global, Regional or National/local)")
            else:
                geo_focus_data = self.data_processor.get_special_fields_data('Q11', "Geographical focus (Global, Regional or National/local)")
            
            if geo_focus_data:
                # Determine chart type based on number of items
                chart_type = 'bar' if len(geo_focus_data) >= 5 else 'pie'
                fig = self.style_manager.create_standardized_chart(
                    data=geo_focus_data,
                    chart_type=chart_type,
                    title=f'Geographical Focus Of Advocacy And Partnerships Outputs{title_suffix}'
                )
            else:
                fig = go.Figure()
                fig.add_annotation(
                    text="No Data Available",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5, xanchor='center', yanchor='middle',
                    showarrow=False, font_size=14
                )
                # Remove direct title setting to avoid conflicts with standardized chart creation in styles.py
                # fig.update_layout(title=f'Q11 Geographical Focus Distribution{title_suffix}')
            
            return fig
        
        # Q11 region/country chart callback (special-q11-region-chart)
        @app.callback(
            Output('special-q11-region-chart', 'figure'),
            [Input('q6q7q10q11-region-filter', 'value')],
            prevent_initial_call=False
        )
        def update_special_q11_region_chart(region_filter):
            """Update Q11 region/country chart based on region filter"""
            title_suffix = f" ({region_filter})" if region_filter and region_filter != 'all' else ""
            
            # Get original data and apply region filter
            original_data = self.data_processor.original_data
            if region_filter and region_filter != 'all' and not original_data.empty:
                if 'Department/Region' in original_data.columns:
                    filtered_data = original_data[original_data['Department/Region'] == region_filter]
                else:
                    filtered_data = original_data
            else:
                filtered_data = original_data
            
            # Get Q11 region/country data from filtered data
            if not filtered_data.empty:
                region_data = self.data_processor.get_special_fields_data_from_filtered(filtered_data, 'Q11', "Specify name of the Region/country")
            else:
                region_data = self.data_processor.get_special_fields_data('Q11', "Specify name of the Region/country")
            
            if region_data:
                fig = self.style_manager.create_standardized_chart(
                    data=region_data,
                    chart_type='bar',
                    title=f'Advocacy & Partnership Outputs Across Regions{title_suffix}'
                )
            else:
                fig = go.Figure()
                fig.add_annotation(
                    text="No Data Available",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5, xanchor='center', yanchor='middle',
                    showarrow=False, font_size=14
                )
            
            return fig
        @app.callback(
            Output('special-q11-region-treemap', 'figure'),
            [Input('q6q7q10q11-region-filter', 'value')],
            prevent_initial_call=False
        )
        def update_q11_region_treemap(region_filter):
            """Update Q11 region/country treemap based on region filter"""
            title_suffix = f" ({region_filter})" if region_filter and region_filter != 'all' else ""
            
            # Get original data and apply region filter
            original_data = self.data_processor.original_data
            if region_filter and region_filter != 'all' and not original_data.empty:
                if 'Department/Region' in original_data.columns:
                    filtered_data = original_data[original_data['Department/Region'] == region_filter]
                else:
                    filtered_data = original_data
            else:
                filtered_data = original_data
            
            # Get Q11 region/country data from filtered data
            if not filtered_data.empty:
                region_data = self.data_processor.get_special_fields_data_from_filtered(filtered_data, 'Q11', "Specify name of the Region/country")
            else:
                region_data = self.data_processor.get_special_fields_data('Q11', "Specify name of the Region/country")
            
            if region_data:
                # Get top 20 regions/countries for treemap
                sorted_region_data = dict(sorted(region_data.items(), key=lambda x: x[1], reverse=True)[:20])
                
                if sorted_region_data:
                    fig = go.Figure(go.Treemap(
                        labels=list(sorted_region_data.keys()),
                        values=list(sorted_region_data.values()),
                        parents=[""] * len(sorted_region_data),
                        textinfo="label+value",
                        textfont_size=12,
                        marker=dict(
                            colorscale='Viridis',
                            colorbar=dict(title="Frequency")
                        )
                    ))
                    
                    fig.update_layout(
                        title=f'Q11 Regions/Countries Distribution{title_suffix}',
                        font_size=12,
                        margin=dict(t=50, l=25, r=25, b=25)
                    )
                else:
                    fig = go.Figure()
                    fig.add_annotation(
                        text="No Data Available",
                        xref="paper", yref="paper",
                        x=0.5, y=0.5, xanchor='center', yanchor='middle',
                        showarrow=False, font_size=14
                    )
                    fig.update_layout(title=f'Q11 Regions/Countries Distribution{title_suffix}')
            else:
                fig = go.Figure()
                fig.add_annotation(
                    text="No Data Available",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5, xanchor='center', yanchor='middle',
                    showarrow=False, font_size=14
                )
                fig.update_layout(title=f'Q11 Regions/Countries Distribution{title_suffix}')
            
            return fig
        
        # Q9 Country or Region treemap callback - commented out as requested
        # @app.callback(
        #     Output('q9-country-region-treemap', 'figure'),
        #     [Input('q6q7q10q11-region-filter', 'value')],
        #     prevent_initial_call=False
        # )
        # def update_q9_country_region_treemap(region_filter):
        #     """Update Q9 Country or Region treemap based on region filter"""
        #     title_suffix = f" ({region_filter})" if region_filter and region_filter != 'all' else ""
        #     
        #     # Get original data and apply region filter
        #     original_data = self.data_processor.original_data
        #     if region_filter and region_filter != 'all' and not original_data.empty:
        #         if 'Department/Region' in original_data.columns:
        #             filtered_data = original_data[original_data['Department/Region'] == region_filter]
        #         elif '部门/区域' in original_data.columns:
        #             filtered_data = original_data[original_data['部门/区域'] == region_filter]
        #         else:
        #             filtered_data = original_data
        #     else:
        #         filtered_data = original_data
        #     
        #     # Get Q9 Country or Region data from filtered data
        #     if not filtered_data.empty:
        #         country_region_data = self.data_processor.get_frequency_data_from_filtered(filtered_data, 'Q9', "Country or Region")
        #     else:
        #         country_region_data = self.data_processor.get_frequency_data('Q9', "Country or Region")
        #     
        #     if country_region_data:
        #         # Get top 20 countries/regions for treemap
        #         sorted_countries = dict(sorted(country_region_data.items(), key=lambda x: x[1], reverse=True)[:20])
        #         
        #         if sorted_countries:
        #             fig = go.Figure(go.Treemap(
        #                 labels=list(sorted_countries.keys()),
        #                 values=list(sorted_countries.values()),
        #                 parents=[""] * len(sorted_countries),
        #                 textinfo="label+value",
        #                 textfont_size=12,
        #                 marker_colorscale='Viridis'
        #             ))
        #             
        #             layout_config = self.style_manager.get_global_chart_config('layout')
        #             fig.update_layout(
        #                 title=f'Q9 Top 20 Countries/Regions (Treemap){title_suffix}',
        #                 **layout_config
        #             )
        #         else:
        #             fig = go.Figure()
        #             fig.add_annotation(
        #                 text="No Data Available",
        #                 xref="paper", yref="paper",
        #                 x=0.5, y=0.5, xanchor='center', yanchor='middle',
        #                 showarrow=False, font_size=14
        #             )
        #             fig.update_layout(title=f'Q9 Countries/Regions (Treemap){title_suffix}')
        #     else:
        #         fig = go.Figure()
        #         fig.add_annotation(
        #             text="No Data Available",
        #             xref="paper", yref="paper",
        #             x=0.5, y=0.5, xanchor='center', yanchor='middle',
        #             showarrow=False, font_size=14
        #         )
        #         fig.update_layout(title=f'Q9 Countries/Regions (Treemap){title_suffix}')
        #     
        #     return fig
        
        # Q11 regions/countries treemap callback
        @app.callback(
            Output('q11-regions-treemap', 'figure'),
            [Input('q6q7q10q11-region-filter', 'value')],
            prevent_initial_call=False
        )
        def update_q11_regions_treemap(region_filter):
            """Update Q11 regions/countries treemap based on region filter"""
            title_suffix = f" ({region_filter})" if region_filter and region_filter != 'all' else ""
            
            # Get original data and apply region filter
            original_data = self.data_processor.original_data
            if region_filter and region_filter != 'all' and not original_data.empty:
                if 'Department/Region' in original_data.columns:
                    filtered_data = original_data[original_data['Department/Region'] == region_filter]
                else:
                    filtered_data = original_data
            else:
                filtered_data = original_data
            
            # Get Q11 regions/countries data from filtered data
            if not filtered_data.empty:
                regions_data = self.data_processor.get_special_fields_data_from_filtered(filtered_data, 'Q11', "Specify name of the Region/country")
            else:
                regions_data = self.data_processor.get_special_fields_data('Q11', "Specify name of the Region/country")
            
            if regions_data:
                # Get top 20 regions for treemap
                sorted_regions = dict(sorted(regions_data.items(), key=lambda x: x[1], reverse=True)[:20])
                
                if sorted_regions:
                    fig = go.Figure(go.Treemap(
                        labels=list(sorted_regions.keys()),
                        values=list(sorted_regions.values()),
                        parents=[""] * len(sorted_regions),
                        textinfo="label+value",
                        textfont_size=12,
                        marker_colorscale='Viridis'
                    ))
                    
                    layout_config = self.style_manager.get_global_chart_config('layout')
                    # Use create_standardized_chart's title handling mechanism to avoid direct title setting
                    title_config = layout_config.get('title', {})
                    title_config['text'] = self.style_manager._wrap_title(f'Q11 Top 20 Regions/Countries (Treemap){title_suffix}')
                    layout_config_copy = layout_config.copy()
                    layout_config_copy['title'] = title_config
                    fig.update_layout(**layout_config_copy)
                else:
                    fig = go.Figure()
                    fig.add_annotation(
                        text="No Data Available",
                        xref="paper", yref="paper",
                        x=0.5, y=0.5, xanchor='center', yanchor='middle',
                        showarrow=False, font_size=14
                    )
                    # fig.update_layout(title=f'Q11 Regions/Countries (Treemap){title_suffix}')
            else:
                fig = go.Figure()
                fig.add_annotation(
                    text="No Data Available",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5, xanchor='center', yanchor='middle',
                    showarrow=False, font_size=14
                )
                # fig.update_layout(title=f'Q11 Regions/Countries (Treemap){title_suffix}')
            
            return fig
    
    def _calculate_works_count_from_filtered_data(self, filtered_data: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """Calculate works count statistics based on filtered data"""
        try:
            if filtered_data.empty:
                return {}
            
            result = {}
            # Q9 removed from analysis, only keep Q6, Q7, Q10, Q11
            questions = ['Q6', 'Q7', 'Q10', 'Q11']
            
            for question in questions:
                # Use standard English column names
                question_col = 'Question'
                user_id_col = 'User ID'
                
                question_data = filtered_data[filtered_data[question_col] == question]
                if not question_data.empty:
                    # Count users with works
                    participants = question_data[user_id_col].nunique()
                    # Total works count
                    total_works = len(question_data)
                    # Average works count
                    avg_works = total_works / participants if participants > 0 else 0
                    
                    result[question] = {
                        'Participants': participants,
                        'Total Works': total_works,
                        'Average Works': avg_works
                    }
                else:
                    result[question] = {
                        'Participants': 0,
                        'Total Works': 0,
                        'Average Works': 0
                    }
            
            return result
        except Exception as e:
            print(f"Calculate filtered works count statistics error: {e}")
            return {}
    
    def get_summary_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get module summary statistics data (for homepage card display)"""
        return self.data_processor.get_summary_stats()
    
    def get_module_stats(self) -> Dict[str, Any]:
        """Get module internal statistics data"""
        return {
            'questions_analyzed': len(self.questions),
            'total_works': sum([len(self.data_processor.get_works_list(q)) for q in self.questions]),
            'data_files_loaded': 4
        }
    
    def get_module_info(self) -> Dict[str, Any]:
        """Get module basic information"""
        return {
            'name': 'Q6Q7Q10Q11 Analysis',
            'description': 'Display analysis results for Q6, Q7, Q10, Q11 questions',
            'route': '/q6q7q10q11',
            'icon': 'fas fa-chart-bar',
            'color': '#8e44ad',
            'features': ['Outputs Count Statistics', 'Frequency Analysis', 'Outputs Detail List'],  # 'CPO/GLO Code Distribution' temporarily commented out
            'questions': self.questions
        }

# Independent running support
if __name__ == '__main__':
    # Create independent Dash application for testing
    app = dash.Dash(__name__)
    app.title = "Q6Q7Q10Q11 Analysis Dashboard"
    
    # Initialize dashboard
    dashboard = Q6Q7Q10Q11Dashboard()
    
    # Set layout
    app.layout = dashboard.get_layout()
    
    # Set callbacks
    dashboard.setup_callbacks(app)
    
    # Run application
    print("Q6Q7Q10Q11 Analysis Dashboard starting...")
    print("Access URL: http://localhost:8051")
    app.run(debug=True, port=8051)