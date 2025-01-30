from django.shortcuts import render


def index(request):
    return render(request, 'charts/index.html')


def partial_view(request):
    return render(request, 'charts/partial.html')
