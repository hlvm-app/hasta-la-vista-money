from django.forms import DateField, Form, SelectDateWidget


class SelectDateForm(Form):
    select_date = DateField(
        label='Выбрать дату',
        widget=SelectDateWidget(
            attrs={'class': 'form-control w-auto d-inline-block'},
        ),
    )
