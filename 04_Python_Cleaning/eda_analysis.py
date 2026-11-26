import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

print("EDA Libraries Imported Successfully!")

# Load cleaned datasets
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "05_Cleaned_Data")
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

orders = pd.read_csv(os.path.join(DATA_DIR, "orders_cleaned.csv"))
customers = pd.read_csv(os.path.join(DATA_DIR, "customers_cleaned.csv"))
order_items = pd.read_csv(os.path.join(DATA_DIR, "order_items_cleaned.csv"))
payments = pd.read_csv(os.path.join(DATA_DIR, "payments_cleaned.csv"))
reviews = pd.read_csv(os.path.join(DATA_DIR, "reviews_cleaned.csv"))

print("\nCleaned datasets loaded successfully!")

# Dataset Overview
print("\n========== DATASET OVERVIEW ==========")

for name, df in {
    "Orders": orders,
    "Customers": customers,
    "Order Items": order_items,
    "Payments": payments,
    "Reviews": reviews
}.items():
    print(f"\n{name}")
    print("Shape:", df.shape)
    print(df.head())

    # Descriptive Statistical Analysis

print("\n========== DESCRIPTIVE STATISTICS ==========")

print("\nORDER ITEMS STATISTICS")
print(order_items[["price", "freight_value"]].describe())

print("\nPAYMENT STATISTICS")
print(payments[["payment_value", "payment_installments"]].describe())

print("\nREVIEW SCORE STATISTICS")
print(reviews["review_score"].describe())

print("\nORDER STATUS DISTRIBUTION")
print(orders["order_status"].value_counts())
# Correlation Analysis

print("\n========== CORRELATION ANALYSIS ==========")

correlation_data = order_items[
    ["price", "freight_value"]
]

correlation = correlation_data.corr()

print(correlation)

plt.figure(figsize=(7, 5))

sns.heatmap(
    correlation,
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Price and Freight Value Correlation")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "correlation_analysis.png"))
plt.show()

# Monthly Revenue Trend Analysis

print("\n========== MONTHLY REVENUE TREND ==========")

orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"]
)

monthly_orders = orders.dropna(
    subset=["order_purchase_timestamp"]
).copy()

monthly_orders["month"] = (
    monthly_orders["order_purchase_timestamp"].dt.to_period("M")
)

monthly_trend = monthly_orders.groupby("month")["order_id"].count()

print(monthly_trend)

plt.figure(figsize=(12, 5))

monthly_trend.plot(kind="line", marker="o")

plt.title("Monthly Order Trend")
plt.xlabel("Month")
plt.ylabel("Total Orders")
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "monthly_order_trend.png"))
plt.show()

# Hypothesis Testing

from scipy.stats import pearsonr

print("\n========== HYPOTHESIS TESTING ==========")

price = order_items["price"]
freight = order_items["freight_value"]

correlation_value, p_value = pearsonr(price, freight)

print("Correlation:", correlation_value)
print("P-value:", p_value)

if p_value < 0.05:
    print("Result: Significant relationship between price and freight value")
else:
    print("Result: No significant relationship between price and freight value")

    # Delivery Time Analysis

print("\n========== DELIVERY TIME ANALYSIS ==========")

orders["order_delivered_customer_date"] = pd.to_datetime(
    orders["order_delivered_customer_date"]
)

orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"]
)

delivery_data = orders.dropna(
    subset=[
        "order_purchase_timestamp",
        "order_delivered_customer_date"
    ]
).copy()

delivery_data["delivery_days"] = (
    delivery_data["order_delivered_customer_date"]
    - delivery_data["order_purchase_timestamp"]
).dt.days

print("Average Delivery Days:",
      round(delivery_data["delivery_days"].mean(), 2))

print("Minimum Delivery Days:",
      delivery_data["delivery_days"].min())

print("Maximum Delivery Days:",
      delivery_data["delivery_days"].max())

plt.figure(figsize=(8, 5))

sns.histplot(delivery_data["delivery_days"], bins=30)

plt.title("Delivery Time Distribution")
plt.xlabel("Delivery Days")
plt.ylabel("Number of Orders")

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "delivery_time_analysis.png"))
plt.show()

# Business Insights

print("\n========== BUSINESS INSIGHTS ==========")

print("1. Average Product Price:",
      round(order_items["price"].mean(), 2))

print("2. Average Freight Value:",
      round(order_items["freight_value"].mean(), 2))

print("3. Average Review Score:",
      round(reviews["review_score"].mean(), 2))

