import pandas as pd
import json
from typing import Dict, Any, List, Union

class DataHandler:
    """Data processing layer - responsible for data import, parsing and preprocessing"""
    
    def __init__(self):
        self.raw_data = None
        self.processed_data = {}
        
    def import_data_from_external(self, source_path: str, data_format: str = 'csv') -> Dict[str, Any]:
        """Import and parse data from external modules"""
        try:
            if data_format.lower() == 'csv':
                # Don't use first row as column names when reading CSV, because first row is data
                self.raw_data = pd.read_csv(source_path, encoding='utf-8', header=None)
            elif data_format.lower() == 'json':
                with open(source_path, 'r', encoding='utf-8') as f:
                    self.raw_data = json.load(f)
            else:
                raise ValueError(f"Unsupported data format: {data_format}")
                
            return self._parse_survey_data()
        except Exception as e:
            print(f"Data import error: {e}")
            return {}
    
    def _parse_survey_data(self) -> Dict[str, Dict[str, int]]:
        """Parse survey data to standard format {question_name: {option: count, ...}, ...}"""
        if self.raw_data is None:
            return {}
            
        processed = {}
        
        # Process CSV format survey statistics data
        if isinstance(self.raw_data, pd.DataFrame):
            # CSV file structure:
            # Row 0: question - question text
            # Row 1: number - question number  
            # Row 2: option - option content
            # Row 3: count - selection count
            
            # Check data row count
            if len(self.raw_data) < 4:
                print(f"Insufficient data rows, expected at least 4 rows, actual {len(self.raw_data)} rows")
                return processed
                
            # Iterate through each column (skip first column as it's row label column)
            for col_idx in range(1, len(self.raw_data.columns)):
                try:
                    # Get current column data
                    question = str(self.raw_data.iloc[0, col_idx]).strip()  # Row 0: question text
                    number = self.raw_data.iloc[1, col_idx]                 # Row 1: question number
                    option = str(self.raw_data.iloc[2, col_idx]).strip()    # Row 2: option content
                    count = self.raw_data.iloc[3, col_idx]                  # Row 3: count
                    
                    # Skip null values or invalid data
                    if (pd.isna(question) or pd.isna(option) or pd.isna(count) or 
                        question == 'nan' or option == 'nan' or str(question).strip() == '' or str(option).strip() == ''):
                        continue
                        
                    # If question doesn't exist, create new question entry
                    if question not in processed:
                        processed[question] = {}
                    
                    # Add option and count
                    try:
                        count_value = int(float(count)) if not pd.isna(count) else 0
                        processed[question][option] = count_value
                    except (ValueError, TypeError):
                        processed[question][option] = 0
                        
                except (IndexError, KeyError) as e:
                    print(f"Error parsing column {col_idx}: {e}")
                    continue
        
        # Filter out empty questions
        processed = {q: opts for q, opts in processed.items() if opts}
        
        self.processed_data = processed
        print(f"Successfully parsed {len(processed)} questions")
        return processed
    
    def custom_parser(self, data: Any, rule: str) -> Dict[str, Any]:
        """Extended custom data parsing rules"""
        # Reserved interface, supports custom parsing rules
        if rule == 'percentage':
            return self._calculate_percentages(data)
        elif rule == 'top_n':
            return self._get_top_n_responses(data, 5)
        else:
            return data
    
    def _calculate_percentages(self, data: Dict[str, Dict[str, int]]) -> Dict[str, Dict[str, float]]:
        """Calculate percentages"""
        result = {}
        for question, options in data.items():
            total = sum(options.values())
            if total > 0:
                result[question] = {option: (count/total)*100 for option, count in options.items()}
            else:
                result[question] = {option: 0.0 for option in options.keys()}
        return result
    
    def _get_top_n_responses(self, data: Dict[str, Dict[str, int]], n: int = 5) -> Dict[str, Dict[str, int]]:
        """Get top N responses for each question"""
        result = {}
        for question, options in data.items():
            sorted_options = sorted(options.items(), key=lambda x: x[1], reverse=True)[:n]
            result[question] = dict(sorted_options)
        return result
    
    def get_question_summary(self) -> Dict[str, Any]:
        """Get question summary information"""
        if not self.processed_data:
            return {}
            
        summary = {
            'total_questions': len(self.processed_data),
            'questions_list': list(self.processed_data.keys()),
            'total_responses_per_question': {}
        }
        
        for question, options in self.processed_data.items():
            summary['total_responses_per_question'][question] = sum(options.values())
            
        return summary
    
    def get_processed_data(self) -> Dict[str, Dict[str, int]]:
        """Get processed data"""
        return self.processed_data