# %% [markdown]
# # Week 7: Visualising Data for Risk Monitoring
#
# Last week, we transformed raw application data into analysis-ready risk
# features. This week, we use visualisation to monitor portfolio behaviour and
# explain risk patterns.
#
# Today's guiding question:
#
# **How can charts help us understand portfolio patterns and communicate insights?**
#
# Choose the chart from the business question:
#
# | Story | Business question | First chart to try | What must happen first? |
# |---|---|---|---|
# | Documentary | What happened, or how did it change over time? | Line | Use a meaningful time field; aggregate to one row per period |
# | Composition | What is the portfolio made up of? | Stacked bar | Aggregate counts or proportions by group |
# | Comparison | Which groups have higher or lower risk? | Bar | Aggregate to one row per group |
# | Distribution | How are numeric values distributed? | Histogram | Choose one numeric column |
# | Relationship | Do two numerical variables move together? | Scatter | Select two numeric columns; sample if needed |
# | Geographic | Where are events or customers located? | Map | Use latitude and longitude (separate dataset) |
#
# We will use auto-completion to generate the Plotly code, then read and interpret the chart. 
#
# **Decide chart type -> Prepare data -> Generate code** -> Read -> Predict -> Modify -> Run -> Verify -> **Interpret**

# %% [markdown]
# ## The Plotly Express pattern to recognise
#
# When AI auto-completion generates a chart, use this scaffold to read it. You do not need to
# memorise every option.
#
# ```python
# import plotly.express as px
#
# fig = px.<chart_type>(
#     data_frame=<dataframe>,
#     x="<column for horizontal axis>",
#     y="<column for vertical axis>",
#     color="<optional grouping column>",
#     hover_data=["<optional extra columns>"],
#     title="<business question answered by this chart>",
# )
#
# fig.show()
# ```
#
# Read it in this order: **DataFrame -> chart type -> x -> y -> colour -> hover
# data -> title.**




# %% [markdown]
# ## Reload the Week 6 Analysis-Ready Dataset
#
# In Week 6, we created features such as:
#
# - `AGE` and `AGE_GROUP`
# - `INCOME_TYPE`
# - `EDUCATION_LEVEL`
# - `CREDIT_INCOME_RATIO`
# - `recent_previous_application_count`
# -  etc...
#
# We now reuse the dataset saved at the end of that lesson. This is a common
# workflow: transform the data once, then use the prepared dataset for
# reporting, monitoring, and modelling.


# %%
# The libraries we used last week
import pandas as pd
import numpy as np
from pathlib import Path

# %%
# New plotly libraries we needed for visualisation
# `uv add plotly` in terminal to install package if you haven't already
import plotly.express as px

# %%
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

pd.set_option("display.max_columns", None)
pd.options.display.float_format = "{:.2f}".format

px.defaults.template = "plotly_white"
    
df_app_enriched = pd.read_csv(DATA_DIR / "week6_application_features.csv")

df_app_enriched.head()

# %%
# Recall the week 6 dataset structure
df_app_enriched.info()


# %% [markdown]
# # Demo 1 - Has application volume changed over time?
#
# ## 1. Decide on chart type before coding
#
# **Business question:** Has application volume changed across quarters?
# 
# Documentary story:
# - We want a change over time -> **line chart**.
# - Each point should represent **one quarter**.
# - Therefore we need to aggregate to one row per quarter.

# %%
df_app_enriched = (
    df_app_enriched
    .assign(application_quarter=lambda x: pd.to_datetime(x["date_application"]).dt.to_period("Q").astype(str)
    )
)

df_app_enriched[["date_application", "application_quarter"]].sample(10)

# %%
df_quarterly_volume = (
    df_app_enriched
    .groupby("application_quarter", as_index=False)
    .agg(application_count=("SK_ID_CURR", "size"))
    .sort_values("application_quarter")
)

df_quarterly_volume

# %% [markdown]
# ## 2. Use AI to draft the Plotly code
#
# **Prompt/code-completion instruction**
#
# > Using `df_quarterly_volume`, write concise Plotly Express code for a line
# > chart. Put `application_quarter` on the x-axis and `application_count` on
# > the y-axis. Add markers, a clear title, and readable axis labels. Do not
# > transform the DataFrame.

# %%
fig = px.line(
    data_frame=df_quarterly_volume,
    x="application_quarter",
    y="application_count",
    markers=True,
    title="Application Volume by Quarter",
    labels={
        "application_quarter": "Quarter",
        "application_count": "Number of Applications"
    }
) 
fig.show()  


