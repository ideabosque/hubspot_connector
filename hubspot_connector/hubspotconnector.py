#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from urllib3.util.retry import Retry

__author__ = "jeffreyw"

import copy, time
from datetime import datetime
from hubspot import HubSpot
from .api.contacts import Contacts
from .api.companies import Companies
from .api.deals import Deals
from .api.products import Products
from .api.line_items import LineItems
from .api.owners import Owners
from .api.notes import Notes
from .api.files import Files
from .api.properties import Properties

class HubspotConnector(object):
    def __init__(self, logger, settings):
        self.HUBSPOT_ACCESS_TOKEN = settings.get("hubspot_access_token")
        self._api_client = None
        self.logger = logger
        self.settings = settings

    def connect(self):
        try:
            retry = Retry(
                total=3,
                backoff_factor=0.3,
                status_forcelist=(500, 502, 504),
            )
            api_client = HubSpot(access_token=self.HUBSPOT_ACCESS_TOKEN, retry=retry)
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
        attachments = properties.pop("attachments", [])
        if exist_contact is None:
            result = api_contacts.create(properties)
        else:
            result = api_contacts.update(contact_id, properties, **params)
        if len(attachments) > 0:
            for attachment in attachments:
                self.attach_file_to_contact(contact_id=result.id, **attachment)
        return result.id

    def get_contact(self, contact_id, id_property=None, properties=[]):
        if not contact_id:
            raise Exception(f"contact_id can not be empty")
        params = {}
        if id_property is not None:
            params["id_property"] = id_property
        if len(properties) > 0:
            params["properties"] = properties
        api_contacts = Contacts(self.logger, self.hubspot)
        exist_contact = api_contacts.get(contact_id, **params)
        return exist_contact

    def associate_contact_deal(self, contact_id, deal_id):
        api_contacts = Contacts(self.logger, self.hubspot)
        return api_contacts.create_association(contact_id=contact_id, to_object_type="deal", to_object_id=deal_id, association_type=4)
    
    def get_contact_primary_company_id(self, contact_id):
        associated_companies = self.get_contact_association(contact_id=contact_id, to_object_type="company")
        try:
            if(len(associated_companies.results) > 0):
                return associated_companies.results[0].id
        except Exception as e:
            return None
    
    def get_contact_association(self, contact_id, to_object_type):
        api_contacts = Contacts(self.logger, self.hubspot)
        return api_contacts.get_all_association(contact_id=contact_id, to_object_type=to_object_type)
    
    def get_contacts(self, **params):
        count_only = params.pop("count_only", False)
        filter_groups = params.pop("filter_groups", None)
        sorts = params.pop("sorts", None)
        query = params.pop("query", None)
        properties = params.pop("properties", None)
        limit = params.pop("limit", 20)
        after = params.pop("after", None)
        limit_count = params.pop("limit_count", 100)
        first_result_response = self.search_contacts(filter_groups=filter_groups, sorts=sorts, query=query, properties=properties,limit=limit, after=after, **params)
        if count_only:
            return first_result_response.total
        count = 0
        contacts = []
        for contact in first_result_response.results:
            contacts.append(contact.properties)
            count = count + 1
        paging = first_result_response.paging
        if paging is not None:
            after = None
            while paging is not None:
                after = paging.next.after
                next_page = self.search_contacts(filter_groups=filter_groups, properties=properties, limit=limit, sorts=sorts, after=after, **params)
                paging = next_page.paging
                next_results = next_page.results
                for n_contact in next_results:
                    
                    contacts.append(n_contact.properties)
                    count = count + 1
                    if count >= limit_count:
                        paging = None

        return contacts
    
    def search_contacts(self, filter_groups=None, sorts=None, query=None, properties=None, limit=20, after=None, **kwargs):
        api_contact = Contacts(self.logger, self.hubspot)
        return api_contact.do_search(filter_groups=filter_groups,sorts=sorts, query=query, properties=properties, limit=limit, after=after, **kwargs)
    
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

    def update_company(self, properties, id_property=None):
        if id_property is not None and not properties.get(id_property, None):
            raise Exception(f"The field {id_property} can not be empty")
        params = {}
        if id_property is not None:
            company_id = properties.get(id_property)
            params["id_property"] = id_property
        else:
            company_id = properties.pop("hs_object_id")
        api_companies = Companies(self.logger, self.hubspot)
        exist_company = api_companies.get(company_id, **params)

        if exist_company is None:
            raise Exception(f"Company({company_id}) does not exists.")
        else:
            result = api_companies.update(company_id, properties, **params)
        return result.id
    
    def get_company(self, company_id, id_property=None, properties=[]):
        if not company_id:
            raise Exception(f"company_id can not be empty")
        params = {}
        if id_property is not None:
            params["id_property"] = id_property
        if len(properties) > 0:
            params["properties"] = properties
        api_companies = Companies(self.logger, self.hubspot)
        exist_company = api_companies.get(company_id, **params)
        return exist_company

    def get_companies(self, **params):
        count_only = params.pop("count_only", False)
        filter_groups = params.pop("filter_groups", None)
        sorts = params.pop("sorts", None)
        query = params.pop("query", None)
        properties = params.pop("properties", None)
        limit = params.pop("limit", 20)
        after = params.pop("after", None)
        limit_count = params.pop("limit_count", 100)
        first_result_response = self.search_companies(filter_groups=filter_groups, sorts=sorts, query=query, properties=properties,limit=limit, after=after, **params)
        if count_only:
            return first_result_response.total
        count = 0
        companies = []
        for company in first_result_response.results:
            companies.append(company.properties)
            count = count + 1
        paging = first_result_response.paging
        if paging is not None:
            after = None
            while paging is not None:
                after = paging.next.after
                next_page = self.search_companies(filter_groups=filter_groups, properties=properties, limit=limit, sorts=sorts, after=after, **params)
                paging = next_page.paging
                next_results = next_page.results
                for n_company in next_results:
                    
                    companies.append(n_company.properties)
                    count = count + 1
                    if count >= limit_count:
                        paging = None

        return companies
    
    def search_companies(self, filter_groups=None, sorts=None, query=None, properties=None, limit=20, after=None, **kwargs):
        api_company = Companies(self.logger, self.hubspot)
        return api_company.do_search(filter_groups=filter_groups,sorts=sorts, query=query, properties=properties, limit=limit, after=after, **kwargs)
    
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

    def get_deal(self, deal_id, properties=[], id_property=None):
        if not deal_id:
            raise Exception(f"The field deal_id can not be empty")
        params = {}
        if id_property is not None:
            params["id_property"] = id_property
        if len(properties) > 0:
            params["properties"] = properties
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

    def get_line_item(self, line_item_id, id_property=None, associations=[], properties=[], properties_with_history=[]):
        if not line_item_id:
            raise Exception(f"The field line_item_id can not be empty")
        api_line_items = LineItems(self.logger, self.hubspot)
        params = {}
        if id_property is not None:
            params["id_property"] = id_property
        if len(associations) > 0:
            params["associations"] = associations
        if len(properties) > 0:
            params["properties"] = properties
        if len(properties_with_history) > 0:
            params["properties_with_history"] = properties_with_history
        exist_line_item = api_line_items.get(line_item_id=line_item_id, **params)
        return exist_line_item
    
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
    
    def update_line_item(self, line_item_id, properties):
        api_line_items = LineItems(self.logger, self.hubspot)
        result = api_line_items.update(line_item_id=line_item_id, properties=properties)
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
            after = paging.next.after
            while paging is not None:
                params["after"] = paging.next.after
                next_page = api_owners.get_page(**params)
                paging = next_page.paging
                owners = owners + next_page.results
                if paging is not None and after == paging.next.after:
                    break

                if paging is not None:
                     after = paging.next.after

        archived_params = {
            "limit": 200,
            "archived": True
        }
        api_response = api_owners.get_page(**archived_params)
        owners = owners + api_response.results
        paging = api_response.paging

        if paging is not None:
            after = paging.next.after
            while paging is not None:
                params["after"] = paging.next.after
                next_page = api_owners.get_page(**archived_params)
                paging = next_page.paging
                owners = owners + next_page.results
                if paging is not None and after == paging.next.after:
                    break
                if paging is not None:
                     after = paging.next.after
        return owners
    
    def get_deals(self, **params):
        count_only = params.pop("count_only", False)
        filter_groups = params.pop("filter_groups", None)
        sorts = params.pop("sorts", None)
        query = params.pop("query", None)
        properties = params.pop("properties", None)
        limit = params.pop("limit", 20)
        limit_count = params.pop("limit_count", 100)
        after = params.pop("after", None)

        first_deal_response = self.search_deals(filter_groups=filter_groups, sorts=sorts, query=query, properties=properties,limit=limit, after=after, **params)
        if count_only:
            return first_deal_response.total
        count = 0
        deals = []
        for deal in first_deal_response.results:
            deals.append(deal.properties)
            count = count + 1
        deals = [
            deal.properties
            for deal in first_deal_response.results
        ]
        paging = first_deal_response.paging
        if paging is not None:
            after = None
            while paging is not None:
                after = paging.next.after
                next_page = self.search_deals(filter_groups=filter_groups, properties=properties, limit=limit, sorts=sorts, after=after, **params)
                paging = next_page.paging
                next_deals = next_page.results
                count = count + 1
                for n_deal in next_deals:
                    deals.append(n_deal.properties)
                    count = count + 1
                    if count >= limit_count:
                        paging = None

        return deals
    
    def search_deals(self, filter_groups=None, sorts=None, query=None, properties=None, limit=20, after=None, **kwargs):
        api_deals = Deals(self.logger, self.hubspot)
        return api_deals.do_search(filter_groups=filter_groups,sorts=sorts, query=query, properties=properties, limit=limit, after=after, **kwargs)

    def update_deal(self, properties, id_property=None):
        if id_property is not None and not properties.get(id_property, None):
            raise Exception(f"The field {id_property} can not be empty")
        params = {}
        if id_property is not None:
            deal_id = properties.get(id_property)
            params["id_property"] = id_property
        else:
            deal_id = properties.pop("hs_object_id")
            
        api_deals = Deals(self.logger, self.hubspot)
        # exist_deal = api_deals.get(deal_id, **params)
        # if exist_deal is None:
        #     result = api_deals.create(properties)
        # else:
        result = api_deals.update(deal_id, properties, **params)
        return result.id
    
    def get_deleted_companies(self):
        api_company = Companies(self.logger, self.hubspot)
        limit = 100
        page_count = 1
        first_result_response = api_company.get_companies_by_page(limit=limit, archived=True)
        companies = []
        for company in first_result_response.results:
            companies.append(self.format_hubspot_object(company))
        page_count = 1
        paging = first_result_response.paging
        if paging is not None:
            after = None
            while paging is not None:
                if page_count % 5 == 0:
                    time.sleep(2)
                after = paging.next.after
                next_page = api_company.get_companies_by_page(limit=limit, after=after, archived=True)
                paging = next_page.paging
                next_companies = next_page.results
                for n_company in next_companies:
                    companies.append(self.format_hubspot_object(n_company))
                if paging is not None and after == paging.next.after:
                    break
                page_count = page_count + 1
        return companies
        
    def format_hubspot_object(self, hubspot_object):
        new_object = hubspot_object.to_dict()
        properties = new_object.pop("properties", {})
        new_object = dict(
            new_object,
            **properties
        )
        return new_object
    
    def get_note(self, note_id, properties=[]):
        if not note_id:
            raise Exception(f"The field note_id can not be empty")
        params = {}
        if len(properties) > 0:
            params["properties"] = properties
        api_notes = Notes(self.logger, self.hubspot)
        exist_note = api_notes.get(note_id, **params)
        return exist_note
    
    def get_file(self, file_id, properties=[]):
        if not file_id:
            raise Exception(f"The field file_id can not be empty")
        params = {}
        if len(properties) > 0:
            params["properties"] = properties
        api_files = Files(self.logger, self.hubspot)
        exist_file = api_files.get(file_id, **params)
        return exist_file
    
    def get_file_with_signed_url(self, file_id):
        if not file_id:
            raise Exception(f"The field file_id can not be empty")
        params = {}
        api_files = Files(self.logger, self.hubspot)
        exist_file_with_signed_url = api_files.get_signed_url(file_id, **params)
        return exist_file_with_signed_url

    def get_properties_by_object_type(self, object_type, properties=None):
        params = {}
        api_properties = Properties(self.logger, self.hubspot)
        if properties is None:
            api_response = api_properties.get_all(object_type, **params)
        else:
            api_response = api_properties.read_batch(object_type, properties, **params)
        return api_response
    
    def upload_file(self, file_content, folder_path, options):
        params = {}
        params["file"] = file_content
        params["folder_path"] = folder_path
        params["options"] = options
        api_files = Files(self.logger, self.hubspot)
        api_response = api_files.upload(**params)
        return api_response
    
    def import_file_from_url(self, params):
        
        api_files = Files(self.logger, self.hubspot)
        api_response = api_files.import_from_url(**params)
        return api_response
    
    
    def create_note(self, properties={}):
        api_notes = Notes(self.logger, self.hubspot)
        exist_note = api_notes.create(properties)
        return exist_note
    
    def association_note_to_contact(self, note_id, contact_id):
        api_notes = Notes(self.logger, self.hubspot)
        api_response = api_notes.create_association(note_id=note_id, to_object_type="contact", to_object_id=contact_id, association_type="note_to_contact")
        return api_response

    def lookup_crm_user_list(self, logger, **kwargs):
        address = kwargs.get("address", "")
        page_size = kwargs.get("page_size", 100)
        page_number = kwargs.get("page_number", 0)
        total = 0

        result = {
            "page_size": page_size,
            "page_number": page_number,
            "total": total,
            "crm_user_list": []
        }
        try:
            response = self.search_contacts_by_address(address=address, limit=page_size)
            result["total"] = response.total
            for contact in response.results:
                result["crm_user_list"].append(
                    {
                        "email": contact.properties.get("email"),
                        "first_name": contact.properties.get("firstname"),
                        "last_name": contact.properties.get("lastname")
                    }
                )
        except Exception as e:
            pass
        
        return result
    
    def search_contacts_by_address(self, address, limit, after=None):
        formated_address = self.format_address(address)
        filter_groups = [
            {
                "filters": [
                    {
                        "value": formated_address.get("country"),
                        "propertyName": "country",
                        "operator": "EQ"
                    },
                    {
                        "value": formated_address.get("state_code"),
                        "propertyName": "hs_state_code",
                        "operator": "EQ"
                    },
                    {
                        "value": formated_address.get("address"),
                        "propertyName": "address",
                        "operator": "CONTAINS_TOKEN"
                    }
                ]
            },
            {
                "filters": [
                    {
                        "value": formated_address.get("country"),
                        "propertyName": "country",
                        "operator": "EQ"
                    },
                    {
                        "value": formated_address.get("zip"),
                        "propertyName": "zip",
                        "operator": "EQ"
                    },
                    {
                        "value": formated_address.get("address"),
                        "propertyName": "address",
                        "operator": "CONTAINS_TOKEN"
                    }
                ]
            },
            {
                "filters": [
                    {
                        "value": formated_address.get("country"),
                        "propertyName": "country",
                        "operator": "EQ"
                    },
                    {
                        "value": formated_address.get("city"),
                        "propertyName": "city",
                        "operator": "EQ"
                    },
                    {
                        "value": formated_address.get("address"),
                        "propertyName": "address",
                        "operator": "CONTAINS_TOKEN"
                    }
                ]
            },
        ]
        return self.search_contacts(filter_groups=filter_groups, sorts=None, query=None, properties=None, limit=limit, after=after, **{})
        

    def format_address(self, address):
        address_arr = address.split(",")
        country = address_arr[-1].strip()
        state_code_and_postcode = address_arr[-2].strip()
        state_code_and_postcode_arr = state_code_and_postcode.strip().split(" ")
        state_code = state_code_and_postcode_arr[0].strip()
        post_code = state_code_and_postcode_arr[1].strip()
        city = address_arr[-3].strip()
        street_address = " ".join(address_arr[:-3]).strip()
        return {
            "country": country,
            "state_code": state_code,
            "zip": post_code,
            "city": city,
            "address": street_address
        }

    def attach_file_to_contact(self, contact_id, **file_params):
        file_id = None
        if file_params.get("url"):
            try:
                api_files = Files(self.logger, self.hubspot)
                params = {
                    "access": file_params.get("access", "PRIVATE"),
                    "url": file_params.get("url"),
                    "folder_path": file_params.get("folder_path","/attachments"),
                    "overwrite": file_params.get("overwrite", False),
                }
                anysc_import_response = api_files.import_from_url(**params)
                task_id = anysc_import_response.id
                wait_limit = int(self.settings.get("import_file_wait_limit", 30))
                wait_count = 0
                while file_id is None and wait_count < wait_limit:
                    task_status = api_files.check_import_status(task_id)
                    if task_status.status == "COMPLETE":
                        if task_status.errors is not None and len(task_status.errors) > 0:
                            self.logger.error(task_status.errors)
                            break
                        if task_status.result is not None and task_status.result.id:
                            file_id = task_status.result.id
                    wait_count += 1
                    time.sleep(1)
            except Exception as e:
                self.logger.error(e)
                pass
            
        if file_id is not None:
            note_properties = {
                "hs_timestamp": int(datetime.now().timestamp()) * 1000,
                "hs_note_body": file_params.get("note"),
                "hs_attachment_ids": str(file_id)
            }
            note = self.create_note(note_properties)
            note_id = note.id
            result = self.association_note_to_contact(note_id=note_id, contact_id=contact_id)
        return
    
    def upload_file_by_url(self, **file_params):
        file_id = None
        if file_params.get("url"):
            try:
                api_files = Files(self.logger, self.hubspot)
                params = {
                    "access": file_params.get("access", "PRIVATE"),
                    "url": file_params.get("url"),
                    "folder_path": file_params.get("folder_path","/attachments"),
                    "overwrite": file_params.get("overwrite", False),
                }
                anysc_import_response = api_files.import_from_url(**params)
                task_id = anysc_import_response.id
                wait_limit = int(self.settings.get("import_file_wait_limit", 30))
                wait_count = 0
                while file_id is None and wait_count < wait_limit:
                    task_status = api_files.check_import_status(task_id)
                    if task_status.status == "COMPLETE":
                        if task_status.errors is not None and len(task_status.errors) > 0:
                            self.logger.error(task_status.errors)
                            break
                        if task_status.result is not None and task_status.result.id:
                            file_id = task_status.result.id
                    wait_count += 1
                    time.sleep(1)
            except Exception as e:
                self.logger.error(e)
                pass

        return file_id
