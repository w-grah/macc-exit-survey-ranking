import pandas as pd
import matplotlib.pyplot as plt
import os

# -----------------------------
# 1. Load Dataset (Skip ImportId Row)
# -----------------------------
file_path = "data/exit_survey_2023.xlsx"

# Skip the second row (ImportId row)
df = pd.read_excel(file_path, skiprows=[1])

# -----------------------------
# 2. Keep ONLY Ranking Columns
# -----------------------------
rank_columns = [col for col in df.columns if " - Rank" in col]

if not rank_columns:
    raise ValueError("No ranking columns found in dataset.")

ranking_data = df[rank_columns]

# Convert to numeric safely
ranking_data = ranking_data.apply(pd.to_numeric, errors="coerce")

# Drop columns that are entirely empty
ranking_data = ranking_data.dropna(axis=1, how="all")

# -----------------------------
# 3. Clean Column Names
# -----------------------------
clean_names = []
for col in ranking_data.columns:
    # Extract course name between last dash and " - Rank"
    parts = col.split(" - ")
    if len(parts) >= 2:
        clean_names.append(parts[-2])
    else:
        clean_names.append(col)

ranking_data.columns = clean_names

# -----------------------------
# 4. Calculate Average Ranking
# -----------------------------
ranking_df = ranking_data.mean().reset_index()
ranking_df.columns = ["Course", "Average Rank"]

ranking_df = ranking_df.sort_values("Average Rank")

# -----------------------------
# 5. Ensure outputs folder exists
# -----------------------------
os.makedirs("outputs", exist_ok=True)

# -----------------------------
# 6. Save CSV
# -----------------------------
ranking_df.to_csv("outputs/rank_order.csv", index=False)

# -----------------------------
# 7. Create Chart
# -----------------------------
plt.figure()
plt.barh(ranking_df["Course"], ranking_df["Average Rank"])
plt.xlabel("Average Rank")
plt.title("MAcc Course Rankings")
plt.gca().invert_yaxis()
plt.tight_layout()

plt.savefig("outputs/rank_order.png")
plt.close()

print("Analysis complete. Files saved to outputs folder.")
