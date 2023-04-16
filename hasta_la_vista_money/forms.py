from django.forms import ModelForm


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

    class Meta:  # noqa: 306
        """Метакласс для базовой модели формы Django."""

        abstract = True

    def __init__(self, *args, **kwargs):
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
        for field in self.fields: # noqa: 528
            self.fields[field].label = self.labels.get(
                field, self.fields[field].label,
            )
