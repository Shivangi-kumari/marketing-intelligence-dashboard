import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Marketing Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

@st.cache_data
def load_data():
    business_df = pd.read_csv('data/business.csv')
    facebook_df = pd.read_csv('data/Facebook.csv')
    google_df = pd.read_csv('data/Google.csv')
    tiktok_df = pd.read_csv('data/TikTok.csv')
    
    business_df['date'] = pd.to_datetime(business_df['date'])
    facebook_df['date'] = pd.to_datetime(facebook_df['date'])
    google_df['date'] = pd.to_datetime(google_df['date'])
    tiktok_df['date'] = pd.to_datetime(tiktok_df['date'])
    
    return business_df, facebook_df, google_df, tiktok_df

def calculate_metrics(business_df, marketing_df, platform_name):
    total_revenue = business_df['total revenue'].sum()
    total_spend = marketing_df['spend'].sum()
    total_attributed_revenue = marketing_df['attributed revenue'].sum()
    total_impressions = marketing_df['impression'].sum()
    total_clicks = marketing_df['clicks'].sum()
    
    roas = total_attributed_revenue / total_spend if total_spend > 0 else 0
    ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
    cpc = total_spend / total_clicks if total_clicks > 0 else 0
    cpm = (total_spend / total_impressions * 1000) if total_impressions > 0 else 0
    
    return {
        'platform': platform_name,
        'total_spend': total_spend,
        'attributed_revenue': total_attributed_revenue,
        'roas': roas,
        'ctr': ctr,
        'cpc': cpc,
        'cpm': cpm,
        'impressions': total_impressions,
        'clicks': total_clicks
    }

def create_kpi_cards(metrics):
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Revenue",
            value=f"${metrics['total_revenue']:,.0f}",
            delta=f"{metrics['revenue_growth']:.1f}%"
        )
    
    with col2:
        st.metric(
            label="Total Spend",
            value=f"${metrics['total_spend']:,.0f}",
            delta=f"{metrics['spend_growth']:.1f}%"
        )
    
    with col3:
        st.metric(
            label="ROAS",
            value=f"{metrics['avg_roas']:.2f}x",
            delta=f"{metrics['roas_growth']:.1f}%"
        )
    
    with col4:
        st.metric(
            label="New Customers",
            value=f"{metrics['new_customers']:,.0f}",
            delta=f"{metrics['customer_growth']:.1f}%"
        )

