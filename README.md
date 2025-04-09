# Kaspersky_Validator
tests and validation for config 

1. Unpack archived project
2. Create virtual environment `python -m venv venv`
3. Activate venv by `source venv/bin/activate`
4. Install requirements `pip install -r requirements.txt`
5. create virtual environment variable `CONFIG_PATH` or you are also able to create `.env`,
then uncomment 3 and 13 lines in `framework/config.py`


3. run tests with coverage from content root: `coverage run  -m pytest`, to see report run `coverage report`.
