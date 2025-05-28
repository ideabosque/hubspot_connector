# Hubspot Connector v0.0.1 Initial Release

We are thrilled to introduce the very first release of the HubspotConnector, version 0.0.1. This marks the beginning of a powerful integration tool designed to simplify your interaction with Hubspot. While this initial release lays the foundation, we have exciting plans for future updates and enhancements.

## Key Features

### Seamless Hubspot Integration

- **HubSpot API Integration**: Connects to the HubSpot CRM API for data synchronization.

- **Objects Management**: Create, update, and retrieve objects(contact, company, deal, products,etc...)

- **Error Handling**: The connector includes comprehensive error handling to help you identify and resolve integration issues.

## Usage Example

Here's a simple example of how to get started with the SuiteTalk Connector:

```python
# Initialize the connector
import logging
import os
import sys
import json
from dotenv import load_dotenv
from hubspot_connector import HubspotConnector

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()

load_dotenv()
setting = {
    "hubspot_access_token": os.getenv("hubspot_access_token")
}

hubspot_connector = HubspotConnector(logger, setting)

# Perform a basic operation, such as retrieving a customer record
email = "test@test.com"  # Replace with an actual contact's email
contact = hubspot_connector.get_contact(contact_id=email, id_property="email")

# Print the contact
print("Contact Record:")
print(contact)
```

## Get Started

To begin integrating your application with Hubspot using the Hubspot Connector, follow these steps:

1. Install the connector via pip:

```bash
pip install hubspot-connector
```

2. Initialize the connector with your Hubspot private app's access token, as shown in the example above.

3. Explore the provided functions and adapt them to your specific integration needs.

## Feedback and Support

Your feedback is invaluable as we continue to develop and enhance the Hubspot Connector. If you encounter any issues, have suggestions, or need assistance, please don't hesitate to [reach out to our support team](mailto:ideabosque@gmail.com).

We're excited to embark on this journey with you, simplifying your Hubspot integration efforts and empowering your business operations.

Thank you for choosing the SuiteTalk Connector, and we look forward to a successful integration partnership.

Best regards,
Your Hubspot Connector Team