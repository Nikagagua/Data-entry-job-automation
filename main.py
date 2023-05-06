import os
import requests
from time import sleep
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

load_dotenv('.env')
chrome_driver_path = os.getenv('CHROME_DRIVER_PATH')
google_form_url = os.getenv('GOOGLE_FORM_URL')
zillow_url = os.getenv('ZILLOW_URL')
gmail = os.getenv('ACCOUNT_GMAIL')
password = os.getenv('ACCOUNT_PASSWORD')
responses_url = os.getenv('RESPONSES_URL')

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5)"
                  " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.64 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

response = requests.get(url=zillow_url, headers=header)
data = response.text
soup = BeautifulSoup(data, "html.parser")
all_link_elements = soup.select(".property-card-data a")

all_links = []
for link in all_link_elements:
    href = link["href"]
    print(href)
    if "http" not in href:
        all_links.append(f"https://www.zillow.com{href}")
    else:
        all_links.append(href)

all_address_elements = soup.select(".property-card-link address")
all_addresses = [address.get_text().split(" | ")[-1] for address in all_address_elements]

all_price_elements = soup.select(".StyledPropertyCardDataArea-c11n-8-85-1__sc-yipmu-0 span")
all_prices = [price.get_text().split("+")[0] for price in all_price_elements if "$" in price.text]

service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service)

for n in range(len(all_links)):
    driver.get(google_form_url)

    sleep(2)
    address = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]'
                                            '/div/div/div[2]/div/div[1]/div/div[1]/input')
    price = driver.find_element(By.XPATH,
                                '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link = driver.find_element(By.XPATH,
                               '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element(By.XPATH,
                                        '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')

    address.send_keys(all_addresses[n])
    price.send_keys(all_prices[n])
    link.send_keys(all_links[n])
    submit_button.click()
