# Current Update about this project 

this pipeline is faiing via github actions. but running perfectly fine in local. Because the GitHub Action runner uses a data center IP address that Naukri doesn't recognize as mine. Even though my credentials are correct, they are blocking the login until an OTP is entered to verify it's really me, Harsh.

Naukri is very aggressive about bot detection. If they see too many login attempts from different GitHub IP addresses, they might temporarily lock my account. So dropping this project.
It could have been solved by Using Selenium Cookies which is the recommended method for bypassing otps.

---

# 🚀 Naukri Profile Auto-Updater

This repository contains a **Python-based automation tool** designed to keep a [Naukri.com](https://www.naukri.com) profile "fresh" in recruiter search results. By automating a minor update to the "Resume Headline" daily, the script ensures the profile timestamp is always current, significantly increasing visibility during active job searches.

---

## 🛠 Features

* **Automated Daily Updates:** Integrated with **GitHub Actions** to run every morning at 9:00 AM IST (03:30 UTC).
* **Headless Browser Execution:** Utilizes Selenium in headless mode for efficient, server-side performance.
* **Secure Credential Management:** Leverages **GitHub Repository Secrets** to handle sensitive login data.
* **Smart Content Toggling:** Logic-based update that toggles a trailing character (space or dot) to trigger the status without visibly changing your headline.

---

## 🏗 Tech Stack

* **Python 3.10+**
* **Selenium WebDriver:** For web automation and DOM interaction.
* **GitHub Actions:** For cloud scheduling and workflow automation.
* **Webdriver-Manager:** To handle Chrome driver binaries automatically.

---

## 📂 Project Structure

```text
├── .github/
│   └── workflows/
│       └── main.yml        # Automation schedule & CI/CD config
├── naukri_update.py        # Core Python automation logic
├── requirements.txt        # Python dependency list
└── README.md               # Project documentation

