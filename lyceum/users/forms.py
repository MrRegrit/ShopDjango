import django.contrib.auth.forms
import django.contrib.auth.models
import django.forms

import users.models


class UserCreationForm(django.contrib.auth.forms.UserCreationForm):
    email = django.forms.EmailField(required=True)

    class Meta:
        model = django.contrib.auth.models.User
        fields = (model.username.field.name, model.email.field.name)

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class UserChangeForm(django.contrib.auth.forms.UserChangeForm):
    password = None

    class Meta(django.contrib.auth.forms.UserChangeForm.Meta):
        model = django.contrib.auth.models.User
        fields = (
            model.email.field.name,
            model.first_name.field.name,
            model.last_name.field.name,
        )


class ProfileChangeForm(django.forms.ModelForm):
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
            model.image.field.name: django.forms.FileInput(
                attrs={
                    "class": "form-control",
                },
            ),
            model.birthday.field.name: django.forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                },
            ),
            model.coffee_count.field.name: django.forms.TextInput(
                attrs={"class": "form-control", "readonly": "readonly"},
            ),
        }


__all__ = []
