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
            self.hubspot_connector.insert_update_contact(contact_properties, id_property="email")
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
            self.hubspot_connector.insert_update_company(contact_properties, id_property="netsuite_company_id")
            logger.info(f"Finished at {time.strftime('%X')}")
        except Exception:
            log = traceback.format_exc()
            logger.exception(log)

    # @unittest.skip("demonstrating skipping")
    def test_insert_update_product(self):
        try:
            logger.info(f"Stated at {time.strftime('%X')}")
            contact_properties = json.load(
                open(
                    "/var/www/projects/hubspot_connector/hubspot_connector/tests/product.json",
                    "r",
                )
            )
            self.hubspot_connector.insert_update_product(contact_properties, id_property="hs_sku")
            logger.info(f"Finished at {time.strftime('%X')}")
        except Exception:
            log = traceback.format_exc()
            logger.exception(log)
if __name__ == "__main__":
    unittest.main()
