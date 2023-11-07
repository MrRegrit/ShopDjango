import django.forms

import feedback.models


class FeedbackForm(django.forms.ModelForm):
    class Meta:
        model = feedback.models.Feedback

        exclude = ["created_at", "status", "extra"]

        labels = {
            model.text.field.name: "Текст обращения",
        }

        help_texts = {
            model.text.field.name: "Введите текст обращение",
        }

        widgets = {
            model.text.field.name: django.forms.Textarea(
                attrs={"type": "text", "rows": 3, "class": "form-control"},
            ),
        }


class FeedbackExtraForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = feedback.models.FeedbackExtra

        exclude = []

        labels = {
            model.mail.field.name: "Почта",
            model.name.field.name: "Имя",
        }

        help_texts = {
            model.name.field.name: "Введите ваше имя",
            model.mail.field.name: "Введите вашу почту",
        }

        widgets = {
            model.mail.field.name: django.forms.EmailInput(
                attrs={
                    "placeholder": "name@example.com",
                },
            ),
        }


class FeedbackFilesForm(django.forms.ModelForm):
    class Meta:
        model = feedback.models.FeedbackFiles

        exclude = ["feedback"]

        labels = {
            model.file.field.name: "Файлы",
        }

        help_texts = {
            model.file.field.name: "Вставьте файлы",
        }

        widgets = {
            model.file.field.name: django.forms.FileInput(
                attrs={
                    "class": "form-control",
                    "multiple": True,
                },
            ),
        }


__all__ = []
