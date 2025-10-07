import streamlit as st
import os
import base64
import pandas as pd
import plotly.graph_objects as go

# Try to apply unified  page  style if available
try:
    from st_styles import apply_page_style, create_chart
    STYLES_AVAILABLE = True
except Exception:
    STYLES_AVAILABLE = False


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


def get_q2_data():
    """Load Q2 data from PART1_base_dataQ2-5.csv"""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        csv_path = os.path.join(project_root, 'orignaldata', 'PART1_base_dataQ2-5.csv')
        
        if os.path.exists(csv_path):
            df = safe_read_csv(csv_path)
            
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
            
            # Filter Q2 data
            q2_data = df[df['question'].str.contains('Q2:', na=False)]
            
            # Create data dictionary for chart
            data_dict = {}
            for _, row in q2_data.iterrows():
                option = str(row['option']).strip()
                count = int(row['count']) if pd.notna(row['count']) else 0
                data_dict[option] = count
            
            return data_dict
        else:
            return {}
    except Exception as e:
        st.error(f"Error loading Q2 data: {e}")
        return {}


def create_q2_chart(data):
    """Create Q2 pie chart with specified title"""
    if not data:
        return None
    
    title = "Distribution of Responses on Whether Entities Conducted Youth Employment Work in the Reference Period"
    
    if STYLES_AVAILABLE:
        try:
            return create_chart(data, 'pie', title)
        except Exception:
            pass
    
    # Fallback chart creation
    fig = go.Figure()
    
    categories = list(data.keys())
    values = list(data.values())
    colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']
    
    fig.add_trace(go.Pie(
        labels=categories,
        values=values,
        marker_colors=colors[:len(categories)],
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': title,
            'font': {'size': 14},
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'pad': {'b': 10}
        },
        height=400,
        paper_bgcolor='white',
        plot_bgcolor='white',
        font_family="Arial",
        margin=dict(t=60, b=20, l=20, r=20),
        autosize=True
    )
    
    return fig


def get_q345_data():
    """Load and process Q3, Q4, Q5 data to create summary table"""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        
        # Load data files
        q3_path = os.path.join(project_root, 'orignaldata', 'PART2_base_dataQ3.csv')
        q4_path = os.path.join(project_root, 'orignaldata', 'PART2_base_dataQ4.csv')
        q5_path = os.path.join(project_root, 'orignaldata', 'PART2_base_dataQ5.csv')
        
        # Initialize result dictionary
        result_data = {}
        
        # Process Q3 data
        if os.path.exists(q3_path):
            df_q3 = safe_read_csv(q3_path)
            
            # Apply global YEAR filter if available
            try:
                selected_year = st.session_state.get('selected_year', 'All')
                if selected_year != 'All':
                    # Check for both 'YEAR' and 'year' columns
                    if 'YEAR' in df_q3.columns:
                        df_q3 = df_q3[df_q3['YEAR'].astype(str).str.strip() == str(selected_year)]
                    elif 'year' in df_q3.columns:
                        df_q3 = df_q3[df_q3['year'].astype(str).str.strip() == str(selected_year)]
            except Exception:
                pass
            
            # Get unique departments
            departments = df_q3['Department/Region'].dropna().unique()
            
            # Initialize departments in result_data
            for dept in departments:
                if dept not in result_data:
                    result_data[dept] = {}
            
            q3_columns = [col for col in df_q3.columns if col not in ['UserId', 'Department/Region', 'year']]
            
            # Group by department and check for YES values
            for dept in departments:
                dept_data = df_q3[df_q3['Department/Region'] == dept]
                for col in q3_columns:
                    col_key = f"Q3_{col.strip()}"
                    # Check if any row for this department has YES for this column
                    has_yes = (dept_data[col].fillna('').str.upper() == 'YES').any()
                    result_data[dept][col_key] = "Yes" if has_yes else ""
        
        # Process Q4 data
        if os.path.exists(q4_path):
            df_q4 = safe_read_csv(q4_path)
            
            # Apply global YEAR filter if available
            try:
                selected_year = st.session_state.get('selected_year', 'All')
                if selected_year != 'All':
                    # Check for both 'YEAR' and 'year' columns
                    if 'YEAR' in df_q4.columns:
                        df_q4 = df_q4[df_q4['YEAR'].astype(str).str.strip() == str(selected_year)]
                    elif 'year' in df_q4.columns:
                        df_q4 = df_q4[df_q4['year'].astype(str).str.strip() == str(selected_year)]
            except Exception:
                pass
            
            departments = df_q4['Department/Region'].dropna().unique()
            
            # Initialize departments in result_data
            for dept in departments:
                if dept not in result_data:
                    result_data[dept] = {}
            
            q4_columns = [col for col in df_q4.columns if col not in ['UserId', 'Department/Region', 'year', 'Other', 'Other (elaborated answ)']]
            
            # Group by department and check for YES values
            for dept in departments:
                dept_data = df_q4[df_q4['Department/Region'] == dept]
                for col in q4_columns:
                    col_key = f"Q4_{col.strip()}"
                    # Check if any row for this department has YES for this column
                    has_yes = (dept_data[col].fillna('').str.upper() == 'YES').any()
                    result_data[dept][col_key] = "Yes" if has_yes else ""
        
        # Process Q5 data
        if os.path.exists(q5_path):
            df_q5 = safe_read_csv(q5_path)
            
            # Apply global YEAR filter if available
            try:
                selected_year = st.session_state.get('selected_year', 'All')
                if selected_year != 'All':
                    # Check for both 'YEAR' and 'year' columns
                    if 'YEAR' in df_q5.columns:
                        df_q5 = df_q5[df_q5['YEAR'].astype(str).str.strip() == str(selected_year)]
                    elif 'year' in df_q5.columns:
                        df_q5 = df_q5[df_q5['year'].astype(str).str.strip() == str(selected_year)]
            except Exception:
                pass
            
            departments = df_q5['Department/Region'].dropna().unique()
            
            # Initialize departments in result_data
            for dept in departments:
                if dept not in result_data:
                    result_data[dept] = {}
            
            q5_columns = [col for col in df_q5.columns if col not in ['UserId', 'Department/Region', 'year', 'Other', 'Other (elaborated answ)']]
            
            # Group by department and check for YES values
            for dept in departments:
                dept_data = df_q5[df_q5['Department/Region'] == dept]
                for col in q5_columns:
                    col_key = f"Q5_{col.strip()}"
                    # Check if any row for this department has YES for this column
                    has_yes = (dept_data[col].fillna('').str.upper() == 'YES').any()
                    result_data[dept][col_key] = "Yes" if has_yes else ""
        
        return result_data
        
    except Exception as e:
        st.error(f"Error loading Q3-Q4-Q5 data: {e}")
        return {}


