# %% [markdown]
# # Week 5: Python & pandas — From SQL to Data Investigation
#
# You already know how to work with data using SQL.
#
# You have learned how to:
# - SELECT columns
# - WHERE / filter rows
# - create calculated values
# - investigate unusual values
# - GROUP BY and summarise data
#
# This week, we are **not starting data analysis again**.
#
# We are learning how Python and pandas express many of the same data skills.
#
# Use `#` (in Python) instead of `--` (in SQL) to comment out code.
#
# ### Workflow
# **READ → PREDICT → MODIFY → RUN → VERIFY**
#
# As more skills are unlocked, we will combine them to investigate real business data.


# %% [markdown]
# # **Part 1: Get Started with Python**
#
# In this part, we will learn how to run Python code in VS Code.

# %% [markdown]
# ## Skill 1 — Run Python Code
#
# There are two ways to run Python code in VS Code:
#
# ### 1. Interactive Window: run cell by cell
#
# When you run a cell, Python automatically displays the value of
# the last expression in that cell. You do not need to use `print()`.
#
# This is useful when exploring data and checking results while developing code.

# %%
"Hello Python"

# %% [markdown]
# ### 2. Run a Python file
#
# Running a Python file runs the code from top to bottom in the terminal.
#
# To see a value, use `print()` explicitly.
#
# This is useful when you want a repeatable script that can be run again.

# %%
print("Hello Python")


# %% [markdown]
# For now, remember:
#
# - `"Hello Python"` → the Interactive Window displays the result
# - `print("Hello Python")` → asks Python to print the result
#
# We will use both.


# %% [markdown]
# ### Text value in Python
#
# Python uses quotes to represent text value.
#
# Single quotes `' '` and double quotes `" "` both work:
#
# Unlike SQL that uses only Single quotes for text values.
#
# ```python
# "Motor"
# 'Motor'
# ```


# %%
print("Hello")

# %% [markdown]
# **MODIFY:** Change `"Hello"` to PRINT your own message.

# %%
# Type your code below:
print("Python is fun!")




# RUN & VERIFY: Did you get what you expected?


# %% [markdown]
# ## Skill 2 — Store Information in Variables
#
# Python can store a value and give it a name. This is called a **variable**.
#
# We use '=' to assign a value to a variable.

# %%
premium = 1000

print(premium)



# %% [markdown]
# ### Unlike SQL
#
# In SQL, we used double quotes for column names:
#
# ```sql
# SELECT "Premium"
# FROM data;
# ```
#
# Python variable names do not need quotes:
#
# ```python
# premium = 1000
# ```
#
# ⚠️ Python is case-sensitive:
#
# `premium`, `Premium`, and `PREMIUM` are different names.


# %% [markdown]
# **PREDICT:** What will `discounted_premium` below contain?

# %%
premium = 1000
discount = 0.20

discounted_premium = premium * (1 - discount)

print(discounted_premium)


# %% [markdown]
# ### SQL comparison
#
# ```sql
# SELECT
#     "PREMIUM_AMOUNT",
#     "PREMIUM_AMOUNT" * (1 - 0.20) AS discounted_premium
# FROM insurance_data;
# ```
#
# The arithmetic idea is the same.
#
# **MODIFY:** Change the discount from 20% to 30%.
#
# Before running, predict the result.


# %%
# Type your code below:
premium = 1000
discount = 0.30

discounted_premium = premium * (1 - discount)

discounted_premium





# RUN & VERIFY: Did you get what you expected?



# %% [markdown]
# ## Skill 3 — Understand Basic Python Data Types
#
# Common Python types:
#
# | Python | Meaning | Similar SQL type |
# |---|---|---|
# | `str` | Text | TEXT / VARCHAR |
# | `int` | Whole number | INTEGER |
# | `float` | Decimal number | NUMERIC |
# | `bool` | True / False | BOOLEAN |
#
# Use `type()` to check the type of a value.


# %%
product = "Motor"
policy_count = 100
loss_ratio = 0.61
profitable = True

print(type(product))
print(type(policy_count))
print(type(loss_ratio))
print(type(profitable))


# %% [markdown]
# **PREDICT:** What happens if we change:
#
# ```python
# policy_count = 100
# ```
#
# to:
#
# ```python
# policy_count = "100"
# ```
#
# Will Python still consider it an integer?


# %%
# Try it here
policy_count = "100"

print(type(policy_count))




# %% [markdown]
# ## Skill 4 — Store Multiple Values in a List
#
# A Python **list** stores several values together.
#
# Lists use square brackets `[]`.


# %%
insurance_types = ["Motor", "Travel", "Property"]

