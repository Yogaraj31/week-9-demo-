# %% [markdown]
# # Week 6 : From Raw Tables to One Customer Feature Dataset
#
# Last week, we learned how to load, inspect, filter, and investigate a DataFrame.
#
# This week, we use those skills to answer a new question:
#
# > Can a customer's current application and previous application history help us
# > understand their default risk?
#
# ## Today's workflow
#
# **READ → PREDICT → MODIFY → RUN → VERIFY**
#
# 1. Apply Week 5 investigation skills to `df_prev`
# 2. Create useful features from `df_app`
# 3. Aggregate previous-application history to one row per customer
# 4. Left-merge the history features back to `df_app`
# 5. Hands-on activities
#
# We are not trying to memorise every method. Focus on the flow:
#
# **raw data → inspect → transform → aggregate → merge → investigate → result**


# %% [markdown]
# ## 0. Load the Two Tables
#
# ### Data grain
#
# | DataFrame | One row represents | Key |
# |---|---|---|
# | `df_app` | one current application/customer | `SK_ID_CURR` |
# | `df_prev` | one previous application | `SK_ID_PREV` |
#
# One customer can have zero, one, or many previous applications.
#
# ```text
# df_app:  one customer       → one row
# df_prev: one customer       → zero, one, or many rows
# ```





# %%
import pandas as pd
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

pd.set_option("display.max_columns", None)
pd.options.display.float_format = "{:.2f}".format

df_app = pd.read_csv(DATA_DIR / "application_train_s1.csv")
df_prev = pd.read_csv(DATA_DIR / "previous_application_s1.csv")



# %% [markdown]
# # Part 1 - Week 5 recap: Investigate `df_prev`
#
# Before we create features, first understand the raw table.


# %% [markdown]
# 1A. Preview the first 10 rows of `df_prev`
 
# %%
# Put your code below
df_prev.head(10)

# %% [markdown]
# 1B. Get the number of rows and columns in `df_prev`
# 1C. Also get a list of column names in `df_prev`


# %%
# Put your code below
# 1B:
df_prev.shape

# %%
# 1C:
df_prev.columns
 

# %% [markdown]
# 1D. Which columns in `df_prev` have missing values,
# 1E. Which columns are text vs numerical?

# %%
# Put your code below
# 1D:
df_prev.info()

# 1E: NAME_CONTRACT_TYPE, NAME_CONTRACT_STATUS, CHANNEL_TYPE are text
# the rest are numerical


# %% [markdown]
# 1F. What are the minimum and maximum values of `AMT_CREDIT` in `df_prev`?


# %%
# 1F:
df_prev["AMT_CREDIT"].describe()

# %%
# Put your code below
# 1F alternative
print(df_prev["AMT_CREDIT"].min())
print(df_prev["AMT_CREDIT"].max())


# %% [markdown]
# 1G. How many unique values are there in `CHANNEL_TYPE` in `df_prev`?
#

# %%
# Put your code below
# 1G:
df_prev["CHANNEL_TYPE"].describe(include = "str")

# %%
# 1G alternative:
df_prev["CHANNEL_TYPE"].value_counts(dropna=False)

# %%
# 1G alternative:
print(df_prev["CHANNEL_TYPE"].unique())
print(df_prev["CHANNEL_TYPE"].nunique())


# %% [markdown]
# 1H: Extract 3 columns from `df_prev`: `SK_ID_CURR`, `AMT_CREDIT`, and `CHANNEL_TYPE`

# %%
# Put your code below
 
df_prev[['SK_ID_CURR', 'AMT_CREDIT', 'CHANNEL_TYPE']]
 

 # %% [markdown]
# 1I. Convert the following SQL to pandas

# ```sql
# SELECT
#     "SK_ID_CURR",
#     "SK_ID_PREV",
#     "DAYS_DECISION",
#     "NAME_CONTRACT_STATUS"
# FROM previous_application
# WHERE "DAYS_DECISION" >= -180;
# ```
  
 # %%
 # Put your code below
df_prev.loc[
df_prev["DAYS_DECISION"] >= -180,
    ["SK_ID_CURR", "SK_ID_PREV", "DAYS_DECISION", "NAME_CONTRACT_STATUS"]
]
 

 # %% [markdown]
