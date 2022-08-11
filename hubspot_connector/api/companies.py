from hubspot.crm.companies import SimplePublicObjectInput
from hubspot.crm.companies.exceptions import ApiException

class Companies(object):
    def __init__(self, logger, api_client):
        self.api_client = api_client
        self.logger = logger

    def get(self, company_id, **params):
        try:
            company_fetched = self.api_client.crm.companies.basic_api.get_by_id(company_id, **params)
            return company_fetched
        except ApiException as e:
            self.logger.error(e)
            return None

    def create(self, properties, **params):
        try:
            simple_public_object_input = SimplePublicObjectInput(
                properties=properties
            )
            api_response = self.api_client.crm.companies.basic_api.create(
                simple_public_object_input=simple_public_object_input,
                **params
            )
            return api_response
        except ApiException as e:
            self.logger.error(e)
            raise Exception(e)

    def update(self, company_id, properties, **params):
        try:

            simple_public_object_input = SimplePublicObjectInput(
                properties=properties
            )
            api_response = self.api_client.crm.companies.basic_api.update(
                company_id=company_id,
                simple_public_object_input=simple_public_object_input,
                **params
            )
            return api_response
        except ApiException as e:
            self.logger.error(e)
            raise Exception(e)