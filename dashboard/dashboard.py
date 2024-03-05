import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

day_rental_df = pd.read_csv("..\Data\day.csv")
hour_rental_df = pd.read_csv("..\Data\hour.csv")
day_rental_df['dteday'] = pd.to_datetime(day_rental_df['dteday'])
hour_rental_df['dteday'] = pd.to_datetime(hour_rental_df['dteday'])
st.header('Dicoding Bike Sharing Dashboard :')
tab1, tab2, tab3 = st.tabs(["Tab 1", "Tab 2", "Tab 3"])
with tab1:
    st.header("Bicycle Rental patterns in a Year")
    day_rental_df['day_type'] = day_rental_df['holiday'].apply(lambda x: 'holiday' if x == 1 else ('working day' if x == 0 else 'weekend'))
    day_rental_df_grouped = day_rental_df.groupby(['dteday', 'day_type']).agg({'cnt': 'mean'}).reset_index()
    fig, ax = plt.subplots()
    for day_type in ['working day', 'holiday', 'weekend']:
        data = day_rental_df_grouped[day_rental_df_grouped['day_type'] == day_type]
        ax.plot(data['dteday'], data['cnt'], label=day_type)
    ax.set_title('Average Bike Rental Count by Day Type')
    ax.set_xlabel('Date')
    ax.set_ylabel('Average Rental Count')
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    st.pyplot(fig)

with tab2:
    st.header("Weathersit")
    weather_mapping = {1: 'Clear', 2: 'Mist', 3: 'Light Snow/Rain', 4: 'Heavy Rain/Snow'}
    hour_rental_df['weather_desc'] = hour_rental_df['weathersit'].map(weather_mapping)
    weather_data_grouped = hour_rental_df.groupby('weather_desc').agg({'cnt': 'mean'}).reset_index()
    fig, ax = plt.subplots()
    ax.bar(weather_data_grouped['weather_desc'], weather_data_grouped['cnt'])
    ax.set_title('Average Bike Rental Count by Weather Condition')
    ax.set_xlabel('Weather Condition')
    ax.set_ylabel('Average Rental Count')
    ax.set_xticklabels(weather_data_grouped['weather_desc'], rotation=45)
    ax.grid(axis='y')
    plt.tight_layout()
    st.pyplot(fig)

with tab3:
    st.header("Number of bicycles rented in a week")
    hourly_data_grouped = hour_rental_df.groupby(['hr', 'weekday']).agg({'cnt': 'mean'}).reset_index()
    hourly_data_pivot = hourly_data_grouped.pivot(index="hr", columns="weekday", values="cnt")
    plt.figure(figsize=(12, 8))
    sns.heatmap(hourly_data_pivot, cmap="crest")
    plt.title('Average Bike Rental Count by Hour and Weekday')
    plt.xlabel('Weekday')
    plt.ylabel('Hour')
    st.pyplot(plt.gcf())

st.caption('Make By Frederick')