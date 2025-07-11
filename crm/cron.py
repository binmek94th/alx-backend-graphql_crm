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