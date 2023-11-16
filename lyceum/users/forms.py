import django.contrib.auth.forms
import django.contrib.auth.models
import django.forms

import users.backends
import users.models


class UserCreationForm(django.contrib.auth.forms.UserCreationForm):
    email = django.forms.EmailField(required=True)

    def clean_email(self):
        email = self.cleaned_data["email"]
        return users.backends.normalize_email(email)

    class Meta(django.contrib.auth.forms.UserCreationForm.Meta):
        model = django.contrib.auth.models.User
        fields = (model.username.field.name, model.email.field.name)

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class UserChangeForm(django.contrib.auth.forms.UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    password = None

    class Meta(django.contrib.auth.forms.UserChangeForm.Meta):
        model = django.contrib.auth.models.User
        fields = (
            model.email.field.name,
            model.first_name.field.name,
            model.last_name.field.name,
        )


class ProfileChangeForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["coffee_count"].widget.attrs["disabled"] = True
        self.fields["coffee_count"].required = False
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

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
