from django.forms import ModelForm
from django.shortcuts import get_object_or_404
from hasta_la_vista_money.users.models import User


def get_category_choices(queryset, parent=None, level=0, max_level=2):
    """Формируем выбор категории в форме."""
    choices = []
    prefix = '   >' * level
    categories = queryset.filter(parent_category=parent)
    for category in categories:
        category_id = category.id
        category_name = category.name
        choices.append((category_id, f'{prefix} {category_name}'))
        if level < max_level - 1:
            subcategories = get_category_choices(
                queryset,
                parent=category,
                level=level + 1,
                max_level=max_level,
            )
            choices.extend(subcategories)
    return choices


class BaseFieldsForm(ModelForm):
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

    def __init__(self, *args, **kwargs):
        """Конструктор класса."""
        super().__init__(*args, **kwargs)
        for field in self.fields:  # noqa: 528
            self.fields[field].label = self.labels.get(
                field,
                self.fields[field].label,
            )


class BaseForm(BaseFieldsForm):
    field = None

    def __init__(self, user=None, depth=None, category_queryset=None, *args, **kwargs):
        """
        Инициализирует экземпляр класса BaseForm.

        Процесс инициализации включает в себя вызов конструктора родительского
        класса, а также установку меток полей формы.

        :param args: Позиционные аргументы.
        :type args: tuple
        :param kwargs: Именованные аргументы.
        :type kwargs: dict
        """
        self.user = user
        super().__init__(*args, **kwargs)
        category_choices = get_category_choices(
            queryset=category_queryset,
            max_level=depth,
        )
        category_choices.insert(0, ('', '----------'))
        self.configure_category_choices(category_choices)

    def configure_category_choices(self, category_choices):
        """Configure category choices for the form."""
        self.fields[self.field].choices = category_choices
