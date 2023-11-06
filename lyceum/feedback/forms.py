import django.forms

import feedback.models


class FeedbackForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = feedback.models.Feedback

        exclude = ["created_at"]

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
                    "placeholder": "name@example.com",
                },
            ),
            model.text.field.name: django.forms.Textarea(
                attrs={"type": "text", "rows": 3},
            ),
        }


__all__ = []
