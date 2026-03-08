from playwright.sync_api import sync_playwright
import tkinter as tk
from tkinter import messagebox
import sys


def manual_login_mode():
    """Режим ручного входа"""
    with sync_playwright() as p:
        # Используем persistent context для сохранения сессии после ручного входа
        user_data_dir = r"C:\!Stud\Kalendar\bot_profile"
        browser = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            headless=False,  # Обязательно False, чтобы вы видели, что вводите
        )
        page = browser.pages[0]
        page.goto("https://sfedu.modeus.org/schedule-calendar/my")
        # Ждем долго, пока вы не залогинитесь
        page.wait_for_selector(".icon-icalendar", timeout=120000)
        browser.close()


def run(headless=True):
    try:
        with sync_playwright() as p:
            user_data_dir = r"C:\!Stud\Kalendar\bot_profile"
            context = p.chromium.launch_persistent_context(
                user_data_dir=user_data_dir,
                executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                headless=headless,
            )

            page = context.pages[0]
            page.goto("https://sfedu.modeus.org/schedule-calendar/my")

            # Ждем кнопку экспорта
            page.wait_for_selector(".icon-icalendar", timeout=20000)

            with page.expect_download() as download_info:
                page.click("button.icon-icalendar")

            download = download_info.value
            download.save_as(r"C:\!Stud\Kalendar\schedule.ics")
            context.close()
            print("Успех!")

    except Exception as e:
        # Если скрипт упал:
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)

        msg = f"Ошибка обновления расписания: {e}\n\nПопробовать зайти вручную?"
        if messagebox.askyesno("Проблема с Модеусом", msg):
            manual_login_mode()
        root.destroy()


if __name__ == "__main__":
    # Запускаем в фоновом режиме (True)
    run(headless=True)