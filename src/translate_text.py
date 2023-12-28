import requests

def translate_text(text, source_lang, target_lang):
    url = "http://localhost:5000/translate"
    payload = {
        "q": text,
        "source": source_lang,
        "target": target_lang,
        "format": "text"
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json().get("translatedText")
    else:
        return text
