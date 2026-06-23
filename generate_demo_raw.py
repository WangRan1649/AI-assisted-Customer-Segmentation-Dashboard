from pathlib import Path
import random
import shutil
import pandas as pd

random.seed(20260622)

raw_path = Path("data/raw/ecommerce_user_behavior_dataset.csv")
backup_dir = Path("_flow_test_backup")
backup_dir.mkdir(exist_ok=True)

auto_backup_path = backup_dir / "raw_before_generated_demo.csv"
if not auto_backup_path.exists():
    shutil.copy2(raw_path, auto_backup_path)

df = pd.read_csv(raw_path, encoding="gbk")
description_row = df.iloc[[0]].copy()
columns = list(df.columns)

rows = []
user_id = 1

def add_user(
    age,
    gender,
    location,
    income,
    interests,
    last_login_days,
    purchase_frequency,
    average_order_value,
    category,
    time_spent,
    pages_viewed,
    subscribed,
):
    global user_id
    total_spending = round(purchase_frequency * average_order_value, 2)

    rows.append({
        "User_ID": f"#DEMO{user_id:04d}",
        "Age": age,
        "Gender": gender,
        "Location": location,
        "Income": income,
        "Interests": interests,
        "Last_Login_Days_Ago": last_login_days,
        "Purchase_Frequency": purchase_frequency,
        "Average_Order_Value": round(average_order_value, 2),
        "Total_Spending": total_spending,
        "Product_Category_Preference": category,
        "Time_Spent_on_Site_Minutes": time_spent,
        "Pages_Viewed": pages_viewed,
        "Newsletter_Subscription": "TRUE" if subscribed else "FALSE",
    })
    user_id += 1

# 1. Female age-51 Apparel VIP users: high spending, recent activity, high frequency
for _ in range(330):
    add_user(
        age=random.choice([49, 50, 51, 52, 53]),
        gender="Female",
        location=random.choice(["Urban", "Suburban"]),
        income=random.randint(180000, 360000),
        interests=random.choice(["Fashion", "Luxury", "Lifestyle"]),
        last_login_days=random.randint(1, 5),
        purchase_frequency=random.randint(9, 15),
        average_order_value=random.uniform(1300, 2300),
        category="Apparel",
        time_spent=random.randint(45, 100),
        pages_viewed=random.randint(25, 75),
        subscribed=True,
    )

# 2. Home & Kitchen churn-risk users: high historical spending, inactive recently
for _ in range(270):
    add_user(
        age=random.randint(35, 58),
        gender=random.choice(["Female", "Male"]),
        location=random.choice(["Suburban", "Rural"]),
        income=random.randint(120000, 280000),
        interests=random.choice(["Home improvement", "Family", "Furniture"]),
        last_login_days=random.randint(60, 130),
        purchase_frequency=random.randint(6, 11),
        average_order_value=random.uniform(900, 1500),
        category="Home & Kitchen",
        time_spent=random.randint(10, 35),
        pages_viewed=random.randint(5, 22),
        subscribed=random.choice([True, False]),
    )

# 3. Electronics potential users: low frequency, high AOV, recent activity
for _ in range(240):
    add_user(
        age=random.randint(24, 40),
        gender=random.choice(["Male", "Female"]),
        location=random.choice(["Urban", "Suburban"]),
        income=random.randint(90000, 220000),
        interests=random.choice(["Technology", "Gaming", "Digital products"]),
        last_login_days=random.randint(2, 14),
        purchase_frequency=random.randint(1, 3),
        average_order_value=random.uniform(1100, 2100),
        category="Electronics",
        time_spent=random.randint(30, 80),
        pages_viewed=random.randint(18, 55),
        subscribed=random.choice([True, False]),
    )

# 4. Books long-tail users: low value, low frequency
for _ in range(160):
    add_user(
        age=random.randint(18, 65),
        gender=random.choice(["Male", "Female"]),
        location=random.choice(["Rural", "Suburban", "Urban"]),
        income=random.randint(30000, 120000),
        interests=random.choice(["Reading", "Education", "Self-learning"]),
        last_login_days=random.randint(20, 90),
        purchase_frequency=random.randint(1, 2),
        average_order_value=random.uniform(80, 260),
        category="Books",
        time_spent=random.randint(5, 30),
        pages_viewed=random.randint(3, 18),
        subscribed=random.choice([True, False]),
    )

demo_df = pd.concat(
    [description_row, pd.DataFrame(rows, columns=columns)],
    ignore_index=True,
)

demo_df.to_csv(raw_path, index=False, encoding="gbk")

business_df = demo_df.iloc[1:].copy()

print("Demo raw dataset generated successfully.")
print("Output:", raw_path)
print("Rows including description row:", len(demo_df))
print("Business rows:", len(business_df))
print()
print("Category distribution:")
print(business_df["Product_Category_Preference"].value_counts())
print()
print("Gender + category distribution:")
print(
    business_df.groupby(["Gender", "Product_Category_Preference"])
    .size()
    .sort_values(ascending=False)
    .head(10)
)