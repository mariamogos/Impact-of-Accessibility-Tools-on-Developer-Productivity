from github import Github
from datetime import datetime, timezone
import csv
import time
import os

ACCESS_TOKEN = "YOUR_GITHUB_TOKEN_HERE"
g = Github(ACCESS_TOKEN)

#timeframes
before_start = datetime(2024, 8, 1, tzinfo=timezone.utc)
before_end = datetime(2024, 11, 30, 23, 59, 59, tzinfo=timezone.utc)
after_start = datetime(2025, 1, 1, tzinfo=timezone.utc)
after_end = datetime(2025, 4, 30, 23, 59, 59, tzinfo=timezone.utc)

input_file = "dev_productivity_by_period.csv"
output_file = "dev_productivity_autumn.csv"
skipped_log = "skipped_users.txt"

fieldnames = [
    "username", "bio",
    "commits_before", "commits_after",
    "prs_created_before", "prs_created_after",
    "prs_reviewed_before", "prs_reviewed_after"
]

processed_users = set()
if os.path.exists(output_file):
    with open(output_file, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            processed_users.add(row["username"])

def mine_users_contributions(user):
    counts = {
        "commits_before": 0,
        "commits_after": 0,
        "prs_created_before": 0,
        "prs_created_after": 0,
        "prs_reviewed_before": 0,
        "prs_reviewed_after": 0
    }

    try:
        for repo in user.get_repos():
            try:
                before_commits = repo.get_commits(author=user.login, since=before_start, until=before_end)
                for commit in before_commits:
                    if commit.author and commit.author.login == user.login:
                        counts["commits_before"] += 1

                after_commits = repo.get_commits(author=user.login, since=after_start, until=after_end)
                for commit in after_commits:
                    if commit.author and commit.author.login == user.login:
                        counts["commits_after"] += 1
            except Exception as e:
                print(f"Error processing commits for {repo.name}: {e}")
                pass

            try:
                pulls = repo.get_pulls(state="all")
                for pull in pulls:
                    if pull.user.login != user.login:
                        continue
                    created_at = pull.created_at
                    if before_start <= created_at <= before_end:
                        counts["prs_created_before"] += 1
                    elif after_start <= created_at <= after_end:
                        counts["prs_created_after"] += 1

                    for review in pull.get_reviews():
                        if review.user and review.user.login == user.login:
                            reviewed_at = review.submitted_at
                            if reviewed_at and before_start <= reviewed_at <= before_end:
                                counts["prs_reviewed_before"] += 1
                            elif reviewed_at and after_start <= reviewed_at <= after_end:
                                counts["prs_reviewed_after"] += 1
            
            except Exception as e:
                print(f"Error processing PRs for {repo.name}: {e}")
                pass

    except Exception as e:
        print(f"error processing repos for {user.login}: {e}")
    return counts

mode = "a" if os.path.exists(output_file) else "w"
with open(output_file, mode=mode, newline='', encoding="utf-8") as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    if mode == "w":
        writer.writeheader()

    with open(input_file, newline='', encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        for index, row in enumerate(reader, start=1):
            username = row["username"]
            bio = row["bio"].strip() if row["bio"] else ""

            if username in processed_users:
                print(f"skipping user {username}, already processed.")
                continue
            
            print(f"Processing user {index}: {username}")
            try:
                user = g.get_user(username)
                counts = mine_users_contributions(user)

                if any(v > 0 for v in counts.values()):
                    writer.writerow({
                        "username": username,
                        "bio": bio,
                        **counts
                    })
                    outfile.flush()
                    processed_users.add(username)
                    print(f"added user {username} to the output file.")
                
                else:
                    print(f"User {username} has no contributions in the specified timeframes.")
                    with open(skipped_log, "a", encoding="utf-8") as skipped_file:
                        skipped_file.write(f"{username}\n")
            
                time.sleep(1) 
            except Exception as e:
                print(f"Error processing user {username}: {e}")
                with open(skipped_log, "a", encoding="utf-8") as skipped_file:
                    skipped_file.write(f"{username}\n")