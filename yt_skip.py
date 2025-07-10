import time
import random
import subprocess
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    WebDriverException,
    TimeoutException,
    NoSuchElementException,
)


# 🔗 Constants
YOUTUBE_URL = "https://www.youtube.com"
CHROMEDRIVER_PATH = "path/to/chromedriver"
CHROME_USER_DATA_DIR = "path/to/chrome-profile"
# OR use import os:
# CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH", "/path/to/chromedriver")
# CHROME_USER_DATA_DIR = os.getenv("CHROME_USER_DATA_DIR", "/path/to/chrome-profile")
#
HEADLESS_MODE = False  # Set to True if running in background/CI

# 🧾 Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger()


# 🧼 Kill all existing chromedriver processes
def kill_chromedriver_processes():
    try:
        subprocess.run(["pkill", "-f", "chromedriver"], check=False)
        log.info("Killed existing chromedriver processes.")
    except Exception as e:
        log.warning(f"Failed to kill chromedriver: {e}")


# 🚀 Start Chrome browser with stealth options
def start_browser():
    log.info("Launching Chrome browser...")

    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--autoplay-policy=no-user-gesture-required")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument(f"--user-data-dir={CHROME_USER_DATA_DIR}")

    if HEADLESS_MODE:
        chrome_options.add_argument("--headless=new")

    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Hide webdriver flag
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """
        },
    )

    driver.get(YOUTUBE_URL)
    time.sleep(5)

    # Try to play and unmute the video
    try:
        driver.execute_script("""
            const video = document.querySelector('video');
            if (video) {
                video.muted = false;
                video.play();
            }
        """)
        log.info("Video unmuted and playback started.")
    except Exception as e:
        log.warning(f"Failed to trigger video playback: {e}")

    return driver


# ⏩ Try to skip YouTube ads
def skip_ads(driver):
    try:
        # Skip skippable ads
        skip_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "ytp-skip-ad-button"))
        )
        skip_button.click()
        log.info("Skipped video ad.")
        time.sleep(random.uniform(1.5, 2.5))
    except (NoSuchElementException, TimeoutException):
        pass
    except Exception as e:
        log.warning(f"Error clicking skip button: {e}")

    # Close overlay ads
    try:
        overlay_close = driver.find_element(
            By.CLASS_NAME, "ytp-ad-overlay-close-button"
        )
        overlay_close.click()
        log.info("Closed overlay ad.")
        time.sleep(random.uniform(0.5, 1.0))
    except NoSuchElementException:
        pass


# 🧠 Main logic
def main():
    log.info("Killing any old ChromeDriver processes...")
    kill_chromedriver_processes()

    driver = start_browser()

    try:
        log.info("Watching for ads... Press Ctrl+C or close browser to exit.")
        while True:
            try:
                skip_ads(driver)
                time.sleep(random.uniform(0.8, 1.2))
            except WebDriverException:
                log.warning("Browser crash or closed. Restarting...")
                try:
                    driver.quit()
                except Exception:
                    pass
                kill_chromedriver_processes()
                driver = start_browser()
    except KeyboardInterrupt:
        log.info("Stopped by user.")
    finally:
        try:
            driver.quit()
        except Exception:
            pass
        log.info("Browser session ended.")


# 🚦 Entry point
if __name__ == "__main__":
    main()
