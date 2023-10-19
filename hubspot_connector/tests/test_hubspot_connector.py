#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "jeffreyw"

import logging, sys, unittest, os, time, json, traceback
from dotenv import load_dotenv

load_dotenv()

setting = {
    "hubspot_access_token": os.getenv("hubspot_access_token"),
}


sys.path.insert(0, "/var/www/projects/hubspot_connector")

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()

from hubspot_connector import HubspotConnector
from hubspot.crm.properties import PropertyCreate, PropertyUpdate

class HubspotConnectorTest(unittest.TestCase):
    def setUp(self):
        self.hubspot_connector = HubspotConnector(logger, setting)
        logger.info("Initiate HubspotConnectorTest ...")

    def tearDown(self):
        del self.hubspot_connector
        logger.info("Destory HubspotConnectorTest ...")

    @unittest.skip("demonstrating skipping")
    def test_insert_update_contact(self):
        try:
            logger.info(f"Stated at {time.strftime('%X')}")
            contact_properties = json.load(
                open(
                    "/var/www/projects/hubspot_connector/hubspot_connector/tests/contact.json",
                    "r",
                )
            )
            id = self.hubspot_connector.insert_update_contact(
                contact_properties, id_property="email"
            )
            logger.info(f"contact id: {id}")
            logger.info(f"Finished at {time.strftime('%X')}")
        except Exception:
            log = traceback.format_exc()
            logger.exception(log)

    @unittest.skip("demonstrating skipping")
    def test_insert_update_company(self):
        try:
            logger.info(f"Stated at {time.strftime('%X')}")
            contact_properties = json.load(
                open(
                    "/var/www/projects/hubspot_connector/hubspot_connector/tests/company.json",
                    "r",
                )
            )
            id = self.hubspot_connector.insert_update_company(
                contact_properties, id_property="netsuite_company_id"
            )
            logger.info(f"company id: {id}")
            logger.info(f"Finished at {time.strftime('%X')}")
        except Exception:
            log = traceback.format_exc()
            logger.exception(log)

    @unittest.skip("demonstrating skipping")
    def test_insert_update_product(self):
        try:
            logger.info(f"Stated at {time.strftime('%X')}")
            contact_properties = json.load(
                open(
                    "/var/www/projects/hubspot_connector/hubspot_connector/tests/product.json",
                    "r",
                )
            )
            id = self.hubspot_connector.insert_update_product(
                contact_properties, id_property="hs_sku"
            )
            logger.info(f"product id: {id}")
            logger.info(f"Finished at {time.strftime('%X')}")
        except Exception:
            log = traceback.format_exc()
            logger.exception(log)
    
    @unittest.skip("demonstrating skipping")
    def test_get_owner(self):
        try:
            kwargs = {}
            response = self.hubspot_connector.hubspot.crm.owners.owners_api.get_by_id(owner_id=43868916, **kwargs)
            print(response)
            
        except Exception:
            log = traceback.format_exc()
            logger.exception(log)

    @unittest.skip("demonstrating skipping")
    def test_get_options(self):
        try:
            kwargs = {"limit": 100}
            response = self.hubspot_connector.hubspot.crm.owners.owners_api.get_page(**kwargs)
            # print(response)
            # print(type(response))
            owners = response.results
            if response.paging is not None:
                count = 1
                paging = response.paging
                while paging is not None:
                    if count >4:
                        break
                    kwargs["after"] = paging.next.after
                    next_page = self.hubspot_connector.hubspot.crm.owners.owners_api.get_page(**kwargs)
                    paging = next_page.paging
                    owners = owners + next_page.results
                    count = count +1
            # if response.paging is not None:
            #     kwargs["after"] = response.paging.next.after
            #     next_page = self.hubspot_connector.hubspot.crm.owners.owners_api.get_page(**kwargs)
            #     print(next_page)
            # else:
            #     owners = response.results
            print(owners)
            print(len(owners))
        except Exception:
            log = traceback.format_exc()
            logger.exception(log)

    # @unittest.skip("demonstrating skipping")
    def test_get_deal(self):
        deal = self.hubspot_connector.get_deal(deal_id="SO-GWI-99020", id_property="deal_number", properties=["notes_last_contacted"])
        print(deal)

    @unittest.skip("demonstrating skipping")
    def test_get_deal_line_item(self):
        line_items_result = self.hubspot_connector.get_deal_association(deal_id=14990000459, to_object_type="line_items")
        if len(line_items_result.results) > 0:
            line_items = []
            for line_item in line_items_result.results:
                try:
                    line_item_result = self.hubspot_connector.get_line_item(line_item_id=line_item.id, properties=["amount", "hs_sku", "quantity", "price", "line_item_priority"], properties_with_history=["line_item_priority"])
                    # self.hubspot_connector.hubspot.crm.
                    print(line_item_result)
                except Exception as e:
                    print(str(e))


    @unittest.skip("demonstrating skipping")
    def test_update_line_item_property(self):

        # response = self.hubspot_connector.hubspot.crm.properties.groups_api.get_all(object_type="line_item")
        # print(response)
        # return
        response = self.hubspot_connector.hubspot.crm.properties.core_api.get_by_name(object_type="line_item", property_name="uom")
        print(response)
        return
    
        response = self.hubspot_connector.hubspot.crm.properties.core_api.get_all(object_type="line_item")
        print(response)
        return
        # property_update = PropertyUpdate(**params)
        # response = self.hubspot_connector.hubspot.crm.properties.core_api.update(object_type="line_item", property_name="line_item_priority", property_update=property_update)
        # print(response)
        # return
    
    @unittest.skip("demonstrating skipping")
    def test_create_line_item_property(self):

        # response = self.hubspot_connector.hubspot.crm.properties.groups_api.get_all(object_type="line_item")
        # print(response)
        # return

        # response = self.hubspot_connector.hubspot.crm.properties.core_api.get_all(object_type="line_item")
        # print(response)
        # return
    
        response = self.hubspot_connector.hubspot.crm.properties.core_api.get_by_name(object_type="line_item", property_name="line_item_priority")
        print(response)
        return
        try:
            params = {
                "name": "item_priority",
                "label": "Item Priority",
                "type": "enumeration",
                "field_type": "select",
                "group_name": "lineiteminformation",
                "hidden": False,
                # "display_order": 2,
                "has_unique_value": False,
                "form_field": True,
                # "modificationMetadata": {
                #     "readOnlyOptions": False,
                #     "readOnlyValue": False,
                #     "readOnlyDefinition": False,
                #     "archivable": True
                # },
                "options": [
                    {
                    "label": "Converted",
                    "description": "Converted",
                    "value": "Converted",
                    "displayOrder": 1,
                    "hidden": False
                    },
                    {
                    "label": "Freshly Placed",
                    "description": "Freshly Placed",
                    "value": "Freshly Placed",
                    "displayOrder": 2,
                    "hidden": False
                    },
                    {
                    "label": "Medium Priority",
                    "description": "Medium Priority",
                    "value": "Medium Priority",
                    "displayOrder": 3,
                    "hidden": False
                    },
                    {
                    "label": "High Priority",
                    "description": "High Priority",
                    "value": "High Priority",
                    "displayOrder": 4,
                    "hidden": False
                    },
                    {
                    "label": "Losing",
                    "description": "Losing",
                    "value": "Losing",
                    "displayOrder": 5,
                    "hidden": False
                    },
                    {
                    "label": "Overdue",
                    "description": "Overdue",
                    "value": "Overdue",
                    "displayOrder": 6,
                    "hidden": False
                    },
                ]
            }
            property_create = PropertyCreate(**params)
            kwargs = {"limit": 100}
            response = self.hubspot_connector.hubspot.crm.properties.core_api.create(object_type="line_item", property_create=property_create)
            print(response)
            # print(type(response))
            
        except Exception:
            log = traceback.format_exc()
            logger.exception(log)


if __name__ == "__main__":
    unittest.main()
