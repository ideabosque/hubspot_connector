from hubspot.crm.contacts import SimplePublicObjectInput
from hubspot.crm.contacts.exceptions import ApiException

class Contacts(object):
    def __init__(self, logger, api_client):
        self.api_client = api_client
        self.logger = logger

    def get(self, email, **params):
        try:
            contact_fetched = self.api_client.crm.contacts.basic_api.get_by_id(email, **params)
            return contact_fetched
        except ApiException as e:
            self.logger.error(e)
            return None

    def create(self, properties, **params):
        try:
            simple_public_object_input = SimplePublicObjectInput(
                properties=properties
            )
            api_response = self.api_client.crm.contacts.basic_api.create(
                simple_public_object_input=simple_public_object_input,
                **params
            )
            return api_response
        except ApiException as e:
            self.logger.error(e)
            return None

    def update(self, email, properties, **params):
        try:

            simple_public_object_input = SimplePublicObjectInput(
                properties=properties
            )
            api_response = self.api_client.crm.contacts.basic_api.update(
                contact_id=email,
                simple_public_object_input=simple_public_object_input,
                **params
            )
            return api_response
        except ApiException as e:
            self.logger.error(e)
            return None