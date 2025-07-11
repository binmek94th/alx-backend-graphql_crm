#!/usr/bin/env python3

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime, timedelta
import logging

# Setup logging
log_path = "/tmp/order_reminders_log.txt"
logging.basicConfig(filename=log_path, level=logging.INFO)

# Time range
today = datetime.utcnow()
seven_days_ago = today - timedelta(days=7)

# Format dates for GraphQL if needed
start_date = seven_days_ago.strftime('%Y-%m-%d')
end_date = today.strftime('%Y-%m-%d')

# Setup GraphQL client
transport = RequestsHTTPTransport(url="http://localhost:8000/graphql", verify=True, retries=3)
client = Client(transport=transport, fetch_schema_from_transport=False)

# GraphQL query
query = gql(f"""
query {{
  orders(orderDate_Gte: "{start_date}") {{
    id
    customer {{
      email
    }}
  }}
}}
""")

# Execute query
try:
    response = client.execute(query)
    for order in response.get("orders", []):
        order_id = order["id"]
        customer_email = order["customer"]["email"]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f"{timestamp} - Order ID: {order_id}, Customer Email: {customer_email}")
except Exception as e:
    logging.error(f"Error occurred: {e}")

# Print confirmation
print("Order reminders processed!")
