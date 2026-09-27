import pandas as pd
import sys
from pathlib import Path
from loguru import logger


def test_pipeline_data_quality(df, config):
    """Run data quality tests on the final dataframe."""
    logger.info("Running data quality tests...")

    try:
        # 1. Check dataframe is not empty
        assert not df.empty, "Final dataset is empty!"

        # 2. Check anomalies and outliers were cleaned
        if 'AMT_INCOME_TOTAL' in df.columns:
            max_income = df['AMT_INCOME_TOTAL'].max()
            assert pd.isna(max_income) or max_income <= config['clean']['income_outlier_max'], "Income outliers were not cleaned properly!"

        if 'DAYS_EMPLOYED' in df.columns:
            assert config['clean']['days_employed_anomaly'] not in df['DAYS_EMPLOYED'].values, "DAYS_EMPLOYED anomaly was not cleaned properly!"

        # 3. Check expected derived columns exist
        expected_cols = [
            'EDUCATION_LEVEL', 'INCOME_GROUP', 'AGE', 'AGE_GROUP', 'AGE_GENDER_SEGMENT',
            'HOME_CAR_OWNERSHIP', 'CREDIT_INCOME_RATIO', 'CREDIT_INCOME_RATIO_GROUP',
            'YEARS_EMPLOYED', 'YEARS_EMPLOYED_GROUP', 'recent_prev_app_count',
            'refused_count', 'bureau_loan_count', 'total_bureau_debt',
            'DEBT_INCOME_RATIO', 'BURDEN_CAT'
        ]
        for col in expected_cols:
            if col not in df.columns:
                logger.warning(f"Expected column missing: {col}")
                assert False, f"Missing expected column: {col}"

        # 4. Check that merge filled NAs appropriately
        assert not df['recent_prev_app_count'].isna().any(), "recent_prev_app_count contains NaN values!"
        assert not df['refused_count'].isna().any(), "refused_count contains NaN values!"
        assert not df['total_bureau_debt'].isna().any(), "total_bureau_debt contains NaN values!"

        logger.info("All data quality tests passed successfully!")
    except AssertionError as e:
        logger.error(f"Data quality test failed: {e}")
        raise