print(insurance_types)


# %% [markdown]
# **MODIFY:** Add `"Health"` to the list.


# %%
# Try it here
insurance_types = ["Motor", "Travel", "Property", "Health"]

print(insurance_types)


# %% [markdown]
# Why do we care about lists?
#
# Soon we will use a list such as:
#
# ```python
# ["AGE", "AMT_INCOME_TOTAL", "TARGET"]
# ```
#
# to tell pandas which rows, columns, or list of values we want.




# %% [markdown]
# # **Part 2: Load & Inspect Data**
#
# We now have enough basic Python to start working with tables using pandas.
# > Refer back to slides for introduction of business context


# %% [markdown]
# ## Skill 5 — Load a Table into pandas
#
# In SQL, we work with **tables**.
#
# In Python pandas, the main table structure is called a **DataFrame**.
#
# | SQL | pandas |
# |---|---|
# | Table | DataFrame |
# | Column | A DataFrame column; becomes a **Series** when selected individually |
# | Row | A row; usually becomes a **Series** when selected individually |
# | Row identifier | Index |

# %% [markdown]
# ## Data descriptions:
#
# Visit [Kaggle Home Credit Default dataset](https://www.kaggle.com/competitions/home-credit-default-risk/overview)
#
# Browse the HomeCredit_columns_description.csv, focusing on: 
# application_{train|test}.csv
#
# A simplified table "application_train_s1.csv" is provided in NTULearn folder.
#
# We will use this for our class demo. 

# %%
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

df = pd.read_csv(
    PROJECT_ROOT / "data" / "application_train_s1.csv"
)

pd.set_option("display.max_columns", None)

df


# %% [markdown]
# ### Import libraries
# We use import to bring in methods and functions from other libraries.
#
# You do not need to memorise the `Path` code today.
#
# The important part is:
#
# ```python
# df = pd.read_csv(...)
# ```
# 
# ### Method
# We use . to access something beloing to a variable (in this case pd library)
#
# Followed by the method name (in this case read_csv)
#
# Method usually ends with (), with the arguments inside the ()
#
# ### Dataframe variable
# We loaded the CSV into a DataFrame and stored it in the variable `df`.
#
# Versus SQL where normally we would not store the result in a variable.
#
# We can name the DataFrame anything we like. In this demo, we call the table `df`.
#
# We can retrieve the dataframe by using `df` again.
#
# ### Row index
# Notice a row label is created by default (0,1,2...), this is called `index`` of the row.
# Similar to Excel's row number but it starts from 0

# %% [markdown]
# ## Skill 6 — Preview the Data
#
# You already know:
#
# ```sql
# SELECT *
# FROM insurance_data
# LIMIT 10;
# ```
#
# In pandas:
#
# Use `df.head(10)` to show the df's first 10 rows.



# %%
df.head(10)

# %% [markdown]
# **PREDICT:** What happens if we change `10` to `5`?
#
# **MODIFY → RUN → VERIFY**


# %%
# Try it here
df.head(5)

# %%
df.tail(5)

# %%
df.sample(5)



# %% [markdown]
# ## Skill 7 — Understand the Structure of the Data
#
# Before analysing unfamiliar data, we first need to understand what we have.


# %% [markdown]
# `df.shape` returns:
#
# ```text
# (number of rows, number of columns)
# ```
#
# Notice we do not need to use () for shape?
#
# That is because shape is a attribute of the variable, not a method


# %%
df.shape



# How many rows and columns does the table df contain?


# %% [markdown]
# What variables are available?
#
# Use `df.columns` to see df's column names.

# %%
df.columns



# %% [markdown]
# `df.info()` helps us inspect:
# - columns
# - data types
# - number of non-missing values
#
# **INVESTIGATE:** Can you already see columns that may contain missing values?


# %%
df.info()

# %% [markdown]
# `df.isna().sum()` helps us inspect the number of missing values for each column.
#
# isna() is similar to SQL's `IS NULL`
#
# df.isna().sum() is similar to SQL's `COUNT(*) WHERE "column" IS NULL`

# %%
df.isna().sum()

# %% [markdown]
# `df.describe()` helps us inspect:
# - distribution of values 

# %%
# describe distribution of numerical columns
df.describe()


# INVESTIGATE: what potential data issues we may need to address?
#
# Look for missing values, outliers, and unusual values.

# %%
# describe distribution of text/string columns
df.describe(include ="str")

# INVESTIGATE: what potential data issues we may need to address?
#
# Look for columns with large number of unique values.




