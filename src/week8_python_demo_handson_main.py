

from week8_python_demo_handson_config import DATA_DIR, DATABASE_FILE, DAYS_EMPLOYED_NA_VALUES, GENDER_MAPPING, AGE_BIN, AGE_BIN_LABEL, EDUCATION_MAPPING
from week8_python_demo_handson_stage_1_load_data import load_data
from week8_python_demo_handson_stage_2_clean_transform import clean_days_employed, clean_gender_code, set_age_bin, set_education_bin, set_age_gender_bin
from week8_python_demo_handson_stage_3_aggregate import join_previous_application, join_bureau


def main():
    print("Start loading data")
    df_app = load_data(DATABASE_FILE, "SELECT * FROM application")
    df_prev = load_data(DATABASE_FILE, "SELECT * FROM previous_application")
    df_bureau = load_data(DATABASE_FILE, "SELECT * FROM bureau")

    print("Start cleaning and transforming data")

    df_app = set_age_bin(df_app, AGE_BIN, AGE_BIN_LABEL)
    df_app = set_education_bin(df_app, EDUCATION_MAPPING)
    
    df_app = clean_days_employed(df_app, DAYS_EMPLOYED_NA_VALUES)
    df_app = clean_gender_code(df_app, GENDER_MAPPING)

    df_app = set_age_gender_bin(df_app)

    print("Start aggregating data")
    df_app = join_previous_application(df_app, df_prev, -180)
    df_app = join_bureau(df_app, df_bureau)

    print("Start saving data")
    df_app.to_csv(DATA_DIR / 'processed_application_data_exercise.csv', index=False)

    print("Data processing complete")

if __name__ == "__main__":
    main()
