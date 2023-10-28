import re

import django.core.exceptions
import django.utils.deconstruct
import transliterate


def normalize_text(text: str):
    normalized_text = re.sub(r"[\s\W_]+", "", text).replace(" ", "")
    normalized_text = transliterate.translit(
        normalized_text.lower(),
        "ru",
        reversed=True,
    )
    return normalized_text


@django.utils.deconstruct.deconstructible
class ValidateMustContain:
    def __init__(self, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs

    def __call__(self, value):
        p_args = "|".join(self.args)
        pattern = rf"\b({p_args})\b"
        match = re.search(pattern, value.lower())
        if not match:
            m_arg = " или ".join(self.args)
            raise django.core.exceptions.ValidationError(
                f"В тексте должно быть слова {m_arg}",
            )


__all__ = ["ValidateMustContain", "normalize_text"]