# # Homework — Data investigation Challenge
#
# You are reviewing the Home Credit dataset before it is used for analysis.
#
# Find **two potential data issues or unusual features** that should be investigated further.
#
# 1. a raw value that needs transformation to be human-readable
# 2. a possible placeholder or coding rule
# 3. a missing value that may be a business signal
# 4. a possible outlier

# %% [markdown]
# Write down your findings

df_app.info()

# %%
# Example: columns with missing values
# Is it okay for it to be missing?
df_app[["FLAG_OWN_CAR", "OWN_CAR_AGE"]]

# %%
# Example: columns with negative values
# Let's convert them to human readable values
df_app["DAYS_BIRTH"]

 # %% [markdown]
# # Part 2 - Create Features from the Current Application
#
# We now return to `df_app`, where one row already represents one customer.
#
# The raw columns are not always directly useful for business analysis. We will create:
#
# 1. `AGE` - a readable value from `DAYS_BIRTH`
# 2. `AGE_GROUP` - an easier business grouping
# 3. `INCOME_TYPE` - broader income categories
 

# %% [markdown]
# ## Skill 1 - Create a readable age feature using `.assign()`
#
# SQL equivalent:
#
# ```sql
# SELECT
#     "DAYS_BIRTH",
#     CAST(-"DAYS_BIRTH" / 365 AS INTEGER) AS age
# FROM application;
# ```
#
# **PREDICT:** A customer has `DAYS_BIRTH = -7300`. What value will `AGE` contain?
#
# In pandas, we use `.assign()` to create a new feature or variable.
#
# `lambda x:` means: take the current DataFrame, call it `x`, and use it to calculate something.
#
# `.astype(int)` converts the result to an integer.

# %%
df_app = (
    df_app
    .assign(
        AGE=lambda x: (-x["DAYS_BIRTH"] / 365).astype(int)
    )
)

df_app[["SK_ID_CURR", "DAYS_BIRTH", "AGE"]].head()

# %% [markdown]
# **VERIFY:** Pick one row. Does `-DAYS_BIRTH / 365` approximately equal `AGE`?


# %% [markdown]
# ## Skill 2 - Group numeric values with `pd.cut()`
#
# Exact ages are useful for modeling, but groups are easier to communicate and compare.
#
# SQL equivalent:
#
# ```sql
# SELECT
#     CASE
#         WHEN age <= 25 THEN '18-25'
#         WHEN age <= 35 THEN '26-35'
#         WHEN age <= 45 THEN '36-45'
#         WHEN age <= 55 THEN '46-55'
#         ELSE '56+'
#     END AS age_group
# FROM application;
# ```
#
# In pandas, we can use `pd.cut()` to convert numeric values into bands.
# 
# For example, `pd.cut(0, 25, 35, np.inf)` returns the following:
#
#  - By default, pandas uses intervals that are **open on the left** and **closed on the right**:
#
# - `(0, 25]` means greater than 0 and up to 25
# - `(25, 35]` means greater than 25 and up to 35
# - `(35, np.inf]` means greater than 35
#
# The round bracket `(` means the value is excluded.
# The square bracket `]` means the value is included.
#
#
# **PREDICT:** Which group should an age of 45 belong to?



# %%
age_bins = [18, 25, 35, 45, 55, np.inf]
age_labels = ["18-25", "26-35", "36-45", "46-55", "56+"]

df_app = (
    df_app
    .assign(
        AGE_GROUP=lambda x: pd.cut(
            x["AGE"],
            bins=age_bins,
            labels=age_labels,
            include_lowest=True
        )
    )
)

df_app[["AGE", "AGE_GROUP"]].head(10)

#
# include_lowest=True means the first bin includes the lowest value (18 in example above).
#
# - `[18,25]` instead of `(18, 25]`


# %%
df_app["AGE_GROUP"].value_counts(dropna=False).sort_index()


# Check that no values are left out in the binning (missing values)

