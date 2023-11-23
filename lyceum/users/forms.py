import django.contrib.auth.forms
import django.contrib.auth.models
import django.forms

import core.mixins
import users.models


class UserCreationForm(
    django.contrib.auth.forms.UserCreationForm,
    core.mixins.FormControlMixin,
):
    email = django.forms.EmailField(required=True)

    class Meta(django.contrib.auth.forms.UserCreationForm.Meta):
        model = users.models.User
        fields = (model.username.field.name, model.email.field.name)


class UserChangeForm(
    django.contrib.auth.forms.UserChangeForm,
    core.mixins.FormControlMixin,
):
    password = None

    class Meta(django.contrib.auth.forms.UserChangeForm.Meta):
        model = users.models.User
        fields = (
            model.email.field.name,
            model.first_name.field.name,
            model.last_name.field.name,
        )


class ProfileChangeForm(django.forms.ModelForm, core.mixins.FormControlMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["coffee_count"].widget.attrs["disabled"] = True
        self.fields["coffee_count"].required = False

    def clean_coffee_count(self):
        instance = getattr(self, "instance", None)
        if instance and instance.pk:
            return instance.coffee_count
        return self.cleaned_data["coffee_count"]

    class Meta:
        model = users.models.Profile
        fields = (
            model.birthday.field.name,
            model.image.field.name,
            model.coffee_count.field.name,
        )
        labels = {
            model.image.field.name: "Аватарка",
            model.coffee_count.field.name: "Выпито кофе",
        }

        widgets = {
            model.birthday.field.name: django.forms.DateInput(
                attrs={
                    "type": "date",
                },
            ),
        }


__all__ = []
