import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# SETTINGS
st.set_page_config(page_title="Supermarket Sales Dashboard", layout="wide")

# LOAD DATA
@st.cache_data
def load_data():
    df = pd.read_csv('supermarket_sales.csv', parse_dates=['Date'])
    return df

df = load_data()

st.title('Supermarket Sales Dashboard')
st.markdown("""
This dashboard offers a comprehensive view of customer ratings and sales data for supermarket branches. 
Use filters below to customize your insights.
""")

# Sidebar filters
branch = st.sidebar.multiselect('Select Branch', options=df['Branch'].unique(), default=df['Branch'].unique())
city = st.sidebar.multiselect('Select City', options=df['City'].unique(), default=df['City'].unique())
customer_type = st.sidebar.multiselect('Customer Type', options=df['Customer type'].unique(), default=df['Customer type'].unique())

df_filtered = df[
    (df['Branch'].isin(branch)) & 
    (df['City'].isin(city)) & 
    (df['Customer type'].isin(customer_type))
]

st.sidebar.markdown(f"**Total records:** {len(df_filtered)}")

# 1. Basic Data Table
st.subheader("Data Table")
st.markdown("This is the filtered sales data table. Useful for quick lookup of details.")
st.dataframe(df_filtered)

# 2. Rating Distribution
st.subheader("Rating Distribution")
st.markdown("This chart shows how customers rated their experience overall.")
fig1, ax1 = plt.subplots()
sns.histplot(df_filtered['Rating'], bins=10, kde=True, ax=ax1)
st.pyplot(fig1)

# 3. Average Rating by Branch
st.subheader("Average Rating by Branch")
st.markdown("This bar chart compares the average customer ratings across different branches.")
branch_rating = df_filtered.groupby('Branch')['Rating'].mean().reset_index()
fig2 = px.bar(branch_rating, x='Branch', y='Rating', color='Branch', text_auto=True)
st.plotly_chart(fig2)

# 4. Average Rating by City
st.subheader("Average Rating by City")
st.markdown("This chart shows average customer ratings by city.")
city_rating = df_filtered.groupby('City')['Rating'].mean().reset_index()
fig3 = px.bar(city_rating, x='City', y='Rating', color='City', text_auto=True)
st.plotly_chart(fig3)

# 5. Boxplot of Ratings by Payment Method
st.subheader("Ratings by Payment Method")
st.markdown("Explore how payment method correlates with customer ratings.")
fig4 = px.box(df_filtered, x='Payment', y='Rating', color='Payment')
st.plotly_chart(fig4)

# 6. Ratings by Product Line
st.subheader("Average Rating by Product Line")
st.markdown("Identify which product lines receive higher ratings from customers.")
prod_rating = df_filtered.groupby('Product line')['Rating'].mean().sort_values().reset_index()
fig5 = px.bar(prod_rating, x='Rating', y='Product line', orientation='h', color='Product line')
st.plotly_chart(fig5)

# 7. Quantity Sold by Product Line
st.subheader("Quantity Sold by Product Line")
st.markdown("Analyze quantity sold across different product lines.")
quantity_data = df_filtered.groupby('Product line')['Quantity'].sum().reset_index()
fig6 = px.bar(quantity_data, x='Product line', y='Quantity', color='Product line')
st.plotly_chart(fig6)

# 8. Total Sales by Product Line
st.subheader("Total Sales by Product Line")
st.markdown("See which product lines generate the most sales revenue.")
sales_data = df_filtered.groupby('Product line')['Total'].sum().reset_index()
fig7 = px.pie(sales_data, values='Total', names='Product line')
st.plotly_chart(fig7)

# 9. gross Income vs Rating Scatter
st.subheader("gross Income vs Rating")
st.markdown("Visualize the relationship between gross income and customer ratings.")
fig8 = px.scatter(df_filtered, x='gross income', y='Rating', color='Product line')
st.plotly_chart(fig8)

