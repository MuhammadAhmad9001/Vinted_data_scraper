import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests



BOT_TOKEN = ""
CHAT_ID = ""

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url, data=payload)


chrome_options = Options()

chrome_options.add_argument("--no-sandbox")

# Set Chrome options
chrome_options.add_argument("--start-maximized")

service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the target URL
url = "https://www.vinted.es/catalog?time=1743802662&catalog_from=0&page=1&catalog[]=5&brand_ids[]=417&brand_ids[]=671&brand_ids[]=15430438&brand_ids[]=481&brand_ids[]=46323&brand_ids[]=4785&order=newest_first"
driver.get(url)

# Let the page load
time.sleep(10)
WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "a.new-item-box__overlay"))
)
WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.CSS_SELECTOR,
        "div.u-flexbox.u-align-items-flex-start.u-ui-padding-bottom-regular"))
)

WebDriverWait(driver, 15).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR,
        "div.u-flexbox.u-align-items-flex-start.u-ui-padding-bottom-regular"))
)

price = driver.find_elements(By.CSS_SELECTOR,
    "div:nth-child(3) > div > div > div > div > div:nth-child(2)"
)

# # Grab links
links = driver.find_elements(By.CSS_SELECTOR, "a.new-item-box__overlay")
dess = driver.find_elements(By.CSS_SELECTOR, "div.u-flexbox.u-align-items-flex-start.u-ui-padding-bottom-regular")

price_elements_testid = driver.find_elements(By.CSS_SELECTOR, 'p[data-testid$="--price-text"]')
price_elements = driver.find_elements(By.CSS_SELECTOR, 'span.web_ui__Text__subtitle.web_ui__Text__underline-none')


# Print them
for link, des, price, dis_price in zip(links, dess, price_elements_testid, price_elements):
    message = (
        f"<b>🛍️ New Item Found</b>\n"
        f"<b>🔗 Link:</b> {link.get_attribute('href')}\n"
        f"<b>📄 Description:</b> {des.text}\n"
        f"<b>💸 Original Price:</b> {dis_price.text}\n"
        f"<b>💰 Display Price:</b> {price.text}"
    )
    print(message, "\n")
    send_telegram_message(message)