# %% [markdown]
# ## Skill 8 — Select One Column
#
# SQL:
#
# ```sql
# SELECT "AMT_INCOME_TOTAL"
# FROM data;
# ```
#
# In pandas, use `df["AMT_INCOME_TOTAL"]` to select a column.
#
# We need to use double quotes here to insert the text label of the column; 
# it is not a variable


# %%
df["AMT_INCOME_TOTAL"]



# %% [markdown]
# Same data skill, different syntax.
#
# **MODIFY:** Select `CODE_GENDER` instead.


# %%
# Write your code below
df["CODE_GENDER"]



# %% [markdown]
# ## Skill 9 — Select Multiple Columns
#
# SQL:
#
# ```sql
# SELECT
#     "SK_ID_CURR",
#     "AMT_INCOME_TOTAL"
# FROM data;
# ```
#
# In pandas:
#
# We will use a Python list (from Skill 4) to tell pandas which columns to return.
#
# ```python
# ["SK_ID_CURR", "AMT_INCOME_TOTAL"]
# ```

# %%
df[["SK_ID_CURR", "AMT_INCOME_TOTAL"]]


# %% [markdown]
# **MODIFY:** Add `NAME_INCOME_TYPE`.


# %%
# Write your code below

df[["SK_ID_CURR", "AMT_INCOME_TOTAL", "NAME_INCOME_TYPE"]]





# %% [markdown]
# ## Skill 10 — Investigate Values in a Column
#
# Before analysing `CODE_GENDER`, we want to know:
#
# **What values actually appear in this field?**

# %% [markdown]
# ### SQL comparison
#
# ```sql
# SELECT
#     "CODE_GENDER",
#     COUNT(*)
# FROM data
# GROUP BY "CODE_GENDER";
# ```
# 
# In pandas:
#
# `value_counts()` is a convenient pandas shortcut for investigating one categorical column.
#
# To include missing values in the count, use `dropna=False`.
#
# **PREDICT:** What values would you normally expect `CODE_GENDER` to contain?


# %%
df["CODE_GENDER"].value_counts(dropna=False)


# **RUN:** Do you notice anything unexpected?

# %% [markdown]
# Notice there is no row index created in the result?
#
# That is because the result is not stored as panda dataframe, but as a pandas series
#
# With row index being `CODE_GENDER` values, instead of usual 0,1,2...
#
# To force the result to be a dataframe, we use `.reset_index()`


# %%
df["CODE_GENDER"].value_counts(dropna=False).reset_index()



# %% [markdown]
# **MODIFY:** Investigate the following columns using the same pattern.
# 1. `"NAME_EDUCATION_TYPE"`
# 2. `"NAME_FAMILY_STATUS"`
# 3. `"OCCUPATION_TYPE"`

# %%
# Write your code below
df["NAME_EDUCATION_TYPE"].value_counts(dropna=False).reset_index()

# %%
df["NAME_FAMILY_STATUS"].value_counts(dropna=False).reset_index()

# %%
df["OCCUPATION_TYPE"].value_counts(dropna=False).reset_index()




# Any data issues to call out?


# %% [markdown]
# # **Part 3: Investigate What We Find**
#
# In this part, we will learn how to use pandas to investigate data.

# %% [markdown]
# ## Skill 11 — Create a Condition
#
# We found a suspicious value in `CODE_GENDER`. We want to filter rows for this value.
#
# In SQL:
#
# ```sql
# WHERE "CODE_GENDER" = 'XNA'
# ```
#
# First, let's see what a condition does in pandas.
#
# In Python, We use `==` to compare values versus `=` to assign values


# %%
df["CODE_GENDER"] == "XNA"


# %% [markdown]
# **PREDICT before running:** Does this return the customer records?
#
# Notice that pandas checks the condition for **every row** and returns:
#
# ```text
# True
# False
# False
# ...
# ```
#
# This is called a **Boolean mask**.


# %% [markdown]
# ## Skill 12 — Filter Rows with `.loc`
#
# Now use the condition to return the actual records.
#
# SQL:
#
# ```sql
# SELECT *
# FROM data
# WHERE "CODE_GENDER" = 'XNA';
# ```
#
# In, pandas:
#
# Think of:
#
# ```python
# df.loc[condition]
# ```
#
# as: **locate the rows of df where the condition is True.**



# %%
df.loc[df["CODE_GENDER"] == "XNA"]

# %%
df.loc[df["CODE_GENDER"] == "XNA"].reset_index()


# %% [markdown]
# **MODIFY:** Find records where `AMT_INCOME_TOTAL > 500000`.


# %%
# Write your code below
df.loc[df["AMT_INCOME_TOTAL"] > 500000]





# RUN & VERIFY: How many rows & columns did you get?