# ## 3. Read and predict
#
# Before running: How many points should there be? Which quarter should have the
# highest point, based on the table above?

# %% [markdown]
# **VERIFY and INTERPRET**
# 1. Which quarter has the highest number of applications?
# 2. Which quarter has the lowest number of applications?
# 3. Does the movement look stable, increasing, decreasing, or irregular?
# 4. What would you investigate before concluding that the portfolio changed?

# %% [markdown]
# **MODIFY**:Now, let's change the prompt to ensure the y-axis starts at zero 

# %%
fig = px.line(
    data_frame=df_quarterly_volume,
    x="application_quarter",
    y="application_count",
    markers=True,
    title="Application Volume by Quarter",
    labels={
        "application_quarter": "Quarter",
        "application_count": "Number of Applications"
    },
    range_y=[0, df_quarterly_volume["application_count"].max() * 1.1]  # Add a 10% buffer above the max value for better visualization
)
fig.show()




# %% [markdown]
# # Demo 2 - How is loan amount distributed?
#
# **Business question:** Is loan amount concentrated in a narrow range or spread
# widely across applicants?
#
# Documentary story:
# - We want the distribution of a numeric field -> **histogram**.
# - No `groupby` is needed: the chart groups loan amounts into bins.

# %%
fig  = px.histogram(
    data_frame=df_app_enriched,
    x="AMT_CREDIT",
    nbins=30,
    title="Distribution of Loan Amounts",
    labels={"AMT_CREDIT": "Loan Amount (in currency units)"},
    hover_data={"AMT_CREDIT": True}
)
fig.show()



# **READ**: check that you understand the code. What is the x-axis? How many bins are there? What does each bar represent?

# %% [markdown]
# **VERIFY**: Check the chart. Does it match your expectation?
#
# - Is the distribution skewed or roughly balanced?
# - Are extreme loan amounts hiding the pattern for most applicants?




# %% [markdown]

# # Demo 3 — Which family status type has the highest and lowest average loan amount?
#
# **Business question:** Which family status type has the highest and lowest average loan
# amount in our portfolio?
#
# Comparison story:
# - We want to compare a measure across categories → **sorted bar chart**.
# - First, use `groupby` to create one row per family status type.
# - A horizontal bar chart makes the family status labels easy to read.

# %%
df_family_status_avg_loan = (
    df_app_enriched
    .groupby("NAME_FAMILY_STATUS", as_index=False)
    .agg(avg_loan_amount=("AMT_CREDIT", "mean"))
    .sort_values("avg_loan_amount", ascending=False)
    .assign(avg_loan_amount=lambda x: x["avg_loan_amount"].astype(int))
)   

df_family_status_avg_loan.head()

# %%
# Create a horizontal bar chart to visualize average loan amount by family status
# Sort so that the largest average loan amount is at the top. Add a clear title and readable axis labels. Include hover data to show the average loan amount when hovering over each bar.
fig = px.bar(
    data_frame=df_family_status_avg_loan,
    x="avg_loan_amount",
    y="NAME_FAMILY_STATUS",
    orientation="h",
    title="Average Loan Amount by Family Status",
    labels={
        "avg_loan_amount": "Average Loan Amount (in currency units)",
        "NAME_FAMILY_STATUS": "Family Status"
    },
    hover_data={"avg_loan_amount": True}
)


# refine the chart by sorting the bars in descending order of average loan amount
fig.update_layout(yaxis={'categoryorder':'total ascending'})

fig.show()




# %% [markdown]

# **READ**: Before running the chart code:
#
# - What does one bar represent?
# - Why must we use `groupby` before plotting?
# - Which family status type do you predict will have the highest average loan amount?
# - What extra information will appear when you hover over a bar?
#
# **VERIFY**: Check the chart.
#
# - Is the highest family status type clearly visible?
# - Does the bar order match `df_family_status_avg_loan`?
# - Can you state one business insight in a plain-English sentence?



# %% [markdown]

# # Demo 4 — Has our gender mix changed over time?
#
# **Business question:** Has the proportion of male and female applicants changed
# over each quarter?
#
# Composition + documentary story:
# - We want to see **what the portfolio is made up of** → gender mix.
# - We also want to see **how it changed over time** → quarter.
# - Use a **100% stacked bar chart**: each bar is one quarter and always totals 100%.
# - Ensure it is a proportion chart, not a count chart, because each quarter may have a different number of applications.

