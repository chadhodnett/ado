from datetime import datetime, timedelta, timezone
from azure.devops.v7_0.release.release_client import ReleaseClient

PROJECT = "2d1ccb81-c104-4f43-9181-25603aff23ef"
ACTIVE = "active"


def labels_without_releases(release_client: ReleaseClient, labels, release_definition):
    missing = []
    for label in labels:
        releases = release_client.get_releases(
            project=PROJECT,
            is_deleted=False,
            status_filter=ACTIVE,
            search_text=label,
        )

        releases = [
            r for r in releases if r.release_definition.id == release_definition
        ]

        if not releases:
            print(
                f"Found no release for {label} in release definition {release_definition}."
            )
            missing.append(label)

    return missing


def get_recent_deleted_releases(release_client: ReleaseClient, release_definition):
    return [
        r
        for r in release_client.get_releases(
            project=PROJECT,
            status_filter=ACTIVE,
            is_deleted=True,
        )
        if r.release_definition.id == release_definition
    ]


def get_stale_releases(
    release_client: ReleaseClient, release_definition, inactive_days=23
):
    """
    BAD - modified time does not include deployments. This would require
    figuring out the last deployment for a release which is not supported

    https://developercommunity.visualstudio.com/t/how-to-get-latest-version-of-deployment-using-rest/1161013
    """
    releases = release_client.get_releases(
        project=PROJECT,
        status_filter=ACTIVE,
        is_deleted=False,
    )
    while release_client.continuation_token_last_request is not None:
        releases += release_client.get_releases(
            project=PROJECT,
            status_filter=ACTIVE,
            is_deleted=False,
            continuation_token=release_client.continuation_token_last_request,
        )

    print(f"Found {len(releases)} stale releases before filter")

    return [
        r
        for r in releases
        if r.release_definition.id == release_definition
        and datetime.now(timezone.utc) - r.modified_on > timedelta(days=inactive_days)
    ]
