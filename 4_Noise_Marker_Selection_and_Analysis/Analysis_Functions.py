# analysis_functions.py
import pandas as pd
import numpy as np
from scipy.stats import levene
from statsmodels.stats.multitest import multipletests

def read_gct(file_path):
    """Read .gct file and process header columns."""
    df = pd.read_csv(file_path, sep='\t', skiprows=2)
    df.columns = [col.strip() for col in df.columns]
    return df

def order_by_age(df, age_order):
    """Categorize and sort data by age."""
    df['age'] = pd.Categorical(df['age'], categories=age_order, ordered=True)
    return df.sort_values('age')

def contains_age_20(value):
    """Check if '20' is in age value."""
    return '20' in str(value)

def contains_age_60_or_70(value):
    """Check if '60' or '70' is in age value."""
    return '60' in str(value) or '70' in str(value)

def levene_test_between_groups(young_group_df, old_group_df):
    """Perform Levene's test between two age groups."""
    p_values = []
    for protein in young_group_df.index:
        young_vals = young_group_df.loc[protein].dropna()
        old_vals = old_group_df.loc[protein].dropna()
        stat, p_value = levene(young_vals, old_vals)
        p_values.append(p_value)
    #adjusted_p_values = multipletests(p_values, alpha=0.1, method='fdr_bh')[1]
    return pd.DataFrame({'p_value': p_values, 'protein': young_group_df.index})

def calculate_cv(data):
    """Calculate coefficient of variation."""
    mean_val = np.mean(data)
    std_dev = np.std(data)
    return std_dev / mean_val if mean_val != 0 else np.nan

def calculate_cv_ratio(young_group_df, old_group_df):
    """Calculate CV ratio between two age groups."""
    cv_ratios = []
    for protein in young_group_df.index:
        young_cv = calculate_cv(young_group_df.loc[protein])
        old_cv = calculate_cv(old_group_df.loc[protein])
        cv_ratios.append(old_cv / young_cv if young_cv != 0 else np.nan)
    return cv_ratios
