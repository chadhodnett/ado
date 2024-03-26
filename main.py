from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v7_0.core import CoreClient
import patch
import psql

nsbb_pending = psql.get_pending("nsbb", "prod")
print(f"Found {len(nsbb_pending)} pending deliveries for nsbb")

sheet_pending = psql.get_pending("sheet", "test")
print(f"Found {len(sheet_pending)} pending deliveries for sheet")

patch.patch_azure_devops_client()

# Fill in with your personal access token and org URL
personal_access_token = "PAT"
organization_url = "https://dev.azure.com/Nucor-NBT"

# Create a connection to the org
credentials = BasicAuthentication("", personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)

# release_client.get_release_definitions("2d1ccb81-c104-4f43-9181-25603aff23ef")
# release_definition_id, name
# 1, DeliveryTracker
# 6, test by labels
# 7, nsbb by labels
# 8, sheet by labels

release_client = connection.clients.get_release_client()

for label in nsbb_pending:
    releases = release_client.get_releases(
        project="2d1ccb81-c104-4f43-9181-25603aff23ef",
        is_deleted=False,
        status_filter="active",
        search_text=label,
    )

    releases = [r for r in releases if r.release_definition.id == 7]

    if not releases:
        print(f"Found no release for nsbb {label}.")


for label in sheet_pending:
    releases = release_client.get_releases(
        project="2d1ccb81-c104-4f43-9181-25603aff23ef",
        is_deleted=False,
        status_filter="active",
        search_text=label,
    )

    releases = [r for r in releases if r.release_definition.id == 8]

    if not releases:
        print(f"Found no release for sheet {label}.")
