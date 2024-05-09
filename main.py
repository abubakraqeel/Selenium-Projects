from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

driver.get("http://orteil.dashnet.org/experiments/cookie/")
cookie = driver.find_element(By.ID, "cookie")
store = driver.find_elements(By.CSS_SELECTOR, "#store div")
item_id = [item.get_attribute("id") for item in store]
five_min = time.time() + 60*5
time_limit = time.time() + 10
while True:
    cookie.click()

    if time.time() > time_limit:

        all_price = driver.find_elements(By.CSS_SELECTOR, "#store b")
        item_prices = []

        for price in all_price:
            text = price.text
            if text != "":
                cost = int(text.split("-")[1].strip().replace(",", ""))
                item_prices.append(cost)
                
        upgrades = {}
        for n in range(len(item_prices)):
            upgrades[item_prices[n]] = item_id[n]
        
        money = driver.find_element(By.ID, "money").text
        if "," in money:
            money = money.replace(",", "")
        cookie_count = int(money)
        
        affordable_upgrades = {}
        for price, id in upgrades.items():
            if cookie_count>price:
                affordable_upgrades[price] = id

        highest_price_affordable_upgrade = max(affordable_upgrades)
        print(highest_price_affordable_upgrade)
        to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]

        driver.find_element(By.ID, to_purchase_id).click()

        time_limit = time.time() + 10

        if time.time() > five_min:
            cookie_per_s = driver.find_element(By.ID, "cps").text
            print(cookie_per_s)
            break