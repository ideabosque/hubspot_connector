from hubspot.crm.properties.exceptions import ApiException
from hubspot.crm.properties.models.batch_read_input_property_name import BatchReadInputPropertyName

class Properties(object):
    def __init__(self, logger, api_client):
        self.api_client = api_client
        self.logger = logger

    def get(self, object_type, property_name, **params):
        try:
            property = self.api_client.crm.properties.core_api.get_by_name(object_type, property_name, **params)
            return property
        except ApiException as e:
            self.logger.error(e)
            return None
        
    def get_all(self, object_type, **params):
        try:
            api_reponse = self.api_client.crm.properties.core_api.get_all(object_type, **params)
            return api_reponse
        except ApiException as e:
            self.logger.error(e)
            return None
        
    def read_batch(self, object_type, properties, **params):
        batch_read_input_property_name = BatchReadInputPropertyName(
            inputs=properties
        )
        try:
            api_reponse = self.api_client.crm.properties.batch_api.read(object_type, batch_read_input_property_name, **params)
            return api_reponse
        except ApiException as e:
            self.logger.error(e)
            return None
