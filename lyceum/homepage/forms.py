import django.forms


class EchoForm(django.forms.Form):
    text = django.forms.CharField(widget=django.forms.Textarea())


__all__ = []
