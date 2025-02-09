import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import altair as alt
from matplotlib.ticker import FuncFormatter

# Load Data
data = pd.read_csv("Cleaned_Food_Order2.csv")

# Set Streamlit page config
st.set_page_config(page_title="NYC Restaurant Order Analysis", page_icon="🍔", layout="wide")

# Add header with animation
def add_header():
    st.markdown("""
        <div style="text-align: center; padding: 10px 0;">
            <h1 style='color: #FF6347;'>🍟 NYC Restaurant Order Analysis 🍽️</h1>
            <img src="https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExZzJpaHc1Y2V3bG1oc3pobmswbXB2YXdwd2Rtcm50ZGptazNjNDY5ZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/QAnAiRpj5Wcl5kdp9a/giphy.gif" width="150" style="border-radius: 50%;">
        </div>
    """, unsafe_allow_html=True)

# Add footer
def add_footer():
    st.markdown("""
        <hr style="border: 1px solid #FF6347;">
        <div style="text-align: center;">
            <p style="color: #FF6347;">Made with 💖 by NYC Data Team | 2025</p>
        </div>
    """, unsafe_allow_html=True)

# Sidebar Logo
def display_logo():
    try:
        img = Image.open("logo.png")
        st.sidebar.image(img, use_column_width=False, width=300)
    except FileNotFoundError:
        st.sidebar.warning("Logo image not found.")

# Title and Navigation Menu
def display_title_and_dropdowns():
    menu = ["Display Info", "Rating vs Other Variables", "Restaurant Info", "Cuisine Info", "Customer Info"]
    choice = st.sidebar.selectbox("Select an option", menu)
    return choice

