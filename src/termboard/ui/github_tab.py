from textual import work
from textual.app import ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Button, DataTable, Label

from ..core.github import (
    GitHubError,
    checkout_pr,
    get_actions,
    get_issues,
    get_pull_requests,
)


class GitHubTab(VerticalScroll):
    """The GitHub integration tab."""

    def compose(self) -> ComposeResult:
        with Horizontal(id="github-header", classes="header-bar"):
            yield Label("🐙 GitHub Integration", classes="title")
            yield Button("Refresh", id="refresh-github", variant="primary")

        yield Label("Pull Requests (Click to Checkout)", classes="section-label")
        yield DataTable(id="prs-table", cursor_type="row")

        yield Label("GitHub Actions", classes="section-label")
        yield DataTable(id="actions-table", cursor_type="row")

        yield Label("Open Issues", classes="section-label")
        yield DataTable(id="issues-table", cursor_type="row")

    def on_mount(self) -> None:
        prs_table = self.query_one("#prs-table", DataTable)
        prs_table.add_columns("ID", "Title", "Author", "State", "CI")

        actions_table = self.query_one("#actions-table", DataTable)
        actions_table.add_columns("Workflow", "Conclusion", "Status")

        issues_table = self.query_one("#issues-table", DataTable)
        issues_table.add_columns("ID", "Title", "Author", "State")

        self.load_data()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "refresh-github":
            self.load_data()

    @work(exclusive=True, thread=False)
    async def load_data(self) -> None:
        prs_table = self.query_one("#prs-table", DataTable)
        actions_table = self.query_one("#actions-table", DataTable)
        issues_table = self.query_one("#issues-table", DataTable)

        prs_table.clear()
        actions_table.clear()
        issues_table.clear()

        try:
            prs = await get_pull_requests()
            for pr in prs:
                ci_status = "N/A"
                if pr.get("statusCheckRollup"):
                    ci_status = pr["statusCheckRollup"][0].get("state", "UNKNOWN")
                author = pr.get("author", {}).get("login", "Unknown")
                prs_table.add_row(
                    f"#{pr['number']}",
                    pr["title"],
                    f"@{author}",
                    pr["state"],
                    ci_status,
                )
            if not prs:
                prs_table.add_row("N/A", "No open pull requests found.", "", "", "")
        except GitHubError as e:
            prs_table.add_row("Error", str(e), "", "", "")

        try:
            actions = await get_actions()
            for action in actions:
                actions_table.add_row(
                    action["name"],
                    action.get("conclusion", "N/A") or "In Progress",
                    action["status"],
                )
            if not actions:
                actions_table.add_row("N/A", "No recent actions found.", "")
        except GitHubError as e:
            actions_table.add_row("Error", str(e), "")

        try:
            issues = await get_issues()
            for issue in issues:
                author = issue.get("author", {}).get("login", "Unknown")
                issues_table.add_row(
                    f"#{issue['number']}", issue["title"], f"@{author}", issue["state"]
                )
            if not issues:
                issues_table.add_row("N/A", "No open issues found.", "", "")
        except GitHubError as e:
            issues_table.add_row("Error", str(e), "", "")

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        if event.data_table.id == "prs-table":
            pr_number_str = event.data_table.get_row_at(event.cursor_row)[0]
            pr_number = pr_number_str.replace("#", "")
            if pr_number.isdigit():
                self.checkout_pr_task(pr_number)

    @work(exclusive=True, thread=False)
    async def checkout_pr_task(self, pr_number: str) -> None:
        self.notify(f"Checking out PR #{pr_number}...")
        try:
            await checkout_pr(pr_number)
            self.notify(
                f"Successfully checked out PR #{pr_number}!", severity="information"
            )
        except GitHubError as e:
            self.notify(f"Failed: {e}", severity="error")
