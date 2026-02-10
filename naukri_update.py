import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def update_naukri():
    options = Options()
    # While testing on your Acer Aspire 7, keep headless OFF to see what happens
    options.add_argument("--headless") 
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 15) # Wait up to 15 seconds for elements

    try:
        print("Opening Naukri Login...")
        driver.get("https://www.naukri.com/nlogin/login")

        # 1. Enter Email - Using placeholder text (more stable than ID)
        email_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Email')]")))
        email_input.send_keys(os.environ['NAUKRI_EMAIL'])

        # 2. Enter Password
        pass_input = driver.find_element(By.XPATH, "//input[@type='password']")
        pass_input.send_keys(os.environ['NAUKRI_PASSWORD'])

        # 3. Click Login
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        print("Logged in successfully!")

      # 4. Navigate to Profile
        time.sleep(5)
        driver.get("https://www.naukri.com/mnjuser/profile")
        print("Profile page loaded...")

        # 5. Click the Edit button inside the lazyResumeHead container
        # Your HTML shows: <div id="lazyResumeHead"> ... <span class="edit icon">editOneTheme</span>
        try:
            # We target the span inside the specific Resume Headline div
            edit_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#lazyResumeHead span.edit.icon")))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit_btn)
            time.sleep(1)
            edit_btn.click()
            print("Resume Headline edit opened!")
        except:
            # Fallback using the 'editOneTheme' text found in your HTML
            print("CSS Selector failed, trying text-based fallback...")
            edit_btn = driver.find_element(By.XPATH, "//div[@id='lazyResumeHead']//span[text()='editOneTheme']")
            driver.execute_script("arguments[0].click();", edit_btn)

        # 6. The Textarea logic
        # After clicking edit, Naukri usually opens a textarea with ID 'resumeHeadlineTxt'
        headline_textarea = wait.until(EC.presence_of_element_located((By.ID, "resumeHeadlineTxt")))
        current_text = headline_textarea.get_attribute("value")
        
        # Toggle a dot at the end
        new_text = current_text[:-1] if current_text.endswith(".") else current_text + "."
        
        headline_textarea.clear()
        headline_textarea.send_keys(new_text)

        # 7. Find the Save button in the drawer that just opened
        # Naukri's save buttons in these drawers usually have a specific class or text
        save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Save']")))
        save_btn.click()
        print("Profile updated successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        time.sleep(2)
        driver.quit()

if __name__ == "__main__":
    update_naukri()