from django.shortcuts import render


# Create your views here.
def welcome_message() -> dict:
    return {
        'text': f"Добро пожаловать!"
    }
