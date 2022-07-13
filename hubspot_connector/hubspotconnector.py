#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "jeffreyw"

from hubspot import HubSpot
from hubspot_connector.api.contacts import Contacts
from hubspot_connector.api.companies import Companies
from hubspot_connector.api.deals import Deals
from hubspot_connector.api.products import Products


class HubspotConnector(object):
    def __init__(self, logger, settings):
        self.HUBSPOT_ACCESS_TOKEN = settings.get("hubspot_access_token")
        self._api_client = None
        self.logger = logger

    def connect(self):
        try:
            api_client = HubSpot(access_token=self.HUBSPOT_ACCESS_TOKEN)
            return api_client
        except Exception as e:
            raise e

    @property
    def hubspot(self):
        self._api_client = (
            self.connect() if self._api_client is None else self._api_client
        )
        return self._api_client

    def insert_update_contact(self, properties, id_property=None):
        if not properties.get("email", None):
            raise Exception(f"The field email can not be empty")
        params = {}
        if id_property is not None:
            contact_id = properties.get(id_property)
            params["id_property"] = id_property
        else:
            contact_id = properties.get("hs_object_id")
        api_contacts = Contacts(self.logger, self.hubspot)
        exist_contact = api_contacts.get(contact_id, **params)

        if exist_contact is None:
            result = api_contacts.create(properties)
        else:
            result = api_contacts.update(contact_id, properties, **params)
        return result.id

    def insert_update_company(self, properties, id_property=None):
        if id_property is not None and not properties.get(id_property, None):
            raise Exception(f"The field {id_property} can not be empty")
        params = {}
        if id_property is not None:
            company_id = properties.get(id_property)
            params["id_property"] = id_property
        else:
            company_id = properties.get("hs_object_id")
        api_companies = Companies(self.logger, self.hubspot)
        exist_company = api_companies.get(company_id, **params)

        if exist_company is None:
            result = api_companies.create(properties)
        else:
            result = api_companies.update(company_id, properties, **params)
        return result.id

    def insert_update_deal(self, properties, id_property=None):
        if id_property is not None and not properties.get(id_property, None):
            raise Exception(f"The field {id_property} can not be empty")
        params = {}
        if id_property is not None:
            deal_id = properties.get(id_property)
            params["id_property"] = id_property
        else:
            deal_id = properties.get("hs_object_id")
        api_deals = Deals(self.logger, self.hubspot)
        exist_deal = api_deals.get(deal_id, **params)

        if exist_deal is None:
            result = api_deals.create(properties)
        else:
            result = api_deals.update(deal_id, properties, **params)
        return result.id

    def insert_update_product(self, properties, id_property=None):
        if id_property is not None and not properties.get(id_property, None):
            raise Exception(f"The field {id_property} can not be empty")
        params = {}
        if id_property is not None:
            product_id = properties.get(id_property)
            params["id_property"] = id_property
        else:
            product_id = properties.get("hs_object_id")
        api_products = Products(self.logger, self.hubspot)
        exist_product = api_products.get(product_id, **params)

        if exist_product is None:
            result = api_products.create(properties)
        else:
            result = api_products.update(product_id, properties, **params)
        return result.id
