from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url
        self.email = page.get_by_test_id("login-email")
        self.password = page.get_by_test_id("login-password")
        self.submit = page.get_by_test_id("login-submit")

    def goto(self) -> None:
        self.page.goto(self.base_url)
        expect(self.submit).to_be_visible()

    def login(self, email: str, password: str) -> None:
        self.email.fill(email)
        self.password.fill(password)
        self.submit.click()

    def expect_error(self, text: str) -> None:
        expect(self.page.get_by_role("alert")).to_contain_text(text)
