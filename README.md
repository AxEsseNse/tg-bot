# axessense-tg-bot
Portfolio Public tg bot 

## Содержание
- [Инструкция по установке](#инструкция-по-установке)
- [Запуск](#запуск)
- [Проверка линтером](#проверка-линтером)

## Инструкция по установке

1. Откройте терминал.
2. Создайте папку для проекта и перейдите в неё:

    ```sh
    mkdir test-sinitskiy
    cd test-sinitskiy
    ```

3. Скачайте репозиторий:

    ```sh
    git clone https://github.com/AxEsseNse/tg_bot.git
    cd async-downloader
    ```

4. Создайте виртуальное окружение:

    ```sh
    python -m venv venv
    ```

5. Активируйте виртуальное окружение:

    ```sh
    .\.venv\Scripts\Activate.ps1  # для Windows PowerShell
    source venv/bin/activate  # для Unix
    ```

6. Установите зависимости:

    ```sh
    pip install -r requirements.txt
    ```

## Запуск

1. Запуск скрипта.

    ```sh
    python app.py
    ```

## Проверка линтером

1. Проверка flake8

    ```sh
    flake8 .
    ```
