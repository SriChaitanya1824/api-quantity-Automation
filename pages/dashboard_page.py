from playwright.sync_api import Page, expect


class DashboardPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def expect_loaded(self) -> None:
        expect(self.page.get_by_role("heading", name="Dashboard")).to_be_visible()
        expect(self.page.get_by_test_id("request-status")).to_be_visible()

    def logout(self) -> None:
        self.page.get_by_test_id("logout-button").click()
        expect(self.page.get_by_test_id("login-submit")).to_be_visible()