# %% [markdown]
# **MODIFY:** Change the upper boundary in `age_bins` by replacing `np.inf` with `60`.
#
# Before running, predict what the result might look like.

# %%
age_bins = [18, 25, 35, 45, 55, 60]
age_labels = ["18-25", "26-35", "36-45", "46-55", "55-60"]

df_app = (
    df_app
    .assign(
        AGE_GROUP2=lambda x: pd.cut(
            x["AGE"],
            bins=age_bins,
            labels=age_labels,
            include_lowest=True
        )
    )
)

df_app[["AGE", "AGE_GROUP2"]].head(10)

# %%
df_app["AGE_GROUP2"].value_counts(dropna=False).sort_index()

# there is missing values for age > 60 because we did not include them in the binning

# %% [markdown]
# ## Skill 3 - Simplify categories with `.map()`
#
# SQL equivalent:
#
# ```sql
# SELECT
#     CASE
#         WHEN "NAME_INCOME_TYPE" IN ('Working', 'Commercial associate',
#                                     'State servant', 'Businessman')
#             THEN 'Working'
#         WHEN "NAME_INCOME_TYPE" = 'Pensioner'
#             THEN 'Retired'
#         ELSE 'Not working'
#     END AS income_type
# FROM application;
# ```
#
# In Python, a mapping dictionary tells Python how to translate old values into new values.
#
# In this example, we map detailed income types into broader business groups:
#
# - `"Working"`
# - `"Retired"`
# - `"Not working"`
#
# Values that are not found in the dictionary will become missing after `.map()`.
#
# **PREDICT:** What will happen to a detailed income type that is not in the mapping?
#


# %%
income_mapping = {
    "Working": "Working",
    "Commercial associate": "Working",
    "State servant": "Working",
    "Businessman": "Working",
    "Pensioner": "Retired"
}

df_app = (
    df_app
    .assign(
        INCOME_TYPE=lambda x: x["NAME_INCOME_TYPE"].map(income_mapping)
    )
)

df_app[["NAME_INCOME_TYPE", "INCOME_TYPE"]].head(30)

# %%
df_app["INCOME_TYPE"].value_counts(dropna=False)

# %%
# this is to check which NAME_INCOME_TYPE are not mapped
df_app.loc[df_app["INCOME_TYPE"].isna(), ["NAME_INCOME_TYPE"]
]


# %% [markdown]
# Notice that some values are missing from the mapping?
# We can use `.fillna("Not working")` to assign a default group for unmapped values.

# %%
df_app = (
    df_app
    .assign(
        INCOME_TYPE=lambda x: x["NAME_INCOME_TYPE"].map(income_mapping).fillna("Not working")
    )
)

df_app["INCOME_TYPE"].value_counts(dropna=False)

# %% [markdown]
# ## Skill 4 - Aggregate values by group
#
# We have created 3 risk features:
# 1. `AGE` - a readable feature from `DAYS_BIRTH`
# 2. `AGE_GROUP` - a business band for age
# 3. `INCOME_TYPE` - a broader income group
#
# Let's see whether `AGE_GROUP` is an important risk segment for credit default.
#
# Since `TARGET = 1` means default, the mean of `TARGET` is the default rate.
#
# SQL equivalent:
#
# ```sql
# SELECT
#     age_group,
#     COUNT(*) AS customer_count,
#     AVG("TARGET") AS default_rate
# FROM application
# GROUP BY age_group;
# ```
#
# In pandas, we use `.groupby()` and `.agg()` for equivalent functionality.
#
# >.agg(aggregated_column_name = ("column_name", "aggregation_method"))
#
# Aggregation method:
# 1. `size` counts the number of rows in each group (similar to SQL `COUNT(*)`)
# 2. `count` counts the number of non-missing values in each group (similar to SQL `COUNT(column)`)
# 3. `mean` calculates the mean of the values in each group (similar to SQL `AVG(column)`)
# 4. `sum` calculates the sum of the values of each group (similar to SQL `SUM(column)`)
#
# **PREDICT:** What will the result look like for the following code?

# %%
age_default_summary = (
    df_app
    .groupby("AGE_GROUP")
    .agg(
        customer_count=("SK_ID_CURR", "size"),
        default_rate=("TARGET", "mean")
    )
    .assign(default_rate=lambda x: x["default_rate"].round(4))
    .reset_index()
)