# Display KPIs and Charts
def display_info():
    col1, col2, col3 = st.columns(3)

    total_revenue = data["Cost of the order"].sum()
    top_revenue_restaurant = data.groupby("Restaurant Name")["Cost of the order"].sum().idxmax()
    top_revenue_cuisine = data.groupby("Cuisine Type")["Cost of the order"].sum().idxmax()

    with col1:
        st.metric(label="Total Revenue", value=f"${total_revenue:,.2f}")
    with col2:
        st.metric(label="Top Revenue Restaurant", value=f"🎉 {top_revenue_restaurant}")
    with col3:
        st.metric(label="Top Revenue Cuisine", value=top_revenue_cuisine)

    st.markdown("---")

    # Revenue by Cuisine as Percentage
    revenue_cuisine = data.groupby("Cuisine Type")["Cost of the order"].sum().reset_index()
    cuisine_orders = data["Cuisine Type"].value_counts().reset_index()
    cuisine_orders.columns = ["Cuisine Type", "Number of Orders"]

    total_revenue = revenue_cuisine["Cost of the order"].sum()
    revenue_cuisine["Revenue Percentage"] = (revenue_cuisine["Cost of the order"] / total_revenue) * 100

    combined_data = pd.merge(revenue_cuisine, cuisine_orders, on="Cuisine Type")
    combined_data = combined_data.sort_values("Cost of the order", ascending=True)

    st.subheader(":fork_and_knife: Revenue and Number of Orders by Cuisine")
    st.markdown("This graph highlights revenue contribution and order volume across different cuisines.")

    bar_chart = alt.Chart(combined_data).mark_bar(color='mediumseagreen').encode(
        x=alt.X('Cuisine Type:N', sort=combined_data["Cuisine Type"].tolist()),
        y=alt.Y('Cost of the order:Q', axis=alt.Axis(title='Revenue')),
        tooltip=[
            'Cuisine Type', 
            alt.Tooltip('Cost of the order:Q', title='Revenue'), 
            alt.Tooltip('Revenue Percentage:Q', title='Revenue %', format='.2f')
        ]
    )

    line_chart = alt.Chart(combined_data).mark_line(color='darkorange', strokeWidth=3).encode(
        x='Cuisine Type:N',
        y=alt.Y('Number of Orders:Q', axis=alt.Axis(title='Number of Orders')),
        tooltip=[
            'Cuisine Type', 
            alt.Tooltip('Number of Orders:Q', title='Number of Orders')
        ]
    ).interactive()

    combined_chart = alt.layer(bar_chart, line_chart).resolve_scale(
        y='independent' 
    ).properties(
        width=300,
        height=400
    ).configure_legend(
        orient='bottom'
    )

    st.altair_chart(combined_chart, use_container_width=True)
    st.markdown("**Summary:** The chart reveals which cuisines are the highest revenue generators and how their order volumes compare.")

    st.markdown("---")

    # Revenue by Restaurant as Percentage
    revenue_restaurant = data.groupby("Restaurant Name")["Cost of the order"].sum()
    revenue_restaurant_percent = (revenue_restaurant / revenue_restaurant.sum()) * 100  
    top_10_revenue_restaurant_percent = revenue_restaurant_percent.sort_values(ascending=False).head(10).reset_index()
    top_10_revenue_restaurant_percent.columns = ['Restaurant Name', 'Revenue Percentage']

    st.subheader(":moneybag: Top 10 Revenue Share by Restaurant (%)")
    st.markdown("This bar chart showcases the top 10 restaurants contributing the most to revenue.")

    chart = alt.Chart(top_10_revenue_restaurant_percent).mark_bar(color='royalblue').encode(
        x=alt.X('Revenue Percentage:Q', title='Revenue Share (%)'),
        y=alt.Y('Restaurant Name:N', sort='-x', title='Restaurant'),
        tooltip=['Restaurant Name', 'Revenue Percentage']
    ).properties(
        width=700,
        height=400
    ).configure_legend(
        orient='bottom'
    ).configure_mark(
        opacity=0.85
    )

    st.altair_chart(chart, use_container_width=True)
    st.markdown("**Summary:** This visualization identifies the top-performing restaurants, highlighting their dominance in revenue generation.")

    st.markdown("---")

    col1, col2 = st.columns(2)

   

    with col1:
        # Prepare the data for top 10 restaurants by order volume
        top_10_orders_restaurant = data["Restaurant Name"].value_counts().head(10)
            
        # Create a dataframe with the restaurant names and their number of orders
        top_10_orders_data = top_10_orders_restaurant.reset_index()
        top_10_orders_data.columns = ['Restaurant Name', 'Number of Orders']
            
        # Heading with icon
        st.subheader(":chart_with_upwards_trend: Top 10 Restaurants by Number of Orders")
        st.markdown("This graph displays the restaurants with the highest number of orders.")
            
        # Altair Bar Chart for Number of Orders
        bar_chart = alt.Chart(top_10_orders_data).mark_bar(color='teal').encode(
        x=alt.X('Restaurant Name:N', sort=top_10_orders_data["Restaurant Name"].tolist()),
        y=alt.Y('Number of Orders:Q', axis=alt.Axis(title='Number of Orders')),
        tooltip=[
                    'Restaurant Name',
                    alt.Tooltip('Number of Orders:Q', title='Number of Orders')
                ]
            )
            
            # Display the chart
        st.altair_chart(bar_chart, use_container_width=True)
            
            # Summary
        st.markdown("**Summary:** This chart highlights the top 10 restaurants based on order volume.")

                
        with col2:
           st.subheader(":calendar: Orders by Day of the Week")
           st.markdown("This pie chart shows the distribution of orders across the week.")
           weekday_orders = data["Day of the week"].value_counts()
                
           fig, ax = plt.subplots(figsize=(4, 4))  # Adjust size if needed
           colors = sns.color_palette("Set3", n_colors=len(weekday_orders))  # A better color palette
                
            # Plot the pie chart
           wedges, texts, autotexts = ax.pie(weekday_orders, labels=weekday_orders.index, autopct='%1.1f%%', 
                                                      startangle=90, colors=colors, wedgeprops={'edgecolor': 'black', 'linewidth': 1})
                
                    # Style the pie chart text
           for text in texts:
                 text.set_fontsize(12)
                 text.set_fontweight('bold')
                
           for autotext in autotexts:
                   autotext.set_fontsize(10)
                   autotext.set_fontweight('bold')
                
                    # Equal aspect ratio ensures that pie is drawn as a circle
           ax.axis('equal')
                
                    # Remove the white background
           fig.patch.set_alpha(0)
           ax.set_facecolor('none')  # No background for axes
                
                    # Adjust layout to avoid clipping
           plt.tight_layout()
                
           st.pyplot(fig)
           st.markdown("**Summary:** The pie chart illustrates peak and low order days, aiding in operational planning.")


# Set style for seaborn plots to remove the white background
sns.set(style="whitegrid")

