"""Cmd to run this script: streamlit run app1.py"""
# Imports
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st


## Page setup
st.set_page_config(page_title="ESOL Solubility Explorer", layout="wide")

st.html("""
<style>
[data-testid="stMainBlockContainer"] {
    padding-top: 2rem !important;
}
</style>
""")

st.title("ESOL Solubility Explorer")


## Data loading
@st.cache_data
def load_data():
    path = Path(__file__).with_name("delaney-processed.csv")
    df = pd.read_csv(path)

    def get_solubility_class(val):
        if val >= -2.0:
            return "Soluble"
        elif val >= -4.0:
            return "Moderate"
        return "Poorly Soluble"

    df["Solubility Class"] = df["measured log solubility in mols per litre"].apply(
        get_solubility_class
    )
    return df


df = load_data()

colors = {
    "Soluble": "#009E73",
    "Moderate": "#0072B2",
    "Poorly Soluble": "#D55E00",
}
classes = ["Soluble", "Moderate", "Poorly Soluble"]


## Input widgets (minimal sidebar)
st.sidebar.header("Filters & View")

view_mode = st.sidebar.selectbox(
    "View",
    [
        "Overview & Parity",
        "Ring & H-Bond Analysis",
        "Dataset Records",
    ],
)

ring_options = ["All"] + sorted(df["Number of Rings"].unique().tolist())
selected_rings = st.sidebar.selectbox("Number of Rings", ring_options)

hbond_options = ["All"] + sorted(df["Number of H-Bond Donors"].unique().tolist())
selected_hbonds = st.sidebar.selectbox("Number of H-Bond Donors", hbond_options)

selected_classes = st.sidebar.multiselect(
    "Solubility Class",
    classes,
    default=classes,
)


# Data filtering
filtered = df[df["Solubility Class"].isin(selected_classes)]

if selected_rings != "All":
    filtered = filtered[filtered["Number of Rings"] == selected_rings]

if selected_hbonds != "All":
    filtered = filtered[filtered["Number of H-Bond Donors"] == selected_hbonds]

if filtered.empty:
    st.warning("No compounds match the selected Rings, H-Bond Donors, and Solubility Class filters.")
    st.stop()


## Overview
st.header("Overview")
st.caption(
    f"View: {view_mode} · "
    f"Rings: {selected_rings} · "
    f"H-Bond Donors: {selected_hbonds} · "
    f"{len(filtered):,} compounds"
)

m1, m2, m3, m4 = st.columns(4)

m1.metric("Avg. Measured logS", f"{filtered['measured log solubility in mols per litre'].mean():.2f} mol/L")
m2.metric("Avg. Predicted logS", f"{filtered['ESOL predicted log solubility in mols per litre'].mean():.2f} mol/L")
m3.metric("Avg. Rings / H-Bonds", f"{filtered['Number of Rings'].mean():.1f} / {filtered['Number of H-Bond Donors'].mean():.1f}")
m4.metric("Avg. Molecular Weight", f"{filtered['Molecular Weight'].mean():.1f} g/mol")