age_default_summary

# What insights can you find from this table?


# %% [markdown]
# ## Hands-on activity #1 [5 mins]
# Analyze `INCOME_TYPE` to see if it is a useful risk segment.

# %%
# Write your code below
INCOME_TYPE_summary = (
    df_app
    .groupby("INCOME_TYPE")
    .agg(
        customer_count=("SK_ID_CURR", "size"),
        default_rate=("TARGET", "mean")
    )
    .assign(default_rate=lambda x: x["default_rate"].round(4))
    .reset_index()
)
INCOME_TYPE_summary



# What insights can you find from this table?

# %% [markdown]
# ## Hands-on activity #2 [20 mins]
#
# Recall the credit-to-income ratio that we calculated in Week 5.
#
# Method chain: `.assign()`, `pd.cut()`, `.groupby()`, and `.agg()` to analyze whether a credit-to-income ratio is a good indicator of default risk.
#


# %%
# Write your code below
#
# 1. Create a new column `CREDIT_INCOME_RATIO` = `AMT_CREDIT` / `AMT_INCOME_TOTAL`
#
df_app = (
    df_app
    .assign(CREDIT_INCOME_RATIO=lambda x: x["AMT_CREDIT"] / x["AMT_INCOME_TOTAL"])
)

df_app[["AMT_CREDIT", "AMT_INCOME_TOTAL", "CREDIT_INCOME_RATIO"]].head()

# %%
# 2. Use the following thresholds to cut the ratio:
# 3. Create a new column called `CREDIT_INCOME_GROUP` from `AMT_CREDIT` and `AMT_INCOME_TOTAL`

ratio_bins = [0, 1, 2, 3, 4, 5, 7, np.inf]
ratio_labels = ["<1x", "1x-2x", "2x-3x", "3x-4x", "4x-5x", "5x-7x", "7x+"]

df_app = (
    df_app
    .assign(
        CREDIT_INCOME_GROUP=lambda x: pd.cut(
            x["CREDIT_INCOME_RATIO"],
            bins=ratio_bins,
            labels=ratio_labels,
            include_lowest=True
        )
    )
)

df_app[["CREDIT_INCOME_RATIO", "CREDIT_INCOME_GROUP"]].head(10)


# %%

# 4. Group by `CREDIT_INCOME_GROUP` and calculate the `size` (customer count) and `mean` of `TARGET` (default rate).

CREDIT_INCOME_GROUP_summary = (
    df_app
    .groupby("CREDIT_INCOME_GROUP")
    .agg(
        customer_count=("SK_ID_CURR", "size"),
        default_rate=("TARGET", "mean")
    )
    .assign(default_rate=lambda x: x["default_rate"].round(4))
    .reset_index()
)
CREDIT_INCOME_GROUP_summary


# 5. What insights can you find from this table?


# %% [markdown]
# # Part 3 - Aggregate Previous Applications to Customer Level
#
# `df_prev` has many rows for a customer, but our final dataset needs one row per
# customer. We therefore create features and then aggregate them by `SK_ID_CURR`.
#
# So that we can join the previous application features to the current application table
# without creating duplicated rows
#
# Let's create a simple record-level flags:
#
# - `RECENT_PREV_APP`: application decided in the last 180 days
#
# Business question: Does having a recent application indicates a higher risk of default?


# %%
df_prev.head()

# %%
# Create a column flag with True if the customer has a recent previous application
df_prev = (
    df_prev
    .assign(
        RECENT_PREV_APP=lambda x: x["DAYS_DECISION"] >= -180
    )
)

# %%
(
df_prev
    .get(["SK_ID_CURR", "SK_ID_PREV", "DAYS_DECISION", "NAME_CONTRACT_STATUS",
     "RECENT_PREV_APP"])
     .sort_values("SK_ID_CURR", ascending=True)
    .head(50)
)

