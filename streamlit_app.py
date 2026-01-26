"""
Uber Eats Data Visualization Dashboard
======================================
Interactive Streamlit app for exploring Uber Eats delivery data.

Run with: streamlit run streamlit_app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Uber Eats Analytics Dashboard",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #06C167;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #06C167;
    }
    </style>
""", unsafe_allow_html=True)

# File paths
CLEANED_FILE = "cleaned_uber_eats_data.csv"


@st.cache_data
def load_data():
    """Load cleaned data with caching."""
    try:
        df = pd.read_csv(CLEANED_FILE)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.info("Make sure you've run the cleaning script first: python 'CLEANING PART.py'")
        return None


def display_overview(df):
    """Display overview metrics."""
    st.markdown("### 📊 Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📦 Total Orders", f"{len(df):,}")
    
    with col2:
        if 'Restaurant ID' in df.columns:
            st.metric("🏪 Restaurants", f"{df['Restaurant ID'].nunique()}")
    
    with col3:
        if 'Driver ID' in df.columns:
            st.metric("🚗 Drivers", f"{df['Driver ID'].nunique()}")
    
    with col4:
        if 'Net_Revenue' in df.columns:
            st.metric("💰 Total Revenue", f"${df['Net_Revenue'].sum():,.0f}")


def plot_daily_orders(df):
    """Plot daily order volume with big visual impact."""
    st.markdown("### 📈 Orders Over Time")
    st.caption("December 2025: Days 1-31 (Note: Spike on Days 25-31 = Holiday Season)")
    
    if 'Day' not in df.columns:
        st.warning("Day column not available")
        return
    
    daily_orders = df.groupby('Day').size().reset_index(name='Orders')
    
    # Create a more visual chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=daily_orders['Day'],
        y=daily_orders['Orders'],
        mode='lines+markers',
        fill='tozeroy',
        line=dict(color='#06C167', width=3),
        marker=dict(size=8, color='#06C167'),
        name='Orders'
    ))
    
    fig.update_layout(
        title='Daily Order Volume',
        xaxis_title='Day of Month',
        yaxis_title='Orders',
        height=450,
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#E0E0E0')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#E0E0E0')
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Big number insights
    col1, col2, col3, col4 = st.columns(4)
    peak_day = daily_orders.loc[daily_orders['Orders'].idxmax()]
    avg_orders = daily_orders['Orders'].mean()
    
    # Calculate non-holiday average (days 1-24)
    non_holiday_orders = daily_orders[daily_orders['Day'] <= 24]['Orders'].mean()
    holiday_orders = daily_orders[daily_orders['Day'] >= 25]['Orders'].mean()
    
    with col1:
        st.metric("🔥 Peak Day", f"Day {int(peak_day['Day'])}", f"{int(peak_day['Orders'])} orders")
    with col2:
        st.metric("📊 Typical Daily", f"{int(non_holiday_orders)}", "orders (Days 1-24)")
    with col3:
        st.metric("🎄 Holiday Avg", f"{int(holiday_orders)}", f"+{int((holiday_orders/non_holiday_orders-1)*100)}%")
    with col4:
        total_days = len(daily_orders)
        st.metric("📅 Days Tracked", f"{total_days}", "December 2025")


def plot_weekly_patterns(df):
    """Plot day of week patterns with simple visuals."""
    st.markdown("### 📅 Orders by Day of Week")
    
    if 'DayOfWeek' not in df.columns:
        st.info("💡 Day of week analysis available in cleaned data")
        return
    
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekly_orders = df.groupby('DayOfWeek').size().reindex([d for d in day_order if d in df['DayOfWeek'].unique()])
    
    # Simple, clean bar chart
    fig = px.bar(
        x=weekly_orders.index, 
        y=weekly_orders.values,
        labels={'x': 'Day', 'y': 'Orders'},
        color=weekly_orders.values,
        color_continuous_scale=['#A8E6CF', '#06C167']
    )
    
    fig.update_layout(
        height=400,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Simple insight boxes
    if 'IsWeekend' in df.columns:
        col1, col2 = st.columns(2)
        with col1:
            weekday_orders = df[df['IsWeekend'] == 0].shape[0]
            st.metric("📋 Weekday Orders", f"{weekday_orders:,}")
        with col2:
            weekend_orders = df[df['IsWeekend'] == 1].shape[0]
            st.metric("🎉 Weekend Orders", f"{weekend_orders:,}")


def plot_time_analysis(df):
    """Analyze and plot time-related metrics."""
    st.markdown("### ⏱️ Delivery Time Analysis")
    
    if 'DayOfWeek' not in df.columns:
        st.warning("Day of week data not available")
        return
    
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekly_orders = df.groupby('DayOfWeek').size().reindex([d for d in day_order if d in df['DayOfWeek'].unique()])
    
    fig = go.Figure(data=[
        go.Bar(x=weekly_orders.index, y=weekly_orders.values,
               marker_color=['#06C167' if day in ['Friday', 'Saturday', 'Sunday'] else '#5FB560' 
                            for day in weekly_orders.index])
    ])
    
    fig.update_layout(
        title='Orders by Day of Week',
        xaxis_title='Day of Week',
        yaxis_title='Number of Orders',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Weekend vs Weekday comparison
    if 'IsWeekend' in df.columns:
        weekend_pct = (df['IsWeekend'].sum() / len(df)) * 100
        st.info(f"📌 **Weekend Orders**: {weekend_pct:.1f}% of total volume")


def plot_time_analysis(df):
    """Analyze and plot time-related metrics."""
    st.markdown("### ⏱️ Delivery Time Analysis")
    
    time_columns = [col for col in df.columns if 'time' in col.lower() or 'duration' in col.lower() or 'wait' in col.lower()]
    
    if not time_columns:
        st.warning("No time-related columns found")
        return
    
    # Let user select which time metric to analyze
    selected_col = st.selectbox("Select time metric:", time_columns)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution plot
        fig = px.histogram(df, x=selected_col, nbins=50,
                          title=f'Distribution of {selected_col}',
                          labels={selected_col: 'Time (minutes)'},
                          color_discrete_sequence=['#06C167'])
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Box plot
        fig = px.box(df, y=selected_col,
                    title=f'{selected_col} - Box Plot',
                    labels={selected_col: 'Time (minutes)'},
                    color_discrete_sequence=['#06C167'])
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    # Statistics - ensure numeric conversion
    col1, col2, col3, col4 = st.columns(4)
    numeric_col = pd.to_numeric(df[selected_col], errors='coerce')
    with col1:
        st.metric("Mean", f"{numeric_col.mean():.1f} min")
    with col2:
        st.metric("Median", f"{numeric_col.median():.1f} min")
    with col3:
        st.metric("Std Dev", f"{numeric_col.std():.1f} min")
    with col4:
        st.metric("Max", f"{numeric_col.max():.1f} min")
    
    # Heatmap: Time by Day of Week and Hour
    st.markdown("#### 🔥 Time Heatmap: Day of Week vs Hour")
    
    # Create a copy with valid data
    df_heatmap = df.copy()
    df_heatmap[selected_col] = pd.to_numeric(df_heatmap[selected_col], errors='coerce')
    df_heatmap = df_heatmap[(df_heatmap[selected_col] > 0) & (df_heatmap[selected_col] < 500)]
    
    if 'DayOfWeek' in df_heatmap.columns and 'Hour' in df_heatmap.columns:
        # Create pivot table for heatmap
        heatmap_data = df_heatmap.pivot_table(
            values=selected_col, 
            index='DayOfWeek', 
            columns='Hour', 
            aggfunc='mean'
        )
        
        # Order days correctly
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        heatmap_data = heatmap_data.reindex([d for d in day_order if d in heatmap_data.index])
        
        # Create heatmap
        fig = px.imshow(heatmap_data,
                       labels=dict(x="Hour of Day", y="Day of Week", color="Minutes"),
                       x=heatmap_data.columns,
                       y=heatmap_data.index,
                       color_continuous_scale='RdYlGn_r',
                       aspect="auto",
                       title=f'Average {selected_col} by Day and Hour')
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Heatmap requires 'DayOfWeek' and 'Hour' columns")
    
    # Time trends by delivery region
    if 'Delivery Region' in df_heatmap.columns:
        st.markdown("#### 📊 Time Analysis by Delivery Region")
        
        region_time = df_heatmap.groupby('Delivery Region')[selected_col].agg(['mean', 'median', 'count']).reset_index()
        region_time.columns = ['Region', 'Average', 'Median', 'Order Count']
        
        fig = px.bar(region_time, 
                    x='Region', 
                    y='Average',
                    title=f'Average {selected_col} by Region',
                    labels={'Average': 'Minutes'},
                    color='Average',
                    color_continuous_scale='RdYlGn_r',
                    text='Average')
        
        fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)


def plot_restaurant_performance(df):
    """Analyze restaurant performance."""
    st.markdown("### 🏪 Restaurant Performance")
    
    restaurant_col = [col for col in df.columns if 'restaurant' in col.lower() and 'id' in col.lower()]
    
    if not restaurant_col:
        st.warning("No restaurant ID column found")
        return
    
    restaurant_col = restaurant_col[0]
    
    # Top restaurants by order volume
    top_n = st.slider("Show top N restaurants:", 5, 50, 20)
    restaurant_orders = df.groupby(restaurant_col).size().sort_values(ascending=False).head(top_n)
    
    fig = px.bar(x=restaurant_orders.values, y=restaurant_orders.index.astype(str),
                 orientation='h',
                 title=f'Top {top_n} Restaurants by Order Volume',
                 labels={'x': 'Number of Orders', 'y': 'Restaurant ID'},
                 color=restaurant_orders.values,
                 color_continuous_scale='Greens')
    
    fig.update_layout(height=max(400, top_n * 20))
    st.plotly_chart(fig, use_container_width=True)


def plot_driver_performance(df):
    """Analyze driver performance."""
    st.markdown("### 🚗 Driver Performance")
    
    driver_col = [col for col in df.columns if 'driver' in col.lower() and 'id' in col.lower()]
    
    if not driver_col:
        st.warning("No driver ID column found")
        return
    
    driver_col = driver_col[0]
    
    # Driver delivery distribution
    driver_deliveries = df.groupby(driver_col).size()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution of deliveries per driver
        fig = px.histogram(driver_deliveries, nbins=30,
                          title='Distribution of Deliveries per Driver',
                          labels={'value': 'Deliveries per Driver', 'count': 'Number of Drivers'},
                          color_discrete_sequence=['#06C167'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Top drivers
        top_drivers = driver_deliveries.sort_values(ascending=False).head(15)
        fig = px.bar(x=top_drivers.values, y=top_drivers.index.astype(str),
                    orientation='h',
                    title='Top 15 Drivers by Deliveries',
                    labels={'x': 'Number of Deliveries', 'y': 'Driver ID'},
                    color=top_drivers.values,
                    color_continuous_scale='Greens')
        st.plotly_chart(fig, use_container_width=True)
    
    # Summary stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Drivers", f"{len(driver_deliveries):,}")
    with col2:
        st.metric("Avg Deliveries/Driver", f"{driver_deliveries.mean():.1f}")
    with col3:
        st.metric("Max Deliveries", f"{driver_deliveries.max()}")


def plot_value_analysis(df):
    """Analyze order values and revenue."""
    st.markdown("### 💰 Revenue & Value Analysis")
    
    value_cols = [col for col in df.columns if 'value' in col.lower() or 'price' in col.lower() or 'amount' in col.lower()]
    
    if not value_cols:
        st.warning("No value/price columns found")
        return
    
    selected_col = st.selectbox("Select value metric:", value_cols, key='value_metric')
    
    # Total revenue metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Revenue", f"${df[selected_col].sum():,.2f}")
    with col2:
        st.metric("Average Order Value", f"${df[selected_col].mean():.2f}")
    with col3:
        st.metric("Median Order Value", f"${df[selected_col].median():.2f}")
    with col4:
        st.metric("Max Order Value", f"${df[selected_col].max():.2f}")
    
    # Revenue by day
    if 'Day' in df.columns:
        daily_revenue = df.groupby('Day')[selected_col].sum().reset_index()
        
        fig = px.area(daily_revenue, x='Day', y=selected_col,
                     title='Daily Revenue',
                     labels={'Day': 'Day of Month', selected_col: 'Revenue ($)'},
                     color_discrete_sequence=['#06C167'])
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)


def show_data_explorer(df):
    """Interactive data explorer."""
    st.markdown("### 🔍 Data Explorer")
    
    # Column selector
    columns_to_show = st.multiselect(
        "Select columns to display:",
        options=df.columns.tolist(),
        default=df.columns[:10].tolist()
    )
    
    # Filter options
    with st.expander("🔧 Apply Filters"):
        if 'Day' in df.columns:
            day_range = st.slider("Filter by day range:", 
                                int(df['Day'].min()), 
                                int(df['Day'].max()), 
                                (int(df['Day'].min()), int(df['Day'].max())))
            df = df[df['Day'].between(day_range[0], day_range[1])]
        
        if 'DayOfWeek' in df.columns:
            selected_days = st.multiselect("Filter by day of week:",
                                          options=df['DayOfWeek'].unique(),
                                          default=df['DayOfWeek'].unique())
            df = df[df['DayOfWeek'].isin(selected_days)]
    
    # Display data
    st.dataframe(df[columns_to_show], use_container_width=True, height=400)
    
    # Download option
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv,
        file_name="uber_eats_filtered_data.csv",
        mime="text/csv"
    )


def display_key_insights(df):
    """Display comprehensive key insights analysis."""
    st.header("🔍 Key Insights")
    st.markdown("Comprehensive analysis of December 2025 delivery data")
    st.warning("🎄 **Holiday Context**: December 25-31 shows elevated activity due to Christmas and New Year's week. This represents peak season, not typical daily volume.")
    
    # Filter for valid data
    df_valid = df[
        (df['Total_Delivery_Time (min)'] > 0) & 
        (df['Total_Delivery_Time (min)'] < 500) &
        (df['Restaurant_Prep_Time (min)'] > 0) &
        (df['Restaurant_Prep_Time (min)'] < 200)
    ].copy()
    
    st.info(f"📊 Analyzing {len(df_valid):,} valid orders out of {len(df):,} total ({len(df_valid)/len(df)*100:.1f}%)")
    
    # ========== BUSIEST TIMES ==========
    st.subheader("📅 Busiest Times")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Busiest Days of the Week**")
        daily = df.groupby('DayOfWeek').size().sort_values(ascending=False)
        for day, count in daily.items():
            pct = count/len(df)*100
            st.metric(day, f"{count:,} orders", f"{pct:.1f}%")
    
    with col2:
        st.markdown("**Peak Ordering Hours**")
        hourly = df.groupby('Hour_of_Day').size().sort_values(ascending=False).head(5)
        for hour, count in hourly.items():
            pct = count/len(df)*100
            st.metric(f"{int(hour):02d}:00", f"{count:,} orders", f"{pct:.1f}%")
    
    st.markdown("---")
    
    # ========== DELIVERY PERFORMANCE ==========
    st.subheader("🚗 Delivery Performance")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Total Delivery Time**")
        dt = df_valid['Total_Delivery_Time (min)']
        st.metric("Average", f"{dt.mean():.1f} min")
        st.metric("Median", f"{dt.median():.1f} min")
        st.caption(f"25th-75th percentile: {dt.quantile(0.25):.1f}-{dt.quantile(0.75):.1f} min")
    
    with col2:
        st.markdown("**Restaurant Prep Time**")
        rp = df_valid['Restaurant_Prep_Time (min)']
        st.metric("Average", f"{rp.mean():.1f} min")
        st.metric("Median", f"{rp.median():.1f} min")
        st.caption(f"25th-75th percentile: {rp.quantile(0.25):.1f}-{rp.quantile(0.75):.1f} min")
    
    with col3:
        st.markdown("**Fastest Region**")
        fastest = df_valid.groupby('Delivery Region')['Total_Delivery_Time (min)'].mean().sort_values()
        for region, time in fastest.items():
            st.metric(region, f"{time:.1f} min")
    
    st.markdown("---")
    
    # ========== REVENUE INSIGHTS ==========
    st.subheader("💰 Revenue Insights")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Revenue", f"${df['Net_Revenue'].sum():,.0f}")
        st.metric("Average Order", f"${df['Net_Revenue'].mean():.2f}")
    
    with col2:
        st.metric("Median Order", f"${df['Net_Revenue'].median():.2f}")
        st.metric("Highest Order", f"${df['Net_Revenue'].max():.2f}")
    
    with col3:
        st.metric("Total Discounts", f"${df['Amount of discount'].sum():,.0f}")
        st.metric("Total Tips", f"${df['Amount of tip'].sum():,.0f}")
    
    with col4:
        st.metric("Total Refunds", f"${df['Refunded amount'].sum():,.0f}")
        weekend_avg = df[df['IsWeekend'] == 1]['Net_Revenue'].mean()
        weekday_avg = df[df['IsWeekend'] == 0]['Net_Revenue'].mean()
        st.metric("Weekend Avg", f"${weekend_avg:.2f}", f"{((weekend_avg-weekday_avg)/weekday_avg*100):.1f}%")
    
    st.markdown("---")
    
    # ========== ORDER TYPES ==========
    st.subheader("📦 Order Types & Patterns")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**ASAP vs Scheduled**")
        order_types = df.groupby('Is ASAP').agg({
            'Day': 'count',
            'Net_Revenue': 'mean'
        })
        order_types.index = ['Scheduled', 'ASAP']
        for order_type, row in order_types.iterrows():
            pct = row['Day']/len(df)*100
            st.metric(order_type, f"{int(row['Day']):,} orders ({pct:.1f}%)", f"${row['Net_Revenue']:.2f} avg")
    
    with col2:
        st.markdown("**Weekend vs Weekday**")
        weekend = df[df['IsWeekend'] == 1]
        weekday = df[df['IsWeekend'] == 0]
        st.metric("Weekday", f"{len(weekday):,} orders ({len(weekday)/len(df)*100:.1f}%)", 
                  f"${weekday['Net_Revenue'].mean():.2f} avg")
        st.metric("Weekend", f"{len(weekend):,} orders ({len(weekend)/len(df)*100:.1f}%)", 
                  f"${weekend['Net_Revenue'].mean():.2f} avg")
    
    st.markdown("---")
    
    # ========== REGIONAL PERFORMANCE ==========
    st.subheader("🌍 Regional Performance")
    regions = df.groupby('Delivery Region').agg({
        'Day': 'count',
        'Net_Revenue': 'sum'
    }).sort_values('Day', ascending=False)
    
    for region, row in regions.iterrows():
        avg_order = row['Net_Revenue'] / row['Day']
        col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
        with col1:
            st.metric("Region", region)
        with col2:
            st.metric("Orders", f"{int(row['Day']):,}")
        with col3:
            st.metric("Revenue", f"${row['Net_Revenue']:,.0f}")
        with col4:
            st.metric("Avg/Order", f"${avg_order:.2f}")
    
    st.markdown("---")
    
    # ========== TOP PERFORMERS ==========
    st.subheader("🏆 Top Performers")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Top 10 Drivers**")
        top_drivers = df.groupby('Driver ID').agg({
            'Day': 'count',
            'Net_Revenue': 'sum'
        }).sort_values('Day', ascending=False).head(10)
        top_drivers.columns = ['Orders', 'Total_Revenue']
        top_drivers['Avg_per_Order'] = top_drivers['Total_Revenue'] / top_drivers['Orders']
        
        for idx, (driver_id, row) in enumerate(top_drivers.iterrows(), 1):
            with st.expander(f"{idx}. Driver {driver_id} - {int(row['Orders'])} orders"):
                col_a, col_b = st.columns(2)
                col_a.metric("Total Revenue", f"${row['Total_Revenue']:,.0f}")
                col_b.metric("Avg per Order", f"${row['Avg_per_Order']:.2f}")
    
    with col2:
        st.markdown("**Top 10 Restaurants**")
        top_restaurants = df.groupby('Restaurant ID').agg({
            'Day': 'count',
            'Net_Revenue': 'sum'
        }).sort_values('Day', ascending=False).head(10)
        top_restaurants.columns = ['Orders', 'Total_Revenue']
        top_restaurants['Avg_per_Order'] = top_restaurants['Total_Revenue'] / top_restaurants['Orders']
        
        for idx, (rest_id, row) in enumerate(top_restaurants.iterrows(), 1):
            with st.expander(f"{idx}. Restaurant {rest_id} - {int(row['Orders'])} orders"):
                col_a, col_b = st.columns(2)
                col_a.metric("Total Revenue", f"${row['Total_Revenue']:,.0f}")
                col_b.metric("Avg per Order", f"${row['Avg_per_Order']:.2f}")
    
    st.markdown("---")
    
    # ========== HOLIDAY IMPACT ==========
    st.subheader("🎄 Holiday Period Impact (Dec 25-31)")
    st.caption("Christmas through New Year's week shows significantly elevated activity")
    holiday = df[df['IsHolidayPeriod'] == 1]
    non_holiday = df[df['IsHolidayPeriod'] == 0]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Holiday Orders", f"{len(holiday):,}", 
                  f"${holiday['Net_Revenue'].mean():.2f} avg")
    with col2:
        st.metric("Typical Orders (Dec 1-24)", f"{len(non_holiday):,}", 
                  f"${non_holiday['Net_Revenue'].mean():.2f} avg")
    with col3:
        volume_increase = ((len(holiday)/7) / (len(non_holiday)/24) - 1) * 100
        revenue_increase = (holiday['Net_Revenue'].mean() / non_holiday['Net_Revenue'].mean() - 1) * 100
        st.metric("Volume Increase", f"+{volume_increase:.1f}%", f"Revenue: +{revenue_increase:.1f}%")


def display_strategy(df):
    """Display assumptions and strategic recommendations in PPT-friendly format."""
    st.header("🎯 Assumptions & Strategic Recommendations")
    st.caption("Clear, actionable insights for presentation")
    st.markdown("---")
    
    # ========== ASSUMPTIONS ==========
    st.subheader("📋 Data Assumptions & Context")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **Dataset Overview:**
        - **Time Period**: December 1-31, 2025 (One month)
        - **Geography**: California - 3 delivery regions
        - **Order Volume**: 18,078 total deliveries
        - **Features**: 26 data points per order
        
        **Key Assumptions:**
        1. **Holiday Spike (Dec 25-31)**: The elevated order volume during Christmas week represents seasonal peak, not typical daily demand
        2. **Geographic Focus**: Palo Alto dominates with 63% of orders - reflects early market adoption, not final state
        3. **Data Quality**: All timestamps converted to minutes; missing values filled with historical averages
        4. **Order Types**: 80% ASAP vs 20% Scheduled reflects current user behavior
        """)
    
    with col2:
        st.metric("📦 Total Orders", "18,078")
        st.metric("💰 Total Revenue", f"${df['Net_Revenue'].sum():,.0f}")
        st.metric("📍 Regions", "3")
        st.metric("🗓️ Days Analyzed", "31")
        st.metric("🎄 Holiday Period", "7 days")
    
    st.markdown("---")
    
    # ========== STRATEGIC RECOMMENDATIONS ==========
    st.subheader("🚀 Top 4 Strategic Recommendations")
    st.caption("Prioritized by ROI and implementation feasibility")
    
    # RECOMMENDATION 1
    with st.container():
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown("### 1️⃣")
            st.markdown("**Priority**")
            st.success("HIGH")
        with col2:
            st.markdown("### 🎯 Boost Scheduled Orders")
            st.markdown("""
            **Current State**: Only 20% of orders are scheduled in advance  
            **Opportunity**: Scheduled orders generate **82% higher revenue** ($79.06 vs $43.48)  
            
            **Action Plan**:
            - Offer 5-10% discount for orders scheduled 2+ hours in advance
            - Add "Plan Ahead Rewards" loyalty program
            - Show potential savings in app when users browse
            
            **Expected Impact**:
            - Increase scheduled orders from 20% → 35%
            - Additional revenue: **+$150K-200K annually**
            - ROI Timeline: **3-6 months**
            """)
            
            # Visualizations for Scheduled Orders Strategy
            st.markdown("")
            st.markdown("**📊 Visual Impact:**")
            
            # Option 1: Side-by-Side Revenue Comparison
            viz_col1, viz_col2 = st.columns(2)
            
            with viz_col1:
                st.markdown("**Average Revenue per Order Type**")
                fig1 = go.Figure()
                fig1.add_trace(go.Bar(
                    x=['ASAP Orders', 'Scheduled Orders'],
                    y=[43.48, 79.06],
                    marker_color=['#FF6B6B', '#06C167'],
                    text=['$43.48', '$79.06'],
                    textposition='outside',
                    textfont=dict(size=16, color='white'),
                    hovertemplate='<b>%{x}</b><br>Average Revenue: %{y}<extra></extra>'
                ))
                fig1.update_layout(
                    title="Revenue Comparison: ASAP vs Scheduled",
                    yaxis_title="Average Revenue ($)",
                    showlegend=False,
                    height=350,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
                )
                fig1.add_annotation(
                    x=1, y=79.06,
                    text="82% Higher!",
                    showarrow=True,
                    arrowhead=2,
                    arrowcolor="#06C167",
                    font=dict(size=14, color="#06C167", family="Arial Black"),
                    ax=-40, ay=-40
                )
                st.plotly_chart(fig1, use_container_width=True)
            
            with viz_col2:
                st.markdown("**Order Distribution: Current vs Target**")
                fig2 = go.Figure()
                
                # Current distribution
                fig2.add_trace(go.Bar(
                    name='Current',
                    x=['ASAP (80%)', 'Scheduled (20%)'],
                    y=[80, 20],
                    marker_color=['#FF6B6B', '#FFA07A'],
                    text=['80%', '20%'],
                    textposition='inside',
                    textfont=dict(size=16, color='white')
                ))
                
                # Target distribution
                fig2.add_trace(go.Bar(
                    name='Target',
                    x=['ASAP (65%)', 'Scheduled (35%)'],
                    y=[65, 35],
                    marker_color=['#FF8C8C', '#06C167'],
                    text=['65%', '35%'],
                    textposition='inside',
                    textfont=dict(size=16, color='white')
                ))
                
                fig2.update_layout(
                    title="Current vs Target Distribution",
                    yaxis_title="Percentage of Orders",
                    barmode='group',
                    height=350,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.1)', range=[0, 100]),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                st.plotly_chart(fig2, use_container_width=True)
            
            # Option 2: Before/After Revenue Projection
            st.markdown("**Monthly Revenue Projection**")
            
            # Calculate projections based on data
            asap_revenue = 43.48 * 0.80  # Current ASAP contribution per order
            scheduled_revenue = 79.06 * 0.20  # Current scheduled contribution per order
            current_avg = asap_revenue + scheduled_revenue  # ~$50.58 per order
            
            target_asap = 43.48 * 0.65
            target_scheduled = 79.06 * 0.35
            target_avg = target_asap + target_scheduled  # ~$56 per order
            
            # Assuming ~600 orders per day (18,078 / 31 days)
            monthly_orders = 18000
            current_monthly = current_avg * monthly_orders
            target_monthly = target_avg * monthly_orders
            increase = target_monthly - current_monthly
            
            fig3 = go.Figure()
            
            fig3.add_trace(go.Bar(
                x=['Current Revenue<br>(20% Scheduled)', 'Projected Revenue<br>(35% Scheduled)', 'Additional Gain'],
                y=[current_monthly, target_monthly, increase],
                marker_color=['#FF6B6B', '#06C167', '#FFD93D'],
                text=[f'${current_monthly:,.0f}', f'${target_monthly:,.0f}', f'+${increase:,.0f}'],
                textposition='outside',
                textfont=dict(size=14, color='white'),
                hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>'
            ))
            
            fig3.update_layout(
                title="Monthly Revenue Impact (Based on 18K Orders/Month)",
                yaxis_title="Monthly Revenue ($)",
                showlegend=False,
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
            )
            
            # Add annotation for percentage increase
            pct_increase = (increase / current_monthly) * 100
            fig3.add_annotation(
                x=1, y=target_monthly,
                text=f"+{pct_increase:.1f}% Growth!",
                showarrow=True,
                arrowhead=2,
                arrowcolor="#06C167",
                font=dict(size=14, color="#06C167", family="Arial Black"),
                ax=-60, ay=-40
            )
            
            st.plotly_chart(fig3, use_container_width=True)
    
    st.markdown("---")
    
    # RECOMMENDATION 2 (formerly #4)
    with st.container():
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown("### 2️⃣")
            st.markdown("**Priority**")
            st.warning("MEDIUM")
        with col2:
            st.markdown("### 🧪 A/B Testing Framework")
            st.markdown("""
            **Current State**: No systematic testing before rolling out new strategies  
            **Opportunity**: Validate all strategies with data before full investment  
            
            **Test Design**:
            - **Group A (Control)**: No promotion
            - **Group B (Test)**: Test new promotional strategies
            
            **What to Measure**:
            - Average order value
            - % of scheduled orders
            - Refund rate
            - Repeat order rate
            
            **Decision Rule**: Launch promo if test group performs >10% better than control  
            
            **Expected Impact**:
            - Reduce risk of failed promotions
            - Data-driven decision making
            - Optimize promo design before full rollout
            - ROI Timeline: **Test in 2-4 weeks, then scale**
            """)
    
    st.markdown("---")
    
    # RECOMMENDATION 3 (formerly #5)
    with st.container():
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown("### 3️⃣")
            st.markdown("**Priority**")
            st.warning("MEDIUM")
        with col2:
            st.markdown("📍 Balance Regional Distribution")
            st.markdown("""
            **Current State**: Palo Alto has 63% of orders; San Jose & Mountain View underserved  
            **Opportunity**: Untapped market potential in two regions  
            
            **Action Plan**:
            - Launch targeted marketing in San Jose & Mountain View
            - Recruit 5-10 popular restaurants per region
            - Offer new user promotions specific to underserved areas
            
            **Expected Impact**:
            - Balance distribution to 50-25-25% split
            - Additional revenue: **+$120K-150K annually**
            - ROI Timeline: **6-9 months**
            """)
    
    st.markdown("---")
    
    # RECOMMENDATION 4 (formerly #6)
    with st.container():
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown("### 4️⃣")
            st.markdown("**Priority**")
            st.warning("MEDIUM")
        with col2:
            st.markdown("### ⚡ Optimize Peak Hour Performance (Focus on Prep Time)")
            st.markdown("""
            **Current State**: Delivery time breakdown shows prep issues  
            **Opportunity**: Reducing prep time = biggest impact on overall delivery speed  
            
            **Key Finding**: Delivery time comes from prep, driver wait, and travel:
            - **Prep Time**: 10.7 minutes (restaurant food preparation)
            - **Driver Wait Time**: 17.1 minutes (driver waiting for order)
            - **Travel Time**: 24.2 minutes (delivery to customer)
            - **Total Average**: ~52 minutes
            
            **Why This Matters**:
            - Prep happens FIRST, so delays here affect everything after
            - Longer deliveries lead to **lower tips** and **higher refund rates**
            - Cascading effect on customer satisfaction
            
            **Action Plan**:
            - Set clear prep time targets (<15 min for most orders)
            - Improve coordination with drivers (better timing = less wait)
            - Use past data to predict prep issues and allocate resources
            - Incentivize faster restaurant preparation (badges, bonuses)
            
            **Expected Impact**:
            - Reduce average delivery time by **20%** (52 min → 42 min)
            - Improve customer satisfaction and repeat orders
            - Increase tips and reduce refunds
            - ROI Timeline: **6-12 months**
            """)
            
            # Add visualization for delivery time breakdown
            st.markdown("")
            st.markdown("**📊 Delivery Time Breakdown by Stage:**")
            
            fig_delivery = go.Figure()
            
            # Data from the presentation
            stages = ['Prep Time', 'Driver Wait Time', 'Travel Time']
            times = [10.7, 17.1, 24.2]
            colors = ['#FF6B6B', '#FFA500', '#06C167']
            
            fig_delivery.add_trace(go.Bar(
                x=stages,
                y=times,
                marker_color=colors,
                text=[f'{t} min' for t in times],
                textposition='outside',
                textfont=dict(size=16, color='white'),
                hovertemplate='<b>%{x}</b><br>Average Time: %{y} minutes<extra></extra>'
            ))
            
            fig_delivery.update_layout(
                title="Average Delivery Time by Operational Stage",
                yaxis_title="Average Minutes",
                showlegend=False,
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)', range=[0, 27])
            )
            
            # Add annotation highlighting prep time impact
            fig_delivery.add_annotation(
                x=0, y=10.7,
                text="Prep happens FIRST<br>Delays cascade!",
                showarrow=True,
                arrowhead=2,
                arrowcolor="#FF6B6B",
                font=dict(size=12, color="#FF6B6B"),
                ax=50, ay=-40
            )
            
            st.plotly_chart(fig_delivery, use_container_width=True)
    
    st.markdown("---")
    
    # ========== BOTTOM LINE ==========
    st.subheader("💰 Bottom Line")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Investment Required",
            "$200K-300K",
            "One-time + Year 1"
        )
    
    with col2:
        st.metric(
            "Expected Revenue Growth",
            "+15-25%",
            "$137K-229K"
        )
    
    with col3:
        st.metric(
            "Payback Period",
            "6-9 months",
            "ROI positive"
        )
    
    with col4:
        st.metric(
            "Delivery Time Improvement",
            "-20%",
            "57→46 min avg"
        )
    
    st.markdown("---")
    
    # ========== IMPLEMENTATION ROADMAP ==========
    st.subheader("📅 90-Day Implementation Roadmap")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Month 1: Quick Wins**")
        st.markdown("""
        ✅ Launch scheduled order discount (5%)  
        ✅ Create driver heat maps  
        ✅ Begin restaurant badge program  
        ✅ Start San Jose marketing  
        """)
    
    with col2:
        st.markdown("**Month 2: Optimization**")
        st.markdown("""
        ✅ Deploy predictive staffing  
        ✅ Recruit new restaurants  
        ✅ Launch Mountain View campaign  
        ✅ Implement zone optimization  
        """)
    
    with col3:
        st.markdown("**Month 3: Scale & Measure**")
        st.markdown("""
        ✅ Full ML forecasting rollout  
        ✅ Performance dashboards live  
        ✅ Measure & adjust initiatives  
        ✅ Plan next quarter expansion  
        """)
    
    st.markdown("---")
    
    # ========== SUCCESS METRICS ==========
    st.subheader("📊 Success Metrics to Track")
    
    metrics_df = pd.DataFrame({
        "Metric": [
            "Scheduled Order %",
            "Average Delivery Time",
            "Palo Alto Order %",
            "Customer Satisfaction",
            "Total Monthly Revenue"
        ],
        "Current": ["20%", "57.3 min", "63%", "4.2/5", "$915K"],
        "Target (Month 3)": ["28-30%", "52-54 min", "58-60%", "4.4/5", "$1.0M"],
        "Target (Month 6)": ["35%+", "<48 min", "50%", "4.5/5", "$1.1M+"]
    })
    
    st.dataframe(metrics_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # ========== KEY TAKEAWAYS ==========
    st.subheader("🎯 Key Takeaways for Presentation")
    
    st.success("""
    **1. Scheduled Orders = Hidden Goldmine**: 82% higher revenue per order with only 20% current adoption  
    **2. Test Before Scaling**: Use A/B testing to validate strategies before full investment  
    **3. Geographic Imbalance**: 63% of orders in one region leaves massive growth opportunity  
    **4. Prep Time = Key Bottleneck**: Reducing restaurant prep time has biggest delivery impact  
    **5. Holiday Data Caveat**: Dec 25-31 spike is seasonal; use Days 1-24 for typical projections  
    """)
    
    st.info("💡 **Pro Tip for PPT**: Focus on #1 Scheduled Orders strategy - it has the highest ROI and is easiest to implement. Use #2 A/B Testing to validate before full rollout!")


# ========================================
# MAIN APP
# ========================================

def main():
    """Main Streamlit app - Simple and Visual."""
    
    # Header
    st.markdown('<p class="main-header">🍔 Uber Eats Data Explorer</p>', unsafe_allow_html=True)
    st.caption("December 2025 Delivery Data Analysis")
    st.info("📅 Dataset: December 1-31, 2025 | Note: Days 25-31 show holiday season spike (Christmas-New Year)")
    st.markdown("---")
    
    # Load data
    with st.spinner("Loading cleaned data..."):
        df = load_data()
    
    if df is None:
        st.error("⚠️ Could not load data. Please run the cleaning script first.")
        st.code("python 'CLEANING PART.py'")
        return
    
    # Sidebar - Simple navigation
    st.sidebar.title("📊 Dashboard")
    st.sidebar.markdown(f"**{len(df):,}** orders")
    st.sidebar.markdown(f"**{df['Day'].nunique()}** days")
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "Choose a view:",
        ["🏠 Overview", "🔍 Key Insights", "🎯 Strategy", "📈 Daily Trends", "📅 Weekly Patterns", "⏱️ Delivery Times", "💰 Revenue"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Quick Stats")
    if 'Net_Revenue' in df.columns:
        st.sidebar.metric("Total Revenue", f"${df['Net_Revenue'].sum():,.0f}")
    if 'Is ASAP' in df.columns:
        asap_pct = (df['Is ASAP'].sum() / len(df) * 100)
        st.sidebar.metric("ASAP Orders", f"{asap_pct:.1f}%")
    
    # Page routing - Simplified
    if page == "🏠 Overview":
        display_overview(df)
        st.markdown("---")
        plot_daily_orders(df)
    
    elif page == "🔍 Key Insights":
        display_key_insights(df)
    
    elif page == "🎯 Strategy":
        display_strategy(df)
        
    elif page == "📈 Daily Trends":
        plot_daily_orders(df)
        
    elif page == "📅 Weekly Patterns":
        plot_weekly_patterns(df)
        
    elif page == "⏱️ Delivery Times":
        plot_time_analysis(df)
        
    elif page == "💰 Revenue":
        plot_value_analysis(df)
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.caption("💡 Tip: Hover over charts for details")
    st.sidebar.caption(f"Updated: {datetime.now().strftime('%H:%M')}")


if __name__ == "__main__":
    main()