# %%
df_gender_mix_by_quarter = (
    df_app_enriched
    .groupby(["application_quarter", "CODE_GENDER"], as_index=False)
    .agg(applicant_count=("SK_ID_CURR", "size"))
    .assign(applicant_proportion=lambda x: x["applicant_count"] / x.groupby("application_quarter")["applicant_count"].transform("sum"))
    .sort_values(["application_quarter", "CODE_GENDER"])
)

df_gender_mix_by_quarter.head(10)

# %%
fig = px.bar(
    data_frame=df_gender_mix_by_quarter,
    x="application_quarter",
    y="applicant_proportion",
    color="CODE_GENDER",
    title="Gender Mix by Quarter",
    labels={
        "application_quarter": "Quarter",
        "applicant_proportion": "Proportion of Applicants",
        "CODE_GENDER": "Gender"
    },
    hover_data={"applicant_count": True, "applicant_proportion": ':.2%'},
    barmode="stack"
)
fig.show()

    # %% [markdown]
#
# **VERIFY**: Check the chart.
#
# - Does each quarter total 100%?
# - Does the chart show portfolio **mix**, or the total number of applicants?
# - Can you state one business insight in a plain-English sentence?

# %% [markdown]
# The default color is counterintuitive
# **MODIFY**: Now modify the chart so that `F` is red, `M` is blue, and `XNA` is grey. 

# %%
fig = px.bar(
    data_frame=df_gender_mix_by_quarter,
    x="application_quarter",
    y="applicant_proportion",
    color="CODE_GENDER",
    color_discrete_map={"F": "red", "M": "blue", "XNA": "grey"},
    title="Gender Mix by Quarter",
    labels={
        "application_quarter": "Quarter",
        "applicant_proportion": "Proportion of Applicants",
        "CODE_GENDER": "Gender"
    },
    hover_data={"applicant_count": True, "applicant_proportion": ':.2%'},
    barmode="stack"
)
fig.show()




# %%
# save the chart to a html file in the output directory
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)
fig.write_html(OUTPUT_DIR / "gender_mix_by_quarter.html")



# %% [markdown]
# # Hands on activities
#
# > Refer to the Week 7 slides for 3 other business questions and attempt 
# > them together as a table group

# %%
# Hands on #1
# Are default rates improving, worsening, or remaining stable by quarter?
#
# > Create a dataframe `df_quarterly_default` that contains the average default rate by quarter.
# > Group by application_quarter to get one row per quarter. 
# > Then Aggregate average default rate by taking mean of `TARGET` for each quarter. 
# > Use Plotly Express to create a line chart with markers.

df_quarterly_default = (
    df_app_enriched
    .groupby("application_quarter", as_index=False)
    .agg(default_rate=("TARGET", "mean"))
    .assign(default_rate=lambda x: x["default_rate"].round(4))  # Convert to percentage
)

df_quarterly_default

# %%
fig = px.line(
    df_quarterly_default,
    x="application_quarter",
    y="default_rate",
    markers=True,
    title="Default Rate by Quarter",
    labels={"application_quarter": "Quarter", "default_rate": "Default Rate"},
)
fig.update_yaxes(tickformat=".2%")  # Format y-axis as percentage
fig.update_yaxes(rangemode="tozero")  # Ensure y-axis starts at zero
fig.show()

# %%
# Hands on #2
# Is the default-rate trend different for male and female applicants, and is the pattern stable over time?
#
# > Create a dataframe `df_quarterly_default_by_gender` that contains the average default rate by quarter and gender.
# > Group by application_quarter and CODE_GENDER to get one row per quarter and gender. 
# > Then Aggregate average default rate by taking mean of `TARGET` for each quarter and gender. 
# > Use Plotly Express to create a line chart by gender with markers.
# > Color the F line red, the M line blue, and the XNA line grey.

df_quarterly_default_by_gender = (
    df_app_enriched
    .assign(CODE_GENDER=lambda x: x["CODE_GENDER"].fillna("Not Available"))
    .groupby(["application_quarter", "CODE_GENDER"], as_index=False)
    .agg(default_rate=("TARGET", "mean"))
    .assign(default_rate=lambda x: x["default_rate"].round(4))  # Convert to percentage
)

df_quarterly_default_by_gender

