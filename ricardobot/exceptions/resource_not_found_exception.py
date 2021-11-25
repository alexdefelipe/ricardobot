class ResourceNotFoundException(Exception):
    def __init__(self, resource: str, resource_id: int or None):
        self.resource = resource
        self.resource_id = resource_id

    def __str__(self):
        id_text = '' if self.resource_id is None else f'with id {self.resource_id}'
        return f'{self.resource} {id_text} not found'
