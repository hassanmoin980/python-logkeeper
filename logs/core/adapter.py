import logging

from logs.core.registry import IssueRegistry


class IssueRegistryAdapter(logging.LoggerAdapter):
    """
    A LoggerAdapter that holds reference to an IssueRegistry
    and ensures error codes are included in log messages
    """

    def __init__(self, logger: logging.Logger, extra=None):
        super().__init__(logger, extra or {})
        self.issue_registry = IssueRegistry

    def process(self, msg, kwargs):
        """
        Ensure that each log message contains an error code.
        If an error is registered, fetch its associated code; otherwise default to "N/A".
        """
        extra = kwargs.setdefault("extra", {})

        # Attempt to extract issue name from kwargs
        issue = extra.get("issue", None)

        # Fetch issue details from the registry if available
        issue = self.issue_registry.get(issue) if issue else None
        error_code = getattr(issue, "_error_code", "XXX") if issue else "XXX"

        # Ensure that the error code is included in logging
        extra.setdefault("error_code", error_code)

        return msg, kwargs

    def get_issue(self, name: str):
        return self.issue_registry.get(name)

    def get_all_issues(self):
        return self.issue_registry.get_all_issues()