# %%
fig = px.line(
    df_quarterly_default_by_gender,
    x="application_quarter",
    y="default_rate",
    color="CODE_GENDER",
    markers=True,
    title="Default Rate by Quarter and Gender",
    labels={"application_quarter": "Quarter", "default_rate": "Default Rate", "CODE_GENDER": "Gender"},
    color_discrete_map={"F": "#d62728", "M": "#1f77b4", "XNA": "#7f7f7f"},
)
fig.update_yaxes(tickformat=".2%")  # Format y-axis as percentage
fig.update_yaxes(rangemode="tozero")  # Ensure y-axis starts at zero
fig.show()


# %%
# Hands on #3
# Which age group has the highest and lowest default rate, and how large is each group?
#
# > Create a dataframe `df_default_by_age_group`
# > Group by age group and aggregate the average default rate and count of applicants.
# > Use Plotly Express to create a line chart with age group on the x-axis, default rate on the y-axis
# > Add the applicant count as hover data. 

df_default_by_age_group = (
    df_app_enriched
    .groupby("AGE_GROUP", as_index=False)
    .agg(
        default_rate=("TARGET", "mean"),
        applicant_count=("SK_ID_CURR", "size")
    )
    .assign(default_rate=lambda x: x["default_rate"].round(4))  # Convert to percentage
)

df_default_by_age_group

# %%
fig = px.line(
    df_default_by_age_group,
    x="AGE_GROUP",
    y="default_rate",
    markers=True,
    title="Default Rate by Age Group",
    labels={"AGE_GROUP": "Age Group", "default_rate": "Default Rate"},
    hover_data={"applicant_count": True},
)
fig.update_yaxes(tickformat=".2%")  # Format y-axis as percentage
fig.update_yaxes(rangemode="tozero")  # Ensure y-axis starts at zero
fig.show()







# %% [markdown]
# # Demo 5 - When the question is "where?"
#
# Home Credit data has no latitude and longitude. But for those with geographical information, 
# a map can be a powerful tool to visualize spatial patterns. 
# Let's use the carshare dataset from Plotly Express to demonstrate a map chart.

# %%
# Load the carshare dataset from Plotly Express
df_carshare = px.data.carshare()

df_carshare.head()

# %%
# Create a scatter mapbox chart to visualize car-share hours by location
fig = px.scatter_map(
    data_frame=df_carshare,
    lat="centroid_lat",
    lon="centroid_lon",
    color="peak_hour",
    hover_data=["car_hours"],
    zoom=9,
    center={"lat": 45.5, "lon": -73.6},
    map_style="carto-positron",
    title="Where Are Car-Share Hours Concentrated?",
)
fig.show()


# %%
# Load the election dataset from Plotly Express
df_election = px.data.election()
geojson_election = px.data.election_geojson()

# %%
df_election.head()

# %%
# These are coordinates defining the polygons for each district. 
# Each feature is a district, and the properties include the district id and name 
geojson_election

# %%
fig = px.choropleth_map(
    data_frame=df_election,
    geojson=geojson_election,
    featureidkey="properties.district",  # Column in geojson_election that matches the district id in df_election
    locations="district",  # Column in df_election that matches the district id in geojson_election
    color="Bergeron",  # Column to color the districts by
    center={"lat": 45.5517, "lon": -73.7073},
    zoom=8,
    hover_data=["Coderre", "Joly"],
    map_style="carto-positron",
    title="Votes for Bergeron by District",
)
fig.show()


# %% [markdown]
# ## Let's commit your changes to the script to your GitHub repository.
# 
# Step 1. Stage the changes
# Step 2. Write a commit message
# Step 3. Commit the changes
# Step 4. Synchronize your local repository with the remote repository



# %% [markdown]
# ## Wrap-Up
#
# - Start with the business question, then choose the chart type that best
#   communicates the story: line charts for trends, bars for comparisons,
#   histograms for distributions, and maps for location-based analysis.
# - Prepare the data before plotting. Aggregate to the correct level, such as
#   one row per quarter, group, or category, so each mark in the chart has a
#   clear meaning.
# - Use proportions when comparing portfolio mix across periods with different
#   volumes, and use counts when the size of the portfolio matters.
# - Interpret default rates together with applicant counts. A high or low rate
#   may be less meaningful when it comes from a very small group.
# - Read, predict, modify, and verify generated Plotly code instead of treating
#   an automatically created chart as the final answer.
# - Improve communication with meaningful titles, readable labels, sensible
#   axis ranges, percentage formatting, colours, and hover information.