# 10. Sales Over Time
st.subheader("Sales Over Time")
st.markdown("Track total daily sales trends.")
daily_sales = df_filtered.groupby('Date')['Total'].sum().reset_index()
fig9 = px.line(daily_sales, x='Date', y='Total')
st.plotly_chart(fig9)

# 11. Average Rating Over Time
st.subheader("Average Rating Over Time")
st.markdown("Monitor changes in average customer ratings over time.")
daily_rating = df_filtered.groupby('Date')['Rating'].mean().reset_index()
fig10 = px.line(daily_rating, x='Date', y='Rating')
st.plotly_chart(fig10)

# 12. Heatmap of Product Line vs Payment Method
st.subheader("Heatmap: Product Line vs Payment Method")
st.markdown("Find patterns in payment method preferences for product lines.")
pivot = pd.pivot_table(df_filtered, values='Total', index='Product line', columns='Payment', aggfunc='sum').fillna(0)
fig11, ax11 = plt.subplots()
sns.heatmap(pivot, annot=True, fmt=".0f", cmap='Blues', ax=ax11)
st.pyplot(fig11)

# 13. Customer Type vs Average Rating
st.subheader("Customer Type vs Average Rating")
st.markdown("Check how member and normal customers rate their experience.")
customer_rating = df_filtered.groupby('Customer type')['Rating'].mean().reset_index()
fig12 = px.bar(customer_rating, x='Customer type', y='Rating', color='Customer type')
st.plotly_chart(fig12)

# 14. Gender vs Average Rating
st.subheader("Gender vs Average Rating")
st.markdown("Explore if there's any difference in ratings by gender.")
gender_rating = df_filtered.groupby('Gender')['Rating'].mean().reset_index()
fig13 = px.bar(gender_rating, x='Gender', y='Rating', color='Gender')
st.plotly_chart(fig13)

# 15. Average Unit Price by Product Line
st.subheader("Average Unit Price by Product Line")
st.markdown("Understand pricing patterns across product lines.")
unit_price_data = df_filtered.groupby('Product line')['Unit price'].mean().reset_index()
fig14 = px.bar(unit_price_data, x='Product line', y='Unit price', color='Product line')
st.plotly_chart(fig14)

# 16. Sales by Payment Method
st.subheader("Sales by Payment Method")
st.markdown("Compare total sales by payment method.")
payment_sales = df_filtered.groupby('Payment')['Total'].sum().reset_index()
fig15 = px.pie(payment_sales, values='Total', names='Payment')
st.plotly_chart(fig15)

# 17. Sales by Branch
st.subheader("Total Sales by Branch")
st.markdown("Identify which branches generate the most revenue.")
branch_sales = df_filtered.groupby('Branch')['Total'].sum().reset_index()
fig16 = px.bar(branch_sales, x='Branch', y='Total', color='Branch')
st.plotly_chart(fig16)

# 18. gross Income by Branch
st.subheader("gross Income by Branch")
st.markdown("Explore gross income performance across branches.")
gross_income_branch = df_filtered.groupby('Branch')['gross income'].sum().reset_index()
fig17 = px.bar(gross_income_branch, x='Branch', y='gross income', color='Branch')
st.plotly_chart(fig17)

# 19. Correlation Heatmap
st.subheader("Correlation Heatmap")
st.markdown("See relationships among numerical variables.")
fig18, ax18 = plt.subplots()
sns.heatmap(df_filtered.select_dtypes('number').corr(), annot=True, cmap='coolwarm', ax=ax18)
st.pyplot(fig18)

# 20. Ratings vs Total Sales by Branch
st.subheader("Ratings vs Total Sales by Branch")
st.markdown("Scatterplot comparing branch sales with average customer ratings.")
branch_data = df_filtered.groupby('Branch').agg({'Total':'sum', 'Rating':'mean'}).reset_index()
fig19 = px.scatter(branch_data, x='Total', y='Rating', color='Branch', size='Total')
st.plotly_chart(fig19)

# Footer
st.markdown("---")
st.markdown("Dashboard created for customer service director and stakeholders to explore detailed insights.")

