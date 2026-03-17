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
