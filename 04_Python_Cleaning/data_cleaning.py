import pandas as pd
import numpy as np
import os

print("Libraries imported successfully!")

# Project directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Correct raw data folder
RAW_DATA = os.path.join(BASE_DIR, "02_Raw data set")

# Load all 9 datasets
orders = pd.read_csv(os.path.join(RAW_DATA, "olist_orders_dataset.csv"))
customers = pd.read_csv(os.path.join(RAW_DATA, "olist_customers_dataset.csv"))
order_items = pd.read_csv(os.path.join(RAW_DATA, "olist_order_items_dataset.csv"))
payments = pd.read_csv(os.path.join(RAW_DATA, "olist_order_payments_dataset.csv"))
reviews = pd.read_csv(os.path.join(RAW_DATA, "olist_order_reviews_dataset.csv"))
products = pd.read_csv(os.path.join(RAW_DATA, "olist_products_dataset.csv"))
sellers = pd.read_csv(os.path.join(RAW_DATA, "olist_sellers_dataset.csv"))
geolocation = pd.read_csv(os.path.join(RAW_DATA, "olist_geolocation_dataset.csv"))
category_translation = pd.read_csv(os.path.join(RAW_DATA, "product_category_name_translation.csv"))

print("\nAll 9 datasets loaded successfully!")

# Display dataset dimensions
datasets = {
    "Orders": orders,
    "Customers": customers,
    "Order Items": order_items,
    "Payments": payments,
    "Reviews": reviews,
    "Products": products,
    "Sellers": sellers,
    "Geolocation": geolocation,
    "Category Translation": category_translation
}

print("\nDATASET DIMENSIONS")

for name, df in datasets.items():
    print(f"{name}: {df.shape}")

    # Dataset Inspection

print("\n========== DATASET INSPECTION ==========")

for name, df in datasets.items():

    print(f"\n--- {name} ---")

    print("\nFirst 5 Rows:")
    print(df.head())

    print("\nData Types:")
    print(df.dtypes)

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Rows:")
    print(df.duplicated().sum())

    # Missing Values Percentage

print("\n========== MISSING VALUE PERCENTAGE ==========")

for name, df in datasets.items():

    missing = df.isnull().sum()
    percentage = (missing / len(df)) * 100

    missing_report = pd.DataFrame({
        "Missing Count": missing,
        "Missing Percentage": percentage.round(2)
    })

    missing_report = missing_report[missing_report["Missing Count"] > 0]

    if not missing_report.empty:
        print(f"\n--- {name} ---")
        print(missing_report)
    else:
        print(f"\n{name}: No missing values")

        # Duplicate Analysis

print("\n========== DUPLICATE ANALYSIS ==========")

for name, df in datasets.items():

    total_duplicates = df.duplicated().sum()

    duplicate_percentage = (total_duplicates / len(df)) * 100

    print(f"\n{name}")
    print("Duplicate Rows:", total_duplicates)
    print("Duplicate Percentage:", round(duplicate_percentage, 2), "%")

    # Outlier Analysis

print("\n========== OUTLIER ANALYSIS ==========")

numeric_columns = {
    "Order Items": ["price", "freight_value"],
    "Payments": ["payment_value"],
    "Products": [
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm"
    ]
}

for dataset_name, columns in numeric_columns.items():

    df = datasets[dataset_name]

    print(f"\n--- {dataset_name} ---")

    for column in columns:

        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        outliers = df[
            (df[column] < lower) |
            (df[column] > upper)
        ]

        print(f"\n{column}")
        print("Outlier Count:", len(outliers))
        print("Lower Limit:", round(lower, 2))
        print("Upper Limit:", round(upper, 2))

        # Missing Value Row Inspection

print("\n========== MISSING VALUE ROW INSPECTION ==========")

for name in ["Orders", "Reviews", "Products"]:

    df = datasets[name]

    missing_rows = df[df.isnull().any(axis=1)]

    print(f"\n{name}")
    print("Rows with Missing Values:", len(missing_rows))
    print(missing_rows.head())

    print("\n========== PRODUCTS MISSING VALUE DETAILS ==========")

print(products.isnull().sum())

print("\nProducts with Missing Values:")
print(products[products.isnull().any(axis=1)].to_string())

# Product Category Cleaning

products["product_category_name"] = products[
    "product_category_name"
].fillna("Unknown")

print("\n========== PRODUCT CATEGORY CLEANING ==========")

print("Missing Categories After Cleaning:",
      products["product_category_name"].isnull().sum())

print("Unknown Categories:",
      (products["product_category_name"] == "Unknown").sum())

print("\n========== ORDER MISSING DATE ANALYSIS ==========")

missing_orders = orders[
    orders["order_approved_at"].isnull() |
    orders["order_delivered_carrier_date"].isnull() |
    orders["order_delivered_customer_date"].isnull()
]

print(missing_orders["order_status"].value_counts())

