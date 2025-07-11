def log_crm_heartbeat():
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

     message = f"{timestamp} CRM is alive"

    # Log file path
    log_file = "/tmp/crm_heartbeat_log.txt"

    with open(log_file, "a") as f:
       f.write(message + "\n")

    try:
        from gql import gql, Client
        from gql.transport.requests import RequestsHTTPTransport

        transport = RequestsHTTPTransport(url="http://localhost:8000/graphql", verify=True, retries=2)
        client = Client(transport=transport, fetch_schema_from_transport=False)

        # Simple query
        query = gql("{ hello }")
        response = client.execute(query)
        hello = response.get("hello", "")
        print(f"GraphQL responded with: {hello}")
    except Exception as e:
        print(f"GraphQL hello query failed: {e}")


def update_low_stock():
    log_file = "/tmp/low_stock_updates_log.txt"
    logging.basicConfig(filename=log_file, level=logging.INFO)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Setup GraphQL client
    transport = RequestsHTTPTransport(url="http://localhost:8000/graphql", verify=True, retries=3)
    client = Client(transport=transport, fetch_schema_from_transport=False)

    # GraphQL mutation
    mutation = gql("""
    mutation {
      updateLowStockProducts {
        updatedProducts {
          name
          stock
        }
        message
      }
    }
    """)

    try:
        result = client.execute(mutation)
        updates = result['updateLowStockProducts']['updatedProducts']
        message = result['updateLowStockProducts']['message']

        logging.info(f"{timestamp} - {message}")
        for product in updates:
            logging.info(f"{timestamp} - Restocked {product['name']} to {product['stock']} units")

    except Exception as e:
        logging.error(f"{timestamp} - Failed to update low stock: {e}")