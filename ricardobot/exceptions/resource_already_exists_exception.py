from typing import Union


class ResourceAlreadyExistsException(Exception):
    def __init__(self, resource: str, resource_id: Union[str, int]):
        self.resource = resource
        self.resource_id = resource_id

    def __str__(self):
        return f'Error when creating a {self.resource} with id {self.resource_id}. It already exists.'