print("4. Most Common Payment Method:",
      payments["payment_type"].mode()[0])

print("5. Total Delivered Orders:",
      (orders["order_status"] == "delivered").sum())

      # Regression Analysis

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

print("\n========== REGRESSION ANALYSIS ==========")

regression_data = order_items[
    ["price", "freight_value"]
].dropna()

X = regression_data[["price"]]
y = regression_data["freight_value"]

model = LinearRegression()
model.fit(X, y)

predictions = model.predict(X)

print("Regression Coefficient:", model.coef_[0])
print("Intercept:", model.intercept_)
print("R2 Score:", r2_score(y, predictions))

plt.figure(figsize=(8, 5))

sns.regplot(
    data=regression_data,
    x="price",
    y="freight_value",
    scatter_kws={"alpha": 0.3}
)

plt.title("Price vs Freight Value Regression")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "regression_analysis.png"))
plt.show()

# Customer Segmentation

print("\n========== CUSTOMER SEGMENTATION ==========")

customer_orders = orders.merge(
    customers[["customer_id", "customer_unique_id"]],
    on="customer_id",
    how="left"
)

customer_segments = customer_orders.groupby(
    "customer_unique_id"
)["order_id"].count().reset_index()

customer_segments.rename(
    columns={"order_id": "total_orders"},
    inplace=True
)

customer_segments["segment"] = np.where(
    customer_segments["total_orders"] > 1,
    "Repeat Customer",
    "One-Time Customer"
)

print(customer_segments["segment"].value_counts())

plt.figure(figsize=(7, 5))

sns.countplot(
    data=customer_segments,
    x="segment"
)

plt.title("Customer Segmentation")
plt.xlabel("Customer Segment")
plt.ylabel("Number of Customers")

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "customer_segmentation.png"))
plt.show()

# Monthly Order Forecasting

# Monthly Order Forecasting

from sklearn.linear_model import LinearRegression

print("\n========== FORECASTING ANALYSIS ==========")

forecast_data = orders.copy()

forecast_data["order_purchase_timestamp"] = pd.to_datetime(
    forecast_data["order_purchase_timestamp"]
)

monthly_orders = (
    forecast_data
    .set_index("order_purchase_timestamp")
    .resample("MS")["order_id"]
    .count()
)

monthly_orders = monthly_orders.loc["2017-01":"2018-08"]

forecast_df = monthly_orders.reset_index()
forecast_df.columns = ["month", "orders"]

forecast_df["month_index"] = np.arange(len(forecast_df))

X = forecast_df[["month_index"]]
y = forecast_df["orders"]

model = LinearRegression()
model.fit(X, y)

future_index = np.arange(
    len(forecast_df),
    len(forecast_df) + 3
).reshape(-1, 1)

predictions = model.predict(future_index)

future_months = pd.date_range(
    start="2018-09-01",
    periods=3,
    freq="MS"
)

print("\nNext 3 Months Order Forecast:")

for month, prediction in zip(future_months, predictions):
    print(month.strftime("%Y-%m"), ":", round(prediction))

plt.figure(figsize=(10, 5))
plt.plot(monthly_orders.index, monthly_orders.values, label="Actual Orders")
plt.plot(future_months, predictions, marker="o", label="Forecast")

plt.title("Monthly Order Forecast")
plt.xlabel("Month")
plt.ylabel("Number of Orders")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "monthly_order_forecast.png"))
plt.show()

# Delivery Time Analysis

print("\n========== DELIVERY TIME ANALYSIS ==========")

orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"]
)

orders["order_delivered_customer_date"] = pd.to_datetime(
    orders["order_delivered_customer_date"]
)

delivery_data = orders.dropna(
    subset=[
        "order_purchase_timestamp",
        "order_delivered_customer_date"
    ]
).copy()

delivery_data["delivery_days"] = (
    delivery_data["order_delivered_customer_date"]
    - delivery_data["order_purchase_timestamp"]
).dt.days

print("Average Delivery Days:",
      round(delivery_data["delivery_days"].mean(), 2))

print("Minimum Delivery Days:",
      delivery_data["delivery_days"].min())

print("Maximum Delivery Days:",
      delivery_data["delivery_days"].max())

plt.figure(figsize=(10, 5))

sns.histplot(
    delivery_data["delivery_days"],
    bins=30
)

plt.title("Delivery Time Analysis")
plt.xlabel("Delivery Days")
plt.ylabel("Number of Orders")

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "delivery_time_analysis.png"))
plt.show()