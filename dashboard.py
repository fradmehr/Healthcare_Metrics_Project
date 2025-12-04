#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt

# # ==============================
# # Page Config
# # ==============================
# st.set_page_config(page_title="Healthcare Staffing Dashboard", layout="wide")
# st.title("🏥 Healthcare Staffing & Facility Metrics Dashboard")

# # ==============================
# # Load Data
# # ==============================
# @st.cache_data
# def load_staffing():
#     return pd.read_csv("PBJ_Daily_Nurse_Staffing_Q2_2024.csv", encoding='latin-1')

# @st.cache_data
# def load_provider():
#     return pd.read_csv("NH_ProviderInfo_Oct2024.csv", encoding='latin-1')

# staff = load_staffing()
# prov = load_provider()

# # ==============================
# # Preprocessing
# # ==============================
# staff["WorkDate"] = pd.to_datetime(staff["WorkDate"], errors="coerce")

# staff["total_nurse_hours"] = (
#     staff["Hrs_RN"] +
#     staff["Hrs_LPN"] +
#     staff["Hrs_CNA"]
# )

# staff["hours_per_patient"] = staff["total_nurse_hours"] / staff["MDScensus"]
# staff.replace([float("inf"), -float("inf")], pd.NA, inplace=True)

# staff = staff.merge(
#     prov[["CMS Certification Number (CCN)", "State", "Provider Type"]],
#     left_on="PROVNUM",
#     right_on="CMS Certification Number (CCN)",
#     how="left"
# )

# # ==============================
# # Sidebar Filters
# # ==============================
# st.sidebar.header("🔎 Filters")

# states = sorted(staff["State"].dropna().unique())
# selected_states = st.sidebar.multiselect("Select State(s)", states, default=states[:5])

# filtered = staff[staff["State"].isin(selected_states)]

# # ==============================
# # KPI Metrics
# # ==============================
# st.subheader("📊 Key Staffing KPIs")

# col1, col2, col3 = st.columns(3)

# col1.metric(
#     "Average Nurse Hours / Patient",
#     round(filtered["hours_per_patient"].mean(), 2)
# )

# col2.metric(
#     "Average Daily Census",
#     int(filtered["MDScensus"].mean())
# )

# col3.metric(
#     "Average Total Nurse Hours",
#     int(filtered["total_nurse_hours"].mean())
# )

# # ==============================
# # Visualization 1: Staffing Trend
# # ==============================
# st.subheader("📈 Total Nurse Hours Over Time")

# trend = (
#     filtered
#     .set_index("WorkDate")
#     .resample("M")["total_nurse_hours"]
#     .mean()
# )

# fig1, ax1 = plt.subplots()
# trend.plot(ax=ax1)
# ax1.set_ylabel("Avg Nurse Hours")
# ax1.set_xlabel("Month")
# st.pyplot(fig1)

# # ==============================
# # Visualization 2: Staffing Mix
# # ==============================
# st.subheader("👩‍⚕️ Staffing Mix (Employee vs Contract)")

# mix = filtered[[
#     "Hrs_RN_emp", "Hrs_RN_ctr",
#     "Hrs_LPN_emp", "Hrs_LPN_ctr",
#     "Hrs_CNA_emp", "Hrs_CNA_ctr"
# ]].sum()

# fig2, ax2 = plt.subplots()
# mix.plot(kind="bar", ax=ax2)
# ax2.set_ylabel("Total Hours")
# ax2.set_title("Staffing Hours by Type")
# st.pyplot(fig2)

# # ==============================
# # Visualization 3: Staffing vs Census
# # ==============================
# st.subheader("🔍 Staffing vs Occupancy Proxy")

# fig3, ax3 = plt.subplots()
# ax3.scatter(
#     filtered["MDScensus"],
#     filtered["total_nurse_hours"],
#     alpha=0.4
# )
# ax3.set_xlabel("Patient Census")
# ax3.set_ylabel("Total Nurse Hours")
# st.pyplot(fig3)

# # ==============================
# # Visualization 4: State-Level Comparison
# # ==============================
# st.subheader("🗺️ Average Nurse Hours per Patient by State")

# state_agg = filtered.groupby("State")["hours_per_patient"].mean()

# fig4, ax4 = plt.subplots()
# state_agg.sort_values().plot(kind="barh", ax=ax4)
# ax4.set_xlabel("Hours per Patient")
# st.pyplot(fig4)

# # ==============================
# # Data Preview
# # ==============================
# st.subheader("📄 Data Preview")
# st.dataframe(filtered.head(20))

# second code

#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

