

def join_previous_application(df_app, df_prev, recent_application_days_threshold=-180):
    df_prev_summary = (df_prev
                   .query('DAYS_DECISION >= @recent_application_days_threshold')
                   .groupby('SK_ID_CURR')
                   .agg(
                       prev_app_count = ('SK_ID_PREV', 'size')
                   )
                  )
    
    df_app = (df_app
    .merge(df_prev_summary, on='SK_ID_CURR', how='left')
    .assign(prev_app_count = lambda x: x['prev_app_count'].fillna(0))
    )
    
    return df_app

def join_bureau(df_app, df_bureau):
    df_bureau_summary = (df_bureau
    .groupby("SK_ID_CURR")
    .agg(
        bureau_loan_count = ("SK_ID_BUREAU", "size"),
        total_bureau_debt = ("AMT_CREDIT_SUM_DEBT", "sum")
        )
    )

    df_app = (df_app
    .merge(df_bureau_summary, on="SK_ID_CURR", how="left")
    .assign(
        total_bureau_debt = lambda x: x["total_bureau_debt"].fillna(0),
        bureau_loan_count = lambda x: x["bureau_loan_count"].fillna(0)
        )
    )
    
    return df_app
