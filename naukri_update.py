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
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Bypass bot detection flag
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    wait = WebDriverWait(driver, 30) # Increased timeout for cloud runner
    actions = ActionChains(driver)

    try:
        print("Opening Naukri Login...")
        driver.get("https://www.naukri.com/nlogin/login")

        # Login
        email_el = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Email')]")))
        email_el.send_keys(os.environ['NAUKRI_EMAIL'])
        
        driver.find_element(By.XPATH, "//input[@type='password']").send_keys(os.environ['NAUKRI_PASSWORD'])
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        
        # Verify Login Success by waiting for a dashboard element
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "nLogo")))
        print("Logged in!")

        time.sleep(5)
        print("Navigating to Profile...")
        driver.get("https://www.naukri.com/mnjuser/profile")
        
        # Hard wait for profile load
        time.sleep(10) 

        # NUCLEAR OPTION: Trigger the Edit Headline Drawer via JavaScript
        # This bypasses the need to 'find' and 'click' the pencil icon
        print("Triggering Headline Drawer via JS...")
        driver.execute_script("document.querySelector('.resumeHeadline .edit').click();")
        
        # Wait for the textarea in the drawer
        textarea = wait.until(EC.visibility_of_element_located((By.ID, "resumeHeadlineTxt")))
        
        current_text = textarea.get_attribute("value")
        if not current_text: # Fallback if value is empty
             current_text = "Fullstack Developer (TCS) | 2.5 Years Exp | Expert in Angular & JavaScript | Serving Notice Period"
             
        new_text = current_text[:-1] if current_text.endswith(".") else current_text + "."

        # Clear and Type
        textarea.click()
        actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).perform()
        time.sleep(2)
        textarea.send_keys(new_text)
        print(f"Text updated.")

        # Save using the btn-dark-ot class found in your HTML
        save_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "form[name='resumeHeadlineForm'] button.btn-dark-ot")))
        driver.execute_script("arguments[0].click();", save_btn)
        
        print("Save clicked!")
        time.sleep(10) # Essential to let the POST request finish

    except Exception as e:
        print(f"Error occurred: {e}")
        driver.save_screenshot("error_state.png")
        # Log the page source to see if we got blocked
        with open("page_source.html", "w") as f:
            f.write(driver.page_source)
    
    finally:
        driver.quit()

if __name__ == "__main__":
    update_naukri()
