import pandas as pd

df = pd.read_csv("dirty_cafe_sales.csv")


all_cols = ["Transaction ID", "Item", "Quantity", "Price Per Unit", "Total Spent", "Payment Method", "Location", "Transaction Date"]

for col in all_cols:
    df[col] = df[col].str.strip()


df = df[~df[all_cols].isin(["UNKNOWN", "ERROR"]).any(axis=1)] # When you put something inside df[ ... ], pandas expects: 	•	A list/Series of True and False values
#Trues get kept and false gets removed
# keep all rows that do not have UNKNOWN and or ERROR 
# Looks across each row (axis=1). If at least one cell in a row is True (meaning it contained "UNKNOWN" or "ERROR"), the whole row is marked True.

#select_dtypes is used to return a subset of a DataFrame including or excluding columns based on their data types
str_cols = df.select_dtypes(include='object').columns
# in pandas object is the type for text/string data.
for col in str_cols:
# lstrip remove leading characters (from the left side) from each string in a Series or Index. 
    df[col] = df[col].astype(str).str.lstrip(',')

itemAndPricePerU = {
    "Coffee": 2,
    "Tea": 1.5,
    "Sandwich": 4,
    "Salad": 5,
    "Cake": 3,
    "Cookie": 1,
    "Smoothie": 4,
    "Juice": 3
}
df["Price Per Unit"] = df["Item"].map(itemAndPricePerU).combine_first(df["Price Per Unit"])
# map(itemAndPrice) → Gets correct price
#combine_first is the thing that actually tells it to replace the original with the mapped value and if map fails (aka return NaN) then keep original val
df["Price Per Unit"] = pd.to_numeric(df["Price Per Unit"], errors="coerce")
df["Total Spent"] = pd.to_numeric(df["Total Spent"], errors="coerce")
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
df["Total Spent"] = (df["Quantity"] * df["Price Per Unit"]).round(2)

#do this before mapping the price with it's item 
unknown_price = ["Item", "Price Per Unit", "Total Spent"]

df[unknown_price] = df[unknown_price].replace(["nan", "NaN", "UNKNOWN", "ERROR"], pd.NA)

df = df.dropna(subset=unknown_price, how='all') #drops all rows where ALL SPECIFIED rows in unknown_price are NA


price_to_item = {} #below it loops through the item and price in itemAndPricePerU hashmap and if the price isn't in the price_to_item hashmap then add it and put the corresponding item that matches that price
for item, price in itemAndPricePerU.items():
    if price not in price_to_item:
        price_to_item[price] = item

df["Item"] = df["Item"].fillna(df["Price Per Unit"].map(price_to_item))

df = df.dropna(subset=["Quantity", "Total Spent"], how="all")


print(df)
print(df.info())
print("\n MISSING VALUES")
print(df.isnull().sum())
print(df[df[["Quantity", "Total Spent"]].isna().any(axis=1)])
df.to_csv("cleaned_cafe_sales.csv", index=False)