# %%
# **Goal:** Create one row per `SK_ID_CURR`.
prev_customer_summary = (
    df_prev
    .groupby("SK_ID_CURR")
    .agg(
        previous_application_count=("SK_ID_PREV", "size"),
        recent_previous_application_count=("RECENT_PREV_APP", "sum")      
    )
    .reset_index()
    
    )

prev_customer_summary.head(10)

# **VERIFY**: Do the 2 new columns look correct?

# %% [markdown]
# # Part 4 - Merge Previous History into the Current Application Dataset
#
# We now have two customer-level DataFrames:
#
# - `df_app`: current application features
# - `prev_customer_summary`: previous-application features
#
# We use a left merge to keep every current applicant, including those with no
# recorded previous application.


# %% [markdown]
# ## Skill 5 - Left merge with `.merge()`
#
# SQL equivalent:
#
# ```sql
# SELECT
#     app.*,
#     prev.previous_application_count,
#     prev.recent_previous_application_count
# FROM application_features AS app
# LEFT JOIN previous_application_summary AS prev
#     ON app."SK_ID_CURR" = prev."SK_ID_CURR";
# ```
#
# **PREDICT:** What will happen to a current applicant with no matching row in
# `prev_customer_summary`?

# %%
df_combined = (
    df_app
    .merge(prev_customer_summary, on="SK_ID_CURR", how="left")
)

df_combined.head()


# %% [markdown]
# ### Verify the merge before using the data
#
# A customer-level left merge should not change the number of rows in `df_app`.

# %%
print("Rows in df_app:", len(df_app))
print("Rows in prev_customer_summary:", len(prev_customer_summary))
print("Rows in df_combined:", len(df_combined))

# %%
(
    df_combined
        .info()
)

# %%
(
    df_combined.describe()
)

# %% [markdown]
# ## Skill 6 - Fill missing values with `.fillna()`
#
# After the left merge, a missing count means that the customer has no matching
# previous-application record in this dataset. For a count feature, we can treat
# this as zero.
#
# SQL equivalent:
#
# ```sql
# COALESCE(previous_application_count, 0) AS previous_application_count
# ```
#
# In pandas, we use `.fillna()` to replace missing values with zero.
# 



# %%
df_combined = (
    df_combined
    .assign(
        previous_application_count=lambda x: x["previous_application_count"].fillna(0),
        recent_previous_application_count=lambda x: x["recent_previous_application_count"].fillna(0)
    )
)

(
df_combined
    .get(["previous_application_count", "recent_previous_application_count"])
    .describe()
)

# **PREDICT**: Does having more recent applications mean a higher-risk customer?

# %% [markdown]
# ## Hands-on activity #3: Code fixing [10 mins]
# Fix the code below to check whether recent previous application counts are
# indicative of the default rate.
#
# *HINT: There are 2 mistakes in the code below.*


# %%
prev_count_bins = [-np.inf, 0, 1, 2, 5, 10, np.inf]
prev_count_labels = ["0", "1", "2", "3-5", "6-10", "10+"]

recent_previous_application_risk_summary = (
    df_combined  # df_app is incorrect because it is the original df, does not contain the recent previous application count
    .assign(
        recent_previous_application_count_group=lambda x: pd.cut(
            x["recent_previous_application_count"],
            bins=prev_count_bins,
            labels=prev_count_labels
        ),
    )
    .groupby("recent_previous_application_count_group")  # this variable name needs to match with the binning variable name in previous steps
    .agg(
        count=("SK_ID_CURR", "size"),
        default_rate=("TARGET", "mean")
    )
    .assign(default_rate=lambda x: x["default_rate"].round(4))
    .reset_index()
)

recent_previous_application_risk_summary

# After fixing the codes, discuss:
# 1. Which previous-application group has the highest default rate?
# 2. Is the relationship monotonic?
# 3. Are there groups with small volume?
# 4. Would you use this feature in a dashboard or model?



