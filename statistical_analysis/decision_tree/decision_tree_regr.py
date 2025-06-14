import pandas as pd
from sklearn.tree import DecisionTreeRegressor, plot_tree
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder

df = pd.read_csv("users_analysis_cleaned.csv")
df["difference"] = df["commits_after"] - df["commits_before"]

keywords = [
    "disabled", "blind", "visually impaired", "deaf", "neurodivergent",
    "autistic", "adhd", "chronic illness", "mobility aid"
]
df["bio"] = df["bio"].fillna("").astype(str).str.lower()
df["match"] = ""
for keyword in keywords:
    mask = (df["match"] == "") & df["bio"].str.contains(keyword, na=False)
    df.loc[mask, "match"] = keyword
df = df[df["match"] != ""]

#one-hot encoding
ohe = OneHotEncoder(sparse_output=False, drop='first')
match_encode = ohe.fit_transform(df[["match"]])
match_encode_df = pd.DataFrame(match_encode, columns=ohe.get_feature_names_out(["match"]))

x = pd.concat([df[["commits_before"]].reset_index(drop=True), match_encode_df.reset_index(drop=True)], axis=1)
y = df["difference"]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

results = []
for max_depth in range(1, 11):
    tree = DecisionTreeRegressor(max_depth=max_depth, random_state=42)
    tree.fit(x_train, y_train)
    y_pred = tree.predict(x_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    results.append((max_depth, mse, r2))
    print(f"Max Depth: {max_depth}, MSE: {mse}, R^2: {r2}")

fit = max(results, key=lambda x: x[2])
fit_depth = fit[0]
print(f"Best max depth: {fit_depth}, MSE: {fit[1]:.2f}, R^2: {fit[2]:.4f}")

fit_tree = DecisionTreeRegressor(max_depth=fit_depth, random_state=42)
fit_tree.fit(x_train, y_train)
y_pred = fit_tree.predict(x_test)
print(f"Mean Squared Error: {mean_squared_error(y_test, y_pred)}")
print(f"R^2 Score: {r2_score(y_test, y_pred)}")

plt.figure(figsize=(12, 8))
plot_tree(fit_tree, feature_names=x.columns, filled=True, rounded=True)
plt.title("Decision Tree Regressor(max_depth=" + str(fit_depth) + ")")
plt.tight_layout()
plt.savefig("decision_tree_regressor_max_depth_with_outliers.png")
plt.show()