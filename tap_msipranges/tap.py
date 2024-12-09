"""MsIPRanges tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_msipranges.client import MsIPRangesStream


class TapMsIPRanges(Tap):
    """MsIPRanges tap class."""

    name = "tap-msipranges"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "download_url",
            th.StringType,
            description=(
              "The download url for the Microsoft Azure API Ranges"
            ),
            default="https://www.microsoft.com/en-us/download/details.aspx?id=56519"
        ),
        th.Property(
            "download_link_xpath",
            th.StringType,
            description=(
              "The XPath expression that extracts a list of download links, "
            ),
            default="//a[contains(@href,'download.microsoft.com/download/')]/@href"
        ),
        th.Property(
            "download_link_xpath_index",
            th.IntegerType,
            description=(
              "The index of the element containing the download link - paired with "
              "the download_link_xpath expression"
            ),
            default=0
        )
    ).to_dict()

    def discover_streams(self) -> list[MsIPRangesStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            MsIPRangesStream(self)
        ]


if __name__ == "__main__":
    TapMsIPRanges.cli()
