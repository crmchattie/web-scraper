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
   ```shell
   git clone https://github.com/crmchattie/web-scraper.git

2. **Navigate to the Project Directory**:  
   ```shell
   cd web-scraper

3. **Install Dependencies**:  
   ```shell
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
- See next step or follow the installation guide for Ollama and the Mistral model available [here](https://www.markhneedham.com/blog/2023/10/03/mistral-ai-own-machine-ollama/).

## Download the tool Ollama
- Download is available [here](https://www.markhneedham.com/blog/2023/10/03/mistral-ai-own-machine-ollama/#:~:text=a%20tool%20called-,Ollama,-.%20We%E2%80%99ll%20choose%20the).

## Download the LLM from Ollama
- Execute the command:
  ```shell
  ollama run mistral:latest

# Running the Application

## Navigate to local repository
- Navigate to wherever you saved the local repository:
  ```shell
  cd web-scraper

## Activate Virtual Environment
- Activate your virtual environment:
  ```shell
  .venv/bin/activate

## First time:
- Run Flask on localhost in order to authenticate with the Google Console.
  ```shell
  flask run --port=5001
- After successfully authenticating, you can skip this step.
- Note, this is run on port 5001 because libretaranslation will be run on port 5000

## Set-up libretranslate:
- In a separate terminal window, repeat steps 1 and 2 above and then run libretranslate on localhost:5000
  ```shell
  libretranslate
-  Note you should have two terminal windows open now

## Set-up LLM:
- In another separate terminal window, run ollama run mistral
  ```shell
  ollama run mistral
- Note you should have three terminal windows open now

## Run the Script:
- Execute the following command in the terminal window you first created
  ```shell
  python app.py
