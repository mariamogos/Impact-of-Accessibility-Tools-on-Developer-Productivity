import pandas as pd

df = pd.read_csv("users_no_outliers.csv")
df["difference"] = df["commits_after"] - df["commits_before"]

p = sum(df["difference"] > 0)
n = sum(df["difference"] < 0)

rank = (p - n) / (p + n)
print(f"Rank: {rank}")