from django.forms import ModelForm


class BaseForm(ModelForm):
    fields = []
    labels = {}

    class Meta:  # noqa: 306
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields: # noqa: 528
            self.fields[field].label = self.labels.get(
                field, self.fields[field].label,
            )
