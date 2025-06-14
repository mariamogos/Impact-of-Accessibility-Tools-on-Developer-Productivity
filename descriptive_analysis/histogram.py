import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("users_analysis_cleaned.csv")
df["difference"] = df["commits_after"] - df["commits_before"]

df = df.sort_values(by=["commits_before", "commits_after", "difference"], ascending=True)

plt.figure(figsize=(10, 6))

plt.subplot(1, 3, 1)
plt.hist(df["commits_before"], bins=30, color='moccasin', edgecolor = 'black', alpha=0.7)
plt.title("Commits Before")
plt.xlabel("Number of Commits")
plt.ylabel("No. of Users")

plt.subplot(1, 3, 2)
plt.hist(df["commits_after"], bins=30, color='pink', edgecolor = 'black', alpha=0.7)
plt.title("Commits After")
plt.xlabel("Number of Commits")
plt.ylabel("No. of Users")

plt.subplot(1, 3, 3)
plt.hist(df["difference"], bins=30, color='paleturquoise', edgecolor = 'black', alpha=0.7)
plt.title("After - Before")
plt.xlabel("Difference in Commits")
plt.ylabel("No. of Users")

plt.tight_layout()
plt.savefig("histogram_with_outliers.png")
plt.show()