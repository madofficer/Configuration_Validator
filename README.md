# Kaspersky_Validator
tests and validation for config 

## Быстрый Старт
1. Распакуйте проект
2. Создайте и активируйте виртуальное окружение
`python -m venv venv`
   1. Linux `source venv/bin/activate`
   2. Windows `venv\Scripts\activate`

 3. Установите зависимости
`pip install -r requirements.txt`

4. Cоздайте переменную окружения `CONFIG_PATH` или файл `.env`,
а затем раскомментируйте 3 и 13 строки в файле `framework/config.py`
5. Запустите тесты
`coverage run -m pytest`
`coverage report`



## Quick Start
1. Unpack archived project
2. Create virtual environment `python -m venv venv`
3. Activate venv by `source venv/bin/activate`
4. Install requirements `pip install -r requirements.txt`
5. create virtual environment variable `CONFIG_PATH` or create `.env`,
then uncomment 3 and 13 lines in `framework/config.py`
6. run tests with coverage from content root: `coverage run  -m pytest`, to see report run `coverage report`.
