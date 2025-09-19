#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Q8Q9 Survey Data Analysis Script
Analyze Q8 (whether providing youth project funding support) and Q9 (project details) statistical information
"""

import pandas as pd
import numpy as np
from collections import defaultdict
import re

def analyze_q8q9_data(csv_file_path, user_ids_filter=None):
    """
    Analyze Q8Q9 data
    
    Args:
        csv_file_path: CSV file path
        user_ids_filter: User ID filter list, if provided, only analyze data for these users
    
    Returns:
        dict: Dictionary containing statistical results
    """
    # Read CSV file, skip first two rows of descriptive information
    df = pd.read_csv(csv_file_path, skiprows=2)
    
    print("CSV file column names:", df.columns.tolist())
    print("First 5 rows of data:")
    print(df.head())
    
    # Get all unique user IDs (first column)
    user_ids = df.iloc[:, 0].unique()
    # Filter out NaN values and header rows
    user_ids = [uid for uid in user_ids if pd.notna(uid) and str(uid).startswith('USR-')]
    
    # If user ID filter is provided, only keep data for these users
    if user_ids_filter is not None:
        user_ids = [uid for uid in user_ids if uid in user_ids_filter]
    
    print(f"Total questionnaire count: {len(user_ids)}")
    
    # Count Q8 response statistics
    q8_yes_count = 0
    q8_no_count = 0
    q8_no_answer_count = 0
    
    # Collect Q9 project information
    projects_info = []
    
    for user_id in user_ids:
        # Get all rows for this user (using first column)
        user_rows = df[df.iloc[:, 0] == user_id]
        
        # Check Q8 answers (Yes and No columns) - column indices need adjustment due to added Department/Region column
        yes_answers = user_rows.iloc[:, 3].dropna()  # Q8 Yes column (original column 2 + 1)
        no_answers = user_rows.iloc[:, 4].dropna()   # Q8 No column (original column 3 + 1)
        
        # Determine Q8 answer
        # Check if user has any 'Yes' response in the YES column
        has_yes_in_yes_column = any(yes_answers.str.lower() == 'yes')
        # Check if user has any 'Yes' response in the NO column (this means they checked NO)
        has_yes_in_no_column = any(no_answers.str.lower() == 'yes')
        
        # If user has 'Yes' in YES column, count as YES
        if has_yes_in_yes_column:
            q8_yes_count += 1
            # Collect Q9 project information
            project_name = user_rows.iloc[:, 5].dropna()  # Project name column (original column 4 + 1)
            if not project_name.empty:
                project_info = {
                    'user_id': user_id,
                    'department_region': user_rows.iloc[:, 1].dropna().iloc[0] if not user_rows.iloc[:, 1].dropna().empty else '',  # Added Department/Region column
                    'project_name': project_name.iloc[0],
                    'related_cpo': user_rows.iloc[:, 6].dropna().iloc[0] if not user_rows.iloc[:, 6].dropna().empty else '',
                    'web_link': user_rows.iloc[:, 7].dropna().iloc[0] if not user_rows.iloc[:, 7].dropna().empty else '',
                    'description': user_rows.iloc[:, 8].dropna().iloc[0] if not user_rows.iloc[:, 8].dropna().empty else '',
                    'country': user_rows.iloc[:, 9].dropna().iloc[0] if not user_rows.iloc[:, 9].dropna().empty else '',
                    'new_or_longstanding': user_rows.iloc[:, 10].dropna().iloc[0] if not user_rows.iloc[:, 10].dropna().empty else '',
                    'funding_source': user_rows.iloc[:, 11].dropna().iloc[0] if not user_rows.iloc[:, 11].dropna().empty else '',
                    'dc_code': user_rows.iloc[:, 12].dropna().iloc[0] if not user_rows.iloc[:, 12].dropna().empty else '',
                    'focus': user_rows.iloc[:, 13].dropna().iloc[0] if not user_rows.iloc[:, 13].dropna().empty else '',
                    'un_joint_programme': user_rows.iloc[:, 14].dropna().iloc[0] if not user_rows.iloc[:, 14].dropna().empty else ''
                }
                projects_info.append(project_info)
        elif has_yes_in_no_column:
            q8_no_count += 1
        else:
            # No clear answer, count as no answer
            q8_no_answer_count += 1
    
    # Calculate percentages
    total_responses = len(user_ids)
    q8_yes_percentage = (q8_yes_count / total_responses) * 100 if total_responses > 0 else 0
    q8_no_percentage = (q8_no_count / total_responses) * 100 if total_responses > 0 else 0
    q8_no_answer_percentage = (q8_no_answer_count / total_responses) * 100 if total_responses > 0 else 0
    
    # Statistical results
    results = {
        'total_questionnaires': total_responses,
        'q8_yes_count': q8_yes_count,
        'q8_no_count': q8_no_count,
        'q8_no_answer_count': q8_no_answer_count,
        'q8_yes_percentage': round(q8_yes_percentage, 2),
        'q8_no_percentage': round(q8_no_percentage, 2),
        'q8_no_answer_percentage': round(q8_no_answer_percentage, 2),
        'projects_info': projects_info
    }
    
    return results

def print_analysis_results(results):
    """
    Print analysis results
    
    Args:
        results: Result dictionary returned by analyze_q8q9_data function
    """
    print("\n=== Q8Q9 Survey Data Analysis Results ===")
    print(f"Total questionnaires: {results['total_questionnaires']} surveys")
    print(f"\nQ8 Response Statistics:")
    print(f"  Selected 'Yes' (providing funding support): {results['q8_yes_count']} surveys ({results['q8_yes_percentage']}%)")
    print(f"  Explicitly selected 'No': {results['q8_no_count']} surveys ({results['q8_no_percentage']}%)")
    print(f"  No answer: {results['q8_no_answer_count']} surveys ({results['q8_no_answer_percentage']}%)")
    
    print(f"\n=== Q9 Project Details (Total {len(results['projects_info'])} projects) ===")
    
    for i, project in enumerate(results['projects_info'], 1):
        print(f"\nProject {i}:")
        print(f"  User ID: {project['user_id']}")
        if project.get('department_region'):
            print(f"  Department/Region: {project['department_region']}")
        print(f"  Project Name: {project['project_name']}")
        if project['country']:
            print(f"  Country/Region: {project['country']}")
        if project['description']:
            # Limit description length for readability
            desc = project['description'][:200] + '...' if len(project['description']) > 200 else project['description']
            print(f"  Project Description: {desc}")
        if project['funding_source']:
            print(f"  Funding Source: {project['funding_source']}")
        if project['focus']:
            print(f"  Focus Area: {project['focus']}")
        if project['new_or_longstanding']:
            print(f"  Project Type: {project['new_or_longstanding']}")
        if project['web_link']:
            print(f"  Website Link: {project['web_link']}")
    
    # Project distribution statistics
    print(f"\n=== Project Statistical Analysis ===")
    
    # Statistics by country
    countries = [p['country'] for p in results['projects_info'] if p['country']]
    if countries:
        country_counts = {}
        for country in countries:
            country_counts[country] = country_counts.get(country, 0) + 1
        print(f"\nDistribution by Country/Region:")
        for country, count in sorted(country_counts.items()):
            print(f"  {country}: {count} projects")
    
    # Statistics by funding source
    funding_sources = [p['funding_source'] for p in results['projects_info'] if p['funding_source']]
    if funding_sources:
        funding_counts = {}
        for source in funding_sources:
            funding_counts[source] = funding_counts.get(source, 0) + 1
        print(f"\nDistribution by Funding Source:")
        for source, count in sorted(funding_counts.items()):
            print(f"  {source}: {count} projects")
    
    # Statistics by focus area
    focus_areas = [p['focus'] for p in results['projects_info'] if p['focus']]
    if focus_areas:
        focus_counts = {}
        for focus in focus_areas:
            focus_counts[focus] = focus_counts.get(focus, 0) + 1
        print(f"\nDistribution by Focus Area:")
        for focus, count in sorted(focus_counts.items()):
            print(f"  {focus}: {count} projects")

def analyze_q8q9_data_filtered(csv_file_path, region_filter=None):
    """
    Analyze Q8Q9 data with region filtering
    
    Args:
        csv_file_path: CSV file path
        region_filter: Region filter condition, if None or 'all' then no filtering
    
    Returns:
        dict: Dictionary containing statistical results
    """
    # Read CSV file, skip first two rows of descriptive information
    df = pd.read_csv(csv_file_path, skiprows=2)
    
    # If there's a region filter condition, filter data first
    if region_filter and region_filter != 'all':
        if 'Department/Region' in df.columns:
            df = df[df['Department/Region'] == region_filter]
        else:
            # If no Department/Region column, use second column
            df = df[df.iloc[:, 1] == region_filter]
    
    # Get all unique user IDs (first column)
    user_ids = df.iloc[:, 0].unique()
    # Filter out NaN values and header rows
    user_ids = [uid for uid in user_ids if pd.notna(uid) and str(uid).startswith('USR-')]
    
    # Count Q8 response statistics
    q8_yes_count = 0
    q8_no_count = 0
    q8_no_answer_count = 0
    
    # Collect Q9 project information
    projects_info = []
    
    for user_id in user_ids:
        # Get all rows for this user (using first column)
        user_rows = df[df.iloc[:, 0] == user_id]
        
        # Check Q8 answers (Yes and No columns)
        yes_answers = user_rows.iloc[:, 3].dropna()  # Q8 Yes column
        no_answers = user_rows.iloc[:, 4].dropna()   # Q8 No column
        
        # Determine Q8 answer
        has_yes_in_yes_column = any(yes_answers.str.lower() == 'yes')
        has_yes_in_no_column = any(no_answers.str.lower() == 'yes')
        
        if has_yes_in_yes_column:
            q8_yes_count += 1
            # Collect Q9 project information
            project_name = user_rows.iloc[:, 5].dropna()  # Project name column
            if not project_name.empty:
                project_info = {
                    'user_id': user_id,
                    'department_region': user_rows.iloc[:, 1].dropna().iloc[0] if not user_rows.iloc[:, 1].dropna().empty else '',
                    'project_name': project_name.iloc[0],
                    'related_cpo': user_rows.iloc[:, 6].dropna().iloc[0] if not user_rows.iloc[:, 6].dropna().empty else '',
                    'web_link': user_rows.iloc[:, 7].dropna().iloc[0] if not user_rows.iloc[:, 7].dropna().empty else '',
                    'description': user_rows.iloc[:, 8].dropna().iloc[0] if not user_rows.iloc[:, 8].dropna().empty else '',
                    'country': user_rows.iloc[:, 9].dropna().iloc[0] if not user_rows.iloc[:, 9].dropna().empty else '',
                    'new_or_longstanding': user_rows.iloc[:, 10].dropna().iloc[0] if not user_rows.iloc[:, 10].dropna().empty else '',
                    'funding_source': user_rows.iloc[:, 11].dropna().iloc[0] if not user_rows.iloc[:, 11].dropna().empty else '',
                    'dc_code': user_rows.iloc[:, 12].dropna().iloc[0] if not user_rows.iloc[:, 12].dropna().empty else '',
                    'focus': user_rows.iloc[:, 13].dropna().iloc[0] if not user_rows.iloc[:, 13].dropna().empty else '',
                    'un_joint_programme': user_rows.iloc[:, 14].dropna().iloc[0] if not user_rows.iloc[:, 14].dropna().empty else ''
                }
                projects_info.append(project_info)
        elif has_yes_in_no_column:
            q8_no_count += 1
        else:
            # No clear answer, default to no
            q8_no_answer_count += 1
    
    # Calculate percentages
    total_responses = len(user_ids)
    q8_yes_percentage = (q8_yes_count / total_responses) * 100 if total_responses > 0 else 0
    q8_no_percentage = (q8_no_count / total_responses) * 100 if total_responses > 0 else 0
    q8_no_answer_percentage = (q8_no_answer_count / total_responses) * 100 if total_responses > 0 else 0
    
    # Statistical results
    results = {
        'total_questionnaires': total_responses,
        'q8_yes_count': q8_yes_count,
        'q8_no_count': q8_no_count,
        'q8_no_answer_count': q8_no_answer_count,
        'q8_yes_percentage': round(q8_yes_percentage, 2),
        'q8_no_percentage': round(q8_no_percentage, 2),
        'q8_no_answer_percentage': round(q8_no_answer_percentage, 2),
        'projects_info': projects_info
    }
    
    return results

def main():
    """
    Main function
    """
    csv_file_path = "orignaldata/Q8Q9_basic_data.csv"
    
    try:
        # Analyze data
        results = analyze_q8q9_data(csv_file_path)
        
        # Print results
        print_analysis_results(results)
        
        # Save results to file
        output_file = "result/q8q9_analysis_results.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("Q8Q9 Survey Data Analysis Results\n")
            f.write("=" * 50 + "\n")
            f.write(f"Total questionnaires: {results['total_questionnaires']} surveys\n")
            f.write(f"Q8 selected 'Yes': {results['q8_yes_count']} surveys ({results['q8_yes_percentage']}%)\n")
            f.write(f"Q8 explicitly selected 'No': {results['q8_no_count']} surveys ({results['q8_no_percentage']}%)\n")
            f.write(f"Q8 no answer: {results['q8_no_answer_count']} surveys ({results['q8_no_answer_percentage']}%)\n\n")
            
            f.write(f"Q9 project details (total {len(results['projects_info'])} projects):\n")
            f.write("-" * 30 + "\n")
            
            for i, project in enumerate(results['projects_info'], 1):
                f.write(f"\nProject {i}:\n")
                f.write(f"  User ID: {project['user_id']}\n")
                if project.get('department_region'):
                    f.write(f"  Department/Region: {project['department_region']}\n")
                f.write(f"  Project Name: {project['project_name']}\n")
                if project['country']:
                    f.write(f"  Country/Region: {project['country']}\n")
                if project['description']:
                    f.write(f"  Project Description: {project['description']}\n")
                if project['funding_source']:
                    f.write(f"  Funding Source: {project['funding_source']}\n")
                if project['focus']:
                    f.write(f"  Focus Area: {project['focus']}\n")
                if project['new_or_longstanding']:
                    f.write(f"  Project Type: {project['new_or_longstanding']}\n")
                if project['web_link']:
                    f.write(f"  Website Link: {project['web_link']}\n")
        
        print(f"\nAnalysis results saved to: {output_file}")
        
    except FileNotFoundError:
        print(f"Error: File not found {csv_file_path}")
        print("Please ensure the CSV file is in the current directory")
    except Exception as e:
        print(f"Error occurred during analysis: {str(e)}")

if __name__ == "__main__":
    main()