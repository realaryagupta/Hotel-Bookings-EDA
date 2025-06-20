import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Set up Streamlit
st.set_page_config(page_title="Hotel Booking Dashboard", layout="wide")

# Custom CSS for blue-green theme and professional styling
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #2E8B57;
        --secondary-color: #20B2AA;
        --accent-color: #4682B4;
        --background-color: #F0F8FF;
        --text-color: #2F4F4F;
    }
    
    /* Main app background - Black */
    .stApp {
        background-color: black !important;
    }
    
    /* Main container styling - Black background */
    .main > div {
        padding-top: 2rem;
        background: black !important;
    }
    
    /* Main content area */
    .block-container {
        background-color: black !important;
        padding-top: 2rem;
    }
    
    /* Title styling */
    .main-title {
        color: #20B2AA;
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(255,255,255,0.1);
    }
    
    .subtitle {
        color: #2E8B57;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-style: italic;
    }
    
    /* Sidebar styling - Better visibility with green text */
    .stSidebar > div:first-child {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%) !important;
        border-right: 3px solid #20B2AA;
    }
    
    /* Sidebar text color - Changed to green */
    section[data-testid="stSidebar"] * {
        color: #228B22 !important;
    }

    
    .stSidebar .stSelectbox label {
        color: #2E8B57 !important;
        font-weight: bold;
    }
    
    .stSidebar .stSelectbox > div > div {
        color: #228B22 !important;
    }
    
    .stSidebar .stButton button {
        background: linear-gradient(135deg, #2E8B57 0%, #20B2AA 100%) !important;
        color: white !important;
        border: none;
        font-weight: bold;
    }
    
    .stSidebar h3 {
        color: #2E8B57 !important;
        border-bottom: 2px solid #20B2AA;
        padding-bottom: 0.5rem;
    }
    
    .stSidebar h1, .stSidebar h2, .stSidebar h4, .stSidebar h5, .stSidebar h6 {
        color: #2E8B57 !important;
    }
    
    .stSidebar p {
        color: #228B22 !important;
    }
    
    .stSidebar .stMarkdown {
        color: #228B22 !important;
    }
    
    .stSidebar .stText {
        color: #228B22 !important;
    }
    
    /* Header styling */
    header[data-testid="stHeader"] {
        background-color: black !important;
        height: 0px;
    }
    
    /* Custom dataframe styling - Responsive table */
    .dataframe-container {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 2px solid #20B2AA;
        margin: 20px 0;
        overflow-x: auto;
        max-width: 100%;
    }
    
    /* Section headers */
    .section-header {
        color: #20B2AA;
        font-size: 2rem;
        font-weight: bold;
        margin: 2rem 0 1rem 0;
        border-bottom: 3px solid #20B2AA;
        padding-bottom: 0.5rem;
    }
    
    .subsection-header {
        color: #2E8B57;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 1.5rem 0 1rem 0;
    }
    
    /* Metric cards styling */
    .metric-card {
        background: linear-gradient(135deg, #20B2AA 0%, #2E8B57 100%);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 10px;
    }
    
    /* Streamlit metrics styling */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #20B2AA 0%, #2E8B57 100%);
        border: 1px solid #2E8B57;
        padding: 1rem;
        border-radius: 15px;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    [data-testid="metric-container"] > label {
        color: white !important;
        font-weight: bold;
    }
    
    [data-testid="metric-container"] > div {
        color: white !important;
    }
    
    /* Custom table styling - Fixed boundaries */
    .styled-table {
        border-collapse: collapse;
        margin: 15px 0;
        font-size: 0.85em;
        font-family: sans-serif;
        width: 100%;
        max-width: 100%;
        border-radius: 10px 10px 0 0;
        overflow: hidden;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
        table-layout: auto;
    }
    
    .styled-table thead tr {
        background: linear-gradient(135deg, #2E8B57 0%, #20B2AA 100%);
        color: #ffffff;
        text-align: left;
    }
    
    .styled-table th,
    .styled-table td {
        padding: 8px 12px;
        border-bottom: 1px solid #E0F6FF;
        word-wrap: break-word;
        max-width: 150px;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .styled-table tbody tr {
        background-color: #F8F9FA;
    }
    
    .styled-table tbody tr:nth-of-type(even) {
        background-color: #E9ECEF;
    }
    
    .styled-table tbody tr:hover {
        background-color: #B0E0E6;
        transition: all 0.3s ease;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #2E8B57 0%, #20B2AA 100%) !important;
        color: white !important;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        background: linear-gradient(135deg, #236B47 0%, #1A9B91 100%) !important;
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background-color: white !important;
        border: 2px solid #20B2AA !important;
        border-radius: 10px;
    }
    
    .stSelectbox label {
        color: #2E8B57 !important;
        font-weight: bold;
    }
    
    /* Text input styling */
    .stTextInput > div > div > input {
        background-color: white !important;
        border: 2px solid #20B2AA !important;
        border-radius: 10px;
        color: black !important;
    }
    
    .stTextInput label {
        color: #20B2AA !important;
        font-weight: bold;
    }
    
    /* Number input styling */
    .stNumberInput > div > div > input {
        background-color: white !important;
        border: 2px solid #20B2AA !important;
        border-radius: 10px;
        color: black !important;
    }
    
    .stNumberInput label {
        color: #20B2AA !important;
        font-weight: bold;
    }
    
    /* DataFrame styling - White background with black text */
    .dataframe {
        background-color: white !important;
        border: 2px solid #20B2AA;
        border-radius: 10px;
        color: black !important;
    }
    
    /* Ensure all table text is black */
    .dataframe tbody tr td {
        color: black !important;
    }
    
    .dataframe thead tr th {
        color: white !important;
        background: linear-gradient(135deg, #2E8B57 0%, #20B2AA 100%) !important;
    }
    
    /* Dataset overview table specific styling */
    [data-testid="stDataFrame"] {
        background-color: white !important;
    }
    
    [data-testid="stDataFrame"] table {
        background-color: white !important;
        color: black !important;
    }
    
    [data-testid="stDataFrame"] td {
        color: black !important;
        background-color: white !important;
    }
    
    [data-testid="stDataFrame"] th {
        color: white !important;
        background: linear-gradient(135deg, #2E8B57 0%, #20B2AA 100%) !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border: 2px solid #20B2AA;
        border-radius: 10px 10px 0px 0px;
        color: #2E8B57;
        font-weight: bold;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #2E8B57 0%, #20B2AA 100%);
        color: white !important;
    }
    
    /* Success message styling */
    .stSuccess {
        background-color: #E6F3E6 !important;
        border: 1px solid #2E8B57 !important;
        color: #2E8B57 !important;
    }
    
    /* Info message styling */
    .stInfo {
        background-color: #E0F7FA !important;
        border: 1px solid #20B2AA !important;
        color: #20B2AA !important;
    }
    
    /* Warning message styling */
    .stWarning {
        background-color: #FFF8E1 !important;
        border: 1px solid #FF8C00 !important;
        color: #FF8C00 !important;
    }
    
    /* Error message styling */
    .stError {
        background-color: #FFEBEE !important;
        border: 1px solid #DC143C !important;
        color: #DC143C !important;
    }
    
    /* Filter info styling */
    .filter-info {
        background: linear-gradient(135deg, #20B2AA 0%, #2E8B57 100%);
        color: white;
        padding: 10px 15px;
        border-radius: 10px;
        margin: 10px 0;
        text-align: center;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Custom function to display styled dataframe with better responsive design
def display_styled_dataframe(df, title=""):
    if title:
        st.markdown(f'<h3 class="subsection-header">{title}</h3>', unsafe_allow_html=True)
    
    # Limit columns displayed and truncate long text
    display_df = df.copy()
    
    # If dataframe is too wide, show only first few columns
    if len(display_df.columns) > 8:
        display_df = display_df.iloc[:, :8]
        st.info(f"Showing first 8 columns of {len(df.columns)} total columns")
    
    # Truncate long text in cells
    for col in display_df.columns:
        if display_df[col].dtype == 'object':
            display_df[col] = display_df[col].astype(str).apply(lambda x: x[:30] + '...' if len(x) > 30 else x)
    
    # Convert dataframe to HTML with custom styling
    df_html = display_df.to_html(classes='styled-table', escape=False, index=False)
    
    st.markdown(f'''
    <div class="dataframe-container">
        {df_html}
    </div>
    ''', unsafe_allow_html=True)

# Title with custom styling
st.markdown('<h1 class="main-title">🏨 Hotel Booking Analysis Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Created by Arya Gupta</p>', unsafe_allow_html=True)

# Set custom color palette for plots
blue_green_colors = ['#2E8B57', '#20B2AA', '#4682B4', '#5F9EA0', '#48D1CC', '#00CED1', '#40E0D0', '#00BFFF']

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

# SIDEBAR FILTERS - MOVED TO TOP
st.sidebar.markdown("### 🔍 Interactive Filters")

# Year filter
years = sorted(df['arrival_date_year'].unique())
selected_year = st.sidebar.selectbox("Select Year", ['All'] + years)

# Hotel type filter
hotel_types = df['hotel'].unique()
selected_hotel = st.sidebar.selectbox("Select Hotel Type", ['All'] + list(hotel_types))

# Customer type filter
customer_types = df['customer_type'].unique()
selected_customer = st.sidebar.selectbox("Select Customer Type", ['All'] + list(customer_types))

# Apply filters
filtered_df = df.copy()

if selected_year != 'All':
    filtered_df = filtered_df[filtered_df['arrival_date_year'] == selected_year]

if selected_hotel != 'All':
    filtered_df = filtered_df[filtered_df['hotel'] == selected_hotel]

if selected_customer != 'All':
    filtered_df = filtered_df[filtered_df['customer_type'] == selected_customer]

# Show filtered data info
if len(filtered_df) != len(df):
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Filtered Data Info")
    st.sidebar.info(f"Showing {len(filtered_df):,} of {len(df):,} bookings")
    
    # Show active filters in main area
    active_filters = []
    if selected_year != 'All':
        active_filters.append(f"Year: {selected_year}")
    if selected_hotel != 'All':
        active_filters.append(f"Hotel: {selected_hotel}")
    if selected_customer != 'All':
        active_filters.append(f"Customer: {selected_customer}")
    
    if active_filters:
        st.markdown(f'''
        <div class="filter-info">
            🔍 Active Filters: {" | ".join(active_filters)}
        </div>
        ''', unsafe_allow_html=True)

# Navigation Menu
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Navigation Menu")
menu = st.sidebar.selectbox("Choose a Section", [
    "Overview",
    "Hotel Insights",
    "Customer Preferences", 
    "Cancellations & Lead Time",
    "Monthly & Yearly Trends",
    "Advanced Analytics"
])

# Section: Overview
if menu == "Overview":
    st.markdown('<h2 class="section-header">🔍 Dataset Overview</h2>', unsafe_allow_html=True)
    
    # Display first few rows with custom styling
    display_styled_dataframe(filtered_df.head(10), "Sample Data Preview")

    st.markdown('<h3 class="subsection-header">📊 Key Statistics</h3>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'''
        <div class="metric-card">
            <h3>Total Bookings</h3>
            <h2>{len(filtered_df):,}</h2>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="metric-card">
            <h3>Unique Hotels</h3>
            <h2>{filtered_df['hotel'].nunique()}</h2>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
        <div class="metric-card">
            <h3>Countries</h3>
            <h2>{filtered_df['country'].nunique()}</h2>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown('<h3 class="subsection-header">📈 Booking Distribution by Hotel Type</h3>', unsafe_allow_html=True)
    fig = px.pie(filtered_df, names='hotel', title='Hotel Booking Percentage', 
                 color_discrete_sequence=blue_green_colors)
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2F4F4F', size=12),
        title_font=dict(color='#2E8B57', size=16)
    )
    st.plotly_chart(fig, use_container_width=True)

# Section: Hotel Insights
elif menu == "Hotel Insights":
    st.markdown('<h2 class="section-header">🏨 Hotel Booking Analysis</h2>', unsafe_allow_html=True)

    hotel_adr = filtered_df.groupby('hotel')['adr'].mean().reset_index()
    fig = px.bar(hotel_adr, x='hotel', y='adr', title='Average ADR by Hotel Type', 
                 color='hotel', color_discrete_sequence=blue_green_colors)
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2F4F4F', size=12),
        title_font=dict(color='#2E8B57', size=16)
    )
    st.plotly_chart(fig, use_container_width=True)

    lead_time = filtered_df.groupby('hotel')['lead_time'].mean().reset_index()
    fig2 = px.bar(lead_time, x='hotel', y='lead_time', title='Average Lead Time by Hotel', 
                  color='hotel', color_discrete_sequence=blue_green_colors)
    fig2.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2F4F4F', size=12),
        title_font=dict(color='#2E8B57', size=16)
    )
    st.plotly_chart(fig2, use_container_width=True)

    repeat_df = filtered_df[filtered_df['is_repeated_guest'] == 1].groupby('hotel').size() / filtered_df.groupby('hotel').size()
    repeat_df = repeat_df.reset_index(name='repeat_rate')
    fig3 = px.bar(repeat_df, x='hotel', y='repeat_rate', title='Repeat Guest Rate by Hotel',
                  color_discrete_sequence=blue_green_colors)
    fig3.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2F4F4F', size=12),
        title_font=dict(color='#2E8B57', size=16)
    )
    st.plotly_chart(fig3, use_container_width=True)

# Section: Customer Preferences
elif menu == "Customer Preferences":
    st.markdown('<h2 class="section-header">👥 Customer Behavior Insights</h2>', unsafe_allow_html=True)

    st.markdown('<h3 class="subsection-header">🍽️ Preferred Meal Type</h3>', unsafe_allow_html=True)

    meal_counts = filtered_df['meal'].value_counts().reset_index()
    meal_counts.columns = ['meal_type', 'count']
    fig = px.bar(meal_counts, x='meal_type', y='count', 
                 labels={'meal_type': 'Meal Type', 'count': 'Count'}, 
                 title='Preferred Meal Types', color_discrete_sequence=blue_green_colors)
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2F4F4F', size=12),
        title_font=dict(color='#2E8B57', size=16)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<h3 class="subsection-header">👤 Customer Types Distribution</h3>', unsafe_allow_html=True)
    fig = px.pie(filtered_df, names='customer_type', title='Customer Type Distribution',
                 color_discrete_sequence=blue_green_colors)
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2F4F4F', size=12),
        title_font=dict(color='#2E8B57', size=16)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<h3 class="subsection-header">🏢 Top Booking Agents</h3>', unsafe_allow_html=True)

    top_agents = filtered_df[filtered_df['agent'] != 0]['agent'].value_counts().head(10).reset_index()
    top_agents.columns = ['agent_id', 'count']

    if len(top_agents) > 0:
        fig = px.bar(top_agents, x='agent_id', y='count',
                    labels={'agent_id': 'Agent', 'count': 'Number of Bookings'},
                    title='Top 10 Booking Agents', color_discrete_sequence=blue_green_colors)
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#2F4F4F', size=12),
            title_font=dict(color='#2E8B57', size=16)
        )
        st.plotly_chart(fig, use_container_width=True)

        # Display top agents table with styling
        display_styled_dataframe(top_agents, "Top Agents Summary")
    else:
        st.info("No agent data available for the current filters.")

# Section: Cancellations & Lead Time
elif menu == "Cancellations & Lead Time":
    st.markdown('<h2 class="section-header">📉 Cancellations & Booking Lead Time</h2>', unsafe_allow_html=True)

    st.markdown('<h3 class="subsection-header">❌ Cancellation Rate</h3>', unsafe_allow_html=True)
    cancel_counts = filtered_df['is_canceled'].value_counts(normalize=True).reset_index()
    cancel_counts.columns = ['Status', 'Percentage']
    cancel_counts['Status'] = cancel_counts['Status'].map({0: 'Not Canceled', 1: 'Canceled'})
    fig = px.pie(cancel_counts, names='Status', values='Percentage', 
                 title='Booking Cancellation Rate', color_discrete_sequence=blue_green_colors)
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2F4F4F', size=12),
        title_font=dict(color='#2E8B57', size=16)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<h3 class="subsection-header">⏰ Lead Time Distribution</h3>', unsafe_allow_html=True)
    fig = px.histogram(filtered_df, x='lead_time', nbins=50, title="Lead Time Distribution",
                       color_discrete_sequence=blue_green_colors)
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2F4F4F', size=12),
        title_font=dict(color='#2E8B57', size=16)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<h3 class="subsection-header">💰 Deposit Type Preferences</h3>', unsafe_allow_html=True)

    deposit_type = filtered_df['deposit_type'].value_counts().reset_index()
    deposit_type.columns = ['deposit_type', 'count']

    fig = px.pie(deposit_type, names='deposit_type', values='count', 
                 title='Deposit Type Distribution', color_discrete_sequence=blue_green_colors)
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2F4F4F', size=12),
        title_font=dict(color='#2E8B57', size=16)
    )
    st.plotly_chart(fig, use_container_width=True)

    # Display deposit type summary table
    display_styled_dataframe(deposit_type, "Deposit Type Summary")

# Section: Monthly & Yearly Trends
elif menu == "Monthly & Yearly Trends":
    st.markdown('<h2 class="section-header">📅 Time-Based Booking Trends</h2>', unsafe_allow_html=True)

    st.markdown('<h3 class="subsection-header">📊 Monthly Booking Trends</h3>', unsafe_allow_html=True)
    monthly = filtered_df['arrival_date_month'].value_counts().reindex([
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]).reset_index()
    monthly.columns = ['Month', 'Bookings']
    fig = px.line(monthly, x='Month', y='Bookings', markers=True,
                  line_shape='spline', color_discrete_sequence=blue_green_colors)
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2F4F4F', size=12),
        title_font=dict(color='#2E8B57', size=16)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<h3 class="subsection-header">📈 Yearly Booking Trends by Hotel</h3>', unsafe_allow_html=True)
    year_hotel = filtered_df.groupby(['arrival_date_year', 'hotel']).size().reset_index(name='Bookings')
    fig = px.bar(year_hotel, x='arrival_date_year', y='Bookings', color='hotel', barmode='group',
                 title='Bookings Per Year by Hotel', color_discrete_sequence=blue_green_colors)
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2F4F4F', size=12),
        title_font=dict(color='#2E8B57', size=16)
    )
    st.plotly_chart(fig, use_container_width=True)

    # Display monthly summary table
    display_styled_dataframe(monthly, "Monthly Bookings Summary")

    # Display yearly summary table
    display_styled_dataframe(year_hotel, "Yearly Bookings Summary")

# Additional Analytics Section
elif menu == "Advanced Analytics":
    st.markdown('<h2 class="section-header">🔬 Advanced Analytics</h2>', unsafe_allow_html=True)
    
    # Create tabs for different advanced analytics
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Correlation Analysis", "💰 Revenue Analysis", "🌍 Geographic Insights", "📈 Predictive Insights"])
    
    with tab1:
        st.markdown('<h3 class="subsection-header">🔗 Feature Correlation Matrix</h3>', unsafe_allow_html=True)
        
        # Select numeric columns for correlation
        numeric_cols = ['lead_time', 'stays_in_weekend_nights', 'stays_in_week_nights', 
                       'adults', 'children', 'babies', 'previous_cancellations',
                       'previous_bookings_not_canceled', 'booking_changes', 'adr',
                       'required_car_parking_spaces', 'total_of_special_requests',
                       'is_canceled', 'total people', 'total stayed']
        
        # Calculate correlation matrix
        corr_data = filtered_df[numeric_cols].corr()
        
        # Create correlation heatmap using plotly
        fig = px.imshow(corr_data, 
                       text_auto=True, 
                       aspect="auto",
                       color_continuous_scale=px.colors.sequential.Teal,
                       title="Feature Correlation Heatmap")
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#2F4F4F', size=10),
            title_font=dict(color='#2E8B57', size=16),
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Key insights from correlation
        st.info("🔍 **Key Insights**: Strong correlations exist between total people and adults, and between total stayed and weekend/weeknight stays.")
    
    with tab2:
        st.markdown('<h3 class="subsection-header">💰 Revenue & ADR Analysis</h3>', unsafe_allow_html=True)
        
        # ADR distribution by hotel type
        fig1 = px.box(filtered_df, x='hotel', y='adr', 
                     title='ADR Distribution by Hotel Type',
                     color='hotel',
                     color_discrete_sequence=blue_green_colors)
        fig1.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#2F4F4F', size=12),
            title_font=dict(color='#2E8B57', size=16)
        )
        st.plotly_chart(fig1, use_container_width=True)
        
        # Revenue by customer type
        customer_revenue = filtered_df.groupby('customer_type').agg({
            'adr': 'mean',
            'total stayed': 'mean'
        }).reset_index()
        customer_revenue['estimated_revenue'] = customer_revenue['adr'] * customer_revenue['total stayed']
        
        fig2 = px.bar(customer_revenue, x='customer_type', y='estimated_revenue',
                     title='Estimated Revenue per Customer Type',
                     color='customer_type',
                     color_discrete_sequence=blue_green_colors)
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#2F4F4F', size=12),
            title_font=dict(color='#2E8B57', size=16)
        )
        st.plotly_chart(fig2, use_container_width=True)
        
        # Revenue summary table
        display_styled_dataframe(customer_revenue, "Revenue Analysis by Customer Type")
    
    with tab3:
        st.markdown('<h3 class="subsection-header">🌍 Geographic Distribution</h3>', unsafe_allow_html=True)
        
        # Top 15 countries by bookings
        top_countries = filtered_df['country'].value_counts().head(15).reset_index()
        top_countries.columns = ['Country', 'Bookings']
        
        fig1 = px.bar(top_countries, x='Bookings', y='Country', orientation='h',
                     title='Top 15 Countries by Bookings',
                     color='Bookings',
                     color_continuous_scale=px.colors.sequential.Teal)
        fig1.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#2F4F4F', size=12),
            title_font=dict(color='#2E8B57', size=16),
            height=600
        )
        st.plotly_chart(fig1, use_container_width=True)
        
        # Country-wise cancellation rate
        country_cancel = filtered_df.groupby('country').agg({
            'is_canceled': ['count', 'sum']
        }).reset_index()
        country_cancel.columns = ['Country', 'Total_Bookings', 'Cancellations']
        country_cancel = country_cancel[country_cancel['Total_Bookings'] >= 50]  # Filter countries with at least 50 bookings
        country_cancel['Cancellation_Rate'] = (country_cancel['Cancellations'] / country_cancel['Total_Bookings'] * 100).round(2)
        country_cancel = country_cancel.sort_values('Cancellation_Rate', ascending=False).head(10)
        
        fig2 = px.bar(country_cancel, x='Country', y='Cancellation_Rate',
                     title='Top 10 Countries by Cancellation Rate (Min 50 bookings)',
                     color='Cancellation_Rate',
                     color_continuous_scale=px.colors.sequential.Reds)
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#2F4F4F', size=12),
            title_font=dict(color='#2E8B57', size=16)
        )
        st.plotly_chart(fig2, use_container_width=True)
        
        # Display geographic summary tables
        col1, col2 = st.columns(2)
        with col1:
            display_styled_dataframe(top_countries.head(10), "Top 10 Countries by Bookings")
        with col2:
            display_styled_dataframe(country_cancel.head(10), "Highest Cancellation Rates by Country")
    
    with tab4:
        st.markdown('<h3 class="subsection-header">📈 Predictive Insights & Patterns</h3>', unsafe_allow_html=True)
        
        # Lead time vs Cancellation analysis
        filtered_df['lead_time_category'] = pd.cut(filtered_df['lead_time'], 
                                                  bins=[0, 30, 90, 180, 365, 1000], 
                                                  labels=['0-30 days', '31-90 days', '91-180 days', '181-365 days', '365+ days'])
        
        lead_cancel = filtered_df.groupby('lead_time_category').agg({
            'is_canceled': ['count', 'sum']
        }).reset_index()
        lead_cancel.columns = ['Lead_Time_Category', 'Total_Bookings', 'Cancellations']
        lead_cancel['Cancellation_Rate'] = (lead_cancel['Cancellations'] / lead_cancel['Total_Bookings'] * 100).round(2)
        
        fig1 = px.bar(lead_cancel, x='Lead_Time_Category', y='Cancellation_Rate',
                     title='Cancellation Rate by Lead Time Category',
                     color='Cancellation_Rate',
                     color_continuous_scale=px.colors.sequential.Reds)
        fig1.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#2F4F4F', size=12),
            title_font=dict(color='#2E8B57', size=16)
        )
        st.plotly_chart(fig1, use_container_width=True)
        
        # Booking changes vs Cancellation
        changes_cancel = filtered_df.groupby('booking_changes').agg({
            'is_canceled': ['count', 'sum']
        }).reset_index()
        changes_cancel.columns = ['Booking_Changes', 'Total_Bookings', 'Cancellations']
        changes_cancel = changes_cancel[changes_cancel['Total_Bookings'] >= 10]  # Filter for meaningful data
        changes_cancel['Cancellation_Rate'] = (changes_cancel['Cancellations'] / changes_cancel['Total_Bookings'] * 100).round(2)
        
        fig2 = px.scatter(changes_cancel, x='Booking_Changes', y='Cancellation_Rate',
                         size='Total_Bookings',
                         title='Relationship between Booking Changes and Cancellation Rate',
                         color='Cancellation_Rate',
                         color_continuous_scale=px.colors.sequential.Viridis)
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#2F4F4F', size=12),
            title_font=dict(color='#2E8B57', size=16)
        )
        st.plotly_chart(fig2, use_container_width=True)
        
        # Special requests analysis
        special_req_stats = filtered_df.groupby('total_of_special_requests').agg({
            'adr': 'mean',
            'is_canceled': 'mean',
            'customer_type': lambda x: x.mode().iloc[0] if not x.empty else 'Unknown'
        }).reset_index()
        special_req_stats.columns = ['Special_Requests', 'Avg_ADR', 'Cancellation_Rate', 'Most_Common_Customer_Type']
        special_req_stats['Cancellation_Rate'] = (special_req_stats['Cancellation_Rate'] * 100).round(2)
        special_req_stats = special_req_stats[special_req_stats['Special_Requests'] <= 5]  # Focus on 0-5 requests
        
        fig3 = px.line(special_req_stats, x='Special_Requests', y='Avg_ADR',
                      title='Average Daily Rate vs Number of Special Requests',
                      markers=True,
                      color_discrete_sequence=blue_green_colors)
        fig3.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#2F4F4F', size=12),
            title_font=dict(color='#2E8B57', size=16)
        )
        st.plotly_chart(fig3, use_container_width=True)
        
        # Display predictive insights tables
        col1, col2 = st.columns(2)
        with col1:
            display_styled_dataframe(lead_cancel, "Lead Time vs Cancellation Analysis")
        with col2:
            display_styled_dataframe(special_req_stats, "Special Requests Impact Analysis")
        
        # Key insights
        st.success("🎯 **Key Predictive Insights**: Longer lead times correlate with higher cancellation rates. Customers with more special requests tend to have higher ADR but varying cancellation patterns.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #2E8B57; font-style: italic; margin-top: 2rem;">
    📊 Hotel Booking Analysis Dashboard | Created by Arya Gupta | Data-Driven Insights for Hospitality Management
</div>
""", unsafe_allow_html=True)