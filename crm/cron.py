from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    filename='/tmp/crm_heartbeat_log.txt',
    level=logging.INFO,
    format='%(message)s',
    filemode='a'
)

async def log_crm_heartbeat():
    # Log heartbeat message with timestamp
    timestamp = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    logging.info(f'{timestamp} CRM is alive')

    # Set up GraphQL client
    transport = AIOHTTPTransport(url='http://localhost:8000/graphql')
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Define GraphQL query for hello field
    query = gql('''
        query {
            hello
        }
    ''')

    try:
        # Execute query to verify GraphQL endpoint
        await client.execute_async(query)
    except Exception as e:
        logging.error(f'GraphQL endpoint error: {str(e)}')