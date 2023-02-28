#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "jeffreyw"

from hubspot import HubSpot
from .api.contacts import Contacts
from .api.companies import Companies
from .api.deals import Deals
from .api.products import Products
from .api.line_items import LineItems
from .api.owners import Owners


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

    def get_contact(self, contact_id, id_property=None):
        if not contact_id:
            raise Exception(f"contact_id can not be empty")
        params = {}
        if id_property is not None:
            params["id_property"] = id_property
        
        api_contacts = Contacts(self.logger, self.hubspot)
        exist_contact = api_contacts.get(contact_id, **params)
        return exist_contact

    def associate_contact_deal(self, contact_id, deal_id):
        api_contacts = Contacts(self.logger, self.hubspot)
        return api_contacts.create_association(contact_id=contact_id, to_object_type="deal", to_object_id=deal_id, association_type=4)

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

    def get_company(self, company_id, id_property=None):
        if not company_id:
            raise Exception(f"company_id can not be empty")
        params = {}
        if id_property is not None:
            params["id_property"] = id_property
        
        api_companies = Companies(self.logger, self.hubspot)
        exist_company = api_companies.get(company_id, **params)
        return exist_company

    def associate_company_deal(self, company_id, deal_id):
        api_companies = Companies(self.logger, self.hubspot)
        return api_companies.create_association(company_id=company_id, to_object_type="deal", to_object_id=deal_id, association_type=6)

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

    def get_deal(self, deal_id, id_property=None):
        if not deal_id:
            raise Exception(f"The field deal_id can not be empty")
        params = {}
        if id_property is not None:
            params["id_property"] = id_property
        api_deals = Deals(self.logger, self.hubspot)
        exist_deal = api_deals.get(deal_id, **params)
        return exist_deal

    def get_deal_association(self, deal_id, to_object_type):
        api_deals = Deals(self.logger, self.hubspot)
        return api_deals.get_all_association(deal_id=deal_id, to_object_type=to_object_type)

    def associate_deal_company(self, deal_id, company_id):
        api_deals = Deals(self.logger, self.hubspot)
        return api_deals.create_association(deal_id=deal_id, to_object_type="company", to_object_id=company_id, association_type=5)

    def associate_deal_contact(self, deal_id, contact_id):
        api_deals = Deals(self.logger, self.hubspot)
        return api_deals.create_association(deal_id=deal_id, to_object_type="contact", to_object_id=contact_id, association_type=3)

    def associate_deal_line_item(self, deal_id, line_item_id):
        api_deals = Deals(self.logger, self.hubspot)
        return api_deals.create_association(deal_id=deal_id, to_object_type="line_items", to_object_id=line_item_id, association_type="deal_to_line_item")

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

    def get_product(self, product_id, id_property=None):
        if not product_id:
            raise Exception(f"The field product_id can not be empty")
        params = {}
        if id_property is not None:
            params["id_property"] = id_property
        api_products = Products(self.logger, self.hubspot)
        exist_product = api_products.get(product_id, **params)
        return exist_product

    def associate_line_item_deal(self, line_item_id, deal_id):
        api_line_items = LineItems(self.logger, self.hubspot)
        return api_line_items.create_association(line_item_id=line_item_id, to_object_type="deal", to_object_id=deal_id, association_type="line_item_to_deal")

    def insert_update_line_item(self, hs_product, quantity, price, associations=[]):
        api_line_items = LineItems(self.logger, self.hubspot)
        params = {
            "id_property": "hs_product_id"
        }
        if associations:
            params["associations"] = associations
        exist_line_item = api_line_items.get(line_item_id=hs_product.id, **params)
        properties = {}
        
        if exist_line_item is None:
            properties["hs_product_id"] = hs_product.id
            properties["name"] = hs_product.properties.get("name")
            # properties["hs_recurring_billing_period"] = "2"
            # properties["recurringbillingfrequency"] = "monthly"
            properties["quantity"] = quantity
            properties["price"] = price
            result = api_line_items.create(properties)
        else:
            properties["quantity"] = quantity
            properties["price"] = price
            result = api_line_items.update(line_item_id=exist_line_item.id, properties=properties)
        return result.id
    
    def get_all_owners(self):
        api_owners = Owners(self.logger, self.hubspot)
        params = {
            "limit": 200
        }
        api_response = api_owners.get_page(**params)
        owners = api_response.results
        paging = api_response.paging
        if paging is not None:
            while paging is not None:
                params["after"] = paging.next.after
                next_page = api_owners.get_page(**params)
                paging = next_page.paging
                owners = owners + next_page.results
        return owners
        


        



