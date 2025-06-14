from scipy.stats import kruskal
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("users_analysis_cleaned.csv")
df["difference"] = df["commits_after"] - df["commits_before"]

df["bio"] = df["bio"].fillna("").astype(str).str.lower()

keywords = [
    "disabled", "blind", "visually impaired", "deaf", "neurodivergent",
    "autistic", "adhd", "chronic illness", "mobility aid"
]

for keyword in keywords:
    df[keyword] = df["bio"].str.contains(keyword, na=False)

df["match"] = ""
for keyword in keywords:
    mask = (df["match"] == "") & df["bio"].str.contains(keyword, na=False)
    df.loc[mask, "match"] = keyword

group = [df[df["match"] == keyword]["difference"].dropna() for keyword in keywords]
statistic, p_value = kruskal(*group)
print(f"Kruskal-Wallis statistic: {statistic}")
print(f"Kruskal-Wallis p-value: {p_value}")
if p_value < 0.05:
    print("Reject the null hypothesis: there is a significant difference in commits.")
else:
    print("Fail to reject the null hypothesis.")

summary = df.groupby("match")["difference"].aggregate(['count', 'mean', 'std']).sort_values(by="mean")
print (summary)

group_mean = df.groupby("match")["difference"].mean().sort_values()
group_mean.plot(kind='bar', color='cornflowerblue', figsize=(10,6))
plt.title("Mean Difference in Commits by Disability Group")
plt.ylabel("Mean Difference in Commits")
plt.axhline(0, color='black', linestyle='--', linewidth=0.8)
plt.tight_layout()
plt.savefig("commits_disability_with_outliers.png")
plt.show()