# ==============================
# Page Config
# ==============================
st.set_page_config(page_title="Healthcare Staffing Dashboard", layout="wide")
st.title("🏥 Healthcare Staffing & Facility Metrics Dashboard")

# ==============================
# Load Data
# ==============================
@st.cache_data
def load_staffing():
    return pd.read_csv("PBJ_Daily_Nurse_Staffing_Q2_2024.csv", encoding="latin-1")

@st.cache_data
def load_provider():
    return pd.read_csv("NH_ProviderInfo_Oct2024.csv", encoding="latin-1")

df = load_staffing()
prov = load_provider()

# ==============================
# Preprocessing
# ==============================
df["WorkDate"] = pd.to_datetime(df["WorkDate"], errors="coerce")

df["census"] = df["MDScensus"]

df["total_nurse_hours"] = (
    df["Hrs_RN"] +
    df["Hrs_LPN"] +
    df["Hrs_CNA"] +
    df.get("Hrs_NAtrn", 0) +
    df.get("Hrs_MedAide", 0)
)

df["hours_per_resident"] = df["total_nurse_hours"] / df["census"].replace(0, np.nan)
df.replace([float("inf"), -float("inf")], pd.NA, inplace=True)

df = df.merge(
    prov[["CMS Certification Number (CCN)", "State", "Provider Type", "Provider Name"]],
    left_on="PROVNUM",
    right_on="CMS Certification Number (CCN)",
    how="left"
)

# ==============================
# Sidebar Filters
# ==============================
st.sidebar.header("🔎 Filters")

states = sorted(df["State"].dropna().unique())
selected_states = st.sidebar.multiselect("Select State(s)", states, default=states[:5])

filtered = df[df["State"].isin(selected_states)]

# ==============================
# KPI Metrics
# ==============================
st.subheader("📊 Key Staffing KPIs")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Average Nurse Hours / Resident",
    round(filtered["hours_per_resident"].mean(), 2)
)

col2.metric(
    "Average Daily Census",
    int(filtered["census"].mean())
)

col3.metric(
    "Average Total Nurse Hours",
    int(filtered["total_nurse_hours"].mean())
)

# ==============================
# ORIGINAL Visualization 1: Staffing Trend
# ==============================
# st.subheader("📈 Total Nurse Hours Over Time")

# trend = (
#     filtered
#     .set_index("WorkDate")
#     .resample("M")["total_nurse_hours"]
#     .mean()
# )

# fig1, ax1 = plt.subplots()
# trend.plot(ax=ax1)
# ax1.set_ylabel("Avg Nurse Hours")
# ax1.set_xlabel("Month")
# st.pyplot(fig1)

# ==============================
# ORIGINAL Visualization 2: Staffing Mix
# ==============================
st.subheader("👩‍⚕️ Staffing Mix (Employee vs Contract)")

mix = filtered[[
    "Hrs_RN_emp", "Hrs_RN_ctr",
    "Hrs_LPN_emp", "Hrs_LPN_ctr",
    "Hrs_CNA_emp", "Hrs_CNA_ctr"
]].sum()

fig2, ax2 = plt.subplots()
mix.plot(kind="bar", ax=ax2)
ax2.set_ylabel("Total Hours")
ax2.set_title("Staffing Hours by Type")
st.pyplot(fig2)

# ==============================
# ORIGINAL Visualization 3: Staffing vs Census
# ==============================
st.subheader("🔍 Staffing vs Occupancy Proxy")

fig3, ax3 = plt.subplots()
ax3.scatter(
    filtered["census"],
    filtered["total_nurse_hours"],
    alpha=0.4
)
ax3.set_xlabel("Patient Census")
ax3.set_ylabel("Total Nurse Hours")
st.pyplot(fig3)

# ==============================
# ORIGINAL Visualization 4: State-Level Comparison
# ==============================
st.subheader("🗺️ Average Nurse Hours per Patient by State")

state_agg = filtered.groupby("State")["hours_per_resident"].mean()

fig4, ax4 = plt.subplots()
state_agg.sort_values().plot(kind="barh", ax=ax4)
ax4.set_xlabel("Hours per Patient")
st.pyplot(fig4)

# ==============================
# NEW Visualization 5: Staffing vs Occupancy (Regression + Correlation)
# ==============================
st.subheader("📌 Staffing vs Occupancy (Regression & Correlation)")

grp = (
    filtered.groupby(["PROVNUM", "WorkDate"], as_index=False)
    .agg(
        census=("census", "mean"),
        hours_per_resident=("hours_per_resident", "mean")
    )
    .dropna()
)

