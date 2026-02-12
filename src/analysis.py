import pandas as pd
import matplotlib.pyplot as plt
import os

# Ensure outputs folder exists
os.makedirs("outputs", exist_ok=True)

# Load dataset
file_path = "data/exit_survey_2024.xlsx"
df = pd.read_excel(file_path)

# -----------------------------
# CLEANING STEP
# -----------------------------

# Try converting all columns to numeric where possible
df_numeric = df.apply(pd.to_numeric, errors="coerce")

# Drop columns that are entirely NaN after conversion
df_numeric = df_numeric.dropna(axis=1, how="all")

if df_numeric.shape[1] == 0:
    raise ValueError("No convertible numeric columns found in dataset.")

# -----------------------------
# CREATE RANKING
# -----------------------------

averages = df_numeric.mean().sort_values(ascending=False)

ranking_df = averages.reset_index()
ranking_df.columns = ["Program_or_Course", "Average_Rating"]

ranking_df["Rank"] = range(1, len(ranking_df) + 1)

# -----------------------------
# SAVE OUTPUTS
# -----------------------------

ranking_df.to_csv("outputs/rank_order.csv", index=False)

# -----------------------------
# CREATE FIGURE
# -----------------------------

plt.figure(figsize=(8, 6))
plt.barh(ranking_df["Program_or_Course"], ranking_df["Average_Rating"])
plt.gca().invert_yaxis()
plt.xlabel("Average Rating")
plt.title("Rank Order of Programs/Courses - 2024")
plt.tight_layout()
plt.savefig("outputs/rank_order.png")
plt.close()

print("Analysis complete.")
