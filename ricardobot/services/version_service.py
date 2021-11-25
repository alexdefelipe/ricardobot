from telebotify.models.message import Message
from ricardobot.persistance.models import Version
from ricardobot.persistance.repositories.version_repository import VersionRepository


class VersionService:
    @staticmethod
    def get_version(message: Message) -> Version:
        user_id = message.from_user.user_id
        if user_id is not 459619074:
            pass
        version_number = message.text.replace("/notificar_version", '')
        return VersionRepository.get(version_number)

    @staticmethod
    def upload_version(message: Message) -> Version:
        user_id = message.from_user.user_id
        if user_id is not 459619074:
            pass
        message_text = message.text.replace("/subir_version", '')
        version_number, changelog = message_text.split('//')
        version = Version(version_number, changelog)
        return VersionRepository.create(version)
