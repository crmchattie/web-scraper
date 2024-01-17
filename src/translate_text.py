import requests
from src.helpers import truncate_string

def translate_text(text, source_lang="auto", target_lang="en"):
    url = "http://localhost:5000/translate"
    payload = {
        "q": text,  # Optionally truncate before translation
        "source": source_lang,
        "target": target_lang,
        "format": "text"
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return truncate_string(response.json().get("translatedText"))
        else:
            print(f"Translation error: {response.status_code}")
            return text
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return text