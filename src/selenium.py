from selenium import webdriver
from selenium.webdriver.support.select import Select


def set_text_in_input_field(input_field: object, input_text: str):
    """Очищает и заполняет выбранный текстовый объект."""
    input_field.clear()
    input_field.send_keys(input_text)
    input_field.submit()


def click_chosen_object_dict(driver: object, object_dict: dict, alternative=False):
    """Кликает выбранные объекты."""
    for _, element_item in object_dict.items():
        if element_item is not None:
            if alternative:
                driver.execute_script("arguments[0].click();", element_item)
            else:
                element_item.click()


def get_driver_options(image_directory: str) -> object:
    """Настраивает драйвер браузера и возвращает объект настроек."""
    driver_options = webdriver.ChromeOptions()
    driver_options.add_argument("--headless")
    driver_options.add_argument("--window-size=1920x1080")
    driver_options.add_argument("--disable-notifications")
    driver_options.add_argument('--no-sandbox')
    driver_options.add_argument('--verbose')
    driver_options.add_experimental_option("prefs", {
        "download.default_directory": image_directory,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False
    })
    driver_options.add_argument('--disable-gpu')
    driver_options.add_argument('--disable-software-rasterizer')
    return driver_options


def download_starmap(driver: object, url: str, starmap_shade_galaxy: bool, hours: str, minutes: str, width: str, height: str):
    """Скачивает изображение звездного неба."""
    driver.get(url)
    width_input_field = driver.find_element_by_css_selector('.pl-export-x')
    height_input_field = driver.find_element_by_css_selector('.pl-export-y')
    set_text_in_input_field(width_input_field, width)
    set_text_in_input_field(height_input_field, height)
    object_dict = {
        'hide_deep_sky': driver.find_element_by_css_selector('.chksn'),
        'hide_planets': driver.find_element_by_css_selector('.chksp'),
        'hide_planets_label': driver.find_element_by_css_selector('.chklp'),
        'hide_constellations_names': driver.find_element_by_css_selector('.chkcn'),
        'hide_daylight': driver.find_element_by_css_selector('.chkdaylig'),
        'show_shade_galaxy': driver.find_element_by_css_selector('.chkgalash') if starmap_shade_galaxy else None,
    }
    click_chosen_object_dict(driver, object_dict)

    stars_option = Select(driver.find_element_by_name('PLlimitmag'))
    stars_option.select_by_visible_text('Faint')

    hours_option = Select(driver.find_element_by_name('hour'))
    hours_option.select_by_visible_text(hours)

    minutes_option = Select(driver.find_element_by_name('min'))
    minutes_option.select_by_visible_text(minutes)

    download_image = driver.find_element_by_css_selector('.pl-svg')
    driver.execute_script("arguments[0].click();", download_image)


def get_driver(image_directory) -> object:
    """Возвращает драйвер веб-браузера."""
    driver_options = get_driver_options(image_directory)
    driver = webdriver.Chrome(chrome_options=driver_options, executable_path="/usr/bin/chromedriver")
    return driver
