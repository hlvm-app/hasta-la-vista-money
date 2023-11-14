import datetime

from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from django.forms import ModelForm
from hasta_la_vista_money.constants import TODAY, NumericParameter


class BaseForm(ModelForm):
    r"""
    Базовая модель формы Django для создания форм на основе модели.

    ПОЛЯ:

        - fields (list): список полей модели, которые должны быть отображены
                         в форме.

        - labels (dict): словарь, содержащий метки для полей формы.

    МЕТОДЫ:

        __init__(self, \*args, \*\*kwargs): конструктор класса,
        который вызывается при создании экземпляра формы.
    """

    fields = []
    labels = {}

    class Meta:  # : 306
        """Метакласс для базовой модели формы Django."""

        abstract = True

    def __init__(self, user=None, depth=None, *args, **kwargs):
        """
        Инициализирует экземпляр класса BaseForm.

        Процесс инициализации включает в себя вызов конструктора родительского
        класса, а также установку меток полей формы.

        :param args: Позиционные аргументы.
        :type args: tuple
        :param kwargs: Именованные аргументы.
        :type kwargs: dict
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:  # noqa: 528
            self.fields[field].label = self.labels.get(
                field,
                self.fields[field].label,
            )


class DateTimePickerWidgetForm(DateTimePickerInput):
    def __init__(self, *args, **kwargs):
        """
        Инициализация параметров календаря.

        :param args:
        :param kwargs:
        """
        options = kwargs.pop('options', {})
        options.setdefault('format', 'DD/MM/YYYY HH:mm')
        options.setdefault('showTodayButton', True)
        options.setdefault(
            'minDate',
            (
                TODAY.replace(
                    month=1,
                    day=1,
                    year=TODAY.year - 1,
                )
                - datetime.timedelta(
                    days=NumericParameter.TODAY_MINUS_FIVE_YEARS.value,
                )
            ).strftime('%d/%m/%Y %H:%M'),
        )
        options.setdefault(
            'maxDate',
            (
                datetime.datetime.today()
                + datetime.timedelta(
                    days=NumericParameter.THREE_HUNDRED_SIXTY_FIVE.value,
                )
            ).strftime(
                '%Y-%m-%d 23:59:59',
            ),
        )
        super().__init__(*args, **kwargs, options=options)
