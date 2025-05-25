
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
import os
import time

def scrape_nykaa():
    offers = []

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    service = Service(executable_path="drivers/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get("https://www.nykaa.com/nykaa-coupon-offer")
        time.sleep(5)  # Let JS content load

        # Use fallback selector: all images inside links
        banner_imgs = driver.find_elements(By.CSS_SELECTOR, ".product-base")

        print(f"Found {len(banner_imgs)} potential banners")

        for img in banner_imgs:
            try:
                parent_link = img.find_element(By.XPATH, "..")
                href = parent_link.get_attribute("href")
                alt_text = img.get_attribute("alt") or "offer"

                if href and "nykaa.com" in href:
                    offers.append({
                        "title": alt_text,
                        "description": "Banner offer from nykaa",
                        "brand": "nykaa",
                        "offer_link": href,
                        "expiry_date": None
                    })
            except Exception as e:
                print("Skipping due to error:", e)
                continue

    finally:
        driver.quit()

    return offers


if _name_ == "_main_":
    offers = scrape_nykaa()
    os.makedirs("data", exist_ok=True)
    with open("data/nykaa_offers.json", "w", encoding="utf-8") as f:
        json.dump(offers, f, indent=2, ensure_ascii=False)

    print(f"✅ Scraped {len(offers)} offers from nykaa.")