def create_q345_table(data):
    """Create a formatted table for Q3-Q4-Q5 data"""
    if not data:
        return None
    
    # Convert to DataFrame
    df = pd.DataFrame.from_dict(data, orient='index')
    df = df.fillna("")
    
    # Reset index to make Department/Region a column
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'Department/Region'}, inplace=True)
    
    # Reorder columns to match the sample format
    q3_cols = [col for col in df.columns if col.startswith('Q3_')]
    q4_cols = [col for col in df.columns if col.startswith('Q4_')]
    q5_cols = [col for col in df.columns if col.startswith('Q5_')]
    
    # Create column order
    column_order = ['Department/Region'] + q3_cols + q4_cols + q5_cols
    df = df.reindex(columns=column_order)
    
    # Create proper column headers with question titles
    display_columns = ['Department/Region']
    
    # Add Q3 title row
    if q3_cols:
        display_columns.append('Q3: Please indicate the cluster(s) of the implementation framework relevant to your work on youth employment.')
        # Add empty columns for Q3 options (except the first one which has the title)
        for i in range(len(q3_cols) - 1):
            display_columns.append('')
    
    # Add Q4 title row  
    if q4_cols:
        display_columns.append('Q4: Please indicate the policy areas relevant to your work on youth employment.')
        # Add empty columns for Q4 options (except the first one which has the title)
        for i in range(len(q4_cols) - 1):
            display_columns.append('')
    
    # Add Q5 title row
    if q5_cols:
        display_columns.append('Q5: Please mark the youth groups targeted in your work on youth employment.')
        # Add empty columns for Q5 options (except the first one which has the title)
        for i in range(len(q5_cols) - 1):
            display_columns.append('')
    
    # Create a multi-level header structure
    # First create the title row
    title_row = [''] + ['Q3: Please indicate the cluster(s) of the implementation framework relevant to your work on youth employment.'] * len(q3_cols) + \
                ['Q4: Please indicate the policy areas relevant to your work on youth employment.'] * len(q4_cols) + \
                ['Q5: Please mark the youth groups targeted in your work on youth employment.'] * len(q5_cols)
    
    # Create option row (clean column names for display)
    option_row = ['Department/Region']
    for col in df.columns[1:]:
        if col.startswith('Q3_'):
            option_row.append(col.replace('Q3_', '').strip())
        elif col.startswith('Q4_'):
            option_row.append(col.replace('Q4_', '').strip())
        elif col.startswith('Q5_'):
            option_row.append(col.replace('Q5_', '').strip())
        else:
            option_row.append(col)
    
    # Create a new DataFrame with proper structure
    result_df = df.copy()
    result_df.columns = option_row
    
    # Add title information as metadata (we'll display it separately)
    result_df.attrs['q3_title'] = 'Q3: Please indicate the cluster(s) of the implementation framework relevant to your work on youth employment.'
    result_df.attrs['q4_title'] = 'Q4: Please indicate the policy areas relevant to your work on youth employment.'
    result_df.attrs['q5_title'] = 'Q5: Please mark the youth groups targeted in your work on youth employment.'
    result_df.attrs['q3_cols'] = len(q3_cols)
    result_df.attrs['q4_cols'] = len(q4_cols)
    result_df.attrs['q5_cols'] = len(q5_cols)
    
    return result_df


