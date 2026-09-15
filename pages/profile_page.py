from playwright.sync_api import Page, expect


class ProfilePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def open(self) -> None:
        self.page.get_by_test_id("nav-profile").click()
        expect(self.page.get_by_test_id("profile-save")).to_be_visible()

    def update(self, full_name: str, department: str) -> None:
        self.page.get_by_test_id("profile-name").fill(full_name)
        self.page.get_by_test_id("profile-department").fill(department)
        self.page.get_by_test_id("profile-save").click()

    def expect_values(self, full_name: str, department: str) -> None:
        expect(self.page.get_by_test_id("profile-name")).to_have_value(full_name)
        expect(self.page.get_by_test_id("profile-department")).to_have_value(department)
