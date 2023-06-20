import undetected_chromedriver as uc
import argparse

def setup_driver():
    # options = uc.ChromeOptions()
    # options.headless = True
    driver = uc.Chrome()

    return driver
 