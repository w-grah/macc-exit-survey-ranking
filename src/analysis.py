import pandas as pd
import matplotlib.pyplot as plt
import os

# -----------------------------
# 1. Load Dataset
# -----------------------------
file_path = "data/exit_survey_2023.xlsx"

df = pd.read_excel(file_path)

# -----------------------------
# 2. Keep Only Numeric Columns
# -----------------------------
numeric_df = df.select_dtypes(include="number")

if numeric_df.empty:
    raise ValueError("No numeric rating columns detected in dataset.")

# Drop rows that are completely empty
numeric_df = numeric_df.dropna(how="all")

# -----------------------------
# 3. Calculate Average Rankings
# -----------------------------
ranking_df = numeric_df.mean().reset_index()
ranking_df.columns = ["Category", "Average Score"]

# Lower score = better rank (if 1 = best)
ranking_df = ranking_df.sort_values("Average Score")

# -----------------------------
# 4. Ensure outputs folder exists
# -----------------------------
os.makedirs("outputs", exist_ok=True)

# -----------------------------
# 5. Save CSV
# -----------------------------
ranking_df.to_csv("outputs/rank_order.csv", index=False)

# -----------------------------
# 6. Create Bar Chart
# -----------------------------
plt.figure()
plt.barh(ranking_df["Category"], ranking_df["Average Score"])
plt.xlabel("Average Ranking")
plt.ylabel("Category")
plt.title("Exit Survey Ranking Results")
plt.gca().invert_yaxis()  # Best ranking at top
plt.tight_layout()

plt.savefig("outputs/rank_order.png")
plt.close()

print("Analysis complete. Files saved to outputs folder.")
