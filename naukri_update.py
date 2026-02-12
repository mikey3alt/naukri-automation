import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

def update_naukri():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 20)
    actions = ActionChains(driver)

    try:
        print("Opening Naukri Login...")
        driver.get("https://www.naukri.com/nlogin/login")

        # 1. Login
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Email')]"))).send_keys(os.environ['NAUKRI_EMAIL'])
        driver.find_element(By.XPATH, "//input[@type='password']").send_keys(os.environ['NAUKRI_PASSWORD'])
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        
        wait.until(EC.url_contains("naukri.com"))
        print("Logged in!")

        # 2. Go to Profile
        time.sleep(3)
        driver.get("https://www.naukri.com/mnjuser/profile")
        
        # Scroll to ensure element is rendered
        driver.execute_script("window.scrollTo(0, 500);")
        time.sleep(2)

        # 3. Open the Headline Drawer
        # Based on your previous error, we target the specific Headline section span
        edit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'resumeHeadline')]//span[contains(@class, 'edit')]")))
        driver.execute_script("arguments[0].click();", edit_btn)
        print("Headline drawer opened!")

        # 4. Handle the New AI-TextArea (The tricky part)
        textarea = wait.until(EC.visibility_of_element_located((By.ID, "resumeHeadlineTxt")))
        
        # Get current text
        current_text = textarea.get_attribute("value")
        new_text = current_text[:-1] if current_text.endswith(".") else current_text + "."

        # INSTEAD OF .clear(), we simulate manual keyboard entry to trigger React listeners
        textarea.click()
        time.sleep(1)
        # Select all (Ctrl+A) and Delete
        actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).perform()
        time.sleep(1)
        # Type the new text
        textarea.send_keys(new_text)
        print(f"Text updated via Keyboard simulation.")

        # 5. Click the Save Button
        # Your HTML shows: <button class="btn-dark-ot" type="submit">Save</button>
        # inside <form name="resumeHeadlineForm">
        save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//form[@name='resumeHeadlineForm']//button[@type='submit' and text()='Save']")))
        
        # Move to button and click via JS to ensure it registers
        driver.execute_script("arguments[0].scrollIntoView(true);", save_btn)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", save_btn)
        
        print("Save button clicked successfully!")
        time.sleep(5) # Crucial: Wait for the AJAX save to finish before driver.quit()

    except Exception as e:
        print(f"Error: {e}")
        driver.save_screenshot("naukri_error.png")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    update_naukri()