# %% [markdown]
# # Part 5 - Hands-on feature engineering and analysis [25 mins]
#
#
# Group 1:
# - Create the features `YEARS_SINCE_REGISTRATION` and `YEARS_SINCE_ID_PUBLISH` from `DAYS_REGISTRATION` and `DAYS_ID_PUBLISH`
# - Group them into business bands and study whether the distribution of years since registration and years since ID publish is useful for risk monitoring.
#
# Group 2:
# - Create the income band `INCOME_GROUP` from `AMT_INCOME_TOTAL`
# - Create the education group `EDUCATION_LEVEL` from `NAME_EDUCATION_TYPE`
# - Study whether the income and education bands are useful risk segments.
#
# Group 3:
# - Create `APPROVED_PREV_APP`: in `df_prev`, count how many times a customer's previous applications had status `Approved` in `NAME_CONTRACT_STATUS`
# - Aggregate at the customer level before joining back to `df_combined`
# - Check that no additional rows are created after joining
# - Create a band and study whether this feature is useful as a risk segment.


# %% [markdown]
# ## Activity 5.1: Create features from `DAYS_REGISTRATION` and `DAYS_ID_PUBLISH`
#


# %%
# 1. Create a new column called `YEARS_SINCE_REGISTRATION` from `DAYS_REGISTRATION`  
# 2. Create a new column called `YEARS_SINCE_ID_PUBLISH` from `DAYS_ID_PUBLISH`

df_combined = (
    df_combined
    .assign(
        YEARS_SINCE_REGISTRATION=lambda x: (-x["DAYS_REGISTRATION"] / 365).astype(int),
        YEARS_SINCE_ID_PUBLISH=lambda x: (-x["DAYS_ID_PUBLISH"] / 365).astype(int)
    )
)

# 3. Check the correct mapping and decide how to group them into bins.
(df_combined
    .get(["DAYS_REGISTRATION", "YEARS_SINCE_REGISTRATION", "DAYS_ID_PUBLISH", "YEARS_SINCE_ID_PUBLISH"])
    .describe()
)

# %%
# 4. Suggested grouping below for `YEARS_SINCE_REGISTRATION`
YEARS_SINCE_REGISTRATION_bins = [0, 5, 10, 15, 20, np.inf]
YEARS_SINCE_REGISTRATION_labels = ["0-5 years", "5-10 years", "10-15 years", "15-20 years",  "20+ years"]

# 5. Create a new business band called `YEARS_SINCE_REGISTRATION_GROUP` from `YEARS_SINCE_REGISTRATION`

df_combined = (
    df_combined
    .assign(YEARS_SINCE_REGISTRATION_GROUP = lambda x: pd.cut(
        x["YEARS_SINCE_REGISTRATION"],
        bins=YEARS_SINCE_REGISTRATION_bins,
        labels=YEARS_SINCE_REGISTRATION_labels,
        include_lowest=True
    ))
)


# 6. Study `YEARS_SINCE_REGISTRATION_GROUP` to see if it is a useful risk segment.
(
    df_combined
    .groupby(["YEARS_SINCE_REGISTRATION_GROUP"])
    .agg(
        count=("SK_ID_CURR", "size"),
        default_rate=("TARGET", "mean")
      )
      .assign(default_rate=lambda x: x["default_rate"].round(4))
      .reset_index()
)


# %%
# 7. Suggested grouping below for `YEARS_SINCE_ID_PUBLISH`
YEARS_SINCE_ID_PUBLISH_bins = [0, 4, 8, 10, 12, np.inf]
YEARS_SINCE_ID_PUBLISH_labels = ["0-4 years", "4-8 years", "8-10 years", "10-12 years",  "12+ years"]

# 8. Create a new business band called `YEARS_SINCE_ID_PUBLISH_GROUP` from `YEARS_SINCE_ID_PUBLISH`
df_combined = (
    df_combined
    .assign(YEARS_SINCE_ID_PUBLISH_GROUP = lambda x: pd.cut(
        x["YEARS_SINCE_ID_PUBLISH"],
        bins=YEARS_SINCE_ID_PUBLISH_bins,
        labels=YEARS_SINCE_ID_PUBLISH_labels,
        include_lowest=True
    ))
)

# 9. Study `YEARS_SINCE_ID_PUBLISH_GROUP` to see if it is a useful risk segment.
(
    df_combined
    .groupby(["YEARS_SINCE_ID_PUBLISH_GROUP"])
    .agg(
        count=("SK_ID_CURR", "size"),
        default_rate=("TARGET", "mean")
      )
      .assign(default_rate=lambda x: x["default_rate"].round(4))
      .reset_index()
)

