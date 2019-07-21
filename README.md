# Form Wizard
Custom form creation and management wizard, written in Django

setup:

1. move into project folder
2. $ pyhton3 -m venv venv
2. $ source venv/bin/activate
3. $ pip install -r requirements.txt
4. add the following line to wix_form_builder/settings.py:
SECRET_KEY = 'gjli4h6k1#zsxw%)xsb)#5)0i-+u4xz48hke-+_n%$ep6ms_io'

5. $ python3 manage.py migrate
6. $ python3 manage.py runserver
7. in your browser go to: localhost:8000/form_builder
