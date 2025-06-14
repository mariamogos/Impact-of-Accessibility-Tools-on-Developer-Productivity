#this script removes outliers and creates a boxplot of the commits before and after
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("users_analysis_cleaned.csv")
columns = ["commits_before", "commits_after"]

plt.figure(figsize=(10,6))
df[columns].boxplot()
plt.title("Boxplot of Commits Before and After")
plt.ylabel("Number of Commits")
plt.grid(True)
plt.tight_layout()
plt.savefig("boxplot_commits.png")
plt.show()

#iqr treshold
def filter(columns):
    q1 = df[columns].quantile(0.25)
    q3 = df[columns].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    print(f"\n{columns.upper()}")
    print(f"Q1 (25%): {q1}")
    print(f"Q3 (75%): {q3}")
    print(f"IQR: {iqr}")
    print(f"Lower Bound: {lower_bound}")
    print(f"Upper Bound: {upper_bound}")
    outliers = df[(df[columns] > upper_bound)]
    print(f"Number of outliers: {len(outliers)}")
    return (df[columns] <= upper_bound)

mask_before = filter("commits_before")
mask_after = filter("commits_after")

outlier_b = df[~mask_before]
outlier_a = df[~mask_after]
overlap = outlier_b.index.intersection(outlier_a.index)
print(f"Overlapping outliers: {len(overlap)}")
df_no_outliers = df[mask_before & mask_after]
df_no_outliers.to_csv("users_no_outliers.csv", index=False)