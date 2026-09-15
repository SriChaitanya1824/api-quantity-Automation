from playwright.sync_api import Page, expect


class ServicesPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def open(self) -> None:
        self.page.get_by_test_id("nav-services").click()
        expect(self.page.get_by_role("heading", name="Service Catalog")).to_be_visible()

    def expect_service_cards(self) -> None:
        expect(self.page.get_by_test_id("service-card").first).to_be_visible()
