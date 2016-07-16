#coding=utf-8
from django.test import TestCase
from models import Order
from mock import patch
from django.contrib.auth.models import User
import json
from django.http import HttpResponse
import datetime

# Create your tests here.


def new_send_mail(a, b, c, d):
    pass


def new_render(a, b, c):
    return HttpResponse()
    # result = json.dumps(c)
    # return HttpResponse(result)


class OrderTest(TestCase):

    def test_ok_create(self):
        with patch('lunch_maker.views.send_mail', new=new_send_mail):
            data = {'meal':'some meal','person':'some person', 'email':'some@email.com', 'byn':1.11, 'byr':100,
                    'comment':'qwerty'}
            self.client.post('/new_order/', data)
            q_order = Order.objects.filter()
            self.assertEquals(q_order.count(), 1)
            order = q_order.get()
            self.assertEquals(order.meal, data["meal"])
            self.assertEquals(order.person, data['person'])
            self.assertEquals(order.email, data['email'])
            self.assertEquals(order.byn, data['byn'])
            self.assertEquals(order.byr, data['byr'])
            self.assertEquals(order.comment, data['comment'])


    def test_ok_delete(self):
        with patch('lunch_maker.views.send_mail', new=new_send_mail):
            data = {'meal': 'some meal', 'person': 'some person', 'email': 'some@email.com', 'byn': 1.11, 'byr': 100,
                    'comment': 'qwerty'}
            Order.objects.create(meal=data['meal'], person=data['person'], email=data['email'], byn=data['byn'],
                                 byr=data['byr'], comment=data['comment'])
            User.objects.create_superuser(username='admin', password='qwerty123', email='admin@admin.com')
            self.client.login(username='admin', password='qwerty123')
            data1 = {'delete':1}
            self.client.post('/delete/', data1)
            order = Order.objects.filter()
            self.assertEquals(order.count(), 0)


    def test_ok_change(self):
        with patch('lunch_maker.views.send_mail', new=new_send_mail):
            data = {'meal': 'some meal', 'person': 'some person', 'email': 'some@email.com', 'byn': 1.11, 'byr': 100,
                    'comment': 'qwerty'}
            Order.objects.create(meal=data['meal'], person=data['person'], email=data['email'], byn=data['byn'],
                                 byr=data['byr'], comment=data['comment'])
            User.objects.create_superuser(username='admin', password='qwerty123', email='admin@admin.com')
            self.client.login(username='admin', password='qwerty123')
            sess = self.client.session
            sess['change_id'] = 1
            sess.save()
            data1 = {'meal': 'other meal', 'person': 'some person', 'email': 'some@email.com', 'byn': 1.11, 'byr': 100,
                    'comment': 'qwerty'}
            self.client.post('/change/', data1)
            order = Order.objects.filter().get()
            self.assertNotEquals(order.meal, data['meal'])


    def test_ok_show(self):
        with patch('lunch_maker.views.render', new=new_render):
            #data = {'meal': 'some meal', 'person': 'some person', 'email': 'some@email.com', 'byn': 1.11, 'byr': 100,
                    #'comment': 'qwerty'}
            #Order.objects.create(meal=data['meal'], person=data['person'], email=data['email'], byn=data['byn'],
                                 #byr=data['byr'], comment=data['comment'])
            User.objects.create_superuser(username='admin', password='qwerty123', email='admin@admin.com')
            self.client.login(username='admin', password='qwerty123')
            result = self.client.get('/show/')
            print "-------------"
            print result