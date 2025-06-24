

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output


df = pd.read_csv("RIYARETAIL.csv", encoding='ISO-8859-1').head(100)
df.dropna(subset=["Customer_ID", "Amount", "Total_Amount"], inplace=True)
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['Sales_per_Purchase'] = df['Amount']
df['products'] = df['products'].fillna("Unknown")
df['Country'] = df['Country'].fillna("Unknown")


sns.set(style="whitegrid")

# 1. Segment vs Gender
plt.figure(figsize=(7, 4))
sns.countplot(data=df, x='Customer_Segment', hue='Gender', palette='Set2')
plt.title("Customer Segment by Gender")
plt.tight_layout()
plt.savefig("seg_gender_100rows.png")
plt.close()

# 2. Ratings by Payment
plt.figure(figsize=(8, 5))
sns.violinplot(data=df, x='Payment_Method', y='Ratings', palette='coolwarm')
plt.title("Ratings by Payment Method")
plt.tight_layout()
plt.savefig("ratings_payment_100rows.png")
plt.close()


app = dash.Dash(__name__)
app.title = "Riya Retail Dashboard"

app.layout = html.Div([
    html.H1("Riya Retail - Dash Dashboard (100 Rows)", style={'textAlign': 'center'}),

    dcc.Graph(
        id='segment-gender-plot',
        figure=px.histogram(df, x="Customer_Segment", color="Gender",
                            barmode="group", title="Customer Segment by Gender",
                            color_discrete_sequence=px.colors.qualitative.Set2)
    ),

    dcc.Graph(
        id='ratings-payment-plot',
        figure=px.violin(df, x="Payment_Method", y="Ratings", box=True, points="all",
                         title="Ratings by Payment Method",
                         color_discrete_sequence=["#AB63FA"])
    ),

    dcc.Graph(
        id='total-sales-country',
        figure=px.bar(
            df.groupby("Country")["Total_Amount"].sum().reset_index(),
            x="Country", y="Total_Amount", color="Country",
            title="Total Sales by Country",
            color_discrete_sequence=px.colors.sequential.Plasma)
    ),

    dcc.Graph(
        id='time-series-sales',
        figure=px.line(
            df.groupby("Date")["Amount"].sum().reset_index(),
            x="Date", y="Amount", markers=True,
            title="Sales Trend Over Time",
            color_discrete_sequence=["#EF553B"])
    )
])

# === LAUNCH DASH ===
if __name__ == '__main__':
    app.run(debug=True)  