## View 1: Overview & Parity (Default 3-chart layout)
if view_mode == "Overview & Parity":
    st.header("Key Descriptor Relationships & Model Parity")

    # 1. Scatter plot: ESOL Predicted vs. Measured Solubility
    scatter_chart = px.scatter(
        filtered,
        x="ESOL predicted log solubility in mols per litre",
        y="measured log solubility in mols per litre",
        color="Solubility Class",
        title="Model Parity: Predicted vs. Measured logS",
        labels={
            "ESOL predicted log solubility in mols per litre": "ESOL Predicted logS (mol/L)",
            "measured log solubility in mols per litre": "Measured logS (mol/L)",
        },
        hover_data=["Compound ID", "Number of Rings", "Number of H-Bond Donors", "Molecular Weight"],
        color_discrete_map=colors,
        render_mode="svg",
    )

    # 2. Histogram: Distribution of Measured Solubility
    hist_chart = px.histogram(
        filtered,
        x="measured log solubility in mols per litre",
        color="Solubility Class",
        nbins=30,
        barmode="overlay",
        title="Histogram of Measured Solubility",
        labels={
            "measured log solubility in mols per litre": "Measured logS (mol/L)",
        },
        color_discrete_map=colors,
    )

    # 3. Distribution chart (Box plot): Molecular Weight by Solubility Class
    dist_chart = px.box(
        filtered,
        x="Solubility Class",
        y="Molecular Weight",
        color="Solubility Class",
        category_orders={"Solubility Class": classes},
        title="Molecular Weight Distribution by Class",
        labels={
            "Solubility Class": "Solubility Class",
            "Molecular Weight": "Molecular Weight (g/mol)",
        },
        color_discrete_map=colors,
    )

    for chart in [scatter_chart, hist_chart, dist_chart]:
        chart.update_layout(
            height=350,
            margin=dict(l=10, r=10, t=80, b=40),
            legend=dict(orientation="h", y=1.12, x=0),
            legend_title_text="",
        )

    left, middle, right = st.columns(3)
    left.plotly_chart(scatter_chart, width="stretch")
    middle.plotly_chart(hist_chart, width="stretch")
    right.plotly_chart(dist_chart, width="stretch")


## View 2: Ring & H-Bond Analysis
elif view_mode == "Ring & H-Bond Analysis":
    st.header("Structural Effects: Rings & H-Bond Donors")

    # 1. Scatter plot: Polar Surface Area vs. Measured Solubility
    psa_scatter = px.scatter(
        filtered,
        x="Polar Surface Area",
        y="measured log solubility in mols per litre",
        color="Solubility Class",
        title="Polar Surface Area vs. Measured logS",
        labels={
            "Polar Surface Area": "Polar Surface Area (Å²)",
            "measured log solubility in mols per litre": "Measured logS (mol/L)",
        },
        hover_data=["Compound ID", "Number of Rings", "Number of H-Bond Donors"],
        color_discrete_map=colors,
        render_mode="svg",
    )

    # 2. Distribution chart: Measured logS by Number of Rings
    ring_dist = px.box(
        filtered,
        x="Number of Rings",
        y="measured log solubility in mols per litre",
        color="Solubility Class",
        title="Solubility Distribution by Number of Rings",
        labels={
            "Number of Rings": "Number of Rings",
            "measured log solubility in mols per litre": "Measured logS (mol/L)",
        },
        color_discrete_map=colors,
    )

    # 3. Distribution chart: Measured logS by Number of H-Bond Donors
    hbond_dist = px.box(
        filtered,
        x="Number of H-Bond Donors",
        y="measured log solubility in mols per litre",
        color="Solubility Class",
        title="Solubility Distribution by H-Bond Donors",
        labels={
            "Number of H-Bond Donors": "Number of H-Bond Donors",
            "measured log solubility in mols per litre": "Measured logS (mol/L)",
        },
        color_discrete_map=colors,
    )

    for chart in [psa_scatter, ring_dist, hbond_dist]:
        chart.update_layout(
            height=350,
            margin=dict(l=10, r=10, t=80, b=40),
            legend=dict(orientation="h", y=1.12, x=0),
            legend_title_text="",
        )

    left, middle, right = st.columns(3)
    left.plotly_chart(psa_scatter, width="stretch")
    middle.plotly_chart(ring_dist, width="stretch")
    right.plotly_chart(hbond_dist, width="stretch")


## View 3: Dataset Records
else:
    st.header("Filtered Compound Data")
    display_cols = [
        "Compound ID",
        "Solubility Class",
        "measured log solubility in mols per litre",
        "ESOL predicted log solubility in mols per litre",
        "Number of Rings",
        "Number of H-Bond Donors",
        "Molecular Weight",
        "Polar Surface Area",
        "smiles",
    ]
    st.dataframe(filtered[display_cols], width="stretch", hide_index=True)