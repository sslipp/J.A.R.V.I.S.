import json
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def parse_all_lesson_links():
    # Настройка драйвера
    driver = webdriver.Chrome(executable_path=r"C:\Users\Rodion\Desktop\J.A.S.M.I.N.E\chromedriver\chromedriver.exe")
    driver.maximize_window()
    driver.get("https://id.human.ua/auth/login")

    # Вход в систему
    driver.find_element(By.ID, "login-email-input").send_keys("stuntdok.smailiki@gmail.com")
    driver.find_element(By.ID, "login-password-input").send_keys("161208Gg")
    driver.find_element(By.ID, "login-submit-button").click()
    time.sleep(5)

    # Переход на календарь
    driver.find_element(By.CLASS_NAME, "overlay--hover").click()
    time.sleep(3)
    driver.get("https://lms.human.ua/app/calendar")
    time.sleep(5)

    # Список для сохранения ссылок каждого урока по номерам уроков
    lesson_links = {}

    # Поиск и обработка каждого урока
    events = driver.find_elements(By.CLASS_NAME, "calendar-event")
    lesson_number = 1  # Номер урока начинается с 1
    for event in events:
        driver.execute_script("arguments[0].scrollIntoView();", event)
        event.click()

        try:
            detail_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "calendar-event-details-item"))
            )

            lesson_link_set = set()

            divs = detail_element.find_elements(By.TAG_NAME, "div")
            for div in divs:
                text_content = div.text
                if ("meet.google.com" in text_content or "us04web.zoom.us" in text_content or "us05web.zoom.us" in text_content):
                    lesson_link_set.add(text_content.strip())

            # Привязываем ссылки к номеру урока
            if lesson_link_set:
                lesson_links[str(lesson_number)] = list(lesson_link_set)[0]  # Берем первую ссылку, если их несколько
            else:
                lesson_links[str(lesson_number)] = None

            lesson_number += 1  # Переходим к следующему уроку
            driver.execute_script("window.scrollTo(0, 0);")
            driver.execute_script("document.elementFromPoint(10, 10).click();")
            time.sleep(1)

        except Exception as e:
            print(f"Не удалось получить данные для урока: {e}")
            lesson_links[str(lesson_number)] = None
            lesson_number += 1
            continue

    driver.quit()

    # Сохранение ссылок в файл с текущей датой
    file_date = datetime.now().strftime("%d.%m.%Y")  # Формат названия файла
    with open(f"{file_date}.json", "w", encoding="utf-8") as file:
        json.dump(lesson_links, file, indent=4, ensure_ascii=False)

    return lesson_links