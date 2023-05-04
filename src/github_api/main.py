from GithubApi import GithubApi


api = GithubApi("<API_TOKEN>")

repos = api.get_repositories()
print(repos)

branches = api.get_repository_branches("<OWNER>", "<REPOSITORY>")
print(branches)

pulls = api.get_repository_pull_requests("<OWNER>", "<REPOSITORY>")
print(pulls)

closed = api.close_repository_pull_request(
    "<OWNER>", "<REPOSITORY>", pull_no=0, title="title", body="body")
print(closed)

crated_pr = api.create_repository_pull_request(
    "<OWNER>", "<REPOSITORY>", title="title", body="body", head="<HEAD>", base="<BASE>")
print(crated_pr)

pr_approve = api.approve_repository_pull_request(
    "<OWNER>", "<REPOSITORY>", pull_no=0, commit_id="<COMMIT_ID>", body="body")
print(pr_approve)