# %% [markdown]
# ## Skill 13 — Filter Rows AND Select Columns
#
# SQL:
#
# ```sql
# SELECT
#     "SK_ID_CURR",
#     "CODE_GENDER"
# FROM data
# WHERE "CODE_GENDER" = 'XNA';
# ```
#
# In pandas:
# 
# ```python
# df.loc[
#     row_condition,
#     columns_to_return
# ]
# ```
# will locate the rows of df where the row_condition is True.
# Then return the columns_to_return.


# %%
df.loc[
    df["CODE_GENDER"] == "XNA",
    ["SK_ID_CURR", "CODE_GENDER"]
]



# %% [markdown]
# **MODIFY:** Find customers with `AMT_INCOME_TOTAL > 500000`.
#
# Return:
# - `SK_ID_CURR`
# - `AMT_INCOME_TOTAL`
# - `NAME_INCOME_TYPE`


# %%
# Write your code below
df.loc[df["AMT_INCOME_TOTAL"] > 500000,
       ["SK_ID_CURR","AMT_INCOME_TOTAL","NAME_INCOME_TYPE"]
]



# RUN & VERIFY: How many rows & columns did you get?

# %% [markdown]
# ## Skill 14 — Combine Multiple Conditions
#
# SQL:
#
# ```sql
# WHERE "AMT_INCOME_TOTAL" > 200000
#   AND "TARGET" = 1
# ```
#
# pandas:
#
# - `&` means AND
# - `|` means OR
#
# Each condition needs parentheses.
#
# **PREDICT:** What does one returned row represent below?


# %%
df.loc[
    (df["AMT_INCOME_TOTAL"] > 200000) & (df["TARGET"] == 1),
    ["SK_ID_CURR", "AMT_INCOME_TOTAL", "TARGET"]
]


# %% [markdown]
# **MODIFY:** Change the income threshold from 200,000 to 100,000,000.
# 
# Select `SK_ID_CURR`, `AMT_INCOME_TOTAL`, `TARGET`, and `OCCUPATION_TYPE`.
#
# Does this customer's high income makes sense based on its occupation?


# %%
# Write your code below

df.loc[df['AMT_INCOME_TOTAL'] > 100000000,
       ['SK_ID_CURR', 'AMT_INCOME_TOTAL', 'TARGET', 'OCCUPATION_TYPE']
       ]




# **RUN & VERIFY**


# %% [markdown]
# # Hands On  — Data Detective
#
# One field records `DAYS_EMPLOYED`.
#
# Before using it for analysis, you want to check whether its values make business sense.
#
# ### Step 1 — Inspect


# %%
df["DAYS_EMPLOYED"].describe()


# %% [markdown]
# ### Step 2 — Predict
# In data description,
# `DAYS_EMPLOYED` represents "How many days before the application
#  the person started current employment".
#
# - What range of values would you reasonably expect?
# - Is anything in the summary surprising?
#
# Discuss with your partner before writing more code.
#
# ### Step 3 — Investigate
#
# Can you filter the records that appear suspicious?
#
# **Hint:** Which unlocked skill allows you to filter rows using a condition?
#
# # You may find these useful:
#
# - `.loc[]`
# - `.value_counts()`
# - selecting columns


# %%
# Write your investigation below

df.loc[df['DAYS_EMPLOYED'] > 0]






# Investigate:
#
# 1. How many records are affected?
# 2. Do the suspicious records share the same value?
# 3. Does the value make business sense?




# %% [markdown]
# ### Step 4 — Verify
#
# Is this:
#
# A. definitely a data error?  
# B. a special coding convention?  
# C. something we need to investigate further?
#
# Would you immediately delete these records? Why or why not?

# %% [markdown]
# # **Part 4 — Sneak Peek of Week 6 Data Transformation**
#
# In this part, we will learn how to transform raw columns into useful analytical features.
# And using method chaining to combine steps.


# %% [markdown]
# ## Skill 15 — Create a New Column
#
# SQL:
#
# ```sql
# SELECT
#     "AMT_CREDIT",
#     "AMT_INCOME_TOTAL",
#     "AMT_CREDIT" / "AMT_INCOME_TOTAL" AS credit_income_ratio
# FROM data;
# ```
#
# In pandas:
# `df["CREDIT_INCOME_RATIO"] = ...` creates or replaces a column called `CREDIT_INCOME_RATIO`.
#


# %%
df["CREDIT_INCOME_RATIO"] = (
    df["AMT_CREDIT"] / df["AMT_INCOME_TOTAL"]
)


# %%
df[
    [
        "AMT_CREDIT",
        "AMT_INCOME_TOTAL",
        "CREDIT_INCOME_RATIO",
    ]
].head()

