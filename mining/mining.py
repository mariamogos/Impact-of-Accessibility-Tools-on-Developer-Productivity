from github import Github
from datetime import datetime, timezone
import csv
import time
import os


ACCESS_TOKEN = "YOUR_GITHUB_TOKEN_HERE"
g = Github(ACCESS_TOKEN)

#timeframes
before_start = datetime(2024, 10, 1, tzinfo=timezone.utc)
before_end = datetime(2024, 10, 31, 23, 59, 59, tzinfo=timezone.utc)
after_start = datetime(2025, 3, 1, tzinfo=timezone.utc)
after_end = datetime(2025, 3, 31, 23, 59, 59, tzinfo=timezone.utc)

keywords = [
    "disabled", "blind", "visually impaired", "deaf", "neurodivergent",
    "autistic", "adhd", "chronic illness", "mobility aid"
]

output_file = "dev_productivity_by_period.csv"
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

def mine_users_contributions(user, before_start, before_end, after_start, after_end):
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
                after_commits = repo.get_commits(author=user.login, since=after_start, until=after_end)
                counts["commits_before"] += before_commits.totalCount
                counts["commits_after"] += after_commits.totalCount
            except:
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

                    reviews = pull.get_reviews()
                    for review in reviews:
                        if review.user and review.user.login == user.login:
                            reviewed_at = review.submitted_at
                            if reviewed_at and before_start <= reviewed_at <= before_end:
                                counts["prs_reviewed_before"] += 1
                            elif reviewed_at and after_start <= reviewed_at <= after_end:
                                counts["prs_reviewed_after"] += 1
            except:
                pass
    except Exception as e:
        print(f"Error processing user {user.login}: {e}")
        
    return counts

mode = "a" if os.path.exists(output_file) else "w"
with open(output_file, mode=mode, newline='', encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    if mode == "w":
        writer.writeheader()

    found_users = set()
    for keyword in keywords:
        query = f"\"{keyword}\" in:bio"
        print(f"Searching for users with keyword: {keyword}")

        try:
            users = g.search_users(query)
            for user in users:
                if user.login not in found_users:
                    found_users.add(user.login)
        except Exception as e:
            print(f"Error searching for users with keyword {keyword}: {e}")
        time.sleep(1)
    print(f"Found {len(found_users)} unique users.")

    user_index = 0
    active_user_count = 0

    for username in sorted(found_users):
        user_index += 1
        if username in processed_users:
            print(f"Skipping already processed user {username} ({user_index}/{len(found_users)})")
            continue

        print(f"[{user_index}/{len(found_users)}] Processing user {username}")

        try:
            user = g.get_user(username)
            bio = user.bio.replace("\n", " ").replace("\r", " ").strip() if user.bio else ""

            counts = mine_users_contributions(user, before_start, before_end, after_start, after_end)

            if any(v > 0 for v in counts.values()):
                writer.writerow({
                    "username": username,
                    "bio": bio,
                    **counts
                })
                csvfile.flush()
                processed_users.add(username)
                active_user_count += 1
                print(f"Added {username} to results. Active user count: {active_user_count}")
            else:
                print(f"No contributions found for {username} in the specified periods.")

            time.sleep(1)

        except Exception as e:
            print(f"Error processing user {username}: {e}")

print(f"Data mining completed. Results saved to {output_file}.")

