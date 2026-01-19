from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

path = 'chromedriver.exe'
service = webdriver.chrome.service.Service(path)
driver = webdriver.Chrome(service = service)

url = 'https://chargeinfo.ksga.org/front/statistics/evCar/'
driver.get(url)
time.sleep(2) 

for _ in range(1):
    body = driver.find_element(By.TAG_NAME, "body")
    body.send_keys(Keys.END)
    time.sleep(1)

table = driver.find_element(By.CSS_SELECTOR,'#tBodyList')
rows = driver.find_elements(By.CSS_SELECTOR, '#tBodyList tr')

for row in rows:
    cols = row.find_elements(By.TAG_NAME, 'td')

    row_data = []

    for col in cols:
        content = col.get_attribute("textContent").strip()    # textContent -> 태그 안에 있는 모든 텍스트
        if '(' in content:
                content = content.split('(')[0].strip()
        row_data.append(content)
    print(row_data)