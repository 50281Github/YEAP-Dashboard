import pandas as pd
import numpy as np
from collections import Counter
from typing import Dict, Any, List

def main():
    print("Starting Q6Q7Q10Q11 data analysis...")
    
    # 1. Load data - first read the complete file to get correct column names and structure
    try:
        full_df = pd.read_csv('orignaldata/Q6Q7Q10Q11_basic_data.csv', encoding='utf-8')
        print(f"Data loaded successfully, {len(full_df)} rows, {len(full_df.columns)} columns")
    except:
        try:
            full_df = pd.read_csv('orignaldata/Q6Q7Q10Q11_basic_data.csv', encoding='gbk')
            print(f"Data loaded successfully, {len(full_df)} rows, {len(full_df.columns)} columns")
        except Exception as e:
            print(f"Data loading failed: {e}")
            return
    
    # 2. Get question numbers and option names rows, and actual data
    # CSV file structure re-analysis:
    # Row 1 (index 0): Question numbers (Q6, Q7, Q9, Q10, Q11)
    # Row 2 (index 1): Option names
    # Row 3 (index 2) onwards: Actual data
    column_names = full_df.columns.tolist()  # Column names
    
    # Read question number row (row 1, index 0) - should contain Q6, Q7, Q9, Q10, Q11
    number_row = full_df.iloc[0].values
    
    # Read option names row (row 2, index 1)
    option_row = full_df.iloc[1].values
    
    # Read actual data starting from row 3 (index 2 onwards)
    df = full_df.iloc[2:].copy()
    df.columns = column_names  # Ensure column names are correct
    
    print("Debug: Checking data row content")
    print(f"Row 1 (question numbers) first 20 values: {list(number_row[:20])}")
    print(f"Row 2 (option names) first 15 values: {list(option_row[:15])}")
    
    # Additional debugging: check specific content of question number row
    print(f"Question number row from column 3 onwards: {list(number_row[3:])}")
    print(f"Looking for Q6, Q7, Q9, Q10, Q11 in question number row...")
    
    # Check actual content of question number row
    print(f"Actual question numbers found: {[val for val in number_row if val in ['Q6', 'Q7', 'Q9', 'Q10', 'Q11']]}")
    
    print(f"Data column names: {list(df.columns)[:10]}")
    print(f"Data shape after processing: {df.shape}")
    if 'UserId' in df.columns:
        print(f"Sample UserId values: {df['UserId'].head(3).tolist()}")
    else:
        print("Warning: UserId column not found")
    
    # 3. Identify column ranges for each question
    q6_cols = []
    q7_cols = []
    q9_cols = []
    q10_cols = []
    q11_cols = []
    
    print("\nAnalyzing columns for question numbers:")
    
    # Question numbers start from column D (index 3), skip first 3 columns (A, B, C)
    for i, num in enumerate(number_row):
        if i >= 3 and pd.notna(num) and str(num).strip() != '':  # Start checking from index 3
            num_str = str(num).strip()
            print(f"Column {i}: '{num_str}'")
            # Check if this is a question number column
            if num_str in ['Q6', 'Q7', 'Q9', 'Q10', 'Q11']:
                if num_str == 'Q6':
                    q6_cols.append(i)
                    print(f"  -> Added to Q6 columns")
                elif num_str == 'Q7':
                    q7_cols.append(i)
                    print(f"  -> Added to Q7 columns")
                elif num_str == 'Q9':
                    q9_cols.append(i)
                    print(f"  -> Added to Q9 columns")
                elif num_str == 'Q10':
                    q10_cols.append(i)
                    print(f"  -> Added to Q10 columns")
                elif num_str == 'Q11':
                    q11_cols.append(i)
                    print(f"  -> Added to Q11 columns")
    
    print(f"Q6 column range: {len(q6_cols)} columns - {q6_cols}")
    print(f"Q7 column range: {len(q7_cols)} columns - {q7_cols}")
    print(f"Q9 column range: {len(q9_cols)} columns - {q9_cols}")
    print(f"Q10 column range: {len(q10_cols)} columns - {q10_cols}")
    print(f"Q11 column range: {len(q11_cols)} columns - {q11_cols}")
    
    # 4. Analyze data for each question
    results = []
    
    # Analyze Q6
    if q6_cols:
        q6_analysis = analyze_question_data(df, q6_cols, option_row, 'Q6')
        results.extend(q6_analysis)
    
    # Analyze Q7
    if q7_cols:
        q7_analysis = analyze_question_data(df, q7_cols, option_row, 'Q7')
        results.extend(q7_analysis)
    
    # Analyze Q9 - Removed, not displayed in dashboard
    # if q9_cols:
    #     q9_analysis = analyze_question_data(df, q9_cols, option_row, 'Q9')
    #     results.extend(q9_analysis)
    
    # Analyze Q10
    if q10_cols:
        q10_analysis = analyze_question_data(df, q10_cols, option_row, 'Q10')
        results.extend(q10_analysis)
    
    # Analyze Q11
    if q11_cols:
        q11_analysis = analyze_question_data(df, q11_cols, option_row, 'Q11')
        results.extend(q11_analysis)
    
    # 5. Save frequency analysis results
    if results:
        freq_df = pd.DataFrame(results)
        freq_df.to_csv('result/q6q7q10q11_frequency_analysis_results.csv', index=False, encoding='utf-8-sig')
        print(f"Frequency analysis results saved, {len(freq_df)} records")
    
    # 6. Analyze outputs count
    works_results = analyze_works_count(df, number_row, option_row)
    if works_results:
        works_df = pd.DataFrame(works_results)
        works_df.to_csv('result/q6q7q10q11_works_count_analysis_results.csv', index=False, encoding='utf-8-sig')
        print(f"Outputs count analysis results saved, {len(works_df)} records")
    
    # 7. Analyze CPO/GLO codes
    cpo_results = analyze_cpo_codes(df, number_row, option_row)
    if cpo_results:
        cpo_df = pd.DataFrame(cpo_results)
        cpo_df.to_csv('result/q6q7q10q11_cpo_glo_analysis_results.csv', index=False, encoding='utf-8-sig')
        print(f"CPO/GLO code analysis results saved, {len(cpo_df)} records")
    
    # 8. Analyze special fields (Q11 geography-related fields)
    special_results = analyze_special_fields(df, number_row, option_row)
    if special_results:
        special_df = pd.DataFrame(special_results)
        special_df.to_csv('result/q6q7q10q11_special_fields_analysis_results.csv', index=False, encoding='utf-8-sig')
        print(f"Special fields analysis results saved, {len(special_df)} records")
    
    # 9. Extract works names
    works_names = extract_works_names(df, number_row, option_row)
    if works_names:
        names_df = pd.DataFrame(works_names)
        names_df.to_csv('result/q6q7q10q11_works_list.csv', index=False, encoding='utf-8-sig')
        print(f"Works name list saved, {len(names_df)} records")
    
    print("Analysis completed!")

