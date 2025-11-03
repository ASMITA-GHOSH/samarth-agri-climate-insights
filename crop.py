import pandas as pd
import streamlit as st

# ----------------------------
# Load Data
# ----------------------------
@st.cache_data
def load_data():
    rain_df = pd.read_csv("rainfall_area-wt_India_1901-2015.csv")
    agri_df = pd.read_csv("RS_Session_266_AU_2112_A.csv")
    return rain_df, agri_df

rain_df, agri_df = load_data()

# ----------------------------
# Preprocess
# ----------------------------
rain_df.columns = rain_df.columns.str.strip().str.lower()
agri_df.columns = agri_df.columns.str.strip()

# Extract clean crop info
agri_df.rename(columns={
    "Crop": "Crop",
    "Production (Lakh Tons) - 2023-24": "Production (Lakh Tons)",
    "Productivity (Yield in kg/ha) - 2023-24": "Yield (kg/ha)"
}, inplace=True)

# ----------------------------
# Streamlit Interface
# ----------------------------
st.set_page_config(page_title="Project Samarth", page_icon="🌾", layout="wide")

st.title("🌾 Project Samarth: Agricultural Production & Rainfall Insights")
st.caption("Data Sources: Ministry of Agriculture (Crop Data) and IMD (Rainfall Data)")

# Sidebar
st.sidebar.header("Select Crop")
crops = sorted(agri_df["Crop"].dropna().unique())
selected_crop = st.sidebar.selectbox("Choose a crop to explore:", crops)

# ----------------------------
# Crop Information Display
# ----------------------------
st.subheader(f"📊 Crop Overview: {selected_crop}")
crop_info = agri_df[agri_df["Crop"] == selected_crop]

st.write(crop_info[["Crop", "Production (Lakh Tons)", "Yield (kg/ha)"]])

# ----------------------------
# Rainfall Trend
# ----------------------------
st.subheader("🌧️ Rainfall Trends (1901–2015)")

if "year" in rain_df.columns:
    year_col = "year"
elif "year" in rain_df.keys():
    year_col = "year"
else:
    # find any similar column
    year_col = [col for col in rain_df.columns if "year" in col][0]

# Compute average annual rainfall across India
rainfall_summary = rain_df.groupby(year_col).mean(numeric_only=True).reset_index()

st.line_chart(rainfall_summary, x=year_col, y=rainfall_summary.columns[1:], height=400)

# ----------------------------
# Insights Section
# ----------------------------
st.subheader("📈 Insights")
st.markdown(f"""
- **{selected_crop}** had a total production of **{float(crop_info['Production (Lakh Tons)'].values[0]):,.2f} Lakh Tons** in 2023–24.
- Its **average productivity** was **{float(crop_info['Yield (kg/ha)'].values[0]):,.2f} kg/ha**.
- Historical rainfall patterns from **1901 to 2015** show long-term variations that can affect crop yields.
""")

st.caption("Developed as part of Project Samarth Challenge — Integrating Government Open Data.")
