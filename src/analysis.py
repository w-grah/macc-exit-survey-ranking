import pandas as pd
import matplotlib.pyplot as plt
import os

# Ensure outputs folder exists
os.makedirs("outputs", exist_ok=True)

# Load dataset
file_path = "data/exit_survey_2024.xlsx"
df = pd.read_excel(file_path)

# -----------------------------
# CLEANING + RESHAPING SECTION
# -----------------------------

# Select numeric columns (assumes ratings are numeric)
rating_columns = df.select_dtypes(include=["number"]).columns

if len(rating_columns) == 0:
    raise ValueError("No numeric rating columns detected in dataset.")

# Calculate average rating per column
averages = df[rating_columns].mean().sort_values(ascending=False)

# Convert to DataFrame
ranking_df = averages.reset_index()
ranking_df.columns = ["Program_or_Course", "Average_Rating"]

# Add rank column
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

