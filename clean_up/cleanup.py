#this script removes users that have no commits before and after the analysis or that do not have a match of the keywords
import pandas as pd

df = pd.read_csv("dev_productivity_autumn.csv")

df["bio"] = df["bio"].fillna("").astype(str).str.lower()

keywords = [
    "disabled", "blind", "visually impaired", "deaf", "neurodivergent",
    "autistic", "adhd", "chronic illness", "mobility aid"
]

for keyword in keywords:
    df[keyword] = df["bio"].str.contains(keyword, na=False)

df["match"] = df[keywords].sum(axis=1)

cleaned_df = df[
    (df["commits_before"]>0) & 
    (df["commits_after"] > 0) &
    (df["match"] > 0)
    ]

cleaned_df.to_csv("users_analysis_cleaned.csv", index=False)