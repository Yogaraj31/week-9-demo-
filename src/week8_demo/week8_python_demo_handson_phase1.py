""" Messy codes combining week 5 to week 7 data preparation for demo

"""
# %%
import pandas as pd
import numpy as np
from pathlib import Path
import sqlite3
pd.set_option('display.max_columns', None) 


# 1. LOAD DATA

# %%
# set relative path to data directory
DATA_DIR = Path(__file__).parent.parent  / 'data'
DATABASE_FILE = DATA_DIR / "home_credit.db"

# %%
def load_data(database_file_path, database_sql):
    
    with sqlite3.connect(database_file_path) as conn:
        df = pd.read_sql_query(
        database_sql,
        conn,
    )
    return df

# %%
# import application data
df_app = load_data(DATABASE_FILE, "SELECT * FROM application")

# %%
# import previous application data
df_prev = load_data(DATABASE_FILE, "SELECT * FROM previous_application")

# %%
# import bureau data
df_bureau = load_data(DATABASE_FILE, "SELECT * FROM bureau") 


# 2. CLEAN TRANSFORM DATA

# %%
# set age bins and labels for categorization

AGE_BIN = [0, 25, 35, 45, 55, np.inf]
AGE_BIN_LABEL = ['0-25', '26-35', '36-45', '46-55', '56+']

def set_age_bin(df_app, AGE_BIN, AGE_BIN_LABEL):
    df_app = (df_app
    .assign(AGE = lambda x: (-x['DAYS_BIRTH'] / 365).astype(int))
    .assign(AGE_GROUP = lambda x: pd.cut(x['AGE'], bins=AGE_BIN, labels=AGE_BIN_LABEL ))
)
    
    return df_app

df_app = set_age_bin(df_app, AGE_BIN, AGE_BIN_LABEL)


# %%
# Do mapping for education levels and create a new column EDUCATION_LEVEL

EDUCATION_MAPPING = {
    'Lower secondary': 'Lower Education',
    'Secondary / secondary special': 'Lower Education',
    'Higher education': 'Higher Education',
    'Academic degree': 'Higher Education'
}

def set_education_bin(df_app, EDUCATION_MAPPING):
    df_app = (df_app
    .assign(
        EDUCATION_LEVEL = lambda x: x['NAME_EDUCATION_TYPE']
            .map(EDUCATION_MAPPING)
            .fillna('Lower Education') 
    )
)
    
    return df_app

df_app = set_education_bin(df_app, EDUCATION_MAPPING)


# %%
# clean up the employee anomaly in DAYS_EMPLOYED by replacing it with NaN

DAYS_EMPLOYED_NA_VALUES = 365243


def clean_days_employed(df_app, DAYS_EMPLOYED_NA_VALUES):
    df_app = (df_app
    .assign(DAYS_EMPLOYED = lambda x: x['DAYS_EMPLOYED'].replace(DAYS_EMPLOYED_NA_VALUES, pd.NA))
)
    
    return df_app

df_app = clean_days_employed(df_app, DAYS_EMPLOYED_NA_VALUES)

df_app.info()

# %%
# clean up xNA values in gender, I found they are actually captured as Female 
# use dictionary to map the values

GENDER_MAPPING = {
    'XNA': 'F',
    'M': 'M',
    'F': 'F'
}

def clean_gender_code(df_app, GENDER_MAPPING):
    df_app = (df_app
          .assign(CODE_GENDER=lambda x: x['CODE_GENDER'].map(GENDER_MAPPING)))
              
    return df_app

df_app = clean_gender_code(df_app, GENDER_MAPPING)

# %%
# Add age x gender segment

def set_age_gender_bin(df_app):

    age_gender_bin = [
            ((df_app['AGE_GROUP'].isin(['0-25', '26-35'])) & (df_app['CODE_GENDER'] == 'M'), 'Young Male'),
            ((df_app['AGE_GROUP'].isin(['0-25', '26-35'])) & (df_app['CODE_GENDER'] == 'F'), 'Young Female'),
            (df_app['AGE_GROUP'].isin(['36-45', '46-55']), 'Middle-aged'),
            (df_app['AGE_GROUP'].isin(['56+']), 'Senior')
    ]
    
    df_app = (df_app
    .assign(
        AGE_GENDER_SEGMENT = df_app['AGE_GROUP'].case_when(age_gender_bin).fillna('Unknown')
    )
)
    
    return df_app

df_app = set_age_gender_bin(df_app)

print(df_app['AGE_GENDER_SEGMENT'].value_counts()) 


# 3. JOIN & AGGREGATE DATA

# %%
# summarize previous application data to get count of recent applications per customer

def join_previous_application(df_app, df_prev, recent_application_days_threshold=-180):
    df_prev_summary = (df_prev
                   .query('DAYS_DECISION >= @recent_application_days_threshold')
                   .groupby('SK_ID_CURR')
                   .agg(
                       prev_app_count = ('SK_ID_PREV', 'size')
                   )
                  )

# merge previous application summary with application data and fill missing values with 0
    df_app = (df_app
    .merge(df_prev_summary, on='SK_ID_CURR', how='left')
    .assign(prev_app_count = lambda x: x['prev_app_count'].fillna(0))
    )
    
    return df_app

df_app = join_previous_application(df_app, df_prev, -180)


# %%
# summarize bureau data by SK_ID_CURR to get total debt and loan count
def join_bureau(df_app, df_bureau):
    df_bureau_summary = (df_bureau
    .groupby("SK_ID_CURR")
    .agg(
        bureau_loan_count = ("SK_ID_BUREAU", "size"),
        total_bureau_debt = ("AMT_CREDIT_SUM_DEBT", "sum")
    )
)

# merge bureau summary with application data and fill missing values with 0
    df_app = (df_app
    .merge(df_bureau_summary, on="SK_ID_CURR", how="left")
    .assign(
        total_bureau_debt = lambda x: x["total_bureau_debt"].fillna(0),
        bureau_loan_count = lambda x: x["bureau_loan_count"].fillna(0)
    )
)
    
    return df_app

df_app = join_bureau(df_app, df_bureau)


# 4. SAVE DATA

# %%
#save the final table
df_app.to_csv(DATA_DIR / 'processed_application_data_exercise.csv', index=False)




