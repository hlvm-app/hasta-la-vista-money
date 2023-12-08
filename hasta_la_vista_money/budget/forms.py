from django.forms import ModelForm
from hasta_la_vista_money.budget.models import DateList


class GenerateDateForm(ModelForm):
    class Meta:
        model = DateList
        fields = '__all__'
        exclude = ('user', 'date')
