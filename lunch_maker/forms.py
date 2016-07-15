#coding=utf-8
from django import forms

class OrderForm(forms.Form):
    meal = forms.CharField(label="Что купить", min_length=1, max_length=250,
                           error_messages={'required':'вы не ввели что купить'})
    person = forms.CharField(min_length=1, max_length=100, label='Кому',
                             error_messages={'required':'вы не ввели ваше имя'})
    email = forms.EmailField(error_messages={'required':'вы не ввели ваш email'})
    byn = forms.FloatField(min_value=0.01, label="Оплачено BYR", required=False)
    byr = forms.IntegerField(min_value=100, label="Оплачено BYR", required=False)
    comment = forms.CharField(widget=forms.Textarea, label='Комментарий', required=False)