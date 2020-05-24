from django.shortcuts import redirect
from qmeet import views


def home():
    return redirect('index')
