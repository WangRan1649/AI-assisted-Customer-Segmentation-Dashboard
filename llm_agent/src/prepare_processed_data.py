from pathlib import Path

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[2]

RAW_FILE = ROOT_DIR / "data" / "raw" / "ecommerce_user_behavior_dataset.csv"

CUSTOMER_SEGMENTS_FILE = ROOT_DIR / "data" / "processed" / "customer_segments.csv"
CROSS_INSIGHTS_FILE = ROOT_DIR / "data" / "processed" / "cross_dimensional_insights.csv"


NUMERIC_COLUMNS = [
    "Age",
    "Income",
    "Last_Login_Days_Ago",
    "Purchase_Frequency",
    "Average_Order_Value",
    "Total_Spending",
    "Time_Spent_on_Site_Minutes",
    "Pages_Viewed",
]


def load_raw_data() -> pd.DataFrame:
    """
    Load raw e-commerce user behavior data.

    The uploaded CSV uses GBK encoding and contains one description row
    under the header. This function removes that description row automatically.
    """

    df = pd.read_csv(RAW_FILE, encoding="gbk")

    # Remove the description row if User_ID is not an actual user ID.
    # In this dataset, real user IDs look like "#1", "#2", etc.
    df = df[df["User_ID"].astype(str).str.startswith("#")].copy()

    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["User_ID", "Purchase_Frequency", "Total_Spending"])

    return df


def assign_customer_segment(row: pd.Series) -> str:
    """
    Assign customer segment based on user-level behavior data.

    Current data granularity:
    - One row represents one user.
    - There is no raw OrderID.
    - Therefore, segmentation is based on user-level fields:
      Purchase_Frequency, Total_Spending, Last_Login_Days_Ago.
    """

    frequency = row["Purchase_Frequency"]
    spending = row["Total_Spending"]
    last_login = row["Last_Login_Days_Ago"]

    if last_login >= 20 and spending >= 2500:
        return "Churn-risk Customers"

    if frequency >= 5 and spending >= 2500:
        return "High-value Customers"

    if frequency <= 4 and spending >= 1000:
        return "Potential Customers"

    if frequency >= 5 and spending < 2500:
        return "Regular Retained Customers"

    return "Other Customers"


def weighted_aov(total_spending: float, purchase_frequency: float) -> float:
    """Calculate weighted AOV from user-level aggregated data."""

    if purchase_frequency == 0:
        return 0

    return total_spending / purchase_frequency


