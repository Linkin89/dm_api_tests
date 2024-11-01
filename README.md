# dm_api_tests

Набор автотестов для тестирования API системы DM. Проект построен на принципах модульного и независимого тестирования API, что позволяет легко добавлять новые тесты и поддерживать существующие.

## 🛠 Технологии и инструменты

<p align="center">
  <img src="https://img.shields.io/badge/python-3.11-blue?logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/pytest-7.4.3-blue?logo=pytest&logoColor=white"/>
  <img src="https://img.shields.io/badge/requests-2.31-blue?logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Allure-2.24-yellow?logo=qameta&logoColor=white"/>
  <img src="https://img.shields.io/badge/Pydantic-2.5-blue?logo=pydantic&logoColor=white"/>
</p>

## 📑 Описание проекта

Проект реализует тесты для проверки различных эндпоинтов API системы, в том числе для верификации корректности работы сервера и функционала системы. Структура кода организована для обеспечения легкости чтения и поддержки.

## 🏗 Паттерны проектирования

В проекте используются следующие паттерны:

| Паттерн | Применение |
|---------|------------|
| **Page Object** | Отделение логики тестов от деталей взаимодействия с API |
| **Builder** | Создание сложных объектов данных для тестов |
| **Singleton** | Настройка единого API-клиента |
| **Adapter** | Интеграция с внешними библиотеками |
| **Decorator** | Добавление дополнительного функционала (логирование) |

## 📋 Тестовые сценарии

<details>
<summary><b>Регистрация и авторизация</b></summary>

- ✓ Успешная регистрация нового пользователя
- ✓ Авторизация существующего пользователя
- ✓ Проверка невалидных данных при авторизации
</details>

<details>
<summary><b>Профиль пользователя</b></summary>

- ✓ Получение данных профиля
- ✓ Обновление информации профиля
</details>

<details>
<summary><b>Управление данными</b></summary>

- ✓ Создание новых записей
- ✓ Редактирование существующих записей
- ✓ Удаление записей
- ✓ Проверка валидации данных
</details>

<details>
<summary><b>API интеграции</b></summary>

- ✓ Проверка форматов ответов
- ✓ Обработка ошибок
- ✓ Проверка лимитов запросов
</details>

## 🔄 Непрерывная интеграция

Проект настроен для работы с GitHub Actions. При каждом пуше в main ветку:

- Запускаются все тесты
- Генерируется отчет Allure
- Проверяется качество кода (линтеры)

## 🚀 Запуск тестов

```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск всех тестов
pytest

# Генерация отчета
allure serve allure-results
```

## 📊 Отчеты Allure

<p align="center">
  <img src="path_to_your_allure_screenshot.png" width="80%">
</p>

---

**Автор:** [Linkin89](https://github.com/Linkin89)

