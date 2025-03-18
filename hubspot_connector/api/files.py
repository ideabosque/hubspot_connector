from hubspot.files.files.exceptions import ApiException
from hubspot.files.files.models import ImportFromUrlInput
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
        
    def upload(self, **params):
        try:
            file_uploaded = self.api_client.files.files.files_api.upload(**params)
            return file_uploaded
        except ApiException as e:
            self.logger.error(e)
            return None
        
    def import_from_url(self, **params):
        import_from_url_input = ImportFromUrlInput(**params)
        try:
            file_imported = self.api_client.files.files.files_api.import_from_url(import_from_url_input=import_from_url_input, **{"async_req":False})
            return file_imported
        except ApiException as e:
            self.logger.error(e)
            return None

    def check_import_status(self, task_id):
        try:
            response = self.api_client.files.files.files_api.check_import(task_id=task_id)
            return response
        except ApiException as e:
            self.logger.error(e)
            return None
