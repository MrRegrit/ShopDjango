import django.contrib.auth.models


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


__all__ = []
