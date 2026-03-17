# Django CMS School Project - Implementation Plan

## Goal
Create a standalone Django CMS project in `cms_school/` with a frontend page at `/school/cms/` containing a form with **Title**, **Image**, **Author**, and **Content** fields, matching the provided wireframe.

---

## Project Structure

```
cms_school/
├── manage.py
├── cms_school/                   # Django project config
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── school/                       # Django app
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py                 # Article model
    ├── views.py                  # CMS view (GET/POST)
    ├── urls.py                   # Route: /school/cms/
    ├── forms.py                  # ArticleForm (ModelForm)
    ├── migrations/
    │   └── __init__.py
    └── templates/
        └── school/
            └── cms.html          # CMS form (Tailwind CSS via CDN)
```

---

## Implementation Steps

### Step 1: Create Django Project Scaffolding
- Run `django-admin startproject cms_school .` inside the `cms_school/` directory
- Run `python manage.py startapp school` to create the school app

### Step 2: Configure `cms_school/settings.py`
- Add `'school'` to `INSTALLED_APPS`
- Configure media file handling for image uploads:
  ```python
  MEDIA_URL = '/media/'
  MEDIA_ROOT = BASE_DIR / 'media'
  ```
- Database: SQLite3 (default)

### Step 3: Create the Article Model (`school/models.py`)
```python
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    author = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

### Step 4: Create the Article Form (`school/forms.py`)
```python
from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'image', 'author', 'content']
```

### Step 5: Create the CMS View (`school/views.py`)
```python
from django.shortcuts import render, redirect
from .forms import ArticleForm

def cms_view(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('cms')
    else:
        form = ArticleForm()
    return render(request, 'school/cms.html', {'form': form})
```

### Step 6: Configure URL Routing

**`school/urls.py`:**
```python
from django.urls import path
from . import views

urlpatterns = [
    path('cms/', views.cms_view, name='cms'),
]
```

**`cms_school/urls.py`:**
```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('school/', include('school.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### Step 7: Create the CMS Template (`school/templates/school/cms.html`)
- Styled with **Tailwind CSS via CDN** (`https://cdn.tailwindcss.com`)
- Form fields matching the wireframe:
  - **Title** - text input
  - **Image** - file upload with drag-and-drop area
  - **Author** - text input
  - **Content** - textarea
  - **Save Content** - submit button
- Centered card layout with white background, shadow, rounded corners

### Step 8: Register Model in Admin (`school/admin.py`)
```python
from django.contrib import admin
from .models import Article

admin.site.register(Article)
```

### Step 9: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 10: Install Pillow (required for ImageField)
```bash
pip install Pillow
```

---

## Verification Plan

### Manual Verification
1. Run the development server: `python manage.py runserver`
2. Open browser to `http://127.0.0.1:8000/school/cms/`
3. Verify the UI matches the wireframe:
   - Form fields: Title, Image, Author, Content are present and correctly laid out
   - Clean, centered card design with Tailwind styling
4. Submit a test article with all fields filled in
5. Verify the article is saved (page redirects back to the form)
6. Create a superuser (`python manage.py createsuperuser`) and check Django admin at `/admin/` to confirm the article was saved

---

## Wireframe Reference
The wireframe shows:
- URL: `35gb.github.dev/school/cms`
- A browser window with a form containing:
  - **Title** field with input box
  - **Image** field with input box
  - **Author** field with input box
  - **Content** field with input box
- Simple, clean layout

---

## Dependencies
- Python 3.x
- Django 4.2+
- Pillow (for ImageField support)
