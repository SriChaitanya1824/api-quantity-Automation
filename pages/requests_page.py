from playwright.sync_api import Page, expect


class RequestsPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def open_create(self) -> None:
        self.page.get_by_test_id("nav-create").click()
        expect(self.page.get_by_test_id("request-create")).to_be_visible()

    def create(self, title: str, description: str) -> None:
        self.page.get_by_test_id("request-title").fill(title)
        self.page.get_by_test_id("request-description").fill(description)
        self.page.get_by_test_id("request-create").click()

    def open_list(self) -> None:
        self.page.get_by_test_id("nav-requests").click()
        expect(self.page.get_by_role("heading", name="Requests")).to_be_visible()

    def filter_by_status(self, status: str) -> None:
        self.page.get_by_test_id("request-filter").select_option(status)

    def cancel_first(self) -> None:
        self.page.get_by_test_id("request-cancel").first.click()

    def expect_request(self, title: str) -> None:
        expect(self.page.get_by_test_id("request-card").filter(has_text=title)).to_be_visible()

    def expect_empty(self) -> None:
        expect(self.page.get_by_test_id("empty-requests")).to_be_visible()