fig5, ax5 = plt.subplots(figsize=(8,5))
ax5.scatter(grp["census"], grp["hours_per_resident"], alpha=0.4)

if not grp.empty:
    m, b = np.polyfit(grp["census"], grp["hours_per_resident"], 1)
    ax5.plot(grp["census"], m * grp["census"] + b, color="red")

ax5.set_xlabel("Occupancy (Census)")
ax5.set_ylabel("Nurse Hours per Resident")
ax5.set_title("Staffing vs Occupancy")
ax5.grid(True)
st.pyplot(fig5)

if not grp.empty:
    r, p = pearsonr(grp["hours_per_resident"], grp["census"])
    st.write(f"📌 Pearson correlation (hours_per_resident vs census): r={r:.3f}, p={p:.3g}")

# ==============================
# NEW Visualization: Staffing vs Occupancy (Detailed Aggregation)
# ==============================
#st.subheader("📌 QUESTION 1: Relationship staffing vs occupancy")

# Prepare aggregation: daily/provider
agg_cols = ["PROVNUM", "WorkDate"]
grouped = (
    filtered.groupby(agg_cols)
    .agg(
        total_nurse_hours=("total_nurse_hours", "sum"),
        census=("census", "mean"),
        hours_per_resident=("hours_per_resident", "mean")
    )
    .reset_index()
)

# Drop rows with missing census or hours_per_resident
grp = grouped.dropna(subset=["census", "hours_per_resident"])

if not grp.empty:
    r, p = pearsonr(grp["hours_per_resident"], grp["census"])
    #st.write(f"📌 Pearson correlation (hours_per_resident vs census): r={r:.3f}, p={p:.3g}")

    figQ1, axQ1 = plt.subplots(figsize=(8,5))
    sns.regplot(
        x="census",
        y="hours_per_resident",
        data=grp.sample(min(len(grp), 2000), random_state=1),
        ax=axQ1,
        scatter_kws={"alpha":0.4}
    )
    axQ1.set_xlabel("Occupancy (census)")
    axQ1.set_ylabel("Nurse hours per resident")
    axQ1.set_title("Staffing Level (hours/resident) vs Occupancy (census)")
    axQ1.grid(True)
    st.pyplot(figQ1)
else:
    st.write("⚠️ Not enough data to compute relationship (missing census or hours_per_resident).")


# ==============================
# NEW Visualization 6: Contract Hours by Provider
# ==============================
st.subheader("👩‍⚕️ Hospitals with Highest Reliance on Contract Staff")

df["contract_hours"] = (
    df.get("Hrs_RN_ctr", 0) +
    df.get("Hrs_LPN_ctr", 0) +
    df.get("Hrs_CNA_ctr", 0) +
    df.get("Hrs_NAtrn_ctr", 0) +
    df.get("Hrs_MedAide_ctr", 0)
)

ot_by_provider = (
    df.groupby(["PROVNUM", "Provider Name"], as_index=False)
    .agg(total_contract_hours=("contract_hours", "sum"))
    .sort_values("total_contract_hours", ascending=False)
)

top10 = ot_by_provider.head(10)

fig6, ax6 = plt.subplots(figsize=(10,6))
ax6.barh(top10["Provider Name"], top10["total_contract_hours"])
ax6.set_xlabel("Total Contract Nurse Hours")
ax6.set_title("Top 10 Providers by Contract Staff Reliance")
ax6.invert_yaxis()
st.pyplot(fig6)

st.dataframe(top10)

# ==============================
# NEW Visualization 7: State & Provider Type Aggregation
# ==============================
st.subheader("🗺️ Average Nurse Hours per Resident by State & Provider Type")

agg = (
    df.groupby(["State", "Provider Type"])
    .agg(
        avg_hours_per_resident=("hours_per_resident", "mean"),
        avg_total_hours=("total_nurse_hours", "mean"),
        observations=("total_nurse_hours", "count")
    )
    .reset_index()
)

agg_sorted = agg.sort_values(["State", "avg_hours_per_resident"]).head(20)
st.dataframe(agg_sorted)

fig7, ax7 = plt.subplots(figsize=(10,6))
sns.barplot(
    data=agg_sorted,
    x="avg_hours_per_resident",
    y="State",
    hue="Provider Type",
    ax=ax7
)
ax7.set_xlabel("Avg Hours per Resident")
ax7.set_ylabel("State")
ax7.set_title("State & Provider Type Comparison")
st.pyplot(fig7)

# ==============================
# Data Preview
# ==============================
st.subheader("📄 Data Preview")
st.dataframe(filtered.head(20))




