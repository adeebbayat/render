from flask import Flask, jsonify
from playwright.sync_api import sync_playwright

URL = "https://www.google.com/maps/place/JOHN+REED+Fitness/@34.0179334,-118.5018669,17z/data=!3m1!4b1!4m6!3m5!1s0x80c2a51ac01a5329:0xba6023a331bcc867!8m2!3d34.017929!4d-118.499292!16s%2Fg%2F11v0kc0bdc"

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "Gym busyness API is running."})

@app.route("/busyness")
def busyness():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        page = browser.new_page()
        page.goto(URL, wait_until="domcontentloaded")

        selector = "div[role='img'][aria-label^='Currently']"
        page.wait_for_selector(selector, timeout=15000)
        busy_div = page.query_selector(selector)
        aria_label = busy_div.get_attribute("aria-label") if busy_div else "Not found"
        browser.close()

    return jsonify({"busyness": aria_label})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
