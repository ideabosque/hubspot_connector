from hubspot.crm.objects.notes.exceptions import ApiException
from hubspot.crm.objects.notes.models.simple_public_object_input import SimplePublicObjectInput

class Notes(object):
    def __init__(self, logger, api_client):
        self.api_client = api_client
        self.logger = logger

    def get(self, note_id, **params):
        try:
            note_fetched = self.api_client.crm.objects.notes.basic_api.get_by_id(note_id, **params)
            return note_fetched
        except ApiException as e:
            self.logger.error(e)
            return None
        
    def create(self, properties):

        simple_public_object_input = SimplePublicObjectInput(properties=properties)
        try:
            note_created = self.api_client.crm.objects.notes.basic_api.create(simple_public_object_input)
            return note_created
        except ApiException as e:
            self.logger.error(e)
            return None

    def create_association(self, note_id, to_object_type, to_object_id, association_type):
        try:
            response = self.api_client.crm.objects.notes.associations_api.create(
                note_id,
                to_object_type,
                to_object_id,
                association_type
            )
            return response
        except ApiException as e:
            self.logger.error(e)
            return False