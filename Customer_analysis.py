import numpy as np
import pandas as pd

raw_data = pd.read_csv('Data/Raw_data.csv')
# print(raw_data.head())

df = pd.read_csv('Data/2_Customer_Feedback_encode.csv')
# print(data.head())

# Count of repeated customer
repeated_customer = df['Customer ID'].value_counts()
repeated_customer = repeated_customer[repeated_customer > 1].reset_index()
repeated_customer.columns = ['Customer ID', 'Count']
print(repeated_customer)

# writing new csv consiting only repeated customer count
repeated_customer.to_csv('Data/3_Repeated_customer_count.csv', index = False)

# Gathering Data to do customer analysis
newdata = pd.read_csv('Data/3_Repeated_Customer_Count.csv')
print(newdata.head())

## 2. what average rating each customer give?
avg_rating = df.groupby('Customer ID')['Service Rating'].mean().reset_index()
avg_rating.columns = ['Customer ID', 'Average Rating']
newdata = pd.merge(newdata, avg_rating, on="Customer ID")
print(newdata.head())

# 3. What is average divery time per customer?
# That can help to know about the pattern of customer repeatation.
avg_delivery_time = df.groupby('Customer ID')['Delivery Time (Minutes)'].mean().reset_index()
avg_delivery_time.columns = ['Customer ID', 'Average Delivery Time']
print(avg_delivery_time)
newdata = pd.merge(newdata, avg_delivery_time, on="Customer ID")

# 4. Is there delivery delay exist most time?
# That can help to know reason about less repeated customer
def get_mode(series):
    return series.mode().iloc[0]

delivery_delay = df.groupby('Customer ID')['Delivery Delay'].apply(get_mode).reset_index()
delivery_delay.columns = ['Customer ID', 'Delivery Delay Mode']
print(delivery_delay)
newdata = pd.merge(newdata, delivery_delay, on = "Customer ID")

# 5. Most time Refund requested are give from customer
refund_request = df.groupby('Customer ID')['Refund Requested'].apply(get_mode).reset_index()
refund_request.columns = ['Customer ID', 'Refund Requested Mode']
print(refund_request)
newdata = pd.merge(newdata, refund_request, on="Customer ID")

# 6. Average Order Value from each customer
avg_order_value = df.groupby('Customer ID')['Order Value (INR)'].mean().reset_index()
avg_order_value.columns = ["Customer ID", "Avg Order Value"]
print(avg_order_value)
newdata = pd.merge(newdata, avg_order_value, on = "Customer ID")

# Step 1: Pop the last column (removes it and returns it)
last_col = newdata.pop(newdata.columns[-1])

# Step 2: Insert it at position 2 (which is the third column, index is 0-based)
newdata.insert(2, last_col.name, last_col)

# 7. From which platform Customer order most?
platform_count = df.groupby('Customer ID')['Platform'].apply(get_mode).reset_index()
platform_count.columns = ['Customer ID', 'Platform Mode']
newdata = pd.merge(newdata, platform_count, on="Customer ID")

# 8. Which category Customer order most?
product_category_count = df.groupby('Customer ID')['Product Category'].apply(get_mode).reset_index()
product_category_count.columns = ['Customer ID', 'Product Category Mode']
newdata = pd.merge(newdata, product_category_count, on="Customer ID")

print(newdata.head())
print(newdata.shape)
newdata.to_csv('Data/4_Customer_Analysis.csv', index = False)