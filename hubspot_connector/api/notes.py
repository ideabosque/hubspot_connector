from hubspot.crm.objects.notes.exceptions import ApiException

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