def create_revenue_trend_chart(business_df, date_range):
    filtered_df = business_df[
        (business_df['date'] >= date_range[0]) & 
        (business_df['date'] <= date_range[1])
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=filtered_df['date'],
        y=filtered_df['total revenue'],
        mode='lines+markers',
        name='Total Revenue',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=6)
    ))
    
    fig.add_trace(go.Scatter(
        x=filtered_df['date'],
        y=filtered_df['gross profit'],
        mode='lines+markers',
        name='Gross Profit',
        line=dict(color='#ff7f0e', width=3),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        title="Revenue & Profit Trends",
        xaxis_title="Date",
        yaxis_title="Amount ($)",
        hovermode='x unified',
        height=400,
        showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_platform_comparison_chart(platform_metrics):
    platforms = [m['platform'] for m in platform_metrics]
    roas_values = [m['roas'] for m in platform_metrics]
    spend_values = [m['total_spend'] for m in platform_metrics]
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('ROAS by Platform', 'Spend by Platform'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    fig.add_trace(
        go.Bar(x=platforms, y=roas_values, name='ROAS', marker_color='#2E8B57'),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Bar(x=platforms, y=spend_values, name='Spend', marker_color='#FF6B6B'),
        row=1, col=2
    )
    
    fig.update_layout(
        title="Platform Performance Comparison",
        height=400,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_campaign_performance_chart(marketing_df, platform_name):
    campaign_performance = marketing_df.groupby('campaign').agg({
        'spend': 'sum',
        'attributed revenue': 'sum',
        'clicks': 'sum',
        'impression': 'sum'
    }).reset_index()
    
    campaign_performance['roas'] = campaign_performance['attributed revenue'] / campaign_performance['spend']
    campaign_performance['ctr'] = (campaign_performance['clicks'] / campaign_performance['impression'] * 100)
    
    top_campaigns = campaign_performance.nlargest(10, 'roas')
    
    fig = px.scatter(
        top_campaigns,
        x='spend',
        y='attributed revenue',
        size='clicks',
        color='roas',
        hover_data=['campaign', 'ctr'],
        title=f"Top {platform_name} Campaigns by ROAS",
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_daily_metrics_chart(business_df, marketing_df, platform_name, date_range):
    filtered_business = business_df[
        (business_df['date'] >= date_range[0]) & 
        (business_df['date'] <= date_range[1])
    ]
    
    filtered_marketing = marketing_df[
        (marketing_df['date'] >= date_range[0]) & 
        (marketing_df['date'] <= date_range[1])
    ]
    
    daily_marketing = filtered_marketing.groupby('date').agg({
        'spend': 'sum',
        'attributed revenue': 'sum',
        'clicks': 'sum'
    }).reset_index()
    
    daily_business = filtered_business.groupby('date').agg({
        'total revenue': 'sum',
        'new customers': 'sum'
    }).reset_index()
    
    daily_combined = pd.merge(daily_marketing, daily_business, on='date', how='outer').fillna(0)
    daily_combined['roas'] = daily_combined['attributed revenue'] / daily_combined['spend'].replace(0, np.nan)
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Daily Spend', 'Daily ROAS', 'Daily Revenue', 'Daily New Customers'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    fig.add_trace(
        go.Scatter(x=daily_combined['date'], y=daily_combined['spend'], name='Spend', line=dict(color='#FF6B6B')),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=daily_combined['date'], y=daily_combined['roas'], name='ROAS', line=dict(color='#4ECDC4')),
        row=1, col=2
    )
    
    fig.add_trace(
        go.Scatter(x=daily_combined['date'], y=daily_combined['total revenue'], name='Revenue', line=dict(color='#45B7D1')),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=daily_combined['date'], y=daily_combined['new customers'], name='New Customers', line=dict(color='#96CEB4')),
        row=2, col=2
    )
    
    fig.update_layout(
        title=f"Daily {platform_name} Performance Metrics",
        height=600,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def main():
    st.title("📊 Marketing Intelligence Dashboard")
    st.markdown("---")
    
    business_df, facebook_df, google_df, tiktok_df = load_data()
    
    min_date = business_df['date'].min()
    max_date = business_df['date'].max()
    
    st.sidebar.title("Filters")
    
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    platform_filter = st.sidebar.multiselect(
        "Select Platforms",
        options=["Facebook", "Google", "TikTok"],
        default=["Facebook", "Google", "TikTok"]
    )
    
    if len(date_range) == 2:
        date_range = [pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])]
        
        filtered_business = business_df[
            (business_df['date'] >= date_range[0]) & 
            (business_df['date'] <= date_range[1])
        ]
        
        total_revenue = filtered_business['total revenue'].sum()
        total_spend = 0
        total_attributed_revenue = 0
        total_new_customers = filtered_business['new customers'].sum()
        
        platform_metrics = []
        
        if "Facebook" in platform_filter:
            filtered_facebook = facebook_df[
                (facebook_df['date'] >= date_range[0]) & 
                (facebook_df['date'] <= date_range[1])
            ]
            fb_metrics = calculate_metrics(filtered_business, filtered_facebook, "Facebook")
            platform_metrics.append(fb_metrics)
            total_spend += fb_metrics['total_spend']
            total_attributed_revenue += fb_metrics['attributed_revenue']
        
        if "Google" in platform_filter:
            filtered_google = google_df[
                (google_df['date'] >= date_range[0]) & 
                (google_df['date'] <= date_range[1])
            ]
            gg_metrics = calculate_metrics(filtered_business, filtered_google, "Google")
            platform_metrics.append(gg_metrics)
            total_spend += gg_metrics['total_spend']
            total_attributed_revenue += gg_metrics['attributed_revenue']
        
        if "TikTok" in platform_filter:
            filtered_tiktok = tiktok_df[
                (tiktok_df['date'] >= date_range[0]) & 
                (tiktok_df['date'] <= date_range[1])
            ]
            tt_metrics = calculate_metrics(filtered_business, filtered_tiktok, "TikTok")
            platform_metrics.append(tt_metrics)
            total_spend += tt_metrics['total_spend']
            total_attributed_revenue += tt_metrics['attributed_revenue']
        
        overall_roas = total_attributed_revenue / total_spend if total_spend > 0 else 0
        avg_roas = np.mean([m['roas'] for m in platform_metrics]) if platform_metrics else 0
        
        metrics = {
            'total_revenue': total_revenue,
            'total_spend': total_spend,
            'avg_roas': avg_roas,
            'new_customers': total_new_customers,
            'revenue_growth': 0,
            'spend_growth': 0,
            'roas_growth': 0,
            'customer_growth': 0
        }
        
        create_kpi_cards(metrics)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(create_revenue_trend_chart(business_df, date_range), use_container_width=True)
        
        with col2:
            if platform_metrics:
                st.plotly_chart(create_platform_comparison_chart(platform_metrics), use_container_width=True)
        
        st.markdown("---")
        
        tab1, tab2, tab3 = st.tabs(["Facebook", "Google", "TikTok"])
        
        with tab1:
            if "Facebook" in platform_filter:
                st.plotly_chart(create_campaign_performance_chart(filtered_facebook, "Facebook"), use_container_width=True)
                st.plotly_chart(create_daily_metrics_chart(business_df, filtered_facebook, "Facebook", date_range), use_container_width=True)
            else:
                st.info("Facebook data not selected in filters")
        
        with tab2:
            if "Google" in platform_filter:
                st.plotly_chart(create_campaign_performance_chart(filtered_google, "Google"), use_container_width=True)
                st.plotly_chart(create_daily_metrics_chart(business_df, filtered_google, "Google", date_range), use_container_width=True)
            else:
                st.info("Google data not selected in filters")
        
        with tab3:
            if "TikTok" in platform_filter:
                st.plotly_chart(create_campaign_performance_chart(filtered_tiktok, "TikTok"), use_container_width=True)
                st.plotly_chart(create_daily_metrics_chart(business_df, filtered_tiktok, "TikTok", date_range), use_container_width=True)
            else:
                st.info("TikTok data not selected in filters")
        
        st.markdown("---")
        
        st.subheader("📈 Key Insights")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Overall ROAS", f"{overall_roas:.2f}x")
        
        with col2:
            best_platform = max(platform_metrics, key=lambda x: x['roas']) if platform_metrics else None
            if best_platform:
                st.metric("Best Performing Platform", f"{best_platform['platform']} ({best_platform['roas']:.2f}x ROAS)")
        
        with col3:
            total_impressions = sum([m['impressions'] for m in platform_metrics])
            st.metric("Total Impressions", f"{total_impressions:,.0f}")
    
    else:
        st.warning("Please select a valid date range")

if __name__ == "__main__":
    main()
