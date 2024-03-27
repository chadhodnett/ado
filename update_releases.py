import argparse
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
import ado
import patch
import psql
import settings

NSBB_RELEASE_DEFINITION_ID = 7
SHEET_RELEASE_DEFINITION_ID = 8

# Choices
KEEP, FREE = "keep", "free"
NSBB, SHEET = "nsbb", "sheet"

patch.patch_azure_devops_client()

# Create a connection to the org
credentials = BasicAuthentication("", settings.PAT)
connection = Connection(base_url=settings.URL, creds=credentials)


def keep(releases, preview=True):
    for release in releases:
        ado.keep_release(release_client, release, preview=preview)


def keep_pending_releases(pipeline):

    if args.pipeline == NSBB:
        environment = "prod"
        definition_id = NSBB_RELEASE_DEFINITION_ID
    elif args.pipeline == SHEET:
        environment = "test"
        definition_id = SHEET_RELEASE_DEFINITION_ID
    else:
        raise ValueError

    pending = psql.get_pending(pipeline, environment)

    releases = ado.get_matching_releases(
        release_client=release_client,
        labels=pending,
        release_definition=definition_id,
    )
    keep(releases=releases, preview=preview)


def free_completed_releases(pipeline):
    # get labels where ALL deliveries are successfully deployed to prod
    # this will require a new query

    # for any releases matching the labels
    # set keep_forever=False

    raise NotImplementedError


def read_args():
    parser = argparse.ArgumentParser(description="Convert psi delivery data.")
    parser.add_argument("retention", choices=[KEEP, FREE])
    parser.add_argument("pipeline", choices=[NSBB, SHEET])
    parser.add_argument("-f", "--force", action="store_true")

    return parser.parse_args()


if __name__ == "__main__":
    args = read_args()

    # create a release client
    release_client = connection.clients.get_release_client()

    preview = not args.force

    if args.retention == KEEP:
        keep_pending_releases(args.pipeline)
    elif args.retention == FREE:
        free_completed_releases(args.pipeline)
    else:
        raise NotImplementedError
