# 💵 Django-проект: «Курс USD к RUB»

## 🧭 Описание

API-эндпоинт [`/get-current-usd/`](http://localhost:8000/get-current-usd/) возвращает:
- **Актуальный курс USD → RUB**
- **Историю из 10 последних запросов**

Данные берутся с внешнего API [exchangerate.host](https://api.exchangerate.host/)  
(запросы не чаще **1 раза в 10 секунд** — ограничение по ТЗ).

---

## 📚 Блок вопросов и оценка времени

- 🧩 [Подзадачи (Task Breakdown)](docs/TASK_BREAKDOWN.md)  
- ❓ [Вопросы к PM и TL](docs/QUESTIONS.md)  
- ⏱ [Оценка времени (Time Estimates)](docs/TIME_ESTIMATES.md)

---

## 🚀 Запуск проекта

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
python manage.py test currency
```

После запуска открой в браузере:  
👉 [http://localhost:8000/get-current-usd/](http://localhost:8000/get-current-usd/)

---

## 🛠 Используемые технологии

- **Django 5**
- **requests**
- **SQLite** (по умолчанию)
- **Flake8** (по умолчанию)
