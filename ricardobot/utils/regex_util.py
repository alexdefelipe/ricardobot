import re
from typing import List

COMMAND_REGEX = r"^/(\w*)"
START_ORDER_REGEX = r"(?:\w+)* ?ricardo ?(?:\w+ )* ?(?:[,!\.])* (?:[\w+ ,.])* ?medio ?(?:\w+)* (?:de){0,1} ?([\w+ ]+) " \
                    r"?(?:y|,) ?(?:\w+)* medio (?:de){0,1} ?([\w+ ]+)(?:[,!\.])* ?y (?:(?:de|para) beb\w+,*)* ?([\w+ " \
                    r"]+)"


def add_regex(*args, **kwargs):
    def decorator(func):
        regex = kwargs["regex"]
        args[0][regex] = func

    return decorator


class RegexUtil:

    @staticmethod
    def apply_command_regex(text: str):
        match = re.search(COMMAND_REGEX, text)
        if match is None:
            return None
        return match.group(1)

    @staticmethod
    def clean_text(text: str) -> str:
        text = text.lower()
        for ch in ['¿', '?', '¡', '!']:
            if ch in text:
                text = text.replace(ch, "")
        text = text.replace("á", "a")
        text = text.replace("é", "e")
        text = text.replace("í", "i")
        text = text.replace("ó", "o")
        text = text.replace("ú", "u")
        return text

    @staticmethod
    def apply_regex(regex: str, text: str) -> List[str]:
        matches = re.findall(regex, RegexUtil.clean_text(text))
        return matches[0] if len(matches) > 0 else None

    @staticmethod
    def regex_applies(regex: str, text: str) -> bool:
        match = RegexUtil.apply_regex(regex, text)
        return match is not None
