#coding=utf-8
from django.shortcuts import render, redirect
from models import Order
from forms import OrderForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, mail_admins
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
            d_now = datetime.datetime.now().time()
            d1 = datetime.time(hour=13)
            d2 = datetime.time(hour=15)
            if d1 <= d_now <= d2:
                mail_admins(u'заказ', u'получен новый заказ')
            Order.objects.create(meal=meal, person=person, email=email, byn=byn, byr=byr, comment=comment)
            return redirect(go_main)
        data = form.errors
        return HttpResponse("{0}".format(data))
    else:
        d_now = datetime.datetime.now().time()
        d1 = datetime.time(hour=15)
        if d1 < d_now:
            context = {'my_form': OrderForm(), 'state':'off'}
        else:
            context = {'my_form':OrderForm()}
        return render(request, 'new_order_page.html', context)

@login_required(login_url='/accounts/login/')
def show(request):
    if request.session.has_key('change_id'):
        del request.session['change_id']
    data = Order.objects.filter().values()
    result_byn = 0
    result_byr = 0
    for i in data:
        if i['byn'] is not None:
            result_byn += i['byn']
    for i in data:
        if i['byr'] is not None:
            result_byr += i['byr']
    result = float(result_byr)/10000 + result_byn
    context = {'data':data, 'result_byn':result_byn, 'result_byr':result_byr, 'result':result}
    return render(request, 'show_page.html', context)


@login_required(login_url='/accounts/login/')
def delete(request):
    if request.method == "POST":
        delete_id = request.POST.get('delete')
        try:
            order = Order.objects.filter(id=delete_id).get()
        except:
            return HttpResponse("выберите заказ из списка")
        send_mail(u'изменения в заказе', u'{0}, ваш заказ удален'.format(order.person),
                  'testdjango31@gmail.com', ['{0}'.format(order.email)])
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
                send_mail(u'изменения в заказе', u'{0} {1}'.format(order.meal, order.comment),
                          'testdjango31@gmail.com', ['{0}'.format(order.email)])
                del request.session['change_id']
                return redirect(show)
            else:
                data = form.errors
                return HttpResponse("{0}".format(data))
        else:
            return HttpResponse('либо вы не выбрали заказ из списка<br>'
                                'либо обратитесь к администратору')
    else:
        context = {'data':Order.objects.filter(), 'step':1}
        return render(request, 'change_page.html', context)