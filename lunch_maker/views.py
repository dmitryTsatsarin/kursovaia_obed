#coding=utf-8
from django.shortcuts import render, redirect
from models import Order
from forms import OrderForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import datetime

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

@login_required(login_url='/accounts/login/')
def show(request):
    data = Order.objects.filter().values()
    result_byn = 0
    result_byr = 0
    for i in data:
        if i['byn'] is not None:
            result_byn += i['byn']
    for i in data:
        if i['byr'] is not None:
            result_byr += i['byr']
    result = result_byr/10000 + result_byn
    context = {'data':data, 'result_byn':result_byn, 'result_byr':result_byr, 'result':result}
    return render(request, 'show_page.html', context)


@login_required(login_url='/accounts/login/')
def delete(request):
    if request.method == "POST":
        delete_id = request.POST.get('delete')
        order = Order.objects.filter(id=delete_id).get()
        send_mail('изменения в заказе', u'{0}, ваш заказ удален'.format(order.person),
                  'testdjango31@gmail.com', ['{0}'.format(order.email)], fail_silently=False)
        Order.objects.filter(id=delete_id).delete()
        return redirect(show)
    else:
        context = {'data':Order.objects.filter()}
        return render(request, 'delete_page.html', context)


@login_required(login_url='/accounts/login/')
def change(request):
    if request.method == "POST":
        if request.POST.get('change'):
            change_id = request.POST.get('change')
            order = Order.objects.filter(id=change_id).get()
            data = {'meal':order.meal, 'person':order.person, 'email':order.email, 'byn':order.byn,
                    'byr':order.byr, 'comment':order.comment}
            context = {'my_form':OrderForm(data)}
            request.session['change_id'] = change_id
            return render(request, 'change_page.html', context)
        if request.session.has_key('change_id'):
            form = OrderForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                order = Order.objects.filter(id=request.session.get('change_id')).get()
                order.meal = data['meal']
                order.person = data['person']
                order.email = data['email']
                order.byn = data['byn']
                order.byr = data['byr']
                order.comment = data['comment']
                order.save()
                del request.session['change_id']
                return redirect(show)
            else:
                data = form.errors
                return HttpResponse("{0}".format(data))
    else:
        context = {'data':Order.objects.filter(), 'step':1}
        return render(request, 'change_page.html', context)