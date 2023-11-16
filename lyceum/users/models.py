import datetime
import sys

import django.conf
import django.contrib.auth
import django.contrib.auth.models
import django.db.models
import django.utils.html
import sorl.thumbnail

if "makemigrations" not in sys.argv and "migrate" not in sys.argv:
    django.contrib.auth.models.User._meta.get_field("email")._unique = True


class UserManager(django.contrib.auth.models.BaseUserManager):
    @classmethod
    def normalize_email(cls, email):
        email = super().normalize_email(email)
        email = email.replace("@ya.ru", "@yandex.ru")
        if "+" in email:
            email_name, email_domen = email.split("@")
            email = email_name.split("+")[0] + "@" + email_domen
        if "@gmail.com" in email:
            email = (
                email.replace("@gmail.com", "").replace(".", "") + "@gmail.com"
            )
        elif "@yandex.ru" in email:
            email = (
                email.replace("@yandex.ru", "").replace(".", "-")
                + "@yandex.ru"
            )
        return email.lower()

    def get_queryset(self):
        return super().get_queryset().select_related("profile")

    def by_mail(self, mail):
        return self.get_queryset().get(email=self.normalize_email(mail))


class Profile(django.db.models.Model):
    def _profile_imgae_upload_to(self, filename):
        return (
            f"users/"
            f"images/{self.user_id}_{datetime.datetime.today().day}/"
            f"{filename}"
        )

    user = django.db.models.OneToOneField(
        django.conf.settings.AUTH_USER_MODEL,
        on_delete=django.db.models.CASCADE,
        verbose_name="пользователь",
        related_name="profile",
        related_query_name="profile",
        editable=False,
    )
    birthday = django.db.models.DateField(
        null=True,
        blank=True,
        verbose_name="дата рождения",
    )
    image = django.db.models.ImageField(
        upload_to=_profile_imgae_upload_to,
        verbose_name="аватарка",
        null=True,
        blank=True,
    )
    coffee_count = django.db.models.PositiveIntegerField(
        default=0,
        verbose_name="количество переходов по /coffee/",
    )
    attempts_count = django.db.models.PositiveIntegerField(
        default=0,
        verbose_name="попытки входа в аккаунт",
    )
    reactivate_time = django.db.models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="время отправки ссылки на переактивацию аккаунта",
    )

    class Meta:
        verbose_name = "Дополнительное поле"
        verbose_name_plural = "Дополнительные поля"

    def __str__(self):
        return str(self.pk)

    def image_tmb(self):
        if self.image:
            return django.utils.html.mark_safe(
                f'<img src="{self.get_image_300x300().url}" width="50">',
            )
        return "Нет изображения"

    def get_image_300x300(self):
        return sorl.thumbnail.get_thumbnail(
            self.image,
            "300x300",
            crop="center",
            quality=51,
        )

    image_tmb.short_description = "превью"
    image_tmb.allow_tags = True


class User(django.contrib.auth.models.User):
    objects = UserManager()

    def active(self):
        return self.is_active

    class Meta:
        proxy = True


__all__ = []
