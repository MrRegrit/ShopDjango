import django.forms


class EchoForm(django.forms.Form):
    text = django.forms.CharField(
        label="Текст",
        help_text="Введите текст",
        widget=django.forms.Textarea(
            attrs={"type": "text", "class": "form-control", "rows": 3},
        ),
    )


__all__ = []
