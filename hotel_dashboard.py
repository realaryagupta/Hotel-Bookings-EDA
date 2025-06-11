import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Set up Streamlit
st.set_page_config(page_title="Hotel Booking Dashboard", layout="wide")
st.title("🏨 Hotel Booking Analysis Dashboard")
st.markdown("#### Created by Arya Gupta")

@st.cache_data
def load_data():
    df = pd.read_csv('Hotel Bookings.csv')
    
    # Clean & transform
    df.drop_duplicates(inplace=True)
    df['company'].fillna(0, inplace=True)
    df['agent'].fillna(0, inplace=True)
    df['country'].fillna('others', inplace=True)
    df['children'].fillna(df['children'].mean(), inplace=True)
    df = df[df['adults'] + df['children'] + df['babies'] > 0]
    df['total people'] = df['adults'] + df['children'] + df['babies']
    df['total stayed'] = df['stays_in_weekend_nights'] + df['stays_in_week_nights']
    df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'], dayfirst=True)
    df[['children', 'company', 'agent']] = df[['children', 'company', 'agent']].astype('int64')
    df = df[df['adr'] <= 5000]
    
    return df

df = load_data()

# Sidebar Navigation
menu = st.sidebar.selectbox("📊 Choose a Section", [
    "Overview",
    "Hotel Insights",
    "Customer Preferences",
    "Cancellations & Lead Time",
    "Monthly & Yearly Trends"
])

# Section: Overview
if menu == "Overview":
    st.header("🔍 Dataset Overview")
    st.write(df.head())

    st.markdown("**Key Stats**")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Bookings", len(df))
    col2.metric("Unique Hotels", df['hotel'].nunique())
    col3.metric("Countries", df['country'].nunique())

    st.subheader("📈 Booking Distribution by Hotel Type")
    fig = px.pie(df, names='hotel', title='Hotel Booking Percentage')
    st.plotly_chart(fig, use_container_width=True)

# Section: Hotel Insights
elif menu == "Hotel Insights":
    st.header("🏨 Hotel Booking Analysis")

    hotel_adr = df.groupby('hotel')['adr'].mean().reset_index()
    fig = px.bar(hotel_adr, x='hotel', y='adr', title='Average ADR by Hotel Type', color='hotel')
    st.plotly_chart(fig, use_container_width=True)

    lead_time = df.groupby('hotel')['lead_time'].mean().reset_index()
    fig2 = px.bar(lead_time, x='hotel', y='lead_time', title='Average Lead Time by Hotel', color='hotel')
    st.plotly_chart(fig2, use_container_width=True)

    repeat_df = df[df['is_repeated_guest'] == 1].groupby('hotel').size() / df.groupby('hotel').size()
    repeat_df = repeat_df.reset_index(name='repeat_rate')
    fig3 = px.bar(repeat_df, x='hotel', y='repeat_rate', title='Repeat Guest Rate by Hotel')
    st.plotly_chart(fig3, use_container_width=True)

# Section: Customer Preferences
elif menu == "Customer Preferences":
    st.header("👥 Customer Behavior Insights")

    st.subheader("Preferred Meal Type")

    meal_counts = df['meal'].value_counts().reset_index()
    meal_counts.columns = ['meal_type', 'count']
    fig = px.bar(meal_counts, x='meal_type', y='count', labels={'meal_type': 'Meal Type', 'count': 'Count'}, title='Preferred Meal Types')
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Customer Types Distribution")
    fig = px.pie(df, names='customer_type', title='Customer Type Distribution')
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top Booking Agents")

    top_agents = df[df['agent'] != 0]['agent'].value_counts().head(10).reset_index()
    top_agents.columns = ['agent_id', 'count']

    fig = px.bar(top_agents, x='agent_id', y='count',
                labels={'agent_id': 'Agent', 'count': 'Number of Bookings'},
                title='Top 10 Booking Agents')
    st.plotly_chart(fig, use_container_width=True)


# Section: Cancellations & Lead Time
elif menu == "Cancellations & Lead Time":
    st.header("📉 Cancellations & Booking Lead Time")

    st.subheader("Cancellation Rate")
    cancel_counts = df['is_canceled'].value_counts(normalize=True).reset_index()
    cancel_counts.columns = ['Status', 'Percentage']
    cancel_counts['Status'] = cancel_counts['Status'].map({0: 'Not Canceled', 1: 'Canceled'})
    fig = px.pie(cancel_counts, names='Status', values='Percentage', title='Booking Cancellation Rate')
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Lead Time Distribution")
    fig = px.histogram(df, x='lead_time', nbins=50, title="Lead Time Distribution")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Deposit Type Preferences")

    deposit_type = df['deposit_type'].value_counts().reset_index()
    deposit_type.columns = ['deposit_type', 'count']

    fig = px.pie(deposit_type, names='deposit_type', values='count', title='Deposit Type Distribution')
    st.plotly_chart(fig, use_container_width=True)


# Section: Monthly & Yearly Trends
elif menu == "Monthly & Yearly Trends":
    st.header("📅 Time-Based Booking Trends")

    st.subheader("Monthly Booking Trends")
    monthly = df['arrival_date_month'].value_counts().reindex([
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]).reset_index()
    monthly.columns = ['Month', 'Bookings']
    fig = px.line(monthly, x='Month', y='Bookings', markers=True)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Yearly Booking Trends by Hotel")
    year_hotel = df.groupby(['arrival_date_year', 'hotel']).size().reset_index(name='Bookings')
    fig = px.bar(year_hotel, x='arrival_date_year', y='Bookings', color='hotel', barmode='group',
                 title='Bookings Per Year by Hotel')
    st.plotly_chart(fig, use_container_width=True)
