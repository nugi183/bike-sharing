import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='darkgrid')

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("main_data.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

df = load_data()

# Sidebar
st.sidebar.header("Filter Data")
min_date = df['dteday'].min()
max_date = df['dteday'].max()

try:
    start_date, end_date = st.sidebar.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
except ValueError:
    st.error("Harap pilih rentang waktu yang valid.")
    st.stop()

# Filter data based on sidebar
main_df = df[(df["dteday"] >= str(start_date)) & 
             (df["dteday"] <= str(end_date))]

# Header Dashboard
st.title("🚲 Bike Sharing Data Dashboard")
st.markdown("Dashboard ini menampilkan hasil analisis penyewaan sepeda berdasarkan data historis tahun 2011-2012.")

# Metrik Utama
col1, col2 = st.columns(2)
with col1:
    total_orders = main_df['cnt'].sum()
    st.metric("Total Penyewaan", value=f"{total_orders:,}")
with col2:
    avg_orders = round(main_df['cnt'].mean(), 2)
    st.metric("Rata-rata Penyewaan per Jam", value=f"{avg_orders:,}")

st.markdown("---")

# Visualisasi 1: Dampak Cuaca
st.subheader("Dampak Kondisi Cuaca terhadap Penyewaan")
fig, ax = plt.subplots(figsize=(10, 5))
weather_df = main_df.groupby('weathersit_desc')['cnt'].mean().reset_index()
sns.barplot(
    x='weathersit_desc', 
    y='cnt', 
    data=weather_df, 
    palette='viridis', 
    ax=ax
)
ax.set_title("Rata-rata Penyewaan Berdasarkan Cuaca", fontsize=14)
ax.set_ylabel("Rata-rata Sewa")
ax.set_xlabel("Kondisi Cuaca")
st.pyplot(fig)

# Visualisasi 2: Pola Jam
st.subheader("Pola Penyewaan Sepeda per Jam (Hari Kerja vs Libur)")
fig2, ax2 = plt.subplots(figsize=(10, 5))
hourly_df = main_df.groupby(['workingday_desc', 'hr'])['cnt'].mean().reset_index()
sns.lineplot(
    x='hr', 
    y='cnt', 
    hue='workingday_desc', 
    data=hourly_df,
    marker='o',
    palette='Set1',
    ax=ax2
)
ax2.set_title("Rata-rata Penyewaan per Jam", fontsize=14)
ax2.set_xlabel("Jam (0-23)")
ax2.set_ylabel("Rata-rata Sewa")
ax2.set_xticks(range(0, 24))
st.pyplot(fig2)

st.caption("Copyright © Anugerah Fadhil Rachman 2026")