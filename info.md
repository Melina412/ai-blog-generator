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
  zb.: npx tailwindcss -i ./src/style/input.css -o ./src/style/output.css --watch

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

### django dev server starten

- `python3 ai_blog_app/manage.py runserver` muss aus dem ordner in dem die env ist, also den pfad zur manage.py noch angeben
- im browser den port `http://127.0.0.1:8000/` öffnen
