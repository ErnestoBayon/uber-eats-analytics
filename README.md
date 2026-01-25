# 🍔 Uber Eats Data Analysis Project

A comprehensive data analysis project for Uber Eats delivery data from a California zone. This project includes data cleaning, exploration, and interactive visualization tools.

## 📁 Project Structure

```
UBER EATS PROJECT/
│
├── UberEatsCaseAnalysis2026.xlsx    # Original data file
├── CLEANING PART.py                  # Data cleaning pipeline
├── streamlit_app.py                  # Interactive dashboard
├── requirements.txt                  # Python dependencies
└── README.md                         # This file
```

## 📊 Data Overview

- **Time Period**: Approximately 1 month (December 2025, Days 1-31+)
- **Geography**: California zone
- **Data Points**: Delivery orders with timestamps, restaurant info, driver info, and order values
- **Key Features**:
  - All timestamps converted to minutes
  - Day 1 = Tuesday (follows calendar pattern)
  - Days 32+ represent deliveries that occurred on next month's Day 1
  - Missing timestamps filled with historical averages (per restaurant/driver, ASAP vs non-ASAP)
  - Holiday period identified (Dec 25-28 shows elevated volume)

## 🚀 Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Data Cleaning

```bash
python "CLEANING PART.py"
```

This will:
- Load the Excel data
- Explore and validate the data
- Handle missing values
- Create derived features (day of week, weekend flags, etc.)
- Save cleaned data to new Excel files

### 3. Launch Interactive Dashboard

```bash
streamlit run streamlit_app.py
```

This will open an interactive web dashboard at `http://localhost:8501`

## 📈 Dashboard Features

The Streamlit dashboard includes:

### Overview Page
- Total orders, unique restaurants, unique drivers
- Daily order volume trends
- Weekly patterns (weekday vs weekend)

### Daily Patterns
- Order volume by day of month
- Day of week analysis
- Peak day identification

### Time Analysis
- Delivery time distributions
- Wait time analysis
- Statistical summaries (mean, median, std dev)

### Restaurant Performance
- Top restaurants by order volume
- Restaurant-level metrics
- Performance comparisons

### Driver Performance
- Deliveries per driver distribution
- Top performing drivers
- Driver efficiency metrics

### Revenue Analysis
- Total revenue and average order value
- Daily revenue trends
- Revenue by day of week

### Data Explorer
- Interactive data table
- Column filtering
- Day/week filtering
- CSV export functionality

## 🔍 Key Insights to Look For

Based on the data structure, focus on:

1. **Time Efficiency**:
   - Average time from order placement to delivery
   - Restaurant preparation times
   - Driver arrival and pickup times

2. **Volume Patterns**:
   - Weekend vs weekday order volume
   - Holiday period impact (Dec 25-28)
   - New Year's Eve spike (Day 31)

3. **Performance Metrics**:
   - Restaurant preparation efficiency
   - Driver delivery efficiency
   - High-performing vs struggling restaurants

4. **Revenue Optimization**:
   - High-value order patterns
   - Peak revenue days
   - ASAP vs pre-order value differences

## 📝 Data Cleaning Steps

The cleaning pipeline includes:

1. **Load and Explore**: Examine all sheets and data structure
2. **Identify Columns**: Categorize datetime, numeric, and categorical columns
3. **Handle Missing Values**: Apply historical averages (already done in source)
4. **Create Features**: Add day of week, weekend flags, holiday period indicators
5. **Validate Data**: Check for duplicates, negative values, and data ranges
6. **Save Results**: Export cleaned data for analysis

## 💡 Business Recommendations

After analyzing the data, consider:

- **Staffing**: Optimize driver allocation based on day/time patterns
- **Marketing**: Target high-value customers during peak times
- **Operations**: Improve restaurant efficiency for slow-performing locations
- **Pricing**: Dynamic pricing strategies based on demand patterns

## 🛠️ Technologies Used

- **Python 3.8+**
- **Pandas**: Data manipulation
- **NumPy**: Numerical computations
- **Matplotlib/Seaborn**: Static visualizations
- **Plotly**: Interactive charts
- **Streamlit**: Web dashboard
- **OpenPyXL**: Excel file handling

## 📧 Notes

- The data assumes Day 1 is a Tuesday
- Days 32+ are next month's spillover (for orders placed on Day 31)
- Historical averages used for imputation are calculated separately for ASAP vs non-ASAP orders
- Extreme wait times observed on Day 31 (New Year's Eve)

## 🎯 Next Steps

1. Run the cleaning script to prepare the data
2. Explore the dashboard to understand patterns
3. Document specific insights for stakeholders
4. Develop targeted business recommendations
5. Consider predictive modeling for demand forecasting

---

**Created**: January 2026  
**Last Updated**: January 14, 2026
