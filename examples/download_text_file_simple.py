import time
from selenium import webdriver

options = webdriver.FirefoxOptions()

driver = webdriver.Remote(
   command_executor="http://selenium:4444/wd/hub",
   desired_capabilities=options.to_capabilities()
   )

try:
    driver.get('file:///etc/passwd')
    print(driver.page_source)
finally:
    driver.quit()
