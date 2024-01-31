"""REST client handling, including MsIPRangesStream base class."""

from __future__ import annotations

import sys
from typing import Any, Callable, Iterable

import requests

from lxml import html

from singer_sdk import typing as th  # JSON Schema typing helpers
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream

if sys.version_info >= (3, 9):
    import importlib.resources as importlib_resources
else:
    import importlib_resources

_Auth = Callable[[requests.PreparedRequest], requests.PreparedRequest]

class MsIPRangesStream(RESTStream):
    """MsIPRanges stream class."""
    
    name = "azure_ip_ranges"
    path = ""
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = None
    change_number = None
    
    schema = th.PropertiesList(
        th.Property("changeNumber", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property(
            "id",
            th.StringType,
        ),
        th.Property(
          "properties",th.ObjectType(
            th.Property("changeNumber",th.IntegerType),
            th.Property("region" ,th.StringType),
            th.Property("regionId" ,th.IntegerType),
            th.Property("platform",th.StringType),
            th.Property("systemService",th.StringType),
            th.Property("addressPrefixes",th.ArrayType(th.StringType)),
            th.Property("networkFeatures",th.ArrayType(th.StringType)),
          ),
        )
    ).to_dict()

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        
        """Obtain the URL from the download_url - visit the page and extract using XPath."""
        download_url = self.config.get("download_url")
        
        page = requests.get(download_url,headers={'User-Agent':'Mozilla'})
        
        tree = html.fromstring(page.content)
        
        download_link_xpath = self.config.get("download_link_xpath")
        
        download_urls = tree.xpath(download_link_xpath)
        
        download_url = download_urls[self.config.get("download_link_xpath_index")]
        
        return download_url

    records_jsonpath = "$.values[*]"


    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """
        if not self.change_number:
            self.change_number = response.json().get('changeNumber')
            
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())
        
    def post_process(self, row, context):
        """Add extra data to each row."""
        
        # Obtain the change number as retrieved in parse_response
        row['changeNumber'] = self.change_number
        return row
