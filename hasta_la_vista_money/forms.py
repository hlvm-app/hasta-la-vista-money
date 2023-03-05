from django.forms import ModelForm


class BaseForm(ModelForm):
    fields = []
    labels = {}

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].label = self.labels.get(
                field, self.fields[field].label
            )
