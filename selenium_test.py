import random
import json
import time
from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def set_viewport_size(driver_in, width, height):
    window_size = driver_in.execute_script("""
        return [window.outerWidth - window.innerWidth + arguments[0],
          window.outerHeight - window.innerHeight + arguments[1]];
        """, width, height)
    driver_in.set_window_size(*window_size)


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

set_viewport_size(driver, random.randint(800, 1000), random.randint(500, 700))

driver.get('https://www.powr.io/users/sign_in')

with open('results.txt', 'w', encoding='utf8') as results:
    try:
        WebDriverWait(driver, 60).until(EC.title_is("Dashboard"))
    except TimeoutException:
        results.write("Время ожидания авторизации исчерпано")
    driver.get('https://www.powr.io/users/me/my-apps')
    time.sleep(5)
    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')
    pages = soup.find_all('span', class_="my-apps__pagination-item")
    last_page = pages[-1].text
    for page_num in range(int(last_page)):
        temp_res = []
        try:
            driver.get(f"https://www.powr.io/users/me/my-apps.json?page_number={page_num + 1}")
        except:
            results.write('Сканирования прервано')
        content = driver.find_element(By.TAG_NAME, 'pre').text
        data = json.loads(content)
        apps = data['apps']
        for app in apps:
            if app.get("content") and app.get("content").get("comments"):
                comments = [comment for comment in app.get("content").get("comments")]
                if comments:
                    comments.sort(key=lambda x: datetime.fromtimestamp(int(x['timeCreated'])))
                    if not comments[-1]["approved"]:
                        temp_res.append(app['id'])

        for app_id in set(temp_res):
            results.write(f'https://www.powr.io/plugins/comments/standalone?id={app_id}&' + '\n')
    driver.quit()
