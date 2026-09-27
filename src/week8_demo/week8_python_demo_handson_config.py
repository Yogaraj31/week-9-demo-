from pathlib import Path
import numpy as np

# set relative path to data directory
DATA_DIR = Path(__file__).resolve().parent.parent.parent / 'data'

DATABASE_FILE = DATA_DIR / "home_credit.db"

# clean up the employee anomaly in DAYS_EMPLOYED by replacing it with NaN
DAYS_EMPLOYED_NA_VALUES = 365243

# gender mapping
GENDER_MAPPING = {
    'XNA': 'F',
    'M': 'M',
    'F': 'F'
}

# set age bins and labels for categorization
AGE_BIN = [0, 25, 35, 45, 55, np.inf]
AGE_BIN_LABEL = ['0-25', '26-35', '36-45', '46-55', '56+']

# Do mapping for education levels and create a new column EDUCATION_LEVEL_2
EDUCATION_MAPPING = {
    'Lower secondary': 'Lower Education',
    'Secondary / secondary special': 'Lower Education',
    'Higher education': 'Higher Education',
    'Academic degree': 'Higher Education'
}