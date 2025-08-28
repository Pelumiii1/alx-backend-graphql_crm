#!/bin/bash
# This script deletes customers with no orders since a year ago.

# Navigate to the project root directory
cd "$(dirname "$0")/../../"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
  source venv/bin/activate
fi

# Django management command to delete inactive customers
DELETED_COUNT=$(python manage.py shell <<EOF
from datetime import timedelta
from django.utils import timezone
from alx_backend_graphql_crm.crm.models import Customer

one_year_ago = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.filter(order__date_ordered__lt=one_year_ago, order__isnull=True)
count = inactive_customers.count()
inactive_customers.delete()
print(count)
EOF
)

# Log the number of deleted customers
TIMESTAMP=$(date +"%Y-%m-%d %T")
echo "$TIMESTAMP - Deleted $DELETED_COUNT inactive customers." >> /tmp/customer_cleanup_log.txt
