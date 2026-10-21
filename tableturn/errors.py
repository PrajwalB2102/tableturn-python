"""Domain refusals and the error types. No FastAPI or Starlette import: services raise these, and
`handlers.py` turns them into application/problem+json.

The class attributes below are the single source of truth for status, type and title. Routes never build error
responses; services raise, the handler maps.
"""

class NoSuchBranch(Exception):
    def __init__(self, branch: str):
        self.branch = branch
        super().__init__(f"Branch '{branch}' does not exist.")


class NoSuchTable(Exception):
    def __init__(self, no: str):
        self.no = no
        super().__init__(f"Table '{no}' does not exist.")
