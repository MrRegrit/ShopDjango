import re

import django.conf

import users.models


class ReversRussionWordsMiddleware:
    counter = 0

    def __init__(self, get_response):
        self.get_response = get_response
        self.ALLOW_REVERSE = django.conf.settings.ALLOW_REVERSE

    def __call__(self, request):
        response = self.get_response(request)
        if self.ALLOW_REVERSE:
            self.__class__.counter += 1
            if self.__class__.counter % 10 == 0:
                content = response.content.decode()
                reversed_content = self.reverse_russian_words(content)
                response.content = reversed_content.encode()
        return response

    @staticmethod
    def reverse_russian_words(text: str) -> str:
        pattern = re.compile(r"\b[а-яА-ЯёЁ]+\b")

        def replace_word(match):
            return match.group()[::-1]

        return pattern.sub(replace_word, text)


class ChangeRequestUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            request.user = users.models.User.objects.get(id=request.user.id)
        return self.get_response(request)


__all__ = []
