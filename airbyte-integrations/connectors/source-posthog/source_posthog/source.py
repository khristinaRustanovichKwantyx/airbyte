#
# Copyright (c) 2021 Airbyte, Inc., all rights reserved.
#

from typing import Any, List, Mapping, Tuple

import pendulum
import requests
from airbyte_cdk.logger import AirbyteLogger
from airbyte_cdk.models import SyncMode
from airbyte_cdk.sources import AbstractSource
from airbyte_cdk.sources.streams import Stream
from airbyte_cdk.sources.streams.http.auth import TokenAuthenticator

from .streams import (
    Annotations,
    Cohorts,
    Events,
    EventsSessions,
    FeatureFlags,
    Insights,
    InsightsPath,
    InsightsSessions,
    Persons,
    PingMe,
    Trends,
)

DEFAULT_BASE_URL = "https://app.posthog.com"


class SourcePosthog(AbstractSource):
    def check_connection(self, logger: AirbyteLogger, config: Mapping[str, Any]) -> Tuple[bool, Any]:
        try:
            _ = pendulum.parse(config["start_date"])
            authenticator = TokenAuthenticator(token=config["api_key"])
            base_url = config.get("base_url", DEFAULT_BASE_URL)

            stream = PingMe(authenticator=authenticator, base_url=base_url)
            records = stream.read_records(sync_mode=SyncMode.full_refresh)
            _ = next(records)
            return True, None
        except Exception as e:
            if isinstance(e, requests.exceptions.HTTPError) and e.response.status_code == requests.codes.UNAUTHORIZED:
                return False, f"Please check you api_key. Error: {repr(e)}"
            return False, repr(e)

    def streams(self, config: Mapping[str, Any]) -> List[Stream]:
        """
        event/sessions stream is dynamic. Probably, it contains a list of CURRENT sessions.
        In Next day session may expire and wont be available via this endpoint.
        So we need a dynamic load data before tests.
        This stream was requested to be removed due to this reason.
        """
        authenticator = TokenAuthenticator(token=config["api_key"])
        base_url = config.get("base_url", DEFAULT_BASE_URL)

        return [
            Annotations(authenticator=authenticator, start_date=config["start_date"], base_url=base_url),
            Cohorts(authenticator=authenticator, base_url=base_url),
            Events(authenticator=authenticator, start_date=config["start_date"], base_url=base_url),
            EventsSessions(authenticator=authenticator, base_url=base_url),
            FeatureFlags(authenticator=authenticator, base_url=base_url),
            Insights(authenticator=authenticator, base_url=base_url),
            InsightsPath(authenticator=authenticator, base_url=base_url),
            InsightsSessions(authenticator=authenticator, base_url=base_url),
            Persons(authenticator=authenticator, base_url=base_url),
            Trends(authenticator=authenticator, base_url=base_url),
        ]
