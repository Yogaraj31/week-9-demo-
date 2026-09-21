""" Messy codes combining week 5 to week 7 data preparation for demo

"""
# %%
import pandas as pd
pd.set_option('display.max_columns', None) 

# %%
import sqlite3

# %%
# set to root of repo
from pathlib import Path

# %%
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

with sqlite3.connect(DATA_DIR / "home_credit.db") as conn:
    df_app = pd.read_sql_query(
        "SELECT * FROM application",
        conn,
    )

df_app.head()


# %%
# set age bins and labels for categorization
import numpy as np

df_app = (df_app
    .assign(AGE = lambda x: (-x['DAYS_BIRTH'] / 365).astype(int))
    .assign(AGE_GROUP = lambda x: pd.cut(x['AGE'], bins=[0, 25, 35, 45, 55, np.inf], labels=['0-25', '26-35', '36-45', '46-55', '56+'] ))
)


# %%
# Do mapping for education levels and create a new column EDUCATION_LEVEL_2
education_mapping = {
    'Lower secondary': 'Lower Education',
    'Secondary / secondary special': 'Lower Education',
    'Higher education': 'Higher Education',
    'Academic degree': 'Higher Education'
}

df_app = (df_app
    .assign(
        EDUCATION_LEVEL = lambda x: x['NAME_EDUCATION_TYPE']
            .map(education_mapping)
            .fillna('Lower Education') 
    )
)

# %%
# import previous application data
with sqlite3.connect(DATA_DIR / "home_credit.db") as conn:
    df_prev = pd.read_sql_query(
        "SELECT * FROM previous_application",
        conn,
    )

df_prev.head()

# %%
df_prev.sample(10)

# %%
# summarize previous application data to get count of recent applications per customer
df_prev_summary = (df_prev
                   .query('DAYS_DECISION >= -180')
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
    
# %%
# clean up the employee anomaly in DAYS_EMPLOYED by replacing it with NaN
df_app = (df_app
    .assign(DAYS_EMPLOYED = lambda x: x['DAYS_EMPLOYED'].replace(365243, pd.NA))
)

df_app.info()

# %%

# %%
# import bureau  data
with sqlite3.connect(DATA_DIR / "home_credit.db") as conn:
    df_bureau = pd.read_sql_query(
        "SELECT * FROM bureau",
        conn,
    )

df_bureau.head()

# %%
# summarize bureau data by SK_ID_CURR to get total debt and loan count
df_bureau_summary = (df_bureau
    .groupby("SK_ID_CURR")
    .agg(
        bureau_loan_count = ("SK_ID_BUREAU", "size"),
        total_bureau_debt = ("AMT_CREDIT_SUM_DEBT", "sum")
    )
)

# %%
# merge bureau summary with application data and fill missing values with 0
df_app = (df_app
    .merge(df_bureau_summary, on="SK_ID_CURR", how="left")
    .assign(
        total_bureau_debt = lambda x: x["total_bureau_debt"].fillna(0),
        bureau_loan_count = lambda x: x["bureau_loan_count"].fillna(0)
    )
)

# %%
# clean up xNA values in gender, I found they are actually captured as Female 
df_app = (df_app
          .assign(CODE_GENDER=lambda x: x['CODE_GENDER'].replace('XNA', 'F')))

# %%
# Add age x gender segment
df_app = (df_app
    .assign(
        AGE_GENDER_SEGMENT = df_app['AGE_GROUP'].case_when([
            ((df_app['AGE_GROUP'].isin(['0-25', '26-35'])) & (df_app['CODE_GENDER'] == 'M'), 'Young Male'),
            ((df_app['AGE_GROUP'].isin(['0-25', '26-35'])) & (df_app['CODE_GENDER'] == 'F'), 'Young Female'),
            (df_app['AGE_GROUP'].isin(['36-45', '46-55']), 'Middle-aged'),
            (df_app['AGE_GROUP'].isin(['56+']), 'Senior')
        ]).fillna('Unknown')
    )
)

print(df_app['AGE_GENDER_SEGMENT'].value_counts()) 


# %%
# Mike asked me to test this out new grouping method for age gender, we are not using it in the actual data prep steps
df_app = (df_app
    .assign(
        AGE_GENDER_SEGMENT2 = df_app['AGE_GROUP'].case_when([
            ((df_app['AGE_GROUP'].isin(['0-25', '26-35'])) & (df_app['CODE_GENDER'] == 'M'), 'Young Male'),
            ((df_app['AGE_GROUP'].isin(['0-25', '26-35'])) & (df_app['CODE_GENDER'] == 'F'), 'Young Female'),
            (df_app['AGE_GROUP'].isin(['36-45', '46-55']) & (df_app['CODE_GENDER'] == 'M'), 'Middle-aged Male'),
            (df_app['AGE_GROUP'].isin(['36-45', '46-55']) & (df_app['CODE_GENDER'] == 'F'), 'Middle-aged Female'),
            (df_app['AGE_GROUP'].isin(['56+']), 'Senior')
        ]).fillna('Unknown')
    )
)

df_app['AGE_GENDER_SEGMENT2'].value_counts()

# %%
# df_app.drop(columns=['AGE'])

# %%
#save the final table
df_app.to_csv(DATA_DIR / 'processed_application_data_exercise.csv', index=False)

