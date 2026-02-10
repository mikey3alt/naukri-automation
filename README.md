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
