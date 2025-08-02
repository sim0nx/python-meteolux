"""Live tests for the MeteoLux API client."""

import pytest

from meteolux.async_api import AsyncMeteoLuxClient
from meteolux.exceptions import NotFoundError
from meteolux.models import (
  ATCReport,
  Bookmarks,
  ObservationMetadataResponse,
  WeatherResponse,
)

# Use pytestmark to apply the 'live' marker to all tests in this file.
# To run these tests, you must run pytest with the "-m live" parameter.
pytestmark = pytest.mark.live


@pytest.mark.xfail(reason='The endpoint consistently returns HTTP 404 Not Found.')
@pytest.mark.asyncio
async def test_get_atc_report_live() -> None:
  """Test the live get_atc_report endpoint.
  This test verifies that the live API returns a valid ATCReport object.
  """
  client = AsyncMeteoLuxClient()
  try:
    atc_report = await client.get_atc_report()
    assert isinstance(atc_report, ATCReport)
    # Check that the nested list is not empty
    assert len(atc_report.forecast.hourly) > 0
  finally:
    await client.close()


@pytest.mark.asyncio
async def test_get_bookmarks_live() -> None:
  """Test the live get_bookmarks endpoint.
  This test verifies that the live API returns a valid Bookmarks object.
  """
  client = AsyncMeteoLuxClient()
  try:
    bookmarks = await client.get_bookmarks(langcode='en', lat=49.6116, long=6.1319)
    assert isinstance(bookmarks, Bookmarks)
    # Check that the nearest city is not None and has a name
    assert bookmarks.nearest_city is not None
    assert bookmarks.nearest_city.name == 'Luxembourg'
  finally:
    await client.close()


@pytest.mark.asyncio
async def test_get_weather_live() -> None:
  """Test the live get_weather endpoint.
  This test verifies that the live API returns a valid WeatherResponse object.
  """
  client = AsyncMeteoLuxClient()
  try:
    weather_response = await client.get_weather(lat=49.6116, long=6.1319, langcode='en')
    assert isinstance(weather_response, WeatherResponse)
    # Check a specific nested field to ensure the data is structured correctly
    assert isinstance(weather_response.forecast.current.temperature.temperature, (int, float))
    assert weather_response.city.name == 'Luxembourg'
  finally:
    await client.close()


@pytest.mark.asyncio
async def test_get_observations_metadata_hvd_live() -> None:
  """Test the live get_observations_metadata_hvd endpoint.
  This test verifies that the live API returns a valid ObservationMetadataResponse object.
  """
  client = AsyncMeteoLuxClient()
  try:
    metadata = await client.get_observations_metadata_hvd()
    assert isinstance(metadata, ObservationMetadataResponse)
    # Check that the metadata list is not empty
    assert len(metadata.data) > 0
  finally:
    await client.close()


@pytest.mark.asyncio
async def test_live_error_handling_not_found() -> None:
  """Test live error handling for a 404 Not Found error.
  This test attempts to get a non-existent station and expects a NotFoundError.
  """
  client = AsyncMeteoLuxClient()
  try:
    with pytest.raises(NotFoundError):
      await client.get_station_information_hvd(station_id='non-existent-station')
  finally:
    await client.close()
