import os
import time
import sys
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
    
    # Essential for GitHub Actions
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Stealth: Hide that this is a bot
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Further hide Selenium
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    wait = WebDriverWait(driver, 30)
    actions = ActionChains(driver)

    try:
        print("Step 1: Opening Naukri Login...")
        driver.get("https://www.naukri.com/nlogin/login")

        # 1. Login
        email_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Email')]")))
        email_field.send_keys(os.environ['NAUKRI_EMAIL'])
        
        driver.find_element(By.XPATH, "//input[@type='password']").send_keys(os.environ['NAUKRI_PASSWORD'])
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        
        # Verify Login by waiting for a dashboard element
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "nLogo")))
        print("Step 2: Logged in successfully!")

        # 2. Go to Profile
        time.sleep(5)
        print("Step 3: Navigating to Profile...")
        driver.get("https://www.naukri.com/mnjuser/profile")
        
        # Hard wait for lazy-load elements (Crucial for GitHub runners)
        time.sleep(10) 

        # 3. Open Headline Drawer (Using JS to avoid element interception)
        print("Step 4: Triggering Headline Drawer...")
        driver.execute_script("document.querySelector('.resumeHeadline .edit').click();")
        
        # 4. Handle the AI-TextArea
        textarea = wait.until(EC.visibility_of_element_located((By.ID, "resumeHeadlineTxt")))
        
        current_text = textarea.get_attribute("value")
        # Ensure we don't clear it if it's empty (failsafe)
        if not current_text:
            current_text = "Fullstack Developer | Angular & JavaScript Expert"
            
        new_text = current_text[:-1] if current_text.endswith(".") else current_text + "."

        # Force React/Vue to recognize change via Keyboard simulation
        textarea.click()
        time.sleep(1)
        actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).perform()
        time.sleep(2)
        textarea.send_keys(new_text)
        print(f"Step 5: Text modified to: {new_text}")

        # 5. Save Button
        # We target the specific button inside the form name you provided
        save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//form[@name='resumeHeadlineForm']//button[@type='submit' and text()='Save']")))
        driver.execute_script("arguments[0].click();", save_btn)
        
        print("Step 6: Save button clicked!")
        
        # Essential: Give the server time to process the POST request
        time.sleep(10) 
        print("Update Completed!")

    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        driver.save_screenshot("error_state.png")
        # Log the HTML to check if we hit a Captcha/Bot wall
        with open("page_dump.html", "w", encoding='utf-8') as f:
            f.write(driver.page_source)
        # Signal failure to GitHub Actions
        sys.exit(1)
    
    finally:
        driver.quit()

if __name__ == "__main__":
    update_naukri()
