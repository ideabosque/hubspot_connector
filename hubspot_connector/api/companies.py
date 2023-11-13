from hubspot.crm.companies import SimplePublicObjectInput,PublicObjectSearchRequest
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


    def create_association(self, company_id, to_object_type, to_object_id, association_type):
        try:
            api_response = self.api_client.crm.companies.associations_api.create(
                company_id=company_id,
                to_object_type=to_object_type,
                to_object_id=to_object_id,
                association_type=association_type
            )
            return api_response
        except ApiException as e:
            self.logger.error(e)
            raise Exception(e)
        
    def do_search(self,filter_groups=None, sorts=None, query=None, properties=None, limit=20, after=None, **kwargs):
        try:
            public_object_search_request = PublicObjectSearchRequest(
                filter_groups=filter_groups,
                sorts=sorts,
                query=query,
                properties=properties,
                limit=limit,
                after=after
            )
            api_response = self.api_client.crm.companies.search_api.do_search(
                public_object_search_request=public_object_search_request,
                **kwargs
            )
            return api_response
        except ApiException as e:
            self.logger.error(e)
            raise Exception(e)
        
    def get_companies_by_page(self, limit=100, after=None, archived=False, properties=[], properties_with_history=[], associations=[]):
        try:
            params = {
                "limit": limit,
                "after": after,
                "archived": archived,
                "properties": properties,
                "properties_with_history": properties_with_history,
                "associations": associations
            }
            api_response = self.api_client.crm.companies.basic_api.get_page(**params)
            return api_response
        except ApiException as e:
            self.logger.error(e)
            raise Exception(e)