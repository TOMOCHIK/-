import requests

def get_text(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            text = response.text
            if len(text) > 100000:  # ограничение на размер текста, например, 100000 символов
                return False, "Текст слишком большой для обработки"
            return True, text
        else:
            return False, "Ошибка при получении URL"
    except Exception as e:
        return False, str(e)