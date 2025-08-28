from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime
import logging

# Configure logging for heartbeat
logging.basicConfig(
    filename='/tmp/crm_heartbeat_log.txt',
    level=logging.INFO,
    format='%(message)s',
    filemode='a'
)

# Configure logging for low stock updates
low_stock_logger = logging.getLogger('low_stock')
low_stock_handler = logging.FileHandler('/tmp/low_stock_updates_log.txt')
low_stock_handler.setFormatter(logging.Formatter('%(asctime)s - Product: %(product_name)s, New Stock: %(new_stock)s'))
low_stock_logger.addHandler(low_stock_handler)
low_stock_logger.setLevel(logging.INFO)

def log_crm_heartbeat():
    # Log heartbeat message with timestamp
    timestamp = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    logging.info(f'{timestamp} CRM is alive')

    # Set up GraphQL client with RequestsHTTPTransport
    transport = RequestsHTTPTransport(url='http://localhost:8000/graphql', use_prepared_statements=True)
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Define GraphQL query for hello field
    query = gql('''
        query {
            hello
        }
    ''')

    try:
        # Execute query to verify GraphQL endpoint
        client.execute(query)
    except Exception as e:
        logging.error(f'GraphQL endpoint error: {str(e)}')

def update_low_stock():
    # Set up GraphQL client
    transport = RequestsHTTPTransport(url='http://localhost:8000/graphql', use_prepared_statements=True)
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Define GraphQL mutation
    mutation = gql('''
        mutation {
            updateLowStockProducts {
                successMessage
                updatedProducts {
                    name
                    stock
                }
            }
        }
    ''')

    try:
        # Execute mutation
        result = client.execute(mutation)
        updated_products = result['updateLowStockProducts']['updatedProducts']

        # Log updated products
        for product in updated_products:
            low_stock_logger.info(
                '',
                extra={'product_name': product['name'], 'new_stock': product['stock']}
            )

    except Exception as e:
        low_stock_logger.error(f'Error updating low stock products: {str(e)}')