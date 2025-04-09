# Kaspersky_Validator
tests and validation for config 

## Быстрый Старт
1. Распакуйте проект

2. Создайте и активируйте виртуальное окружение
`python -m venv venv`
`source venv/bin/activate`

 3. Установите зависимости
`pip install -r requirements.txt`

4. Cоздайте переменную окружения `CONFIG_PATH` с помощью `export CONFIG_PATH=./config/config.ini`
или будет использован путь по умолчанию `/var/opt/kaspersky/config.ini`

5. Запустите тесты из корня проекта
`coverage run -m pytest`
`coverage report`



## Quick Start
1. Unpack archived project

2. Create virtual environment and Activate it
`python -m venv venv`
`source venv/bin/activate`

3. Install requirements `pip install -r requirements.txt`

4. Create virtual environment variable `CONFIG_PATH` with `export CONFIG_PATH=./config/config.ini`
or default path is going to be used `/var/opt/kaspersky/config.ini`

5. run tests with coverage from content root 
`coverage run  -m pytest`
`coverage report`.
