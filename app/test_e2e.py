import pytest

from selenium import webdriver


@pytest.fixture(autouse=True, scope="module")
def chrome_web_driver():
    driver = webdriver.Chrome(
        executable_path="tools/drivers/chromedriver_mac64/chromedriver")
    driver.get("http://localhost:5001")
    yield driver
    driver.quit()


def test_brower_title_contains_app_name(chrome_web_driver):
    assert "Find the entities" in chrome_web_driver.title
