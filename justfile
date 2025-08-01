# use PowerShell instead of sh:
set shell := ["powershell.exe", "-c"]

set dotenv-load := true

username:=env('DJANGO_SUPERUSER_USERNAME')
email:=env('DJANGO_SUPERUSER_EMAIL')
password:=env('DJANGO_SUPERUSER_PASSWORD')

default:
    echo 'Hello, world!'

test:
    pytest

serve: manage
    runserver

manage *ARGS:
    python backend/manage.py {{ARGS}}

createsuperuser: manage
    createsuperuser --noinput --username {{username}} --email {{email}} --password {{password}}

migrate: manage
    migrate