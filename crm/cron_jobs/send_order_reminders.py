from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(
    filename='/tmp/order_reminders_log.txt',
    level=logging.INFO,
    format='%(asctime)s - Order ID: %(order_id)s, Customer Email: %(email)s'
)

# Set up GraphQL client
transport = AIOHTTPTransport(url='http://localhost:8000/graphql')
client = Client(transport=transport, fetch_schema_from_transport=True)

# Define GraphQL query
query = gql('''
    query GetPendingOrders($startDate: DateTime!) {
        orders(orderDate_Gte: $startDate) {
            id
            customerEmail
        }
    }
''')

async def send_order_reminders():
    # Calculate date range (last 7 days)
    start_date = datetime.now() - timedelta(days=7)
    
    try:
        # Execute query
        result = await client.execute_async(
            query,
            variable_values={'startDate': start_date.isoformat()}
        )
        
        # Log each order
        for order in result['orders']:
            logging.info(
                '',
                extra={'order_id': order['id'], 'email': order['customerEmail']}
            )
        
        print("Order reminders processed!")
        
    except Exception as e:
        logging.error(f"Error processing reminders: {str(e)}")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(send_order_reminders())