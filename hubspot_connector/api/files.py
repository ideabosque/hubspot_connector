from hubspot.files.files.exceptions import ApiException

class Files(object):
    def __init__(self, logger, api_client):
        self.api_client = api_client
        self.logger = logger

    def get(self, file_id, **params):
        try:
            file_fetched = self.api_client.files.files.files_api.get_by_id(file_id, **params)
            return file_fetched
        except ApiException as e:
            self.logger.error(e)
            return None
        
    def get_signed_url(self, file_id, **params):
        try:
            file_fetched = self.api_client.files.files.files_api.get_signed_url(file_id, **params)
            return file_fetched
        except ApiException as e:
            self.logger.error(e)
            return None
