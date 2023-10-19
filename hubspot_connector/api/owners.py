from hubspot.crm.owners.exceptions import ApiException

class Owners(object):
    def __init__(self, logger, api_client):
        self.api_client = api_client
        self.logger = logger

    def get(self, owner_id, **params):
        try:
            owner_fetched = self.api_client.crm.owners.owners_api.get_by_id(owner_id, **params)
            return owner_fetched
        except ApiException as e:
            self.logger.error(e)
            return None
        
    def get_page(self, **params):
        try:
            api_reponse = self.api_client.crm.owners.owners_api.get_page(**params)
            return api_reponse
        except ApiException as e:
            self.logger.error(e)
            return None