def rating_vs_others():
    
    sns.set(style="whitegrid")
    st.subheader("Rating vs Other Variables")
    
    # Reduced figure size and improved layout
    col1,col2,col3=st.columns([1,2,1])
    with col2:
          # Adjusted size for better fit in Streamlit
        fig, ax = plt.subplots(figsize=(6,4))
            # Graph 1: Rating vs Preparation Time
        sns.regplot(x="Rating", y="Food preparing time", data=data, ax=ax, scatter_kws={'s': 50, 'color': 'blue'}, line_kws={'color': 'red', 'lw': 2})
        ax.set_title("Rating vs Preparation Time")
        ax.set_xlabel("Rating")
        ax.xaxis.set_major_formatter(FuncFormatter(lambda val, _: f'{int(val)}'))
        ax.tick_params(axis='x', labelsize=10)
        st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
        st.pyplot(fig)
        st.markdown(
                """
                <div style="text-align:center; font-size:20px; color:#6495ED;">
                    <p style="text-align:center; font-size:22px; color:#6495ED;"><b>Summary:</b> A Rating vs. Food Preparation Time graph typically shows whether faster food preparation correlates with higher or lower customer ratings, helping identify the impact of speed on customer satisfaction.</p>
                </div>
                """, unsafe_allow_html=True)
       
    col1,col2,col3=st.columns([1,2,1])
    with col2:
        fig, ax = plt.subplots(figsize=(4, 3))
            # Graph 2: Rating vs Delivery Time
        sns.regplot(x="Rating", y="Delivery time", data=data, ax=ax, scatter_kws={'s': 50, 'color': 'green'}, line_kws={'color': 'red', 'lw': 2})
        ax.set_title("Rating vs Delivery Time")
        ax.set_xlabel("Rating")
        ax.xaxis.set_major_formatter(FuncFormatter(lambda val, _: f'{int(val)}'))
        ax.tick_params(axis='x', labelsize=10)
        st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
        st.pyplot(fig)
        st.markdown(
                """
                <div style="text-align:center; font-size:20px; color:#6495ED;">
                    <p style="text-align:center; font-size:22px; color:#6495ED;"><b>Summary:</b> A Rating vs. Food Delivery Time graph highlights the impact of delivery speed on customer satisfaction, showing whether quicker deliveries lead to higher ratings or if delays result in lower ratings.</p>
                </div>
                """, unsafe_allow_html=True)
    col1,col2,col3=st.columns([1,2,1])
    with col2:
        fig, ax = plt.subplots(figsize=(4, 3))
            # Graph 3: Rating vs Cost of the Order
        sns.regplot(x="Rating", y="Cost of the order", data=data, ax=ax, scatter_kws={'s': 50, 'color': 'purple'}, line_kws={'color': 'red', 'lw': 2})
        ax.set_title("Rating vs Cost of Order")
        ax.set_xlabel("Rating")
        ax.xaxis.set_major_formatter(FuncFormatter(lambda val, _: f'{int(val)}'))
        ax.tick_params(axis='x', labelsize=10)
        st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
        st.pyplot(fig)
        st.markdown(
            """
            <div style="text-align:center; font-size:20px; color:#6495ED;">
                <p style="text-align:center; font-size:22px; color:#6495ED;"><b>Summary:</b>
A Rating vs. Food Cost graph reveals how food pricing influences customer satisfaction, showing whether higher costs lead to better ratings or if affordability drives positive feedback.</p>
            </div>
            """, unsafe_allow_html=True)

        # Adjust layout to prevent overlap
    plt.tight_layout()
    
        # Display the plot in Streamlit
    
    
        # Conclusion block with a clean style
    st.markdown(
    
        """
        <div style="background-color:#f8f9fa; padding:10px; border-radius:8px;">
            <h3 style="color:#FF5733; text-align:center;">📌 Conclusion</h3>
            <p style="font-size:18px; color:#333; text-align:center;">
                Other factors such as <b>food quality, service, and customer experience</b> might play a more crucial role in determining ratings.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
# Restaurant Info
def restaurant_info():
    restaurant = st.selectbox("Select a Restaurant", sorted(data["Restaurant Name"].unique()))
    restaurant_data = data[data["Restaurant Name"] == restaurant]

    total_revenue = restaurant_data["Cost of the order"].sum()
    avg_rating = restaurant_data["Rating"].mean()
    most_selling_cuisine = restaurant_data.groupby("Cuisine Type")["Cost of the order"].sum().idxmax()
    price_range = (restaurant_data["Cost of the order"].min(), restaurant_data["Cost of the order"].max())

    st.subheader(f"{restaurant}")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Revenue", value=f"${total_revenue:,.2f}")
    with col2:
        st.metric(label="Average Rating", value=f"{avg_rating:.2f}")
    with col3:
        st.metric(label="Most Selling Cuisine", value=most_selling_cuisine)

    st.write(f"**Price Range:** ${price_range[0]} - ${price_range[1]}")
    st.write(f"**Available Cuisines:** {', '.join(restaurant_data['Cuisine Type'].unique())}")

    revenue_cuisine = restaurant_data.groupby("Cuisine Type")["Cost of the order"].sum()
    st.subheader("Revenue by Cuisine")
    st.bar_chart(revenue_cuisine)
    st.markdown(
            """
            <div style="text-align:center; font-size:20px; color:#6495ED;">
                <p style="text-align:center; font-size:22px; color:#6495ED;"><b>Summary:</b>
A Cuisine vs. Revenue graph compares the revenue generated by different cuisines, helping identify the most profitable cuisine types and guiding menu optimization strategies..</p>
            </div>
            """, unsafe_allow_html=True)


    
# Cuisine Info
def cuisine_info():
    cuisine = st.selectbox("Select a Cuisine", sorted(data["Cuisine Type"].unique()))
    cuisine_data = data[data["Cuisine Type"] == cuisine]

    total_revenue = cuisine_data["Cost of the order"].sum()
    price_range = (cuisine_data["Cost of the order"].min(), cuisine_data["Cost of the order"].max())
    most_ordered_restaurant = cuisine_data.groupby("Restaurant Name")["Cost of the order"].sum().idxmax()

    st.subheader(f"{cuisine} Cuisine")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Total Revenue", value=f"${total_revenue:,.2f}")
    with col2:
        st.metric(label="Most Ordered From", value=most_ordered_restaurant)

    st.write(f"**Price Range:** ${price_range[0]} - ${price_range[1]}")

    revenue_restaurant = cuisine_data.groupby("Restaurant Name")["Cost of the order"].sum()
    st.subheader("Revenue by Restaurant")
    st.bar_chart(revenue_restaurant)
    st.markdown(
            """
            <div style="text-align:center; font-size:20px; color:#6495ED;">
                <p style="text-align:center; font-size:22px; color:#6495ED;"><b>Summary:</b>
A Restaurant vs. Revenue graph compares the revenue generated by different restaurants, helping identify top-performing locations and guiding business growth strategies.</p>
            </div>
            """, unsafe_allow_html=True)
    

# Customer Info
def customer_info():
    customer_order_counts = data["Customer ID"].value_counts()
    frequent_customers = customer_order_counts[customer_order_counts > 2]
    top_20_customers = frequent_customers.head(20)

    customer_data = data[data["Customer ID"].isin(frequent_customers.index)]
    total_orders = customer_data.groupby("Customer ID").size()
    total_revenue = ((customer_data.groupby("Customer ID")["Cost of the order"].sum())/(data["Cost of the order"].sum()))*100

    top_20_orders = total_orders[top_20_customers.index]
    top_20_revenue = total_revenue[top_20_customers.index]

    total_customers = data["Customer ID"].nunique() 
    permanent_customers = len(frequent_customers)  
    temporary_customers = total_customers - permanent_customers 

    permanent_percentage = (permanent_customers / total_customers) * 100
    temporary_percentage = (temporary_customers / total_customers) * 100

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Permanent Customers (%)", value=f"{permanent_percentage:.2f}%")
    with col2:
        st.metric(label="Temporary Customers (%)", value=f"{temporary_percentage:.2f}%")

    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Bar chart: Top 20 Customers vs No. of Orders
    color1 = "tab:blue"
    ax1.bar(top_20_orders.index.astype(str), top_20_orders.values, color=color1, alpha=0.6, label="No. of Orders")
    ax1.set_xlabel("Top 20 Customers")
    ax1.set_ylabel("Number of Orders", color=color1)
    ax1.tick_params(axis="y", labelcolor=color1)
    ax1.set_xticklabels(top_20_orders.index, rotation=45, ha="right")  # Rotate labels for clarity

    # Twin y-axis for revenue (line chart)
    ax2 = ax1.twinx()
    color2 = "tab:red"
    ax2.plot(top_20_revenue.index.astype(str), top_20_revenue.values, color=color2, marker="o", linestyle="-", linewidth=2, label="Total Revenue (%)")
    ax2.set_ylabel("Total Revenue (%)", color=color2)
    ax2.tick_params(axis="y", labelcolor=color2)

    # Title and Legend
    fig.suptitle("Top 20 Frequent Customers: Orders vs Revenue(%)", fontsize=14, fontweight="bold")
    fig.legend(loc="upper left")
    st.pyplot(fig)

    st.markdown(
            """
            <div style="text-align:center; font-size:20px; color:#6495ED;">
                <p style="text-align:center; font-size:22px; color:#6495ED;"><b>Summary:</b>
A Regular Customers vs. Revenue Generated graph shows the contribution of repeat customers to overall revenue, helping assess their impact on business profitability and customer retention value</p>
            </div>
            """, unsafe_allow_html=True)
    

    customer_info_table = pd.DataFrame({
        "Total Orders": total_orders,
        "Total Revenue": total_revenue
    }).reset_index().rename(columns={"index": "Customer ID"}).sort_values(by="Total Orders", ascending=False).reset_index()

    st.subheader("Frequent Customers (Ordered More Than 2 Times)")
    st.dataframe(customer_info_table, use_container_width=True)
    

# Main Function
def main():
    display_logo()
    add_header()
    choice = display_title_and_dropdowns()

    if choice == "Display Info":
        display_info()
    elif choice == "Rating vs Other Variables":
        rating_vs_others()
    elif choice == "Restaurant Info":
        restaurant_info()
    elif choice == "Cuisine Info":
        cuisine_info()
    elif choice == "Customer Info":
        customer_info()

    add_footer()

if __name__ == "__main__":
    main()



