"""Модуль описания конфигурации Django приложения - bot."""

from django.apps import AppConfig


class BotConfig(AppConfig):
    """Класс для конфигурации приложения Bot в Django."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hasta_la_vista_money.bot'
