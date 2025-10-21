import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# ------------------------------
# 1. Load the dataset
# ------------------------------
df = pd.read_csv("data/processed/videos_processed_with_views_per_month.csv")


# ------------------------------
# 2. Convert duration_readable (HH:MM:SS) to numeric minutes
# ------------------------------
def duration_to_minutes(duration_str):
    """
    Converts a string in HH:MM:SS or MM:SS format to total minutes.
    Returns NaN if it cannot be parsed.
    """
    try:
        parts = duration_str.split(':')
        if len(parts) == 3:
            h, m, s = map(int, parts)
            return h * 60 + m + s / 60
        elif len(parts) == 2:
            m, s = map(int, parts)
            return m + s / 60
        else:
            return np.nan
    except Exception:
        return np.nan


# ------------------------------
# 3. Ensure views column exists and is numeric
# ------------------------------
views_col = "views_por_mes"  # adjust if your CSV uses a different name
if views_col not in df.columns:
    raise ValueError(f"CSV missing '{views_col}' column")

# Convert to numeric (remove commas or bad strings)
df[views_col] = pd.to_numeric(df[views_col].astype(str).str.replace(",", ""), errors="coerce")

# ------------------------------
# 4. Drop rows with invalid durations or views
# ------------------------------
df_clean = df.dropna(subset=["duration_minutes", views_col])

if df_clean.empty:
    raise ValueError("No valid data left after preprocessing. Check your CSV!")

print(f"Number of valid rows for fitting: {len(df_clean)}")
print(df_clean[["duration_readable", "duration_minutes", views_col]].head())

# -------
# 4a. testing
# --------

print("First 10 numeric durations:")
print(df_clean[["duration_readable", "duration_minutes"]].head(10))


# ------------------------------
# 5. Prepare data for fitting
# ------------------------------
x = df_clean["duration_minutes"].values
y = df_clean[views_col].values

# ------------------------------
# 6. Define the rational function model
# ------------------------------
def rational_func(x, a, b, c):
    return (a + b*x) / (1 + c*x)

# ------------------------------
# 7. Fit the model
# ------------------------------
popt, _ = curve_fit(rational_func, x, y, p0=[1, 1, 0.1])
a, b, c = popt

# ------------------------------
# 8. Compute R²
# ------------------------------
y_pred = rational_func(x, *popt)
ss_res = np.sum((y - y_pred)**2)
ss_tot = np.sum((y - np.mean(y))**2)
r2 = 1 - (ss_res / ss_tot)

print("\nRational Regression Results")
print("----------------------------")
print(f"a = {a:.4f}")
print(f"b = {b:.4f}")
print(f"c = {c:.4f}")
print(f"R² = {r2:.4f}")

# ------------------------------
# 9. Plot data and fitted curve
# ------------------------------
plt.figure(figsize=(8, 5))
plt.scatter(x, y, color="blue", label="Data", alpha=0.7)
plt.plot(np.sort(x), rational_func(np.sort(x), *popt), color="red", label=f"Rational fit (R²={r2:.3f})")
plt.xlabel("Video duration (minutes)")
plt.ylabel("Views per month")
plt.title("Rational Regression: Views vs. Duration")
plt.legend()
plt.tight_layout()
plt.show()
