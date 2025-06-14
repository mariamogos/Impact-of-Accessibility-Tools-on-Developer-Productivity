import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("users_no_outliers.csv")
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
df = df.dropna(subset = ["match"])

change = df.groupby("match")["difference"].mean().sort_values()

mean = df["difference"].mean()
print(f"Overall mean difference: {mean}")

plt.figure(figsize=(10, 6))
change.plot(kind="barh", color='lightblue', edgecolor='black', alpha=0.7)
plt.title("Average Difference in Commits by Disability")
plt.xlabel("Average Difference in Commits")
plt.ylabel("Disability Group")
plt.tight_layout()
plt.savefig("barchart_with_outliers.png")
plt.show()