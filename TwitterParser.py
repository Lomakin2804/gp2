from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
import json
import numpy as np
from posts_processing import process_post
from files_management import clear_duplicates


class TwitterParser:

    def __init__(self, driver_path="./chromedriver", cookies_file="cookie_data.json"):
        self.driver_path = driver_path
        self.cookies_file = cookies_file
        self.driver = None
        self.cookie_packs = self._load_cookies()

    def _load_cookies(self):
        with open(self.cookies_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _setup_driver(self):
        service = Service(executable_path="./chromedriver")
        self.driver = webdriver.Chrome(service=service)
        self.driver.get("https://x.com/explore")
        time.sleep(2)
        print("-- Driver in work")

    def get_login_cookies(self):
        self._setup_driver()
        input("Войдите в аккаунт и нажмите Enter...")

        cookies = self.driver.get_cookies()
        try:
            with open(self.cookies_file, "r", encoding="utf-8") as f:
                all_cookies = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            all_cookies = []

        all_cookies.append(cookies)
        with open(self.cookies_file, "w", encoding="utf-8") as f:
            json.dump(all_cookies, f, ensure_ascii=False)

        self.cookie_packs = all_cookies
        return f"Данные о новом аккаунте сохранены. Всего {len(all_cookies)} аккаунтов."

    def parse_project_tweets(self, project_name):
        cookie_pack_index = 0

        self._setup_driver()

        for cookie in self.cookie_packs[cookie_pack_index]:
            self.driver.add_cookie(cookie)
        print("-- Cookies updated")
        time.sleep(2)

        self.driver.refresh()

        WebDriverWait(self.driver, 5).until(
            ec.presence_of_element_located((By.XPATH, "//button[@data-testid='app-bar-close']"))
        )
        button_close = self.driver.find_element(By.XPATH, "//button[@data-testid='app-bar-close']")
        button_close.click()

        WebDriverWait(self.driver, 5).until(
            ec.presence_of_element_located((By.XPATH, "//a[@data-testid='AppTabBar_Explore_Link']"))
        )
        explore = self.driver.find_element(By.XPATH, "//a[@data-testid='AppTabBar_Explore_Link']")
        explore.click()

        WebDriverWait(self.driver, 5).until(
            ec.presence_of_element_located((By.TAG_NAME, "input"))
        )
        input_element = self.driver.find_element(By.TAG_NAME, "input")
        input_element.send_keys(project_name + Keys.ENTER)
        time.sleep(3)

        print(f"--Starting parsing on project '{project_name}'")
        scroll = self.driver.find_element(By.TAG_NAME, "body")
        posts_count = 0
        err = False
        prev_posts, no_posts_count = 0, 0
        with open(f"{project_name}_processed_posts.json", "w", encoding="utf-8") as f:
            while True:
                # Прокручиваем
                c, s = 0, 0
                stop = np.random.randint(17, 28)
                for _ in range(50):
                    if c == stop:
                        c = 0
                        stop = np.random.randint(40, 50)
                        time.sleep(np.random.randint(1, 3))
                    scroll.send_keys(Keys.ARROW_DOWN)
                    c += 1
                time.sleep(1)

                # Считываем посты
                posts = self.driver.find_elements(By.XPATH, "//div[@data-testid='cellInnerDiv']")

                if posts == prev_posts:
                    no_posts_count += 1
                    print(f"Посты не обновились {no_posts_count}/5 раз.")
                else:
                    no_posts_count = 0
                prev_posts = posts
                # Если 5 раз подряд постов не прибавилось — конец страницы
                if no_posts_count >= 5:
                    print("Конец страницы...")
                    break

                if len(posts) == 0:
                    print("CRITICAL ERROR: Session is blocked...")
                    err = True
                for index in range(len(posts)):
                    for k in range(3):
                        try:
                            post = self.driver.find_elements(By.XPATH, "//div[@data-testid='cellInnerDiv']")[index]
                            post_html = post.get_attribute("outerHTML")
                            processed_post = process_post(post_html)
                            break
                        except Exception as e:
                            print("VALUE ERROR: stale element not found in the current frame", e)
                        if k == 2:
                            print("Skipping posts")
                    if processed_post is None:
                        continue
                    elif processed_post == "Error: TryAgain":
                        print("CRITICAL ERROR: Session is blocked...")
                        err = True
                        break
                    f.write(json.dumps(processed_post, ensure_ascii=False) + "\n")
                    posts_count += 1
                    if posts_count % 50 == 0:
                        print(f"Собрано {posts_count} постов (с дубликатами)")
                if posts_count > 800:
                    break
                if err:
                    break

        print("Parsing finished.")
        time.sleep(5)
        self.driver.quit()

        clear_duplicates(f"{project_name}_processed_posts.json")
