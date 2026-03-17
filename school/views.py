from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ArticleForm
from .models import Article


def cms_view(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Article saved successfully!')
            return redirect('cms')
    else:
        form = ArticleForm()
    articles = Article.objects.all().order_by('-created_at')
    return render(request, 'school/cms.html', {'form': form, 'articles': articles})
