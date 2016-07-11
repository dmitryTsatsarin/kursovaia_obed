from django.shortcuts import render

# Create your views here.

def go_main(request):
    return render(request, 'main_page.html', {})


def new_order(request):
    return render(request, 'new_order_page.html', {})