# %%
df.shape


# **VERIFY:** Pick one row and check:
#
# ```text
# AMT_CREDIT / AMT_INCOME_TOTAL
# ```
#
# Does it approximately equal `CREDIT_INCOME_RATIO`?


# %% [markdown]
# ## Skill 16 — Build a pandas Chain
#
# We have learned several individual pandas operations.
#
# pandas allows us to connect operations together:
#
# **DATA → FILTER → SELECT → PREVIEW → RESULT**
#
# This is called **method chaining**.
#
# The operation looks similar to a SQL query. Instead of inside-out in SQL,
# it reads top-to-bottom.
#
#
# Let's see how we can use it to build a pandas chain.


# %%
# Run this sequentially by uncomment each new line
result = (
    df
    .assign(CREDIT_INCOME_RATIO2 =lambda x: (x["AMT_CREDIT"] / x["AMT_INCOME_TOTAL"]).round(2))
    .query("CREDIT_INCOME_RATIO2 > 3")
    .get(["NAME_INCOME_TYPE"])
    .value_counts(dropna=False)
    .reset_index()
    .rename(columns={"count": "customer_count"})
    .sort_values(by="customer_count", ascending=True)
    .head(5)
)

result


# %% [markdown]
# ### Preview: Where We Are Going
#
# The dataframe result previous steps is **not being replaced**, but continues with the next operation.
#
# Don't worry about memorising all the syntax yet.
#
# Some methods below are new, such as `.assign()`, `.query()`, and `.get()`.
# We will learn what they do by using them repeatedly.
#
# Focus first on the **flow of the analysis**:
#
# **DataFrame → transform → filter → select → summarise → result**
#
# This method-chaining pattern is the pandas style we will use going forward.



# %% [markdown]
# # Reflection: Week 5 — Skills Unlocked
#
# ### Part 1 — Get Started with Python
# 1. Run Python code
# 2. Variables
# 3. Data types
# 4. Lists
#
# ### Part 2 — Load & Inspect Data
# 5. Load a DataFrame
# 6. Preview data
# 7. Inspect structure
# 8. Select one column
# 9. Select multiple columns
# 10. Investigate categorical values
#
# ### Part 3 — Investigate What We Find
# 11. Create a condition
# 12. Filter with `.loc`
# 13. Filter + select columns
# 14. Multiple conditions
#
# ### Part 4 — Sneak Peek of Week 6 Data Transformation
# 15. Create a new column
# 16. Build a pandas chain


# %% [markdown]
# # SQL → pandas Skill Map
#
# | SQL | pandas |
# |---|---|
# | Table | DataFrame |
# | `SELECT column` | `df["column"]` |
# | `SELECT col1, col2` | `df[["col1", "col2"]]` |
# | `WHERE condition` | `df.loc[condition]` |
# | `SELECT ... WHERE ...` | `df.loc[condition, columns]` |
# | `AND` | `&` |
# | `OR` | "|" |
# | Calculated column | `df["new"] = expression` |
# | `LIMIT 10` | `df.head(10)` |
# | `GROUP BY + COUNT` | `.value_counts()` |
#
# We did not relearn these data concepts today.
#
# We learned how Python expresses concepts we already understand from SQL.
#
# We are also starting to develop a new pattern:
#
# **Load data → inspect → filter → transform → investigate → communicate a result**
#
#


# %% [markdown]
# # Homework — Data investigation Challenge
#
# You are reviewing the Home Credit dataset before it is used for analysis.
#
# Find **two potential data issues or unusual features** that should be investigated further.
#
# Such as:any raw values whether it needs some transformation
#
# 1. a raw value that needs transformation to be human-readable
# 2. a possible placeholder or coding rule
# 3. a missing value that may be a business signal
# 4. a possible outlier
#
# For each:
#
# 1. What did you observe?
# 2. Which Python skills did you use?
# 3. How many records or values appear to be affected?
# 4. Why might this matter for analysis?
# 5. What would you recommend doing next?
#
# Use only the skills unlocked in Week 5.
#
# Useful tools:
#
# ```python
# df.head()
# df.shape
# df.info()
# df["column"]
# df[["column1", "column2"]]
# df["column"].describe()
# df["column"].value_counts(dropna=False)
# df.loc[condition]
# df.loc[condition, columns]
# ```
#
# You do **not** need to fix the issue.
#


# %% [markdown]
# Let's commit your changes to the script to your GitHub repository.
# 
# Step 1. Stage the changes
# Step 2. Write a commit message
# Step 3. Commit the changes
# Step 4. Synchronize your local repository with the remote repository