def create_html_table_with_headers(df, original_data):
    """Create HTML table with merged header cells for Q3, Q4, Q5 sections"""
    
    # Identify Q3, Q4, Q5 columns based on original data structure
    all_columns = df.columns.tolist()
    dept_col = 'Department/Region'
    data_columns = [col for col in all_columns if col != dept_col]
    
    # Get sample original data to identify column types
    sample_orig_keys = list(original_data[list(original_data.keys())[0]].keys())
    
    q3_cols = []
    q4_cols = []
    q5_cols = []
    
    for col in data_columns:
        # Check if this column corresponds to Q3, Q4, or Q5 in original data
        for orig_key in sample_orig_keys:
            if orig_key.startswith('Q3_') and orig_key.replace('Q3_', '').strip() == col:
                q3_cols.append(col)
                break
            elif orig_key.startswith('Q4_') and orig_key.replace('Q4_', '').strip() == col:
                q4_cols.append(col)
                break
            elif orig_key.startswith('Q5_') and orig_key.replace('Q5_', '').strip() == col:
                q5_cols.append(col)
                break
    
    # Count columns for each section
    q3_count = len(q3_cols)
    q4_count = len(q4_cols)
    q5_count = len(q5_cols)
    
    # Start building HTML table
    html = """
    <style>
    .q345-table {
        border-collapse: collapse;
        width: 100%;
        margin: 20px 0;
        font-family: Arial, sans-serif;
        font-size: 13px;
        table-layout: fixed;
    }
    .q345-table th, .q345-table td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
        vertical-align: top;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    .q345-table th {
        background-color: #f2f2f2;
        font-weight: bold;
    }
    .q345-table .title-header {
        background-color: #e6f3ff;
        font-weight: bold;
        text-align: center;
        font-size: 12px;
        padding: 6px;
    }
    .q345-table .dept-col {
        background-color: #f9f9f9;
        font-weight: bold;
        width: 160px;
        min-width: 160px;
        max-width: 160px;
    }
    .q345-table .option-header {
        background-color: #f8f8f8;
        font-size: 11px;
        text-align: center;
        padding: 6px;
        width: 100px;
        min-width: 100px;
        max-width: 100px;
    }
    .q345-table .data-cell {
        text-align: center;
        font-size: 12px;
        width: 100px;
        min-width: 100px;
        max-width: 100px;
    }
    .q345-table .percentage-row {
        background-color: #f0f8ff;
        font-weight: bold;
        font-style: italic;
    }
    .q345-table .percentage-cell {
        text-align: center;
        font-size: 12px;
        font-weight: bold;
        background-color: #f0f8ff;
        color: #0066cc;
    }
    </style>
    <table class="q345-table summary-table">
    """
    
    # Create title header row
    html += "<tr>"
    html += f'<th class="dept-col" rowspan="2">{dept_col}</th>'
    
    if q3_count > 0:
        html += f'<th class="title-header" colspan="{q3_count}">Q3: Please indicate the cluster(s) of the implementation framework relevant to your work on youth employment.</th>'
    
    if q4_count > 0:
        html += f'<th class="title-header" colspan="{q4_count}">Q4: Please indicate the policy areas relevant to your work on youth employment.</th>'
    
    if q5_count > 0:
        html += f'<th class="title-header" colspan="{q5_count}">Q5: Please mark the youth groups targeted in your work on youth employment.</th>'
    
    html += "</tr>"
    
    # Create column header row
    html += "<tr>"
    
    # Add Q3 column headers
    for col in q3_cols:
        html += f'<th class="option-header">{col}</th>'
    
    # Add Q4 column headers
    for col in q4_cols:
        html += f'<th class="option-header">{col}</th>'
    
    # Add Q5 column headers
    for col in q5_cols:
        html += f'<th class="option-header">{col}</th>'
    
    html += "</tr>"
    
    # Add data rows
    for _, row in df.iterrows():
        html += "<tr>"
        html += f'<td class="dept-col">{row[dept_col]}</td>'
        
        # Add Q3 data
        for col in q3_cols:
            value = row[col] if col in row else ""
            # Convert Yes/No to ○/× symbols
            if value == "Yes":
                display_value = "○"
            else:
                display_value = "×"  # No and empty values show as ×
            html += f'<td class="data-cell symbol-cell">{display_value}</td>'
        
        # Add Q4 data
        for col in q4_cols:
            value = row[col] if col in row else ""
            # Convert Yes/No to ○/× symbols
            if value == "Yes":
                display_value = "○"
            else:
                display_value = "×"  # No and empty values show as ×
            html += f'<td class="data-cell symbol-cell">{display_value}</td>'
        
        # Add Q5 data
        for col in q5_cols:
            value = row[col] if col in row else ""
            # Convert Yes/No to ○/× symbols
            if value == "Yes":
                display_value = "○"
            else:
                display_value = "×"  # No and empty values show as ×
            html += f'<td class="data-cell symbol-cell">{display_value}</td>'
        
        html += "</tr>"
    
    # Add percentage statistics row
    html += '<tr class="percentage-row">'
    html += '<td class="dept-col">Coverage Rate</td>'
    
    # Calculate and add Q3 percentages
    for col in q3_cols:
        total_count = len(df)
        yes_count = len(df[df[col] == "Yes"])
        percentage = round((yes_count / total_count * 100), 1) if total_count > 0 else 0
        html += f'<td class="percentage-cell">{percentage}%</td>'
    
    # Calculate and add Q4 percentages
    for col in q4_cols:
        total_count = len(df)
        yes_count = len(df[df[col] == "Yes"])
        percentage = round((yes_count / total_count * 100), 1) if total_count > 0 else 0
        html += f'<td class="percentage-cell">{percentage}%</td>'
    
    # Calculate and add Q5 percentages
    for col in q5_cols:
        total_count = len(df)
        yes_count = len(df[df[col] == "Yes"])
        percentage = round((yes_count / total_count * 100), 1) if total_count > 0 else 0
        html += f'<td class="percentage-cell">{percentage}%</td>'
    
    html += "</tr>"
    
    html += "</table>"
    
    return html


