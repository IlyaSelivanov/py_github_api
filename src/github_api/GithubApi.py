import json
from HttpSession import HttpSession
from response_models import Branch, PullRequest, PullRequestApprove, Repository


class GithubApi:
    def __init__(self, token) -> None:
        self.session = HttpSession(token=token)

    def get_repositories(self):
        self.session.create_request("GET", "/user/repos")
        raw_response = self.session.get_response()

        return self.__parse_raw_response(Repository, raw_response.text)

    def get_repository_branches(self, owner, repo):
        self.session.create_request("GET", f"/repos/{owner}/{repo}/branches")
        raw_response = self.session.get_response()

        return self.__parse_raw_response(Branch, raw_response.text)

    def get_repository_pull_requests(self, owner, repo):
        self.session.create_request("GET", f"/repos/{owner}/{repo}/pulls")
        raw_response = self.session.get_response()

        return self.__parse_raw_response(PullRequest, raw_response.text)

    def close_repository_pull_request(self, owner, repo, pull_no, title="", body=""):
        json_body = {
            "title": f"{title}",
            "body": f"{body}",
            "state": "closed"
        }

        self.session.create_request(
            method="PATCH", url=f"/repos/{owner}/{repo}/pulls/{str(pull_no)}", json=json_body)
        raw_response = self.session.get_response()

        return self.__parse_raw_response(PullRequest, raw_response.text)

    def create_repository_pull_request(self, owner, repo, title="", body="", head="", base=""):
        json_body = {
            "title": f"{title}",
            "body": f"{body}",
            "head": f"{head}",
            "base": f"{base}"
        }

        self.session.create_request(
            method="POST", url=f"/repos/{owner}/{repo}/pulls", json=json_body)
        raw_response = self.session.get_response()

        return self.__parse_raw_response(PullRequest, raw_response.text)

    def approve_repository_pull_request(self, owner, repo, pull_no, commit_id, body="", comments=[{}]):
        assert commit_id is not None or commit_id != ""

        json_comments = json.dumps(comments)

        json_body = {
            "commit_id": f"{commit_id}",
            "body": f"{body}",
            "event": "APPROVE",
            "comments": f"{json_comments}"
        }

        self.session.create_request(
            method="POST", url=f"/repos/{owner}/{repo}/pulls/{str(pull_no)}", json=json_body)
        raw_response = self.session.get_response()

        return self.__parse_raw_response(PullRequestApprove, raw_response.text)

    def __parse_raw_response(self, type_name, text):
        res = []
        loaded = json.loads(text)

        if isinstance(loaded, dict):
            res.append(type_name(loaded))
            return res

        for item in loaded:
            res.append(type_name(item))

        return res
