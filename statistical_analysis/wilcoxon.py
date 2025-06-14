import pandas as pd
from scipy.stats import wilcoxon

df = pd.read_csv("users_analysis_cleaned.csv")
df["difference"] = df["commits_after"] - df["commits_before"]

df_drop_zeros = df[df["difference"] != 0]

statistic, p_value = wilcoxon(
    df_drop_zeros["commits_after"],
    df_drop_zeros["commits_before"])

print(f"Wilcoxon statistic: {statistic}")
print(f"Wilcoxon p-value: {p_value}")

if p_value < 0.05:
    print("Reject the null hypothesis: there is no significant difference in commits.")
else:
    print("Fail to reject the null hypothesis.")