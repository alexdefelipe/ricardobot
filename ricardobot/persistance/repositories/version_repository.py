import peewee as pw

from ricardobot.exceptions.resource_already_exists_exception import ResourceAlreadyExistsException
from ricardobot.persistance.models import Version


class VersionRepository:
    @staticmethod
    def get(version_number: str):
        return Version.get(Version.version == version_number)

    @staticmethod
    def create(version: Version) -> Version:
        try:
            created_version = version.save()
            return created_version
        except pw.IntegrityError:
            raise ResourceAlreadyExistsException("Version", version.version)
