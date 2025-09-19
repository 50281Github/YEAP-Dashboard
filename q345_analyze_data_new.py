#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unified Q345 Data Analysis Script - Supports Multiple Data Sources
1. New data source: q345_option_other.csv (original user response data, supports region breakdown)
2. Old data source: question_response_count_statistics.csv (statistical summary data)
Automatically detects data source and selects appropriate processing method
"""

import pandas as pd
import os

def detect_data_source():
    """
    Detect available data sources
    Returns: (data_source_type, file_path)
    """
    new_data_path = 'orignaldata/q345_option_other.csv'
    old_data_path = 'orignaldata/question_response_count_statistics.csv'
    
    if os.path.exists(new_data_path):
        print(f"Detected new data source: {new_data_path}")
        return 'new', new_data_path
    elif os.path.exists(old_data_path):
        print(f"Detected old data source: {old_data_path}")
        return 'old', old_data_path
    else:
        print(f"No available data source found")
        return None, None

def load_q345_data():
    """
    Load Q345 data file - automatically detect data source
    """
    data_source_type, file_path = detect_data_source()
    
    if data_source_type is None:
        return None, None, None
    
    if data_source_type == 'new':
        return load_new_format_data(file_path)
    else:
        return load_old_format_data(file_path)

def load_new_format_data(file_path):
    """
    Load new data format (q345_option_other.csv)
    Data structure consistent with Q8Q9: starts from row 4, includes region information
    """
    # Read number row (row 2) to get column assignments
    number_df = pd.read_csv(file_path, header=None, skiprows=1, nrows=1, encoding='utf-8')
    number_row = number_df.iloc[0].tolist()
    
    # Read data, using row 3 as column names
    df = pd.read_csv(file_path, header=2, encoding='utf-8')
    
    print(f"New format data loading completed")
    print(f"Data shape: {df.shape}")
    print(f"Column names: {list(df.columns)[:10]}...")  # Show first 10 columns only
    print(f"Number row: {number_row[:10]}...")  # Show first 10 number values
    
    return df, number_row, 'new'

def load_old_format_data(file_path):
    """
    Load old data format (question_response_count_statistics.csv)
    Data structure: row 1 questions, row 2 numbers, row 3 options, row 4 statistics
    """
    df = pd.read_csv(file_path, encoding='utf-8')
    
    print(f"Old format data loading completed")
    print(f"Data shape: {df.shape}")
    print(f"Column names: {list(df.columns)[:10]}...")  # Show first 10 columns only
    
    return df, None, 'old'

def analyze_old_format_data(df):
    """
    Analyze old data format (statistical summary data)
    """
    if df is None or df.empty:
        print("Data is empty, cannot analyze")
        return None
    
    # Analyze Q3, Q4, Q5 questions
    q3_data = []
    q4_data = []
    q5_data = []
    
    for col in df.columns:
        if col.startswith('Q3'):
            q3_data.append({
                'question': col,
                'number': df.iloc[0, df.columns.get_loc(col)],
                'option': df.iloc[1, df.columns.get_loc(col)],
                'count': int(df.iloc[2, df.columns.get_loc(col)])
            })
        elif col.startswith('Q4'):
            q4_data.append({
                'question': col,
                'number': df.iloc[0, df.columns.get_loc(col)],
                'option': df.iloc[1, df.columns.get_loc(col)],
                'count': int(df.iloc[2, df.columns.get_loc(col)])
            })
        elif col.startswith('Q5'):
            q5_data.append({
                'question': col,
                'number': df.iloc[0, df.columns.get_loc(col)],
                'option': df.iloc[1, df.columns.get_loc(col)],
                'count': int(df.iloc[2, df.columns.get_loc(col)])
            })
    
    # Function to filter Other options
    def filter_other_options_old(data_list, group_name):
        """Filter out 'Other' options for Q4 and Q5, keep them for Q3"""
        if group_name not in ['Q4', 'Q5']:
            return data_list
        
        # For Q4 and Q5, exclude all Other options
        filtered_data = []
        for item in data_list:
            if item['option'] in ['Other', 'Other (elaborated answ)']:
                print(f"    Skipping {item['option']} for {group_name} (Other options excluded)")
                continue
            else:
                filtered_data.append(item)
        
        return filtered_data
    
    # Calculate correct proportions
    def calculate_proportions_old(data_list, group_name):
        # First filter Other options for Q4 and Q5
        data_list = filter_other_options_old(data_list, group_name)
        
        total_count = sum(item['count'] for item in data_list)
        results = []
        
        print(f"\n{group_name} Question Analysis")
        print(f"{group_name} question count: {len(data_list)}")
        print(f"{group_name} total responses: {total_count}")
        print()
        
        for item in data_list:
            count = item['count']
            percentage = (count / total_count * 100) if total_count > 0 else 0
            
            # Filter out items with percentage less than 5%
            if percentage >= 5.0 and yes_count >= 2:
                result = {
                    'group': group_name,
                    'question': item['question'],
                    'option': item['option'],
                    'count': count,
                    'total_count': total_count,
                    'percentage': round(percentage, 1)
                }
                results.append(result)
                
                print(f"{item['question']}: {count} times ({percentage:.1f}%)")
                print(f"  • {item['option']}")
                print()
        
        return results
    
    # Analyze each group of questions
    q3_results = calculate_proportions_old(q3_data, 'Q3')
    q4_results = calculate_proportions_old(q4_data, 'Q4')
    q5_results = calculate_proportions_old(q5_data, 'Q5')
    
    # Merge all results
    all_results = q3_results + q4_results + q5_results
    
    print(f"\nSummary Statistics")
    print(f"Q3: {len(q3_data)} questions, {sum(item['count'] for item in q3_data)} responses")
    print(f"Q4: {len(q4_data)} questions, {sum(item['count'] for item in q4_data)} responses")
    print(f"Q5: {len(q5_data)} questions, {sum(item['count'] for item in q5_data)} responses")
    
    return all_results

def analyze_q345_by_region(df, number_row):
    """
    Analyze Q345 data by region
    """
    if df is None or df.empty:
        print("Data is empty, cannot analyze")
        return None
    
    # Get region column (second column: Department/Region)
    region_col = df.columns[1]
    
    # Get all unique regions
    regions = df[region_col].dropna().unique()
    print(f"\nDiscovered regions: {list(regions)}")
    
    # Store analysis results
    all_results = []
    
    # Analyze data for each region
    for region in regions:
        if pd.isna(region) or region == '':
            continue
            
        print(f"\nAnalyzing region: {region}")
        
        # Filter data for this region
        region_data = df[df[region_col] == region]
        print(f"Data rows for this region: {len(region_data)}")
        
        # Analyze Q3, Q4, Q5 questions
        region_results = analyze_questions_for_region(region_data, region, number_row)
        all_results.extend(region_results)
    
    # Global analysis (all regions combined)
    print(f"\nAnalyzing global data")
    global_results = analyze_questions_for_region(df, 'ALL', number_row)
    all_results.extend(global_results)
    
    return all_results

def analyze_questions_for_region(region_data, region_name, number_row):
    """
    Analyze Q3, Q4, Q5 questions for a specific region
    """
    results = []
    
    # Get Q3, Q4, Q5 related columns based on number_row
    q3_cols = []
    q4_cols = []
    q5_cols = []
    
    for i, col in enumerate(region_data.columns):
        if i < len(number_row):
            number_val = number_row[i]
            if str(number_val) == '3':
                q3_cols.append(col)
            elif str(number_val) == '4':
                q4_cols.append(col)
            elif str(number_val) == '5':
                q5_cols.append(col)
    
    print(f"  Q3 columns: {len(q3_cols)}")
    print(f"  Q4 columns: {len(q4_cols)}")
    print(f"  Q5 columns: {len(q5_cols)}")
    
    # Analyze each question group
    q3_results = analyze_question_group(region_data, q3_cols, 'Q3', region_name)
    q4_results = analyze_question_group(region_data, q4_cols, 'Q4', region_name)
    q5_results = analyze_question_group(region_data, q5_cols, 'Q5', region_name)
    
    results.extend(q3_results)
    results.extend(q4_results)
    results.extend(q5_results)
    
    return results

def analyze_question_group(data, question_cols, group_name, region_name):
    """
    Analyze specific question group (Q3, Q4 or Q5)
    """
    results = []
    
    # Calculate total number of records in the dataset
    total_records = len(data)
    
    for col in question_cols:
        # Get option name (extracted from column name)
        option_name = extract_option_name(col)
        
        # Skip Other options for Q4 and Q5
        if group_name in ['Q4', 'Q5'] and 'Other' in option_name:
            print(f"    Skipping {option_name} for {group_name} (Other options excluded)")
            continue
        
        # Count the number of "YES" in this column
        yes_count = (data[col].str.upper() == 'YES').sum()
        
        # Calculate percentage based on total records
        percentage = (yes_count / total_records * 100) if total_records > 0 else 0
        
        # Filter out items with percentage less than 5%
        if percentage >= 5.0 and yes_count >= 2:
            result = {
                'group': group_name,
                'question': col,
                'option': option_name,
                'count': yes_count,
                'total_count': total_records,
                'percentage': round(percentage, 1)
            }
            
            results.append(result)
            
            if yes_count > 0:  # Only show options with responses
                print(f"    {option_name}: {yes_count}/{total_records} ({percentage:.1f}%)")
    
    return results

def extract_option_name(column_name):
    """
    Extract option name from column name
    """
    # Split column name, get the part after the question
    parts = str(column_name).split(':')
    if len(parts) > 1:
        option_part = parts[1].strip()
        # Further clean option name
        if '.' in option_part:
            option_part = option_part.split('.')[0].strip()
        return option_part
    return str(column_name)

def merge_other_options(results):
    """
    Merge Other options
    """
    merged_results = []
    other_groups = {}
    
    for result in results:
        option = result['option']
        key = result['group']  # Only use group as key, since region has been removed
        
        if 'Other' in option:
            if key not in other_groups:
                other_groups[key] = {
                    'group': result['group'],
                    'question': result['question'],
                    'option': 'Other',
                    'count': 0,
                    'total_count': result['total_count'],
                    'percentage': 0
                }
            other_groups[key]['count'] += result['count']
        else:
            merged_results.append(result)
    
    # Add merged Other options
    for key, other_result in other_groups.items():
        if other_result['count'] > 0:
            total = other_result['total_count']
            other_result['percentage'] = round((other_result['count'] / total * 100) if total > 0 else 0, 1)
            merged_results.append(other_result)
    
    return merged_results

def save_results(results):
    """
    Save analysis results to CSV file
    """
    if not results:
        print("No results to save")
        return
    
    # Ensure result directory exists
    os.makedirs('result', exist_ok=True)
    
    # Convert to DataFrame
    df = pd.DataFrame(results)
    
    # Adjust column order to match existing format: group,question,option,count,percentage,total_count
    column_order = ['group', 'question', 'option', 'count', 'percentage', 'total_count']
    df = df[column_order]
    
    # Save to CSV
    csv_filename = 'result/q345_analysis_results.csv'
    df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
    
    print(f"\nAnalysis completed! Results saved to {csv_filename}")
    
    # Display summary statistics
    print(f"\nSummary Statistics:")
    
    # Statistics by question group
    group_stats = df.groupby('group').agg({
        'count': 'sum',
        'total_count': 'first'
    })
    
    print("\nStatistics by question group:")
    for group, stats in group_stats.iterrows():
        print(f"  {group}: {stats['count']} valid responses, total {stats['total_count']} responses")
    
    return df

def main():
    """
    Main function - unified processing of multiple data sources
    """
    print("Starting Q345 data analysis (unified version)")
    print("Supports new regional split data and old statistical summary data")
    
    # Load data
    df, number_row, data_type = load_q345_data()
    if df is None:
        return
    
    # Choose analysis method based on data type
    if data_type == 'new':
        print("\nUsing new data analysis method (supports regional split)")
        # Analyze by region
        results = analyze_q345_by_region(df, number_row)
        if not results:
            print("Analysis failed")
            return
        
        # Merge Other options
        merged_results = merge_other_options(results)
    else:
        print("\nUsing old data analysis method (statistical summary data)")
        # Analyze statistical summary data
        merged_results = analyze_old_format_data(df)
        if not merged_results:
            print("Analysis failed")
            return
    
    # Save results
    save_results(merged_results)
    
    print("\nQ345 data analysis completed!")

if __name__ == "__main__":
    main()