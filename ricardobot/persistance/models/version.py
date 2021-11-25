import peewee as pw

from ricardobot.persistance.models import BaseModel


class Version(BaseModel):
    version = pw.CharField()
    changelog = pw.TextField()

    def __init__(self, version: str, changelog: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.version = version
        self.changelog = changelog
