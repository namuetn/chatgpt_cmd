import undetected_chromedriver as uc

def setup_driver():
    # options = uc.ChromeOptions()
    # options.headless = True
    driver = uc.Chrome()

    return driver
