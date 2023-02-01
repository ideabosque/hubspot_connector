from hubspot.crm.line_items import SimplePublicObjectInput
from hubspot.crm.line_items.exceptions import ApiException

class LineItems(object):
    def __init__(self, logger, api_client):
        self.api_client = api_client
        self.logger = logger

    def get(self, line_item_id, **params):
        try:
            line_item_fetched = self.api_client.crm.line_items.basic_api.get_by_id(line_item_id, **params)
            return line_item_fetched
        except ApiException as e:
            self.logger.error(e)
            return None

    def create(self, properties, **params):
        try:
            simple_public_object_input = SimplePublicObjectInput(
                properties=properties
            )
            api_response = self.api_client.crm.line_items.basic_api.create(
                simple_public_object_input=simple_public_object_input,
                **params
            )
            return api_response
        except ApiException as e:
            self.logger.error(e)
            raise Exception(e)

    def update(self, line_item_id, properties, **params):
        try:

            simple_public_object_input = SimplePublicObjectInput(
                properties=properties
            )
            api_response = self.api_client.crm.line_items.basic_api.update(
                line_item_id=line_item_id,
                simple_public_object_input=simple_public_object_input,
                **params
            )
            return api_response
        except ApiException as e:
            self.logger.error(e)
            raise Exception(e)

    def create_association(self, line_item_id, to_object_type, to_object_id, association_type):
        try:
            api_response = self.api_client.crm.line_items.associations_api.create(
                line_item_id=line_item_id,
                to_object_type=to_object_type,
                to_object_id=to_object_id,
                association_type=association_type
            )
            return api_response
        except ApiException as e:
            self.logger.error(e)
            raise Exception(e)