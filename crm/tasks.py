from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    filename='/tmp/crm_report_log.txt',
    level=logging.INFO,
    format='%(message)s',
    filemode='a'
)

@shared_task
def generate_crm_report():
    # Set up GraphQL client
    transport = RequestsHTTPTransport(url='http://localhost:8000/graphql', use_prepared_statements=True)
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Define GraphQL query
    query = gql('''
        query {
            totalCustomers
            totalOrders
            totalRevenue
        }
    ''')

    try:
        # Execute query
        result = client.execute(query)

        # Extract data
        customers = result['totalCustomers']
        orders = result['totalOrders']
        revenue = result['totalRevenue']

        # Log report
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logging.info(f'{timestamp} - Report: {customers} customers, {orders} orders, {revenue} revenue')

    except Exception as e:
        logging.error(f'Error generating CRM report: {str(e)}')