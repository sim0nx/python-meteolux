from typing import Any

import httpx
import pytest

from meteolux.async_api import AsyncMeteoLuxClient
from meteolux.exceptions import NotFoundError
from meteolux.models import (
  ATCReport,
  Bookmarks,
  ObservationMetadataResponse,
  WeatherResponse,
)


@pytest.mark.asyncio
async def test_get_atc_report_success(respx_mock) -> None:
  """
  Test the successful response of get_atc_report using the respx fixture.
  """
  # Mock the response data to match the new nested Pydantic model
  mock_response_data: dict[str, Any] = {
    'forecast': {
      'hourly': [
        {
          'date': '2025-08-02T10:00:00Z',
          'qnh': 1013,
          'wind': {'direction': 'S', 'speed': '10kt'},
          'wind1500': {'direction': 'S', 'speed': '12kt'},
          'wind2500': {'direction': 'SW', 'speed': '15kt'},
          'wind5000': {'direction': 'W', 'speed': '20kt'},
          'wind10000': {'direction': 'NW', 'speed': '25kt'},
        }
      ]
    }
  }

  # Mock the specific GET request using the full URL
  respx_mock.get('https://metapi.ana.lu/api/v1/atc/report').mock(return_value=httpx.Response(200, json=mock_response_data))

  # Instantiate the client inside the test
  client = AsyncMeteoLuxClient()

  # Call the client method
  atc_report = await client.get_atc_report()

  # Assert the response is a Pydantic model instance
  assert isinstance(atc_report, ATCReport)

  # Assert the data was parsed correctly according to the new nested structure
  assert isinstance(atc_report.forecast.hourly, list)
  assert len(atc_report.forecast.hourly) == 1
  assert atc_report.forecast.hourly[0].wind.direction == 'S'


@pytest.mark.asyncio
async def test_get_bookmarks_success(respx_mock) -> None:
  """
  Test the successful response of get_bookmarks.
  """
  mock_response_data = {
    'cities': [
      {
        'id': 1,
        'name': 'Luxembourg',
        'region': 'S',
        'canton': 'Luxembourg',
        'domain': 'villes',
        'lat': 49.6116,
        'long': 6.1319,
        'temperature': 20.5,
        'icon': {'id': 1, 'name': 'sun'},
      }
    ],
    'nearestCity': {
      'id': 1,
      'name': 'Luxembourg',
      'region': 'S',
      'canton': 'Luxembourg',
      'domain': 'villes',
      'lat': 49.6116,
      'long': 6.1319,
      'temperature': 20.5,
      'icon': {'id': 1, 'name': 'sun'},
    },
  }

  # Mock the specific GET request with query parameters using the full URL
  respx_mock.get('https://metapi.ana.lu/api/v1/metapp/bookmarks', params={'langcode': 'en', 'lat': 49.6116, 'long': 6.1319}).mock(
    return_value=httpx.Response(200, json=mock_response_data)
  )

  client = AsyncMeteoLuxClient()
  bookmarks = await client.get_bookmarks(langcode='en', lat=49.6116, long=6.1319)

  assert isinstance(bookmarks, Bookmarks)
  assert bookmarks.nearest_city.name == 'Luxembourg'
  assert len(bookmarks.cities) == 1


@pytest.mark.asyncio
async def test_get_weather_success(respx_mock) -> None:
  """
  Test the successful response of get_weather.
  """
  mock_response_data = {
    'city': {'id': 1, 'name': 'Luxembourg', 'region': 'S', 'canton': 'Luxembourg', 'domain': 'villes', 'lat': 49.6116, 'long': 6.1319},
    'forecast': {
      'current': {
        'date': '2025-08-02T16:00:00+02:00',
        'icon': {'id': 1, 'name': 'sun'},
        'wind': {'direction': 'S', 'speed': '10kt', 'gusts': '15kt'},
        'rain': '0.0 mm',
        'snow': '0.0 cm',
        'type': 'current',
        'temperature': {'temperature': 25, 'humidex': None, 'felt': 26},
      },
      'hourly': [],
      'daily': [],
    },
    'vigilances': [
      {
        'datetimeStart': '2025-08-02T00:00:00+02:00',
        'datetimeEnd': '2025-08-03T00:00:00+02:00',
        'level': 2,
        'type': 1,
        'group': 1,
        'region': 'all',
        'description': 'Yellow alert for storms.',
      }
    ],
    'roadStatus': [],
    'ephemeris': {
      'date': '2025-08-02',
      'sunrise': '05:59',
      'sunset': '21:00',
      'moonrise': '12:00',
      'moonset': '02:00',
      'sunshine': 'PT15H1M',
      'moonIcon': {'id': 'full', 'name': 'Full Moon'},
      'uvIndex': 5,
    },
    'radar': {'realTime': [], 'forecast': []},
    'satellite': {'infrared': [], 'visual': []},
    'data': {'history': [], 'forecast': []},
  }

  respx_mock.get('https://metapi.ana.lu/api/v1/metapp/weather', params={'lat': 49.6116, 'long': 6.1319, 'langcode': 'en'}).mock(
    return_value=httpx.Response(200, json=mock_response_data)
  )

  client = AsyncMeteoLuxClient()
  weather_response = await client.get_weather(lat=49.6116, long=6.1319, langcode='en')

  assert isinstance(weather_response, WeatherResponse)
  assert weather_response.city.name == 'Luxembourg'
  # Assertion updated to match the new nested structure
  assert weather_response.forecast.current.temperature.temperature == 25
  assert weather_response.vigilances[0].level == 2


@pytest.mark.asyncio
async def test_get_observations_metadata_hvd_success(respx_mock) -> None:
  """
  Test the successful response of get_observations_metadata_hvd.
  """
  mock_response_data = {
    'licence': ['Creative Commons', 'https://creativecommons.org/public-domain/cc0/'],
    'docUrl': '/docs',
    'data': [
      {
        'id': 'air_temperature',
        'name': 'Air Temperature',
        'description': 'Temperature of the air at 2 m height',
        'dataType': 'realtime',
        'unit': 'degC',
        'category': 'Temperature',
        'performanceCategory': 'A',
        'qualitycode': 0,
        'timeoffsets': 'PT0H',
        'timeresolution': 'PT1M',
        'sensorlevels': {'levelType': 'height_above_ground', 'unit': 'm', 'value': 2.0},
      }
    ],
    'totalItemCount': 1,
    'qualityCodes': {'0': 'Value is controlled and found O.K.'},
    'performanceCategory': {'A': 'The sensor type fulfills the requirements from WMO/CIMOs on measurement accuracy, calibration and maintenance.'},
  }

  respx_mock.get('https://metapi.ana.lu/api/v1/hvd/observations/metadata').mock(return_value=httpx.Response(200, json=mock_response_data))

  client = AsyncMeteoLuxClient()
  metadata = await client.get_observations_metadata_hvd()

  assert isinstance(metadata, ObservationMetadataResponse)
  assert metadata.total_item_count == 1
  assert metadata.data[0].name == 'Air Temperature'
  assert metadata.data[0].unit == 'degC'


@pytest.mark.asyncio
async def test_error_handling(respx_mock) -> None:
  """
  Test that an HTTP error status code raises an httpx.HTTPStatusError.
  """
  respx_mock.get('https://metapi.ana.lu/api/v1/atc/report').mock(return_value=httpx.Response(404, json={'detail': 'Not Found'}))

  client = AsyncMeteoLuxClient()
  with pytest.raises(NotFoundError):
    await client.get_atc_report()
