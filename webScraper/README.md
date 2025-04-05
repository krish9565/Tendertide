# TenderTide 🌀  
**Automated Tender Aggregator and Publisher**

TenderTide is a Django-based web application that automatically scrapes and aggregates tender information from various public procurement and government websites. The collected data is published on the TenderTide platform for easy access and monitoring.

---

## 🔍 Features

- **Automated Scraping**: Fetches tender data using `BeautifulSoup`, `Selenium`, and public REST APIs.
- **Multi-source Support**: Handles both static and JavaScript-rendered websites.
- **Scheduled Updates**: Periodically updates tenders to keep data fresh and relevant.
- **MongoDB Integration**: Stores tender data using MongoDB for fast, flexible querying.
- **Centralized Dashboard**: All fetched tenders are displayed on a user-friendly website.

---

## 🛠 Tech Stack

- **Backend**: Django (Python)
- **Database**: MongoDB
- **Scraping Tools**: BeautifulSoup, Selenium
- **Other**: REST APIs, Cron jobs (or `Celery` if used)

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- MongoDB
- ChromeDriver (for Selenium)
- Virtualenv (recommended)

### Installation

1. **Clone the repository:**

```bash
git clone https://github.com/your-username/TenderTide.git
cd TenderTide


Create and activate a virtual environment:

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt


Set up MongoDB connection in settings.py:

python
Copy
Edit
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'your-db-name',
    }
}

Run migrations and start server:

bash
Copy
Edit
python manage.py migrate
python manage.py runserver

Contributions
Contributions, issues, and suggestions are welcome! Feel free to open a pull request or issue.

vbnet
Copy
Edit

Let me know if you want to include images/screenshots or badges (build, license, etc.) too!