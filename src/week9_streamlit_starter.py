"""
Streamlit Barebone Starter -- Week 9
========================================
Clone this repo, then run:
    uv run streamlit run src/week9_streamlit_starter.py

This is intentionally minimal. In class we will build it up together:
    - add sidebar filters
    - add KPI metrics
    - add a drilldown chart with a dimension/metric picker
    - publish it to Streamlit Community Cloud

Data source: processed_data_cube.csv, produced by running main.py
(the cube is created by create_cubes() in stage_3_aggregate.py).
"""

from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

st.set_page_config(page_title="Home Credit Dashboard", layout="wide")

DATA_PATH = Path(__file__).resolve().parent.parent / "data"/  "processed_data_cube.csv"


@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)


def main():
    st.title("Home Credit Dashboard")
    st.markdown("Starter dashboard -- we'll build this up together in class.")

    df = load_data()

    month_options = sorted(
        set(zip(df["YEAR_APPLIED"].astype(int), df["MONTH_APPLIED"].astype(int)))
    )
    if not month_options:
        st.info("No application-month data is available.")
        st.stop()

    selected_months = st.sidebar.select_slider(
        "Application month range",
        options=month_options,
        value=(month_options[0], month_options[-1]),
        format_func=lambda month: pd.Timestamp(
            year=month[0], month=month[1], day=1
        ).strftime("%b %Y"),
    )
    start_month, end_month = selected_months
    month_index = df["YEAR_APPLIED"] * 12 + df["MONTH_APPLIED"]
    start_index = start_month[0] * 12 + start_month[1]
    end_index = end_month[0] * 12 + end_month[1]
    month_filtered_df = df.loc[month_index.between(start_index, end_index)]

    burden_categories = sorted(df["BURDEN_CAT"].dropna().unique())
    selected_burden = st.sidebar.selectbox(
        "Burden category",
        options=["All categories", *burden_categories],
    )
    filtered_df = month_filtered_df
    if selected_burden != "All categories":
        filtered_df = month_filtered_df.loc[
            month_filtered_df["BURDEN_CAT"] == selected_burden
        ]

    age_groups = sorted(df["AGE_GROUP"].dropna().unique())
    selected_age_group = st.sidebar.selectbox(
        "Age group",
        options=["All age groups", *age_groups],
    )
    if selected_age_group != "All age groups":
        filtered_df = filtered_df.loc[
            filtered_df["AGE_GROUP"] == selected_age_group
        ]

    if filtered_df.empty:
        st.info("No applications are available for the selected filters.")
        st.stop()

    total_applications = filtered_df["total_applications"].sum()
    total_defaults = filtered_df["total_defaults"].sum()
    total_credit = filtered_df["total_credit"].sum()
    default_rate = total_defaults / total_applications if total_applications else 0

    applications_col, default_rate_col, credit_col = st.columns(3)
    applications_col.metric(
        "Total applications (thousands)", f"{total_applications / 1_000:,.1f}"
    )
    default_rate_col.metric("Default rate (%)", f"{default_rate:.2%}")
    credit_col.metric("Total credit (in millions)", f"{total_credit / 1_000_000:,.1f}")

    st.subheader("Data cube preview")
    st.dataframe(filtered_df.head(20), width = 'stretch')

    st.subheader("Applications by contract type")

    chart_df = (filtered_df
                .groupby("NAME_CONTRACT_TYPE")
                .agg({"total_applications": "sum"})
                .reset_index()
                )

    fig = px.bar(chart_df, 
                 x="NAME_CONTRACT_TYPE",
                 y="total_applications")

    st.plotly_chart(fig, width= 'stretch')

    monthly_trend_df = (filtered_df
                        .groupby(["YEAR_APPLIED", "MONTH_APPLIED"])
                        .agg({
                            "total_applications": "sum",
                            "total_credit": "sum",
                        })
                        .reset_index()
                        .sort_values(["YEAR_APPLIED", "MONTH_APPLIED"])
                        )
    monthly_trend_df["application_month"] = pd.to_datetime(
        monthly_trend_df[["YEAR_APPLIED", "MONTH_APPLIED"]]
        .rename(columns={"YEAR_APPLIED": "year", "MONTH_APPLIED": "month"})
        .assign(day=1)
    )

    st.subheader("Total applications and credit over time")
    trend_fig = make_subplots(specs=[[{"secondary_y": True}]])
    trend_fig.add_trace(
        go.Scatter(
            x=monthly_trend_df["application_month"],
            y=monthly_trend_df["total_applications"],
            name="Applications",
            mode="lines+markers",
        ),
        secondary_y=False,
    )
    trend_fig.add_trace(
        go.Scatter(
            x=monthly_trend_df["application_month"],
            y=monthly_trend_df["total_credit"],
            name="Credit",
            mode="lines+markers",
        ),
        secondary_y=True,
    )
    trend_fig.update_xaxes(title_text="Application month", tickformat="%b %Y")
    trend_fig.update_yaxes(title_text="Total applications", secondary_y=False)
    trend_fig.update_yaxes(title_text="Total credit", secondary_y=True)
    st.plotly_chart(trend_fig, width="stretch")

    age_default_df = (filtered_df
                      .groupby("AGE_GROUP")
                      .agg({"total_defaults": "sum"})
                      .reset_index()
                      )
    age_default_df = age_default_df.loc[age_default_df["total_defaults"] > 0]

    st.subheader("Share of defaults by age group")
    if age_default_df.empty:
        st.info("No defaults are recorded for the selected filters.")
    else:
        age_default_fig = px.pie(
            age_default_df,
            names="AGE_GROUP",
            values="total_defaults",
            hole=0.35,
        )
        age_default_fig.update_traces(textinfo="label+percent")
        st.plotly_chart(age_default_fig, width="stretch")


if __name__ == "__main__":
    main()
