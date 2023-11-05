import django.forms

import feedback.models


class FeedbackForm(django.forms.ModelForm):
    class Meta:
        model = feedback.models.Feedback

        fields = (model.mail.field.name, model.text.field.name)
        labels = {
            model.mail.field.name: "Почта",
            model.text.field.name: "Текст обращения",
        }

        help_texts = {
            model.mail.field.name: "Введите вашу почту",
            model.text.field.name: "Введите текст обращение",
        }

        widgets = {
            model.mail.field.name: django.forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "name@example.com",
                },
            ),
            model.text.field.name: django.forms.Textarea(
                attrs={"type": "text", "class": "form-control", "rows": 3},
            ),
        }


__all__ = []
