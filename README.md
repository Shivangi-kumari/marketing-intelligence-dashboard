
# Marketing Intelligence Dashboard

A comprehensive Business Intelligence dashboard built with Streamlit for analyzing marketing performance and business outcomes.

## Features

- **Interactive KPI Metrics**: Real-time overview of revenue, spend, ROAS, and customer acquisition
- **Multi-Platform Analysis**: Facebook, Google, and TikTok campaign performance comparison
- **Campaign Performance**: Detailed analysis of individual campaigns with ROAS and CTR metrics
- **Daily Trends**: Time-series analysis of key performance indicators
- **Interactive Filters**: Date range and platform selection for focused analysis
- **Responsive Design**: Modern, clean interface optimized for business stakeholders

## Data Sources

- `business.csv`: Daily business performance data (orders, revenue, customers)
- `Facebook.csv`: Facebook advertising campaign data
- `Google.csv`: Google advertising campaign data  
- `TikTok.csv`: TikTok advertising campaign data

## Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

2. Run the dashboard:
```bash
streamlit run app.py
```

3. Open your browser to `http://localhost:8501`

## Usage

1. **Select Date Range**: Use the sidebar to filter data by date
2. **Choose Platforms**: Select which advertising platforms to analyze
3. **View KPIs**: Monitor key performance indicators at the top
4. **Explore Trends**: Analyze revenue and profit trends over time
5. **Compare Platforms**: See ROAS and spend comparison across platforms
6. **Drill Down**: Use tabs to explore individual platform performance

## Key Metrics

- **ROAS (Return on Ad Spend)**: Attributed revenue divided by advertising spend
- **CTR (Click-Through Rate)**: Percentage of impressions that resulted in clicks
- **CPC (Cost Per Click)**: Average cost per click
- **CPM (Cost Per Mille)**: Cost per thousand impressions
- **Revenue Growth**: Period-over-period revenue change
- **Customer Acquisition**: New customer acquisition metrics

## Dashboard Sections

1. **Overview**: High-level KPIs and platform comparison
2. **Revenue Trends**: Time-series analysis of revenue and profit
3. **Platform Performance**: Individual platform deep-dives
4. **Campaign Analysis**: Top-performing campaigns by ROAS
5. **Daily Metrics**: Granular daily performance tracking

## Technical Details

- Built with Streamlit for rapid development and deployment
- Uses Plotly for interactive visualizations
- Pandas for data processing and analysis
- Responsive design with modern UI components
- Cached data loading for optimal performance
