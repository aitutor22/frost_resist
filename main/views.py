from django.shortcuts import render

# pages that aren't part of dropdown
def index(request):
    return render(request, 'main/index.html', {})
