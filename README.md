# tap-msipranges

`tap-msipranges` is a Singer tap for Microsoft Azure IP Ranges and Service Tags – Public Cloud.

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

The tap extracts the current download link from the page: [Azure IP Ranges and Service Tags – Public Cloud](https://www.microsoft.com/en-us/download/confirmation.aspx?id=56519), which is of the format:
`https://download.microsoft.com/download/7/1/D/{GUID}/ServiceTags_Public_{release_yyyymmdd}.json`. It then leverages the Meltano SDK to extract and produce Singer spec records to stdout, to be fed into a Singer target.

## Installation

Install from GitHub:

```bash
pipx install git+https://github.com/ORG_NAME/tap-msipranges.git@main
```

## Capabilities

* `catalog`
* `state`
* `discover`
* `about`
* `stream-maps`
* `schema-flattening`
* `batch`

## Settings

By default this tap goes to [Azure IP Ranges and Service Tags – Public Cloud](https://www.microsoft.com/en-us/download/confirmation.aspx?id=56519) - however it could be reconfigured to extract a download link from any Microsoft `/download/confirmation.aspx` type page. The JSON schema is hardcoded into `tap_msipranges/client.py` - so that would need to be updated for other file structures.

The settings below are provided should the "Azure IP Ranges" MS page move or be reconfigured such that the JSON download link is not found at the 'failoverLink' location (the failoverLink is the "Click here if your download has not started automatically link"):

| Setting                  | Required | Default | Description |
|:-------------------------|:--------:|:-------:|:------------|
| download_url             | False    | https://www.microsoft.com/en-us/download/confirmation.aspx?id=56519 | The download url for the Microsoft Azure API Ranges |
| download_link_xpath      | False    | //a[contains(@class, 'failoverLink') and contains(@href,'download.microsoft.com/download/')]/@href | The XPath expression that extracts a list of download links  |
| download_link_xpath_index| False    |       0 | The index of the element containing the download link - paired with the download_link_xpath expression |
| stream_maps              | False    | None    | Config object for stream maps capability. For more information check out [Stream Maps](https://sdk.meltano.com/en/latest/stream_maps.html). |
| stream_map_config        | False    | None    | User-defined config values to be used within map expressions. |
| flattening_enabled       | False    | None    | 'True' to enable schema flattening and automatically expand nested properties. |
| flattening_max_depth     | False    | None    | The max depth to flatten schemas. |
| batch_config             | False    | None    |             |

A full list of supported settings and capabilities is available by running: `tap-msipranges --about`

## Supported Python Versions

* 3.8
* 3.9
* 3.10
* 3.11
* 3.12
* 3.13
* 3.14
* 3.15
* 3.16

A full list of supported settings and capabilities for this
tap is available by running:

```bash
tap-msipranges --about
```

### Configure using environment variables

This Singer tap will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.

### Source Authentication and Authorization

Not required, the source is a public webpage

## Usage

You can easily run `tap-msipranges` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-msipranges --version
tap-msipranges --help
tap-msipranges --config CONFIG --discover > ./catalog.json
```

## Developer Resources

Follow these instructions to contribute to this project.

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-msipranges` CLI interface directly using `poetry run`:

```bash
poetry run tap-msipranges --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

<!--
Developer TODO:
Your project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any "TODO" items listed in
the file.
-->

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-msipranges
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-msipranges --version
# OR run a test `elt` pipeline:
meltano elt tap-msipranges target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