# What insights can you find from this table?

# %% [markdown]
# ## Activity 5.2: Create income and education segments from `AMT_INCOME_TOTAL` and `NAME_EDUCATION_TYPE`
#



# %%
# 1. Suggested grouping below for `AMT_INCOME_TOTAL`

income_bins = [0, 100000, 150000, 200000, np.inf]
income_labels = [
    "Low Income",
    "Medium Income",
    "High Income",
    "Very High Income"
]


# 2. Create a new business band called `INCOME_GROUP` from `AMT_INCOME_TOTAL`
df_combined = (
    df_combined
    .assign(
        INCOME_GROUP=lambda x: pd.cut(
            x["AMT_INCOME_TOTAL"],
            bins=income_bins,
            labels=income_labels,
            include_lowest=True
        )
    )
)

# What insights can you find from this table?

# %%
# 3. Check how many rows were not assigned to a group
income_group_summary = (
    df_combined["INCOME_GROUP"]
    .value_counts(dropna=False)
    .sort_index()
    .reset_index()
)

income_group_summary

# %%
# 4. Study `INCOME_GROUP` to see if it is a useful risk segment.
# %%
income_default_summary = (
    df_combined
    .groupby("INCOME_GROUP")
    .agg(
        count=("SK_ID_CURR", "size"),
        default_rate=("TARGET", "mean")
    )
    .assign(default_rate=lambda x: x["default_rate"].round(4))
    .reset_index()
)

income_default_summary

# What insights can you find from this table?


# %%
# 5. Suggested mapping below for `NAME_EDUCATION_TYPE`
education_mapping = {
    "Lower secondary": "Lower Education",
    "Secondary / secondary special": "Lower Education",
    "Higher education": "Higher Education",
    "Academic degree": "Higher Education"
}

# 6. Create a new band called `EDUCATION_LEVEL` from `NAME_EDUCATION_TYPE`
df_combined = (
    df_combined
    .assign(
        EDUCATION_LEVEL=lambda x: x["NAME_EDUCATION_TYPE"]
        .map(education_mapping)
        .fillna("Other")
    )
)


# %%
# 7. Check how many rows were not assigned to a group

df_combined["EDUCATION_LEVEL"].value_counts(dropna=False)

# %%
# 8. Study `EDUCATION_LEVEL` to see if it is a useful risk segment.
education_default_summary = (
    df_combined
    .groupby("EDUCATION_LEVEL")
    .agg(
        count=("SK_ID_CURR", "size"),
        default_rate=("TARGET", "mean")
    )
    .assign(default_rate=lambda x: x["default_rate"].round(4))
    .reset_index()
)

education_default_summary

# What insights can you find from this table?

# %% [markdown]
# ## Activity 5.3: Create an approved-previous-applications segment from `df_prev`

# %%
# 1. Create a new boolean column called `APPROVED_PREV_APP` from `NAME_CONTRACT_STATUS` in `df_prev`
df_prev_1 = (
    df_prev
    .assign(
        APPROVED_PREV_APP=lambda x: x["NAME_CONTRACT_STATUS"] == 'Approved'
    )
)

# 2. Check if `APPROVED_PREV_APP` is calculated correctly
(
df_prev_1
    .get(["SK_ID_CURR", "SK_ID_PREV", "DAYS_DECISION", "NAME_CONTRACT_STATUS",
     "APPROVED_PREV_APP"])
     .sort_values("SK_ID_CURR", ascending=True)
    .head(50)
)

# %%
# 3. Create an aggregated column called `approved_prev_app_count` from `APPROVED_PREV_APP` 
# by summing up the values. Store this a new dataframe.
prev_customer_summary_1 = (
    df_prev_1
    .groupby("SK_ID_CURR")
    .agg(
        approved_prev_app_count=("APPROVED_PREV_APP", "sum")
    )
    .reset_index()
)

prev_customer_summary_1.head(10)

