import pandas as pd

def load_and_clean_data(file_path):
    """
    Loads the dataset and performs basic cleaning.
    Converts dates to datetime objects and handles missing values.
    """
    df = pd.read_csv(file_path)
    
    # Convert 'date' column to datetime format if it exists
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        
    # Fill missing numeric values with 0 and categorical with 'Unknown'
    numeric_cols = df.select_dtypes(include=['number']).columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    
    df[numeric_cols] = df[numeric_cols].fillna(0)
    df[categorical_cols] = df[categorical_cols].fillna('Unknown')
    
    return df

def filter_by_date(df, start_date, end_date):
    """
    Filters the DataFrame based on a specified date range.
    """
    if 'date' in df.columns:
        mask = (df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)
        return df.loc[mask]
    return df

def filter_by_category(df, column_name, selected_category):
    """
    Filters the DataFrame by a single category selection.
    """
    if selected_category and selected_category != 'All':
        return df[df[column_name] == selected_category]
    return df

def filter_by_multiselect(df, column_name, selected_categories):
    """
    Filters the DataFrame allowing multiple category selections.
    """
    if selected_categories:
        return df[df[column_name].isin(selected_categories)]
    return df

def filter_by_numerical_range(df, column_name, min_val, max_val):
    """
    Filters the DataFrame strictly within a numerical range.
    """
    return df[(df[column_name] >= min_val) & (df[column_name] <= max_val)]

def filter_by_text_search(df, column_name, search_keyword):
    """
    Filters the DataFrame based on a text search keyword (case-insensitive).
    """
    if search_keyword:
        return df[df[column_name].str.contains(search_keyword, case=False, na=False)]
    return df