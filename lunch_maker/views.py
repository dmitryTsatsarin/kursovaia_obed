#coding=utf-8
from django.shortcuts import render, redirect
from models import Order
from forms import OrderForm
from django.http import HttpResponse

# Create your views here.

def go_main(request):
    return render(request, 'main_page.html', {})


def new_order(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            meal = data['meal']
            person = data['person']
            email = data['email']
            byn = data['byn']
            byr = data['byr']
            comment = data['comment']
            if byn is None and byr is None:
                return HttpResponse("мы работаем только по предоплате")
            Order.objects.create(meal=meal, person=person, email=email, byn=byn, byr=byr, comment=comment)
            return redirect(go_main)
        data = form.errors
        return HttpResponse("{0}".format(data))
    else:
        context = {'my_form':OrderForm()}
        return render(request, 'new_order_page.html', context)