def analyze_question_data(df, col_indices, option_row, question_name):
    """
    Analyze data for a single question
    """
    results = []
    data_rows = df  # Actual data is already properly sliced from row 5
    
    for col_idx in col_indices:
        if col_idx < len(option_row) and pd.notna(option_row[col_idx]):
            option_name = str(option_row[col_idx]).strip()
            
            # Skip work names, CPO/GLO code columns, Web link and Short description (these are handled in other analyses or don't need analysis)
            if ('name' in option_name.lower() or 'cpo' in option_name.lower() or 'glo' in option_name.lower() or 
                'web link' in option_name.lower() or 'short description' in option_name.lower()):
                continue
            
            # Get all non-empty values from this column, excluding "0" values
            column_data = data_rows.iloc[:, col_idx].dropna()
            column_data = column_data[column_data != '']
            column_data = column_data[column_data != '0']  # Exclude "0" values
            column_data = column_data[column_data != 0]  # Exclude numeric 0 values
            
            # Data standardization: remove leading/trailing spaces, standardize case (capitalize first letter, lowercase rest)
            column_data = column_data.astype(str).str.strip()
            # For simple Yes/No type answers, standardize case
            column_data = column_data.apply(lambda x: x.capitalize() if x.lower() in ['yes', 'no'] else x)
            # For answers containing "Youth only" or "Youth Only", standardize format
            column_data = column_data.apply(lambda x: 'Youth only' if x.lower() == 'youth only' else x)
            column_data = column_data.apply(lambda x: 'Youth are one of the target groups' if x.lower() == 'youth are one of the target groups' else x)
            
            # Standardize funding source options
            column_data = column_data.apply(lambda x: 'extrabudgetary' if x.lower() == 'extrabudgetary' else x)
            column_data = column_data.apply(lambda x: 'Regular Budget' if x.lower() == 'regular budget' else x)
            
            # Standardize publication type options
            column_data = column_data.apply(lambda x: 'Technical Report' if x.lower() == 'technical report' else x)
            column_data = column_data.apply(lambda x: 'Working paper' if x.lower() == 'working paper' else x)
            column_data = column_data.apply(lambda x: 'Guidance/Tools' if x.lower() == 'guidance/tools' else x)
            column_data = column_data.apply(lambda x: 'Data/Database' if x.lower() == 'data/database' else x)
            column_data = column_data.apply(lambda x: 'Evaluation' if x.lower() == 'evaluation' else x)
            
            # Additional standardization for common variations
            column_data = column_data.apply(lambda x: 'best practices/lessons learned' if x.lower() == 'best practices/lessons learned' else x)
            
            if len(column_data) > 0:
                # Count frequencies
                value_counts = column_data.value_counts()
                
                for value, count in value_counts.items():
                    percentage = count/len(column_data)*100
                    # Filter out items with percentage less than 5%
                    if percentage >= 5.0:
                        results.append({
                            'Question': question_name,
                            'Variable Name': option_name,
                            'Variable Value': str(value),
                            'Frequency': count,
                            'Percentage': f"{percentage:.1f}%"
                        })
    
    return results

