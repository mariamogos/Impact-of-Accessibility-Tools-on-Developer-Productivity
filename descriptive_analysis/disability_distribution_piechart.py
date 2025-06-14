import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("users_no_outliers.csv")
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

matched_df = df.dropna(subset=["match"])

counts = matched_df["match"].value_counts().to_dict()
labels = list(counts.keys())
sizes = list(counts.values())
total = sum(sizes)
percentage = [count/total * 100 for count in sizes]

plt.figure(figsize=(10, 6))
patches, _, autotexts = plt.pie(
    sizes,
    labels=labels,
    autopct='%1.1f%%',
    startangle=140,
    wedgeprops={'linewidth': 1, 'edgecolor': 'white'}
)

for autotext in autotexts:
    autotext.set_color('black')
    autotext.set_fontsize(10)

legend_labels = [f"{label} ({percent:.1f}%)" for label, percent in zip(labels, percentage)]
plt.legend(patches, legend_labels, title="Disability Distribution", loc="best")

plt.title("Disability Distribution (n = {})".format(total), fontsize=14)
plt.axis('equal')
plt.tight_layout()
plt.savefig("disability_distribution_no_outliers.png")
plt.show()