def get_base64_image(image_path):
    """Convert image to base64 string for embedding in HTML"""
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""


def create_layout():
    """Landing page with logo and dynamic year-based title"""
    if STYLES_AVAILABLE:
        try:
            apply_page_style()
        except Exception:
            pass

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
        margin-top: -5px;
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
    
    # Add Q2 pie chart as the first chart
    st.title("📊 Survey Overview")
    st.markdown("**Comprehensive overview of survey responses and key insights**")
    st.markdown("---")
    
    # Load and display Q2 data
    q2_data = get_q2_data()
    if q2_data:
        q2_chart = create_q2_chart(q2_data)
        if q2_chart:
            st.plotly_chart(q2_chart, use_container_width=True, config={'displayModeBar': False})
        else:
            st.error("Failed to create Q2 chart")
    else:
        st.warning("No Q2 data available")
    
    st.markdown("---")
    
    # Add Q3-Q4-Q5 summary table as the second chart
    st.subheader("📋 Q3-Q4-Q5 Summary Table")
    
    # Load and display Q3-Q4-Q5 data
    q345_data = get_q345_data()
    
    if q345_data:
        # Create table with proper formatting
        q345_df = create_q345_table(q345_data)
        
        if q345_df is not None and not q345_df.empty:
            html_table = create_html_table_with_headers(q345_df, q345_data)
            st.markdown(html_table, unsafe_allow_html=True)
        else:
            st.error("Failed to create Q3-Q4-Q5 table")
    else:
        st.warning("No Q3-Q4-Q5 data available")
    
    st.markdown("---")
    st.write("Use the sidebar to select year and navigate other dashboards.")