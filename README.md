Naukri Profile Auto-Updater 🚀
This project automates the process of updating a Naukri.com profile daily. By making a minor, non-destructive change to the "Resume Headline," the script triggers Naukri's search algorithm to mark the profile as "Updated Today," keeping it at the top of recruiter search results.

🛠 Features
Daily Automation: Powered by GitHub Actions to run every morning at 9:00 AM IST.

Headless Execution: Runs in a virtual browser environment without needing a physical screen.

Security First: Uses GitHub Secrets to securely store credentials; no passwords are saved in the code.

Smart Toggling: Toggles a trailing space or dot in the headline to ensure a "change" is detected without altering your professional content.

🏗 Tech Stack
Python 3.x

Selenium WebDriver: For web automation and browser interaction.

GitHub Actions: For cloud scheduling and CI/CD.

Webdriver-Manager: To handle browser driver binaries automatically.

🚀 Setup & Installation
1. Local Development
To test the script on your machine (e.g., your Acer Aspire 7):

Clone the repository.

Install dependencies:

Bash
pip install -r requirements.txt
Set temporary environment variables for testing:

DOS
set NAUKRI_EMAIL=your@email.com
set NAUKRI_PASSWORD=yourpassword
Run the script:

Bash
python naukri_update.py
2. GitHub Actions Deployment
Push this code to a Private GitHub repository.

Navigate to Settings > Secrets and variables > Actions.

Add the following Repository Secrets:

NAUKRI_EMAIL: Your Naukri login email.

NAUKRI_PASSWORD: Your Naukri password.

The workflow is configured to run automatically at 03:30 UTC (9:00 AM IST) daily.

📂 Project Structure
Plaintext
├── .github/
│   └── workflows/
│       └── main.yml        # GitHub Actions schedule configuration
├── naukri_update.py        # Main Python automation script
├── requirements.txt        # List of Python dependencies
└── README.md               # Project documentation
⚠️ Disclaimer
This project is for educational purposes. Automated interaction with Naukri.com may violate their Terms of Service. Use responsibly and avoid high-frequency updates to prevent account flagging.
