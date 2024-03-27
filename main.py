from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
import ado
import patch
import psql
import settings

# release_client.get_release_definitions("2d1ccb81-c104-4f43-9181-25603aff23ef")
# release_definition_id, name
# 1, DeliveryTracker
# 6, test by labels
# 7, nsbb by labels
# 8, sheet by labels

NSBB_RELEASE_DEFINITION_ID = 7
SHEET_RELEASE_DEFINITION_ID = 8

patch.patch_azure_devops_client()

# Create a connection to the org
credentials = BasicAuthentication("", settings.PAT)
connection = Connection(base_url=settings.URL, creds=credentials)

release_client = connection.clients.get_release_client()

nsbb_pending = psql.get_pending("nsbb", "prod")
print(f"Found {len(nsbb_pending)} pending deliveries for nsbb")

sheet_pending = psql.get_pending("sheet", "test")
print(f"Found {len(sheet_pending)} pending deliveries for sheet")

nsbb_missing = ado.labels_without_releases(
    release_client=release_client,
    labels=nsbb_pending,
    release_definition=NSBB_RELEASE_DEFINITION_ID,
)

sheet_missing = ado.labels_without_releases(
    release_client=release_client,
    labels=sheet_pending,
    release_definition=SHEET_RELEASE_DEFINITION_ID,
)

print(f"nsbb missing: {nsbb_missing}")
print(f"sheet missing: {sheet_missing}")
