import os

from pi18n import TranslationService

root_path = f"{os.environ['RICARDOBOT_ROOT_PATH']}"
translation_service = TranslationService(f"{root_path}/resources/i18n", os.environ.get("LOCALE", "es"))
