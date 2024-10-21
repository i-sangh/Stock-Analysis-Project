from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def stock_data(request):
    return render(request, 'websocket_handler/stock_data.html')