# %%
# 4. Left join the new dataframe back to `df_combined` and fill missing values with 0.
df_combined = (
    df_combined
    .merge(prev_customer_summary_1, on="SK_ID_CURR", how="left")
    .assign(approved_prev_app_count = lambda x: x["approved_prev_app_count"].fillna(0))
)

# 5. Check that the left join did not change the number of rows in `df_combined`
df_combined.shape

# %%
# 6. Suggested grouping below for `approved_prev_app_count`
approved_prev_app_count_bins = [0, 1, 2, 3, 4, 5, 6,  np.inf]
approved_prev_app_count_label = ["0-1", "1-2", "2-3", "3-4", "4-5", "5-6", "6+"]

# 7. Create a new business band called `APPROVED_PREV_APP_GROUP` from `approved_prev_app_count`
df_combined = (
    df_combined
    .assign(APPROVED_PREV_APP_GROUP = lambda x: pd.cut(
        x["approved_prev_app_count"],
        bins=approved_prev_app_count_bins,
        labels=approved_prev_app_count_label,
        include_lowest=True
    ))
)

# 8. Study `APPROVED_PREV_APP_GROUP` to see if it is a useful risk segment.
(
    df_combined
    .groupby(["APPROVED_PREV_APP_GROUP"])
    .agg(
        count=("SK_ID_CURR", "size"),
        default_rate=("TARGET", "mean")
    )
    .assign(default_rate=lambda x: x["default_rate"].round(4))
    .reset_index()
)

# What insights can you find from this table?

# %% [markdown]
# ## Skill 7: Save the analysis-ready dataset with `to_csv(...)`
#
# In a professional workflow, we often save the transformed dataset so it can be reused
# in the next step: visualization, dashboarding, modeling, or AI-assisted reporting.


# %%

output_path = DATA_DIR / "week6_application_features.csv"

df_combined.to_csv(output_path, index=False)

print("Saved file to:", output_path)


# %% [markdown]
# ## Week 6 Wrap-Up
#
# Today, we moved from raw data inspection to feature engineering.
#
# Key message:
#
# **Data transformation is not just syntax. It is business judgement encoded in Python.**
#
# We used pandas to:
#
# - create readable features
# - group values into business bands
# - simplify categories
# - compare default rates
# - merge customer history
# - build a reusable output dataset
#
# numerical features created:
# - AGE
# - YEARS_SINCE_REGISTRATION 
# - YEARS_SINCE_ID_PUBLISH 
# - CREDIT_INCOME_RATIO
# - previous_application_count
# - recent_previous_application_count
# - approved_prev_app_count
#
# categorical features created:
# - AGE_GROUP
# - INCOME_TYPE
# - CREDIT_INCOME_GROUP 
# - YEARS_SINCE_REGISTRATION_GROUP
# - YEARS_SINCE_ID_PUBLISH_GROUP
# - INCOME_GROUP 
# - EDUCATION_LEVEL 
# - recent_previous_application_count_group
# - APPROVED_PREV_APP_GROUP



# %% [markdown]
# ## 3. SQL Thinking vs pandas Method Chaining
#
# Many Week 6 steps are familiar from SQL.
#
# The difference is that pandas lets us build a repeatable Python workflow.
#
# | Task | SQL | pandas |
# |---|---|---|
# | Create new column | `AS` | `.assign()` |
# | Map categories | `CASE WHEN value IN (...)` | `.map()` |
# | Bin numeric values | `CASE WHEN amount < ...` | `pd.cut()` |
# | Filter rows | `WHERE` | `.query()`, `.loc[]` |
# | Group data | `GROUP BY` | `.groupby()` |
# | Aggregate metrics | `COUNT`, <br> `AVG`, `SUM` | `.value_counts()` or  `.agg()` |
# | Join tables | `LEFT JOIN` | `.merge(..., how="left")` |
# | Fill missing values | `COALESCE()` | `.fillna()` |

# %% [markdown]
# ## Let's commit your changes to the script to your GitHub repository.
# 
# Step 1. Stage the changes
# Step 2. Write a commit message
# Step 3. Commit the changes
# Step 4. Synchronize your local repository with the remote repository

