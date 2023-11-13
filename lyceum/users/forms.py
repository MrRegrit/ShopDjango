import django.contrib.auth.forms
import django.contrib.auth.models
import django.forms

import users.models


class UserCreationForm(django.contrib.auth.forms.UserCreationForm):
    email = django.forms.EmailField(required=True)

    class Meta:
        model = django.contrib.auth.models.User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class UserChangeForm(django.contrib.auth.forms.UserChangeForm):
    password = None

    class Meta:
        model = django.contrib.auth.models.User
        fields = ("email", "first_name", "last_name")


class ProfileChangeForm(django.forms.ModelForm):
    class Meta:
        model = users.models.Profile
        exclude = ["coffee_count"]
        labels = {
            model.image.field.name: "Аватарка",
        }

        widgets = {
            model.image.field.name: django.forms.FileInput(
                attrs={
                    "class": "form-control",
                },
            ),
        }


__all__ = []
