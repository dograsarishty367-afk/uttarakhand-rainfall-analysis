import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

os.makedirs("outputs", exist_ok=True)


# -------------------------------
# 1. Start Program
# -------------------------------

print("Rainfall Pattern Analyzer for Landslide Risk\n")

# -------------------------------
# 2. Load Dataset
# -------------------------------

data = pd.read_csv("data/rainfall_uttarakhand.csv")
print("Dataset loaded successfully!\n")

# -------------------------------
# 3. Preview Dataset
# -------------------------------

print("First 5 rows of the dataset:\n")
print(data.head())

# -------------------------------
# 4. Select Monthly Rainfall Columns
# -------------------------------

months = [
    "JAN","FEB","MAR","APR","MAY","JUN",
    "JUL","AUG","SEP","OCT","NOV","DEC"
]

rainfall = data.set_index("Year")[months]

# -------------------------------
# 5. Calculate Average Rainfall
# -------------------------------

monthly_avg = rainfall.mean()

print("\nAverage Monthly Rainfall (mm):\n")
print(monthly_avg)

# -------------------------------
# 6. Detect Extreme Rainfall Events
# -------------------------------

threshold = 200

extreme_events = (rainfall > threshold).sum()

print("\nExtreme Rainfall Events (>200 mm):\n")
print(extreme_events)

# -------------------------------
# 7. Landslide Risk Classification
# -------------------------------

def landslide_risk(value):

    if value > 300:
        return "High Risk"

    elif value > 150:
        return "Moderate Risk"

    else:
        return "Low Risk"


risk_levels = monthly_avg.apply(landslide_risk)

print("\nEstimated Landslide Risk by Month:\n")
print(risk_levels)

# -------------------------------
# 8. Detect Extreme Rainfall Years
# -------------------------------

data["Total_Rainfall"] = rainfall.sum(axis=1)

top_years = data[["Year", "Total_Rainfall"]].sort_values(
    by="Total_Rainfall",
    ascending=False
).head(10)

print("\nTop 10 Extreme Rainfall Years:\n")
print(top_years)

# -------------------------------
# Visualizations
# -------------------------------

fig, axes = plt.subplots(2, 1, figsize=(10,10))

# Bar chart
monthly_avg.plot(kind="bar", ax=axes[0])
axes[0].set_title("Average Monthly Rainfall - Uttarakhand")
axes[0].set_xlabel("Month")
axes[0].set_ylabel("Rainfall (mm)")

# Heatmap
sns.heatmap(
    rainfall,
    cmap="Blues",
    cbar_kws={"label": "Rainfall (mm)"},
    ax=axes[1]
)

axes[1].set_title("Rainfall Heatmap - Uttarakhand")
axes[1].set_xlabel("Month")
axes[1].set_ylabel("Year")

plt.tight_layout()
plt.savefig("outputs/rainfall_visualizations.png")