def analyze_works_count(df, number_row, option_row):
    """
    Analyze works count
    """
    results = []
    data_rows = df  # Actual data is already properly sliced from row 5
    
    questions = ['Q6', 'Q7', 'Q10', 'Q11']  # Remove Q9 to match dashboard display
    
    for question in questions:
        # Find the first column for this question (works name column)
        name_col_idx = None
        for i, num in enumerate(number_row):
            if pd.notna(num) and str(num).strip() == question:
                name_col_idx = i
                break
        
        if name_col_idx is not None:
            # Get data from works name column
            works_data = data_rows.iloc[:, name_col_idx].dropna()
            works_data = works_data[works_data != '']
            
            # Count users with works
            users_with_works = data_rows[data_rows.iloc[:, name_col_idx].notna() & 
                                       (data_rows.iloc[:, name_col_idx] != '')]['UserId'].nunique()
            
            # Total works count
            total_works = len(works_data)
            
            # Average works per user
            avg_works = total_works / users_with_works if users_with_works > 0 else 0
            
            results.append({
                'Question': question,
                'Users with Related Works': users_with_works,
                'Total Works Count': total_works,
                'Average Works Count': f"{avg_works:.2f}"
            })
    
    return results

def analyze_cpo_codes(df, number_row, option_row):
    """
    Analyze CPO/GLO codes
    """
    results = []
    data_rows = df  # Actual data is already properly sliced from row 5
    
    questions = ['Q6', 'Q7', 'Q10', 'Q11']  # Remove Q9 to match dashboard display
    
    for question in questions:
        # Find the CPO/GLO code column for this question (usually the second column)
        cpo_col_idx = None
        question_cols = []
        
        for i, num in enumerate(number_row):
            if pd.notna(num) and str(num).strip() == question:
                question_cols.append(i)
        
        if len(question_cols) >= 2:
            cpo_col_idx = question_cols[1]  # Second column is usually CPO/GLO code
            
            # Get CPO/GLO code data, excluding "0" values
            cpo_data = data_rows.iloc[:, cpo_col_idx].dropna()
            cpo_data = cpo_data[cpo_data != '']
            cpo_data = cpo_data[cpo_data != '0']  # Exclude "0" values
            
            # Data standardization: remove leading/trailing spaces
            cpo_data = cpo_data.astype(str).str.strip()
            
            if len(cpo_data) > 0:
                # Count frequencies
                value_counts = cpo_data.value_counts()
                
                for code, count in value_counts.items():
                    percentage = count/len(cpo_data)*100
                    # Filter out items with percentage less than 5%
                    if percentage >= 5.0:
                        results.append({
                            'Question': question,
                            'CPO/GLO Code': str(code),
                            'Frequency': count,
                            'Percentage': f"{percentage:.1f}%"
                        })
    
    return results

