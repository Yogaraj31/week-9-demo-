import pandas as pd

def clean_days_employed(df_app, DAYS_EMPLOYED_NA_VALUES):
    df_app = (df_app
    .assign(DAYS_EMPLOYED = lambda x: x['DAYS_EMPLOYED'].replace(DAYS_EMPLOYED_NA_VALUES, pd.NA))
    )
    
    return df_app

def clean_gender_code(df_app, GENDER_MAPPING):
    df_app = (df_app
          .assign(CODE_GENDER=lambda x: x['CODE_GENDER'].map(GENDER_MAPPING)))
              
    return df_app

def set_age_bin(df_app, age_bin, age_bin_label):
    df_app = (df_app
    .assign(AGE = lambda x: (-x['DAYS_BIRTH'] / 365).astype(int))
    .assign(AGE_GROUP = lambda x: pd.cut(x['AGE'], bins=age_bin, labels=age_bin_label ))
    )
    
    return df_app

def set_education_bin(df_app, EDUCATION_MAPPING):
    df_app = (df_app
    .assign(
        EDUCATION_LEVEL = lambda x: x['NAME_EDUCATION_TYPE']
            .map(EDUCATION_MAPPING)
            .fillna('Lower Education') 
    )
    )
    
    return df_app

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