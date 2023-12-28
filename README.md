# Web Scraper

## Description
Web Scraper is a desktop application designed for scraping and analyzing web content. It integrates with Selenium, BeautifulSoup, Libretranslation, Mistral's LLM and Google Sheets API with OAuth credentials in order to do that.

## Getting Started

### Prerequisites
- Python 3.9+
- Pip (Python package manager)
- A Google account with access to Google Cloud Platform
- Internet access for setup and operation
- Download Ollama and the Mistral model

### Installation
1. **Clone the Repository**:  
   ```bash
   git clone https://github.com/crmchattie/web-scraper.git

2. **Navigate to the Project Directory**:  
   ```bash
   cd web-scraper

3. **Install Dependencies**:  
   ```bash
   pip install -r requirements.txt

# Google Cloud and OAuth Setup

## Google Cloud Project:
- Create a new project on [Google Cloud Console](https://console.cloud.google.com/).
- Enable the Google Sheets and Google Drive APIs for your project.

## OAuth Credentials:
- In the Google Cloud Console, navigate to "APIs & Services" > "Credentials".
- Create credentials for a desktop application and download the `credentials.json` file.
- Place `credentials.json` in your project's root directory.

# Ollama and Mistral AI Model
- Follow the installation guide for Ollama and the Mistral model available [here](https://www.markhneedham.com/blog/2023/10/03/mistral-ai-own-machine-ollama/).

# Running the Application
## Activate Virtual Environment
- Activate your virtual environment before running the application:
  ```shell
  .venv/bin/activate
## First time:
- Run Flask on localhost in order to authenticate with the Google Console.
- After successfully authenticating, you can skip this step.
- Note, this is run on port 5001 because libretaranslation will be run on port 5000
  ```shell
  flask run --port=5001
## Set-up libretranslation:
- In a separate terminal window, run libretranslation on localhost:5000
  ```shell
  libretranslate
## Execute the Script:
  ```shell
  python app.py
