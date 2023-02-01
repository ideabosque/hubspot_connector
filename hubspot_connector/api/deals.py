from hubspot.crm.deals import SimplePublicObjectInput
from hubspot.crm.deals.exceptions import ApiException

class Deals(object):
    def __init__(self, logger, api_client):
        self.api_client = api_client
        self.logger = logger

    def get(self, deal_id, **params):
        try:
            deal_fetched = self.api_client.crm.deals.basic_api.get_by_id(deal_id, **params)
            return deal_fetched
        except ApiException as e:
            self.logger.error(e)
            return None

    def create(self, properties, **params):
        try:
            simple_public_object_input = SimplePublicObjectInput(
                properties=properties
            )
            api_response = self.api_client.crm.deals.basic_api.create(
                simple_public_object_input=simple_public_object_input,
                **params
            )
            return api_response
        except ApiException as e:
            self.logger.error(e)
            raise Exception(e)

    def update(self, deal_id, properties, **params):
        try:

            simple_public_object_input = SimplePublicObjectInput(
                properties=properties
            )
            api_response = self.api_client.crm.deals.basic_api.update(
                deal_id=deal_id,
                simple_public_object_input=simple_public_object_input,
                **params
            )
            return api_response
        except ApiException as e:
            self.logger.error(e)
            raise Exception(e)

    def get_all_association(self, deal_id, to_object_type):
        try:
            api_response = self.api_client.crm.deals.associations_api.get_all(
                deal_id=deal_id,
                to_object_type=to_object_type
            )
            return api_response
        except ApiException as e:
            self.logger.error(e)
            raise Exception(e)

    def create_association(self, deal_id, to_object_type, to_object_id, association_type):
        try:
            api_response = self.api_client.crm.deals.associations_api.create(
                deal_id=deal_id,
                to_object_type=to_object_type,
                to_object_id=to_object_id,
                association_type=association_type
            )
            return api_response
        except ApiException as e:
            self.logger.error(e)
            raise Exception(e)