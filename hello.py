from preswald import text, plotly, connect, get_df, table
import pandas as pd
import plotly.express as px
import os

# Set a title for the app
text("# Order Data Analysis")
text("Exploring the orders dataset ")

# Load the dataset
connect()
df = get_df("data/List_of_Orders_Small.csv")  # Load the smaller dataset

if df is None:
    text("⚠️ Error: Data could not be loaded. Trying manual load...")
    csv_path = "data/List_of_Orders_Small.csv"
    
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        text("✅ Data loaded successfully!")
    else:
        text(f"❌ File '{csv_path}' not found! Check the directory.")
        df = None  # Stop further execution if file is missing

# Proceed only if df is successfully loaded
if df is not None:
    # Normalize column names (removes extra spaces)
    df.columns = df.columns.str.strip()

    # Show dataset table
    table(df, title="Order Data Overview")

    # Convert "Order Date" column to datetime format safely
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce", dayfirst=True)

    # Orders Per State Visualization
    state_counts = df["State"].value_counts().reset_index()
    state_counts.columns = ["State", "Order Count"]
    fig_state = px.bar(state_counts, x="State", y="Order Count",
                       title="Orders Per State", labels={"Order Count": "Number of Orders"},
                       text_auto=True)
    plotly(fig_state)

    # Orders Per City Visualization (Top 10 Cities for readability)
    city_counts = df["City"].value_counts().head(10).reset_index()
    city_counts.columns = ["City", "Order Count"]
    fig_city = px.bar(city_counts, x="City", y="Order Count",
                      title="Top 10 Orders Per City", labels={"Order Count": "Number of Orders"},
                      text_auto=True)
    plotly(fig_city)