def summarize_segments(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate customer_segments.csv automatically from raw user-level data.
    """

    df["customer_segment"] = df.apply(assign_customer_segment, axis=1)

    total_users = df["User_ID"].nunique()

    segment_summary = (
        df.groupby("customer_segment")
        .agg(
            customer_count=("User_ID", "nunique"),
            total_spending=("Total_Spending", "sum"),
            total_purchase_frequency=("Purchase_Frequency", "sum"),
            avg_frequency=("Purchase_Frequency", "mean"),
            avg_total_spending=("Total_Spending", "mean"),
        )
        .reset_index()
    )

    segment_summary["share"] = (
        segment_summary["customer_count"] / total_users * 100
    ).round(1).astype(str) + "%"

    segment_summary["weighted_aov"] = segment_summary.apply(
        lambda row: weighted_aov(
            row["total_spending"],
            row["total_purchase_frequency"],
        ),
        axis=1,
    ).round(2)

    preference = (
        df.groupby(["customer_segment", "Product_Category_Preference"])
        .size()
        .reset_index(name="count")
        .sort_values(["customer_segment", "count"], ascending=[True, False])
        .drop_duplicates("customer_segment")
        .rename(columns={"Product_Category_Preference": "category_preference"})
    )

    segment_summary = segment_summary.merge(
        preference[["customer_segment", "category_preference"]],
        on="customer_segment",
        how="left",
    )

    role_mapping = {
        "High-value Customers": "Core profit engine",
        "Potential Customers": "Growth engine",
        "Churn-risk Customers": "Dormant premium assets",
        "Regular Retained Customers": "Traffic foundation",
        "Other Customers": "Long-tail users",
    }

    issue_mapping = {
        "High-value Customers": "Need loyalty protection and VIP retention",
        "Potential Customers": "Large base but low repurchase frequency",
        "Churn-risk Customers": "High historical spending but low recent engagement",
        "Regular Retained Customers": "Frequent buyers with relatively lower spending",
        "Other Customers": "Low engagement and limited short-term value",
    }

    priority_mapping = {
        "High-value Customers": "Stabilize",
        "Potential Customers": "Convert",
        "Churn-risk Customers": "Recover",
        "Regular Retained Customers": "Upsell",
        "Other Customers": "Nurture",
    }

    segment_summary["business_role"] = segment_summary["customer_segment"].map(role_mapping)
    segment_summary["key_issue"] = segment_summary["customer_segment"].map(issue_mapping)
    segment_summary["action_priority"] = segment_summary["customer_segment"].map(priority_mapping)

    segment_summary["frequency_range"] = segment_summary["avg_frequency"].round(2).astype(str)
    segment_summary["monetary_range"] = (
        "Avg total spending ¥" + segment_summary["avg_total_spending"].round(2).astype(str)
    )

    output = segment_summary.rename(columns={"customer_segment": "segment"})[
        [
            "segment",
            "share",
            "customer_count",
            "business_role",
            "frequency_range",
            "monetary_range",
            "weighted_aov",
            "category_preference",
            "key_issue",
            "action_priority",
        ]
    ]

    segment_order = [
        "High-value Customers",
        "Potential Customers",
        "Churn-risk Customers",
        "Regular Retained Customers",
        "Other Customers",
    ]

    output["segment"] = pd.Categorical(output["segment"], categories=segment_order, ordered=True)
    output = output.sort_values("segment")

    return output


def build_cross_dimensional_insights(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate cross_dimensional_insights.csv automatically.

    These insights are generated from the raw data instead of being manually written.
    """

    # 1. Age + Gender + Weighted AOV insight
    age_gender = (
        df.groupby(["Age", "Gender"])
        .agg(
            customer_count=("User_ID", "nunique"),
            total_spending=("Total_Spending", "sum"),
            total_purchase_frequency=("Purchase_Frequency", "sum"),
        )
        .reset_index()
    )

    age_gender["weighted_aov"] = age_gender.apply(
        lambda row: weighted_aov(row["total_spending"], row["total_purchase_frequency"]),
        axis=1,
    )

    # Avoid selecting tiny groups by requiring at least 5 users
    age_gender_valid = age_gender[age_gender["customer_count"] >= 5].copy()
    elite_row = age_gender_valid.sort_values(
        ["weighted_aov", "customer_count"],
        ascending=False,
    ).iloc[0]

    # 2. Region + Category insight
    region_category = (
        df.groupby(["Location", "Product_Category_Preference"])
        .agg(
            customer_count=("User_ID", "nunique"),
            total_spending=("Total_Spending", "sum"),
            total_purchase_frequency=("Purchase_Frequency", "sum"),
        )
        .reset_index()
    )

    region_category["weighted_aov"] = region_category.apply(
        lambda row: weighted_aov(row["total_spending"], row["total_purchase_frequency"]),
        axis=1,
    )

    region_category_valid = region_category[region_category["customer_count"] >= 10].copy()
    best_region_category = region_category_valid.sort_values(
        ["weighted_aov", "customer_count"],
        ascending=False,
    ).iloc[0]

    # 3. Pareto-style value concentration
    user_value = df[["User_ID", "Total_Spending"]].copy()
    user_value = user_value.sort_values("Total_Spending", ascending=False)
    top_10_count = max(1, int(len(user_value) * 0.1))

    top_10_spending = user_value.head(top_10_count)["Total_Spending"].sum()
    total_spending = user_value["Total_Spending"].sum()
    top_10_share = round(top_10_spending / total_spending * 100, 1)

    # 4. Churn recovery insight
    churn_users = df[
        (df["Last_Login_Days_Ago"] >= 20)
        & (df["Total_Spending"] >= 2500)
    ]

    churn_share = round(len(churn_users) / len(df) * 100, 1)

    if not churn_users.empty:
        churn_top_category = (
            churn_users["Product_Category_Preference"]
            .value_counts()
            .idxmax()
        )
    else:
        churn_top_category = "N/A"

    rows = [
        {
            "insight_name": "Elite Customer Segment",
            "dimension": "Age + Gender + Weighted AOV",
            "key_finding": (
                f"{elite_row['Gender']} customers around age {int(elite_row['Age'])} "
                f"show the highest weighted AOV among groups with sufficient sample size."
            ),
            "business_meaning": "This group should be treated as a priority profit-driving segment.",
            "recommended_action": "Design premium product campaigns, expert review content, and VIP service benefits for this segment.",
        },
        {
            "insight_name": "Regional Category Opportunity",
            "dimension": "Location + Product Category + Weighted AOV",
            "key_finding": (
                f"{best_region_category['Location']} customers in the "
                f"{best_region_category['Product_Category_Preference']} category show strong weighted AOV performance."
            ),
            "business_meaning": "Regional category preference can reveal underexplored market opportunities.",
            "recommended_action": "Create region-specific product bundles and content campaigns based on category preference.",
        },
        {
            "insight_name": "Pareto Value Concentration",
            "dimension": "Customer Value Contribution",
            "key_finding": f"The top 10% users contribute approximately {top_10_share}% of total spending.",
            "business_meaning": "Revenue is concentrated among higher-value customers.",
            "recommended_action": "Prioritize retention and service resources for top-value users.",
        },
        {
            "insight_name": "Churn Recovery",
            "dimension": "Last Login + Total Spending + Category Preference",
            "key_finding": (
                f"{churn_share}% of users are high-spending but inactive, "
                f"with strongest preference in {churn_top_category}."
            ),
            "business_meaning": "These users should be treated as dormant premium assets rather than low-value inactive users.",
            "recommended_action": "Build win-back campaigns with product upgrade reminders, after-sales recovery, and service follow-up.",
        },
    ]

    return pd.DataFrame(rows)


def main() -> None:
    print("Loading raw e-commerce user behavior data...")
    df = load_raw_data()

    print("Generating customer_segments.csv...")
    customer_segments = summarize_segments(df)
    CUSTOMER_SEGMENTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    customer_segments.to_csv(CUSTOMER_SEGMENTS_FILE, index=False, encoding="utf-8-sig")

    print("Generating cross_dimensional_insights.csv...")
    cross_insights = build_cross_dimensional_insights(df)
    CROSS_INSIGHTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    cross_insights.to_csv(CROSS_INSIGHTS_FILE, index=False, encoding="utf-8-sig")

    print(f"Done. Saved to: {CUSTOMER_SEGMENTS_FILE}")
    print(f"Done. Saved to: {CROSS_INSIGHTS_FILE}")


if __name__ == "__main__":
    main()