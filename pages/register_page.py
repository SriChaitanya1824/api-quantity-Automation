from playwright.sync_api import Page, expect


class RegisterPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def open_from_login(self) -> None:
        self.page.get_by_role("button", name="Create account").click()
        expect(self.page.get_by_test_id("register-submit")).to_be_visible()

    def register(self, name: str, email: str, password: str, department: str = "IT") -> None:
        self.page.get_by_test_id("register-name").fill(name)
        self.page.get_by_test_id("register-email").fill(email)
        self.page.get_by_label("Department").fill(department)
        self.page.get_by_test_id("register-password").fill(password)
        self.page.get_by_test_id("register-submit").click()

    def expect_success(self) -> None:
        expect(self.page.get_by_text("Registration complete")).to_be_visible()
