from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication


def labels_without_releases(release_client, labels, release_definition):
    missing = []
    for label in labels:
        releases = release_client.get_releases(
            project="2d1ccb81-c104-4f43-9181-25603aff23ef",
            is_deleted=False,
            status_filter="active",
            search_text=label,
        )

        releases = [
            r for r in releases if r.release_definition.id == release_definition
        ]

        if not releases:
            print(f"Found no release for nsbb {label}.")
            missing.append(label)

    return missing
