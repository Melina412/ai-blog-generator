## tailwind ohne frontend framework

### 1. CDN

- sehr einfache und schnelle methode, keine installation erforderlich
- script tag in html head einfügen : `<script src="https://cdn.tailwindcss.com"></script>`
- eignet sich gut für development, aber nicht für produktion
- problem: ohne installation funktioniert die tailwind intellisense erweiterung nicht, man bekomt also keine vorschläge für die klassen. wenn man tailwind nicht auswendig kann, ist es ziemlich ätzend. dann geht installation am ende doch schneller

### 2. tailwind CLI

- npm i -D tailwindcss
- tailwind.config.js erstellen
- input.css file erstellen und hier @tailwind base; @tailwind components; @tailwind utilities; rein packen
- output.css im html als stylesheet verlinken
- tailwind build compiler starten mit dem command:
  `npx tailwindcss -i <path>/input.css -o <path>/output.css --watch`
  -- minify um den code auf eine zeile zu beschränken
  zb.: npx tailwindcss -i ./src/style/input.css -o ./src/style/output.css -- minify --watch

(es ist trotzdem noch viel zu viel css code wtf tailwind?)

## django

⚠️ vs code hat scheinbarbar ziemliche probleme mit der venv, wenn sie sich in einem unerordner des projekts befindet. man muss den ordner in dem die venv erstellt wurde als untersten ordner im arbeitsbereich öffnen und immer sicher stellen, dass der richtige interpreter, in dem fall `Python 3.12.2 ('env':venv) ./env/bin/python` ausgewählt ist, BEVOR man die packages installiert. sonst bekommt man bei allen importen fehler von pylance angezeigt, weil die importe nicht aufgelöst werden können.

### django project setup

- package installieren `pip install Django==5.0.6`
- projekt erstellen `django-admin startproject project_name` (ai_blog_app)
- in den ersten ordner wechseln `cd project_name` (es wird noch ein unterordner mit dem gleichen namen erstellt)
- app erstellen `python3 manage.py startapp app_name` (blog_generator)

```py
# (unterordner)ai_blog_app -- settings.py
# 'blog_generator' hinzufügen

INSTALLED_APPS = [
    'blog_generator'
]
```

```py
# (unterordner)blog_generator
# neue file urls.py erstellen
# denke das ist liste mit urls für routing ?!

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index')
]
```

```py
# (unterordner)blog_generator -- views.py

from django.shortcuts import render

# Create your views here.
def index(request):
    pass
```

```py
# (unterordner)ai_blog_app -- urls.py
# das ist das routing vom main prpoject, hier muss man die route angeben wo django nach der page suchen soll

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog_generator.urls'))
]
```

- neuen ordner 'templates' erstellen
- hier werden die html files rein kopiert (lol?)

```py
# (unterordner)ai_blog_app -- settings.py
# [BASE_DIR, 'templates'] ergänzen

TEMPLATES = [
    {
        'DIRS': [BASE_DIR, 'templates'],
    },
]
```

- ich versuche erst mal die files so direkt aus dem frontend einzubinden. ka ob das so richtig ist, hoffe da gibts keine probleme beim deployment :/

```py
# (unterordner)ai_blog_app -- settings.py

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent.parent
CSS_DIR = PROJECT_DIR / 'frontend' / 'src' / 'style'

TEMPLATES = [
    {
        'DIRS': [BASE_DIR, '.././frontend/src'],
    },
]

STATICFILES_DIRS = [
    CSS_DIR,
]
```

```html
<!-- in den html files: -->
<head>
  {% load static %}
  <link href="{% static 'output.css' %}" rel="stylesheet" />
</head>
```

also die richtige variante laut django docs wäre im app folder sowohl den templates ordner und einen static ordner zu erstellen. die css files sind dann in `blog_generator/static/blog_generator/<file>`

### django dev server starten

- `python3 ai_blog_app/manage.py runserver` muss aus dem ordner in dem die env ist, also den pfad zur manage.py noch angeben
- im browser den port `http://127.0.0.1:8000/` öffnen

### .env zugriff

`pip install python-dotenv` mit os kann man nur auf die envs des systems zugreifen, nicht die aus der .env

```py

# (unterordner)ai_blog_app -- settings.py
import os
from dotenv import load_dotenv
load_dotenv()

# Achtung! SECRET_KEY in settings.py muss auch geheim sein. ggf neuen erstellen:
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())

```

### postgresql einrichten

im tutorial wird das mit grovery gemacht aber das gefällt mir nicht. stattdessen habe ich **aiven** gefunden, ein cloud service mit einer forever free pgsql bis 5gb storage 🤑

`pip install psycopg` das braucht man für die pg connection

```py
# (unterordner)ai_blog_app -- settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}
```

`python3 ai_blog_app/manage.py makemigrations`
`python3 ai_blog_app/manage.py migrate`
hiermit werden die django voreinstellungen in die db migriert

### django admin panel

einfach im browser aufrufen unter `http://127.0.0.1:8000/admin`

admin erstellen: `python3 ai_blog_app/manage.py createsuperuser`

```py
# (unterordner)ai_blog_app -- settings.py

```

```py
# (unterordner)ai_blog_app -- settings.py

```

```py
# (unterordner)ai_blog_app -- settings.py

```
