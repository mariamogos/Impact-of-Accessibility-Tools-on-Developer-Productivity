import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import shapiro, probplot, normaltest

df = pd.read_csv("users_no_outliers.csv")
df["difference"] = df["commits_after"] - df["commits_before"]

plt.figure(figsize=(10, 6))
probplot(df["difference"], dist="norm", plot=plt)
plt.title("Q-Q Plot of Differences")
plt.tight_layout()
plt.savefig("qq_no_outliers.png")
plt.show()


shapiro_stat, shapiro_test = shapiro(df["difference"])
print(f"Shapiro-Wilk Test Statistic W: {shapiro_stat}, p-value: {shapiro_test}")
if shapiro_test > 0.05:
    print("The data is normally distributed (fail to reject H0)")
else:
    print("The data is not normally distributed (reject H0)")

dagostino_stat, dagostino_test = normaltest(df["difference"])
print(f"D'Agostino's K-squared Test Statistic: {dagostino_stat}, p-value: {dagostino_test}")
if dagostino_test > 0.05:
    print("The data is normally distributed (fail to reject H0)")
else:
    print("The data is not normally distributed (reject H0)")