def analyze_special_fields(df, number_row, option_row):
    """
    Analyze special fields: Q9 project names, Q11 geographical focus and region/country names
    """
    results = []
    data_rows = df  # Actual data is already properly sliced from row 5
    
    # Analyze Q9 project names - Removed, not displayed in dashboard
    # q9_name_col_idx = None
    # for i, num in enumerate(number_row):
    #     if pd.notna(num) and str(num).strip() == 'Q9':
    #         q9_name_col_idx = i
    #         break
    # 
    # if q9_name_col_idx is not None:
    #     # Get Q9 project name data
    #     q9_names = data_rows.iloc[:, q9_name_col_idx].dropna()
    #     q9_names = q9_names[q9_names != '']
    #     q9_names = q9_names[q9_names != '0']
    #     
    #     # Data standardization
    #     q9_names = q9_names.astype(str).str.strip()
    #     
    #     if len(q9_names) > 0:
    #         # Count frequencies
    #         value_counts = q9_names.value_counts()
    #         
    #         for value, count in value_counts.items():
    #             results.append({
    #                 'Question': 'Q9',
    #                 'Variable Name': 'Initiative/programme/project\'s name',
    #                 'Variable Value': str(value),
    #                 'Frequency': count,
    #                 'Percentage': f"{count/len(q9_names)*100:.1f}%"
    #             })
    
    # Analyze Q11 geography-related fields
    q11_cols = []
    for i, num in enumerate(number_row):
        if pd.notna(num) and str(num).strip() == 'Q11':
            q11_cols.append(i)
    
    if len(q11_cols) >= 5:  # Q11 has at least 5 columns
        # Geographical focus field (5th column)
        geo_focus_col_idx = q11_cols[4] if len(q11_cols) > 4 else None
        # Region/country name field (6th column)
        region_name_col_idx = q11_cols[5] if len(q11_cols) > 5 else None
        
        # Analyze geographical focus
        if geo_focus_col_idx is not None:
            geo_focus_data = data_rows.iloc[:, geo_focus_col_idx].dropna()
            geo_focus_data = geo_focus_data[geo_focus_data != '']
            geo_focus_data = geo_focus_data[geo_focus_data != '0']
            
            # Data standardization - normalize case for National/local
            geo_focus_data = geo_focus_data.astype(str).str.strip()
            # Normalize case: convert National/local variations to consistent format
            geo_focus_data = geo_focus_data.str.replace('National/Local', 'National/local', case=False)
            geo_focus_data = geo_focus_data.str.replace('national/local', 'National/local', case=False)
            
            if len(geo_focus_data) > 0:
                value_counts = geo_focus_data.value_counts()
                
                for value, count in value_counts.items():
                    percentage = count/len(geo_focus_data)*100
                    # Filter out items with percentage less than 5%
                    if percentage >= 5.0:
                        results.append({
                            'Question': 'Q11',
                            'Variable Name': 'Geographical focus (Global, Regional or National/local)',
                            'Variable Value': str(value),
                            'Frequency': count,
                            'Percentage': f"{percentage:.1f}%"
                        })
        
        # Analyze region/country names
        if region_name_col_idx is not None:
            region_name_data = data_rows.iloc[:, region_name_col_idx].dropna()
            region_name_data = region_name_data[region_name_data != '']
            region_name_data = region_name_data[region_name_data != '0']
            
            # Data standardization
            region_name_data = region_name_data.astype(str).str.strip()
            
            if len(region_name_data) > 0:
                value_counts = region_name_data.value_counts()
                
                for value, count in value_counts.items():
                    percentage = count/len(region_name_data)*100
                    # Filter out items with percentage less than 5%
                    if percentage >= 5.0:
                        results.append({
                            'Question': 'Q11',
                            'Variable Name': 'Specify name of the Region/country',
                            'Variable Value': str(value),
                            'Frequency': count,
                            'Percentage': f"{percentage:.1f}%"
                        })
    
    return results

def extract_works_names(df, number_row, option_row):
    """
    Extract works name list
    """
    results = []
    data_rows = df  # Actual data is already properly sliced from row 5
    
    questions = ['Q6', 'Q7', 'Q10', 'Q11']  # Remove Q9 to match dashboard display
    
    for question in questions:
        # Find the first column for this question (works name column)
        name_col_idx = None
        for i, num in enumerate(number_row):
            if pd.notna(num) and str(num).strip() == question:
                name_col_idx = i
                break
        
        if name_col_idx is not None:
            # Iterate through each row of data
            for idx, row in data_rows.iterrows():
                work_name = row.iloc[name_col_idx]
                user_id = row['UserId']
                
                # If work name is not empty
                if pd.notna(work_name) and str(work_name).strip() != '':
                    # Get department/region information (assumed to be in column 2, index 1)
                    department_region = row.iloc[1] if len(row) > 1 and pd.notna(row.iloc[1]) else ''
                    
                    results.append({
                        'Question': question,
                        'User ID': user_id,
                        'Department/Region': str(department_region).strip() if department_region else '',
                        'Work Name': str(work_name).strip()
                    })
    
    return results

if __name__ == "__main__":
    main()