print("\nMissing Dates by Order Status:")
print(
    missing_orders.groupby("order_status")[
        [
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date"
        ]
    ].apply(lambda x: x.isnull().sum())
)

print("\n========== ORDER DATE DATA TYPES ==========")

date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for column in date_columns:
    orders[column] = pd.to_datetime(orders[column], errors="coerce")

print(orders[date_columns].dtypes)

# Review Comments Cleaning

reviews["review_comment_title"] = reviews[
    "review_comment_title"
].fillna("No Comment")

reviews["review_comment_message"] = reviews[
    "review_comment_message"
].fillna("No Comment")

print("\n========== REVIEW COMMENTS CLEANING ==========")

print("Missing Titles:",
      reviews["review_comment_title"].isnull().sum())

print("Missing Messages:",
      reviews["review_comment_message"].isnull().sum())

print("\n========== PRODUCTS MISSING VALUES ==========")
print(products.isnull().sum())

print("\n========== PRODUCT MISSING ROW INSPECTION ==========")

missing_products = products[products.isnull().any(axis=1)]

print("Total Missing Product Rows:", len(missing_products))
print(missing_products.head(10).to_string())

print("\n========== FINAL MISSING VALUE CHECK ==========")

for name, df in datasets.items():
    print(f"\n{name}:")
    print(df.isnull().sum().sum(), "missing values")

    print("\n========== PRODUCTS MISSING VALUE ANALYSIS ==========")

missing_products = products[products.isnull().any(axis=1)]

print("Total Missing Product Rows:", len(missing_products))

print("\nMissing Values by Column:")
print(products.isnull().sum())

print("\nRows with Missing Physical Details:")
print(
    missing_products[
        missing_products["product_weight_g"].isnull() |
        missing_products["product_length_cm"].isnull() |
        missing_products["product_height_cm"].isnull() |
        missing_products["product_width_cm"].isnull()
    ].to_string()
)

print("\n========== PRODUCTS PHYSICAL DETAILS INSPECTION ==========")

physical_missing = products[
    products["product_weight_g"].isnull() |
    products["product_length_cm"].isnull() |
    products["product_height_cm"].isnull() |
    products["product_width_cm"].isnull()
]

print(physical_missing.to_string())

print("\n========== PRODUCT MISSING DATA VERIFICATION ==========")

original_products = pd.read_csv(
    r"C:\Users\laksh\Downloads\Ecommerce_Business_Analytics\02_Raw data set\olist_products_dataset.csv"
)

print(
    original_products[
        original_products["product_id"].isin(
            ["09ff539a621711667c43eba6a3bd8466",
             "5eb564652db742ff8f28759cd8d2652a"]
        )
    ].to_string()
)

print("\n========== GEOLOCATION DUPLICATE ANALYSIS ==========")

print("Total Rows:", len(geolocation))
print("Duplicate Rows:", geolocation.duplicated().sum())

print("\nSample Duplicate Records:")
print(
    geolocation[
        geolocation.duplicated(keep=False)
    ].head(10).to_string()
)

print("\n========== GEOLOCATION EXACT DUPLICATE CHECK ==========")

exact_duplicates = geolocation[
    geolocation.duplicated(keep=False)
]

print("Exact Duplicate Records:", len(exact_duplicates))

print("\nDuplicate Count by Zip Code:")
print(
    exact_duplicates["geolocation_zip_code_prefix"]
    .value_counts()
    .head(10)
)

print("\n========== GEOLOCATION DUPLICATE CLEANING ==========")

before = len(geolocation)

geolocation = geolocation.drop_duplicates().copy()

after = len(geolocation)

print("Rows Before Cleaning:", before)
print("Rows After Cleaning:", after)
print("Exact Duplicates Removed:", before - after)
print("Remaining Duplicates:", geolocation.duplicated().sum())

print("\n========== FINAL DATA QUALITY VALIDATION ==========")

for name, df in datasets.items():

    print(f"\n{name}")
    print("Total Rows:", len(df))
    print("Missing Values:", df.isnull().sum().sum())
    print("Duplicate Rows:", df.duplicated().sum())

    datasets["Geolocation"] = geolocation

    import os

print("\n========== SAVING CLEANED DATASETS ==========")

output_folder = "05_Cleaned_Data"

os.makedirs(output_folder, exist_ok=True)

for name, df in datasets.items():
    file_name = name.replace(" ", "_").lower() + "_cleaned.csv"

    file_path = os.path.join(output_folder, file_name)

    df.to_csv(file_path, index=False)

    print(f"{file_name} - Saved successfully")

print("\nAll cleaned datasets saved!")
print("\n========== REVIEW ID DUPLICATE CHECK ==========")

print("Total rows:", len(reviews))
print("Unique review IDs:", reviews["review_id"].nunique())
print("Duplicate review IDs:", reviews["review_id"].duplicated().sum())
print("Missing review IDs:", reviews["review_id"].isnull().sum())