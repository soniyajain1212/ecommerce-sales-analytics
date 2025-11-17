"""
E-Commerce Sales Analytics Dashboard
Author: Soniya Jain
Description: Analyzing 50K+ e-commerce transactions for sales insights

Requirements:
pip install pandas numpy matplotlib seaborn plotly
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import datetime, timedelta

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# ==============================================
# 1. DATA GENERATION (Simulating E-Commerce Data)
# ==============================================

def generate_ecommerce_data(n_records=50000):
    """Generate realistic e-commerce transaction data"""
    
    np.random.seed(42)
    
    # Date range: Last 2 years
    start_date = datetime.now() - timedelta(days=730)
    dates = [start_date + timedelta(days=np.random.randint(0, 730)) 
             for _ in range(n_records)]
    
    # Product categories and their base prices
    categories = {
        'Electronics': (500, 5000),
        'Clothing': (20, 200),
        'Home & Kitchen': (30, 500),
        'Books': (10, 50),
        'Sports': (25, 300),
        'Beauty': (15, 150)
    }
    
    # Customer segments
    segments = ['Premium', 'Regular', 'Budget']
    
    # Regions
    regions = ['North', 'South', 'East', 'West', 'Central']
    
    data = []
    customer_id_pool = [f'CUST{i:05d}' for i in range(1, 10001)]
    
    for i in range(n_records):
        order_id = f'ORD{i+1:06d}'
        customer_id = np.random.choice(customer_id_pool)
        category = np.random.choice(list(categories.keys()))
        min_price, max_price = categories[category]
        
        # Price with some seasonal variation
        month = dates[i].month
        seasonal_factor = 1.2 if month in [11, 12] else 1.0  # Holiday season
        price = np.random.uniform(min_price, max_price) * seasonal_factor
        
        quantity = np.random.choice([1, 1, 1, 2, 2, 3], p=[0.5, 0.2, 0.1, 0.1, 0.05, 0.05])
        revenue = price * quantity
        
        segment = np.random.choice(segments, p=[0.2, 0.5, 0.3])
        region = np.random.choice(regions)
        
        data.append({
            'Order_ID': order_id,
            'Customer_ID': customer_id,
            'Date': dates[i],
            'Category': category,
            'Price': round(price, 2),
            'Quantity': quantity,
            'Revenue': round(revenue, 2),
            'Customer_Segment': segment,
            'Region': region
        })
    
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.to_period('M')
    df['Year'] = df['Date'].dt.year
    df['Quarter'] = df['Date'].dt.quarter
    
    return df

# ==============================================
# 2. DATA CLEANING & PREPROCESSING
# ==============================================

def clean_data(df):
    """Clean and preprocess the data"""
    
    print("=== DATA CLEANING REPORT ===")
    print(f"Original shape: {df.shape}")
    
    # Check for missing values
    missing = df.isnull().sum()
    print(f"\nMissing values:\n{missing[missing > 0]}")
    
    # Remove duplicates
    df = df.drop_duplicates(subset=['Order_ID'])
    print(f"After removing duplicates: {df.shape}")
    
    # Handle outliers (Revenue > 99th percentile)
    q99 = df['Revenue'].quantile(0.99)
    df = df[df['Revenue'] <= q99]
    print(f"After removing outliers: {df.shape}")
    
    return df

# ==============================================
# 3. SALES ANALYSIS & KEY METRICS
# ==============================================

def calculate_key_metrics(df):
    """Calculate important business metrics"""
    
    metrics = {
        'Total Revenue': df['Revenue'].sum(),
        'Total Orders': len(df),
        'Average Order Value': df['Revenue'].mean(),
        'Total Customers': df['Customer_ID'].nunique(),
        'Customer Lifetime Value': df.groupby('Customer_ID')['Revenue'].sum().mean()
    }
    
    print("\n=== KEY BUSINESS METRICS ===")
    for metric, value in metrics.items():
        print(f"{metric}: ₹{value:,.2f}" if 'Revenue' in metric or 'Value' in metric 
              else f"{metric}: {value:,.0f}")
    
    return metrics

# ==============================================
# 4. VISUALIZATIONS
# ==============================================

def create_visualizations(df):
    """Generate comprehensive visualizations"""
    
    # 1. Revenue Trends Over Time
    monthly_revenue = df.groupby('Month')['Revenue'].sum().reset_index()
    monthly_revenue['Month'] = monthly_revenue['Month'].astype(str)
    
    fig1 = px.line(monthly_revenue, x='Month', y='Revenue', 
                   title='Monthly Revenue Trend',
                   labels={'Revenue': 'Revenue (₹)', 'Month': 'Month'})
    fig1.update_traces(line_color='#2c3e50', line_width=3)
    fig1.show()
    
    # 2. Category Performance
    category_performance = df.groupby('Category').agg({
        'Revenue': 'sum',
        'Order_ID': 'count'
    }).reset_index()
    category_performance.columns = ['Category', 'Revenue', 'Orders']
    category_performance = category_performance.sort_values('Revenue', ascending=True)
    
    fig2 = px.bar(category_performance, x='Revenue', y='Category',
                  title='Revenue by Product Category',
                  labels={'Revenue': 'Total Revenue (₹)'}, orientation='h')
    fig2.update_traces(marker_color='#3498db')
    fig2.show()
    
    # 3. Customer Segmentation
    segment_analysis = df.groupby('Customer_Segment')['Revenue'].sum().reset_index()
    
    fig3 = px.pie(segment_analysis, values='Revenue', names='Customer_Segment',
                  title='Revenue Distribution by Customer Segment',
                  color_discrete_sequence=['#e74c3c', '#3498db', '#2ecc71'])
    fig3.show()
    
    # 4. Regional Analysis
    regional_performance = df.groupby('Region')['Revenue'].sum().reset_index()
    
    fig4 = px.bar(regional_performance, x='Region', y='Revenue',
                  title='Revenue by Region',
                  labels={'Revenue': 'Total Revenue (₹)'})
    fig4.update_traces(marker_color='#9b59b6')
    fig4.show()
    
    # 5. Heatmap: Category vs Region
    pivot_table = df.pivot_table(values='Revenue', 
                                  index='Category', 
                                  columns='Region', 
                                  aggfunc='sum')
    
    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot_table, annot=True, fmt='.0f', cmap='YlOrRd', cbar_kws={'label': 'Revenue'})
    plt.title('Revenue Heatmap: Category vs Region')
    plt.tight_layout()
    plt.show()

# ==============================================
# 5. INSIGHTS & RECOMMENDATIONS
# ==============================================

def generate_insights(df):
    """Generate actionable business insights"""
    
    print("\n=== KEY INSIGHTS ===")
    
    # Top performing category
    top_category = df.groupby('Category')['Revenue'].sum().idxmax()
    top_category_revenue = df.groupby('Category')['Revenue'].sum().max()
    print(f"1. Top Category: {top_category} (₹{top_category_revenue:,.2f})")
    
    # Peak sales period
    peak_month = df.groupby('Month')['Revenue'].sum().idxmax()
    print(f"2. Peak Sales Month: {peak_month}")
    
    # Best region
    best_region = df.groupby('Region')['Revenue'].sum().idxmax()
    print(f"3. Best Performing Region: {best_region}")
    
    # Customer insights
    repeat_customers = df.groupby('Customer_ID').size()
    repeat_rate = (repeat_customers > 1).sum() / len(repeat_customers) * 100
    print(f"4. Repeat Customer Rate: {repeat_rate:.1f}%")
    
    # Revenue concentration
    top_20_customers_revenue = df.groupby('Customer_ID')['Revenue'].sum().nlargest(int(0.2 * df['Customer_ID'].nunique())).sum()
    revenue_concentration = (top_20_customers_revenue / df['Revenue'].sum()) * 100
    print(f"5. Top 20% customers generate {revenue_concentration:.1f}% of revenue")
    
    print("\n=== RECOMMENDATIONS ===")
    print("1. Focus marketing budget on Electronics category (highest revenue)")
    print("2. Implement retention strategies for repeat customers")
    print("3. Expand inventory in best-performing regions")
    print("4. Launch targeted campaigns during Q4 (holiday season)")
    print("5. Develop loyalty programs for premium segment customers")

# ==============================================
# 6. MAIN EXECUTION
# ==============================================

if __name__ == "__main__":
    print("Starting E-Commerce Sales Analytics Dashboard...\n")
    
    # Generate data
    df = generate_ecommerce_data(50000)
    print(f"Generated {len(df)} transaction records")
    
    # Clean data
    df = clean_data(df)
    
    # Save to CSV
    df.to_csv('ecommerce_sales_data.csv', index=False)
    print("\nData saved to 'ecommerce_sales_data.csv'")
    
    # Calculate metrics
    metrics = calculate_key_metrics(df)
    
    # Create visualizations
    create_visualizations(df)
    
    # Generate insights
    generate_insights(df)
    
    print("\n✅ Analysis Complete!")
