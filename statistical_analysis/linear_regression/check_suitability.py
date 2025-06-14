import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("users_no_outliers.csv")
df["difference"] = df["commits_after"] - df["commits_before"]

keywords = [
    "disabled", "blind", "visually impaired", "deaf", "neurodivergent",
    "autistic", "adhd", "chronic illness", "mobility aid"
]

features = ["commits_before", "commits_after"] + keywords
data = df[features + ["difference"]].dropna()

sns.pairplot(data[["commits_before", "commits_after", "difference"]])
plt.suptitle("Linear Regression Assumptions", y=1.02)
plt.tight_layout()
plt.savefig("linear_regression_assumptions_without_outliers.png")
plt.show()

#multicollinearity
X = data[features]
X_scaled = StandardScaler().fit_transform(X)
vif = pd.DataFrame()
vif["VIF"] = [variance_inflation_factor(X_scaled, i) for i in range(X_scaled.shape[1])]
vif["features"] = features
print(vif)

print(data.describe())