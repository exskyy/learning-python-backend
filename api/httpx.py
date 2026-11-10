import httpx

url = "https://pypi.org/pypi/requests/2.32.3/json"  
HEADERS = {"User-Agent": "MyApp/1.0"}  # Заголовки запроса
def fetch_data(url, params=None):
    try:
        response = httpx.get(url, params=params, headers=HEADERS, timeout=httpx.Timeout(10.0, connect=5.0), follow_redirects=True)  # Устанавливаем таймауты для запроса
        print(response.status_code)
        response.raise_for_status()  # Проверяем статус ответа, выбрасываем исключение при ошибке
        return response.json()  # Возвращаем JSON-данные
    except httpx.TimeoutException as e:
        print("Сервер долго отвечал:", e)
        return None
    except httpx.HTTPStatusError as e:
        print("Сервер ответил ошибкой:", e.response.status_code)
        return None
    except httpx.RequestError as e:
        print("Ошибка запроса:", e)
        return None   
    except ValueError as e:
        print("Ошибка при обработке JSON:", e)
        return None
print("Начинаем запрос к серверу...")
print("URL:", url)

data = fetch_data(url, params={"q": "python", "page": 1})
if data is not None:
    print(data["info"]["version"])
else:
    print("Не удалось получить данные с сервера, но программа продолжает работу.")