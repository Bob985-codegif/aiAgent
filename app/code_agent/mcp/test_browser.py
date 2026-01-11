from selenium import webdriver

if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.get("https://www.baidu.com")
    time.sleep(5)
