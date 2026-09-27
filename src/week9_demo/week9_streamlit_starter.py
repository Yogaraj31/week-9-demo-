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

Data source: processed_data_cube.csv, produced by running main_pipeline.py
(the cube is created by create_cubes() in stage_3_aggregate.py).
"""

from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Home Credit Dashboard", layout="wide")

DATA_PATH = Path(__file__).resolve().parent.parent.parent / "data"/  "processed_data_cube.csv"


@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)


def main():
    st.title("Home Credit Dashboard")
    st.markdown("Starter dashboard -- we'll build this up together in class.")

    df = load_data()

    st.subheader("Data cube preview")
    st.dataframe(df.head(20), width = 'stretch')

    st.subheader("Applications by contract type")

    chart_df = df.groupby("NAME_CONTRACT_TYPE")["total_applications"].sum().reset_index()
    fig = px.bar(chart_df, x="NAME_CONTRACT_TYPE", y="total_applications")

    st.plotly_chart(fig, width= 'stretch')


if __name__ == "__main__":
    main()
