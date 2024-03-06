from datetime import datetime
from random import randint

from requests import post, get, delete, put

BASE_URL = "http://127.0.0.1:8080"

# Тестирование ответа сервера
print(get(f'{BASE_URL}/api/jobs').json())  # Тест - Получение всех работ.
print(get(f'{BASE_URL}/api/jobs/1').json())  # Тест - Корректное получение одной работы.
print(get(f'{BASE_URL}/api/jobs/999').json())  # Тест - Ошибочный запрос на получение одной работы — неверный id.
print(get(f'{BASE_URL}/api/jobs/s').json())  # Тест - Ошибочный запрос на получение одной работы — строка.

# Тестирование POST-запроса
data1 = {
    "team_leader_id": 999,
    "job": "Working hard",
    "work_size": 100,
    "collaborators": "1, 2, 3",
    "start_date": datetime.now().isoformat(),
    "end_date": None,
    "is_finished": False
}
print(post(f"{BASE_URL}/api/jobs",
           json=data1).json())  # Тест - Ошибочный запрос на cоздание работы - не существующий в БД team_leader_id

data2 = {
    "team_leader_id": 4,
    "job": "Working hard",
    "work_size": 100,
    "collaborators": "1, 2, 3",
    "start_date": datetime.now().isoformat(),
}
print(post(f"{BASE_URL}/api/jobs",
           json=data2).json())  # Тест - Ошибочный запрос на cоздание работы - отсутствует поле is_finished

print(post(f"{BASE_URL}/api/jobs", json={}).json())  # Тест - Ошибочный запрос на cоздание работы - запрос пустой

data3 = {
    "team_leader_id": 4,
    "job": "Test working",
    "work_size": 100,
    "collaborators": "1, 2, 3",
    "start_date": datetime.now().isoformat(),
    "end_date": None,
    "is_finished": False,
    "categories": [1]
}
print(post(f"{BASE_URL}/api/jobs", json=data3).json())  # Тест - корректное создание работы. В ответе id работы

print(get(f"{BASE_URL}/api/jobs").json())  # Тест - получение всех работ для проверки создания новой работы

# Тестирование удаления
print(delete(f"{BASE_URL}/api/jobs/999").json())  # Тест - Ошибочный запрос на удаление работы — несуществующий id
print(delete(f"{BASE_URL}/api/jobs/s").json())  # Тест - Ошибочный запрос на удаление работы — неверный id
print(delete(f"{BASE_URL}/api/jobs/5").json())  # Тест - Корректный запрос на удаление работы

print(get(f"{BASE_URL}/api/jobs").json())  # Тест - получение всех работ для проверки удаления

# Тестирование редактирования
print(put(f"{BASE_URL}/api/jobs/999",
          json={}).json())  # Тест - Ошибочный запрос на редактирование работы — несуществующий id
print(put(f"{BASE_URL}/api/jobs/s", json={}).json())  # Тест - Ошибочный запрос на редактирование работы — неверный id

data4 = {
    "id": 2,
    "team_leader_id": 4,
    "job": "Working hard",
    "work_size": randint(1, 100),
    "collaborators": "1, 2, 3",
    "start_date": datetime.now().isoformat(),
    "end_date": None,
    "is_finished": False
}
print(put(f"{BASE_URL}/api/jobs/2", json=data4).json())  # Тест - Корректный запрос на редактирование работы

print(get(f"{BASE_URL}/api/jobs").json())  # Тест - получение всех работ для проверки редактирования
