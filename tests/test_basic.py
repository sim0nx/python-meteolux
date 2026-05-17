from typing import Any

import httpx
import pytest
from pydantic import json

from meteolux.async_api import AsyncMeteoLuxClient
from meteolux.exceptions import NotFoundError
from meteolux.models import (
  ATCReport,
  Bookmarks,
  ObservationMetadataResponse,
  WeatherResponse,
)
import json

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
  mock_response_data_str = """
  {
  "city": {
    "id": 456,
    "name": "Luxembourg",
    "region": "S",
    "canton": "Luxembourg",
    "domain": "fluvial",
    "lat": 49.611567,
    "long": 6.133836
  },
  "forecast": {
    "current": {
      "date": "2026-05-17T22:42:00",
      "icon": {
        "id": 10,
        "name": "Cloudy"
      },
      "wind": {
        "direction": "SE",
        "speed": "05-10",
        "gusts": null
      },
      "rain": "0",
      "snow": "0",
      "type": "current",
      "temperature": {
        "temperature": 10,
        "humidex": null,
        "felt": null
      }
    },
    "hourly": [
      {
        "date": "2026-05-17T18:00:00",
        "icon": {
          "id": 21,
          "name": "Light rain"
        },
        "wind": {
          "direction": "S",
          "speed": "05-10",
          "gusts": null
        },
        "rain": "1-2",
        "snow": 0,
        "type": "hourly",
        "temperature": {
          "temperature": [
            10,
            12
          ],
          "humidex": null,
          "felt": null
        }
      },
      {
        "date": "2026-05-18T00:00:00",
        "icon": {
          "id": 22,
          "name": "Moderate rain"
        },
        "wind": {
          "direction": "SO",
          "speed": "05-10",
          "gusts": null
        },
        "rain": "3-5",
        "snow": 0,
        "type": "hourly",
        "temperature": {
          "temperature": [
            7,
            9
          ],
          "humidex": null,
          "felt": null
        }
      },
      {
        "date": "2026-05-18T06:00:00",
        "icon": {
          "id": 21,
          "name": "Light rain"
        },
        "wind": {
          "direction": "SO",
          "speed": "05-10",
          "gusts": null
        },
        "rain": "1-3",
        "snow": 0,
        "type": "hourly",
        "temperature": {
          "temperature": [
            8,
            10
          ],
          "humidex": null,
          "felt": null
        }
      },
      {
        "date": "2026-05-18T12:00:00",
        "icon": {
          "id": 30,
          "name": "Light rain shower"
        },
        "wind": {
          "direction": "O",
          "speed": "05-10",
          "gusts": null
        },
        "rain": "1-2",
        "snow": 0,
        "type": "hourly",
        "temperature": {
          "temperature": [
            13,
            15
          ],
          "humidex": null,
          "felt": null
        }
      },
      {
        "date": "2026-05-18T18:00:00",
        "icon": {
          "id": 9,
          "name": "Partly cloudy"
        },
        "wind": {
          "direction": "O",
          "speed": "05-10",
          "gusts": null
        },
        "rain": "0",
        "snow": 0,
        "type": "hourly",
        "temperature": {
          "temperature": [
            9,
            11
          ],
          "humidex": null,
          "felt": null
        }
      },
      {
        "date": "2026-05-19T00:00:00",
        "icon": {
          "id": 9,
          "name": "Partly cloudy"
        },
        "wind": {
          "direction": "S",
          "speed": "05-10",
          "gusts": null
        },
        "rain": "0",
        "snow": 0,
        "type": "hourly",
        "temperature": {
          "temperature": [
            5,
            7
          ],
          "humidex": null,
          "felt": null
        }
      },
      {
        "date": "2026-05-19T06:00:00",
        "icon": {
          "id": 21,
          "name": "Light rain"
        },
        "wind": {
          "direction": "S",
          "speed": "05-10",
          "gusts": null
        },
        "rain": "0-1",
        "snow": 0,
        "type": "hourly",
        "temperature": {
          "temperature": [
            6,
            8
          ],
          "humidex": null,
          "felt": null
        }
      },
      {
        "date": "2026-05-19T12:00:00",
        "icon": {
          "id": 21,
          "name": "Light rain"
        },
        "wind": {
          "direction": "S",
          "speed": "05-10",
          "gusts": null
        },
        "rain": "1-2",
        "snow": 0,
        "type": "hourly",
        "temperature": {
          "temperature": [
            12,
            14
          ],
          "humidex": null,
          "felt": null
        }
      },
      {
        "date": "2026-05-19T18:00:00",
        "icon": {
          "id": 21,
          "name": "Light rain"
        },
        "wind": {
          "direction": "S",
          "speed": "10-20",
          "gusts": null
        },
        "rain": "1-2",
        "snow": 0,
        "type": "hourly",
        "temperature": {
          "temperature": [
            11,
            13
          ],
          "humidex": null,
          "felt": null
        }
      },
      {
        "date": "2026-05-20T00:00:00",
        "icon": {
          "id": 17,
          "name": "Light rain and drizzle"
        },
        "wind": {
          "direction": "S",
          "speed": "10-20",
          "gusts": null
        },
        "rain": "1-2",
        "snow": 0,
        "type": "hourly",
        "temperature": {
          "temperature": [
            9,
            11
          ],
          "humidex": null,
          "felt": null
        }
      },
      {
        "date": "2026-05-20T06:00:00",
        "icon": {
          "id": 30,
          "name": "Light rain shower"
        },
        "wind": {
          "direction": "SO",
          "speed": "10-20",
          "gusts": "40-50"
        },
        "rain": "1-2",
        "snow": 0,
        "type": "hourly",
        "temperature": {
          "temperature": [
            11,
            13
          ],
          "humidex": null,
          "felt": null
        }
      },
      {
        "date": "2026-05-20T12:00:00",
        "icon": {
          "id": 30,
          "name": "Light rain shower"
        },
        "wind": {
          "direction": "O",
          "speed": "10-20",
          "gusts": "40-50"
        },
        "rain": "1-2",
        "snow": 0,
        "type": "hourly",
        "temperature": {
          "temperature": [
            15,
            17
          ],
          "humidex": null,
          "felt": null
        }
      },
      {
        "date": "2026-05-20T18:00:00",
        "icon": {
          "id": 9,
          "name": "Partly cloudy"
        },
        "wind": {
          "direction": "SO",
          "speed": "10-20",
          "gusts": null
        },
        "rain": "0",
        "snow": 0,
        "type": "hourly",
        "temperature": {
          "temperature": [
            14,
            16
          ],
          "humidex": null,
          "felt": null
        }
      },
      {
        "date": "2026-05-21T00:00:00",
        "icon": {
          "id": 10,
          "name": "Cloudy"
        },
        "wind": {
          "direction": "SO",
          "speed": "10-20",
          "gusts": null
        },
        "rain": "0",
        "snow": 0,
        "type": "hourly",
        "temperature": {
          "temperature": [
            9,
            11
          ],
          "humidex": null,
          "felt": null
        }
      },
      {
        "date": "2026-05-21T06:00:00",
        "icon": {
          "id": 4,
          "name": "Cloudy"
        },
        "wind": {
          "direction": "O",
          "speed": "05-10",
          "gusts": null
        },
        "rain": "0",
        "snow": 0,
        "type": "hourly",
        "temperature": {
          "temperature": [
            11,
            13
          ],
          "humidex": null,
          "felt": null
        }
      },
      {
        "date": "2026-05-21T12:00:00",
        "icon": {
          "id": 3,
          "name": "Partly cloudy"
        },
        "wind": {
          "direction": "O",
          "speed": "05-10",
          "gusts": null
        },
        "rain": "0",
        "snow": 0,
        "type": "hourly",
        "temperature": {
          "temperature": [
            17,
            19
          ],
          "humidex": null,
          "felt": null
        }
      },
      {
        "date": "2026-05-21T18:00:00",
        "icon": {
          "id": 8,
          "name": "High clouds"
        },
        "wind": {
          "direction": "N",
          "speed": "05-10",
          "gusts": null
        },
        "rain": "0",
        "snow": 0,
        "type": "hourly",
        "temperature": {
          "temperature": [
            16,
            18
          ],
          "humidex": null,
          "felt": null
        }
      },
      {
        "date": "2026-05-22T00:00:00",
        "icon": {
          "id": 7,
          "name": "Clear sky"
        },
        "wind": {
          "direction": "NE",
          "speed": "00-05",
          "gusts": null
        },
        "rain": "0",
        "snow": 0,
        "type": "hourly",
        "temperature": {
          "temperature": [
            10,
            12
          ],
          "humidex": null,
          "felt": null
        }
      },
      {
        "date": "2026-05-22T06:00:00",
        "icon": {
          "id": 1,
          "name": "Sunny"
        },
        "wind": {
          "direction": "NE",
          "speed": "05-10",
          "gusts": null
        },
        "rain": "0",
        "snow": 0,
        "type": "hourly",
        "temperature": {
          "temperature": [
            12,
            14
          ],
          "humidex": null,
          "felt": null
        }
      },
      {
        "date": "2026-05-22T12:00:00",
        "icon": {
          "id": 1,
          "name": "Sunny"
        },
        "wind": {
          "direction": "NE",
          "speed": "00-05",
          "gusts": null
        },
        "rain": "0",
        "snow": 0,
        "type": "hourly",
        "temperature": {
          "temperature": [
            21,
            23
          ],
          "humidex": null,
          "felt": null
        }
      },
      {
        "date": "2026-05-22T18:00:00",
        "icon": {
          "id": 8,
          "name": "High clouds"
        },
        "wind": {
          "direction": "NE",
          "speed": "05-10",
          "gusts": null
        },
        "rain": "0",
        "snow": 0,
        "type": "hourly",
        "temperature": {
          "temperature": [
            18,
            20
          ],
          "humidex": null,
          "felt": null
        }
      }
    ],
    "daily": [
      {
        "date": "2026-05-18T00:00:00",
        "icon": {
          "id": 30,
          "name": "Light rain shower"
        },
        "wind": {
          "direction": "",
          "speed": "05-10",
          "gusts": null
        },
        "rain": "5-7",
        "snow": "0",
        "type": "daily",
        "temperatureMin": {
          "temperature": 7,
          "humidex": null,
          "felt": 7
        },
        "temperatureMax": {
          "temperature": 15,
          "humidex": null,
          "felt": null
        },
        "sunshine": 5,
        "uvIndex": 0
      },
      {
        "date": "2026-05-19T00:00:00",
        "icon": {
          "id": 21,
          "name": "Light rain"
        },
        "wind": {
          "direction": "",
          "speed": "10-20",
          "gusts": null
        },
        "rain": "1-3",
        "snow": "0",
        "type": "daily",
        "temperatureMin": {
          "temperature": 5,
          "humidex": null,
          "felt": 5
        },
        "temperatureMax": {
          "temperature": 14,
          "humidex": null,
          "felt": null
        },
        "sunshine": 0,
        "uvIndex": 0
      },
      {
        "date": "2026-05-20T00:00:00",
        "icon": {
          "id": 30,
          "name": "Light rain shower"
        },
        "wind": {
          "direction": "",
          "speed": "10-20",
          "gusts": "40-50"
        },
        "rain": "1-3",
        "snow": "0",
        "type": "daily",
        "temperatureMin": {
          "temperature": 9,
          "humidex": null,
          "felt": 9
        },
        "temperatureMax": {
          "temperature": 17,
          "humidex": null,
          "felt": null
        },
        "sunshine": 4,
        "uvIndex": 0
      },
      {
        "date": "2026-05-21T00:00:00",
        "icon": {
          "id": 4,
          "name": "Cloudy"
        },
        "wind": {
          "direction": "",
          "speed": "10-20",
          "gusts": null
        },
        "rain": "0",
        "snow": "0",
        "type": "daily",
        "temperatureMin": {
          "temperature": 9,
          "humidex": null,
          "felt": null
        },
        "temperatureMax": {
          "temperature": 19,
          "humidex": null,
          "felt": null
        },
        "sunshine": 7,
        "uvIndex": 0
      },
      {
        "date": "2026-05-22T00:00:00",
        "icon": {
          "id": 1,
          "name": "Sunny"
        },
        "wind": {
          "direction": "",
          "speed": "05-10",
          "gusts": null
        },
        "rain": "0",
        "snow": "0",
        "type": "daily",
        "temperatureMin": {
          "temperature": 10,
          "humidex": null,
          "felt": null
        },
        "temperatureMax": {
          "temperature": 23,
          "humidex": null,
          "felt": null
        },
        "sunshine": 14,
        "uvIndex": 0
      }
    ]
  },
  "vigilances": [],
  "roadStatus": [],
  "ephemeris": {
    "date": "2026-05-17",
    "sunrise": "05:47",
    "sunset": "21:16",
    "moonrise": "05:32",
    "moonset": "22:58",
    "sunshine": 1,
    "moonIcon": {
      "id": "NL",
      "name": "Waxing Crescent"
    },
    "uvIndex": 0
  },
  "radar": {
    "realTime": [
      {
        "date": "2026-05-17T19:49:00Z",
        "provider": "rmib",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/rmib_app_202605171949.jpeg"
      },
      {
        "date": "2026-05-17T19:54:00Z",
        "provider": "rmib",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/rmib_app_202605171954.jpeg"
      },
      {
        "date": "2026-05-17T19:59:00Z",
        "provider": "rmib",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/rmib_app_202605171959.jpeg"
      },
      {
        "date": "2026-05-17T20:04:00Z",
        "provider": "rmib",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/rmib_app_202605172004.jpeg"
      },
      {
        "date": "2026-05-17T20:09:00Z",
        "provider": "rmib",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/rmib_app_202605172009.jpeg"
      },
      {
        "date": "2026-05-17T20:14:00Z",
        "provider": "rmib",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/rmib_app_202605172014.jpeg"
      },
      {
        "date": "2026-05-17T20:18:00Z",
        "provider": "rmib",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/rmib_app_202605172018.jpeg"
      },
      {
        "date": "2026-05-17T20:24:00Z",
        "provider": "rmib",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/rmib_app_202605172024.jpeg"
      },
      {
        "date": "2026-05-17T20:29:00Z",
        "provider": "rmib",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/rmib_app_202605172029.jpeg"
      },
      {
        "date": "2026-05-17T20:34:00Z",
        "provider": "rmib",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/rmib_app_202605172034.jpeg"
      },
      {
        "date": "2026-05-17T20:39:00Z",
        "provider": "rmib",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/rmib_app_202605172039.jpeg"
      },
      {
        "date": "2026-05-17T20:44:00Z",
        "provider": "rmib",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/rmib_app_202605172044.jpeg"
      },
      {
        "date": "2026-05-17T20:49:00Z",
        "provider": "rmib",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/rmib_app_202605172049.jpeg"
      }
    ],
    "forecast": [
      {
        "date": "2026-05-17T20:45:00Z",
        "provider": "dwd",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/dwd_fx_app_202605172045.jpeg"
      },
      {
        "date": "2026-05-17T20:50:00Z",
        "provider": "dwd",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/dwd_fx_app_202605172050.jpeg"
      },
      {
        "date": "2026-05-17T20:55:00Z",
        "provider": "dwd",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/dwd_fx_app_202605172055.jpeg"
      },
      {
        "date": "2026-05-17T21:00:00Z",
        "provider": "dwd",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/dwd_fx_app_202605172100.jpeg"
      },
      {
        "date": "2026-05-17T21:05:00Z",
        "provider": "dwd",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/dwd_fx_app_202605172105.jpeg"
      },
      {
        "date": "2026-05-17T21:10:00Z",
        "provider": "dwd",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/dwd_fx_app_202605172110.jpeg"
      },
      {
        "date": "2026-05-17T21:15:00Z",
        "provider": "dwd",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/dwd_fx_app_202605172115.jpeg"
      },
      {
        "date": "2026-05-17T21:20:00Z",
        "provider": "dwd",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/dwd_fx_app_202605172120.jpeg"
      },
      {
        "date": "2026-05-17T21:25:00Z",
        "provider": "dwd",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/dwd_fx_app_202605172125.jpeg"
      },
      {
        "date": "2026-05-17T21:30:00Z",
        "provider": "dwd",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/dwd_fx_app_202605172130.jpeg"
      },
      {
        "date": "2026-05-17T21:35:00Z",
        "provider": "dwd",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/dwd_fx_app_202605172135.jpeg"
      },
      {
        "date": "2026-05-17T21:40:00Z",
        "provider": "dwd",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/dwd_fx_app_202605172140.jpeg"
      },
      {
        "date": "2026-05-17T21:45:00Z",
        "provider": "dwd",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/dwd_fx_app_202605172145.jpeg"
      }
    ]
  },
  "satellite": {
    "infrared": [
      {
        "date": "2026-05-17T18:10:00Z",
        "provider": "eumetsat",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/app_sat_ir_202605171810.png"
      },
      {
        "date": "2026-05-17T18:30:00Z",
        "provider": "eumetsat",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/app_sat_ir_202605171830.png"
      },
      {
        "date": "2026-05-17T18:40:00Z",
        "provider": "eumetsat",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/app_sat_ir_202605171840.png"
      },
      {
        "date": "2026-05-17T18:50:00Z",
        "provider": "eumetsat",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/app_sat_ir_202605171850.png"
      },
      {
        "date": "2026-05-17T19:00:00Z",
        "provider": "eumetsat",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/app_sat_ir_202605171900.png"
      },
      {
        "date": "2026-05-17T19:10:00Z",
        "provider": "eumetsat",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/app_sat_ir_202605171910.png"
      },
      {
        "date": "2026-05-17T19:30:00Z",
        "provider": "eumetsat",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/app_sat_ir_202605171930.png"
      },
      {
        "date": "2026-05-17T19:40:00Z",
        "provider": "eumetsat",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/app_sat_ir_202605171940.png"
      },
      {
        "date": "2026-05-17T19:50:00Z",
        "provider": "eumetsat",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/app_sat_ir_202605171950.png"
      },
      {
        "date": "2026-05-17T20:00:00Z",
        "provider": "eumetsat",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/app_sat_ir_202605172000.png"
      },
      {
        "date": "2026-05-17T20:10:00Z",
        "provider": "eumetsat",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/app_sat_ir_202605172010.png"
      },
      {
        "date": "2026-05-17T20:30:00Z",
        "provider": "eumetsat",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/app_sat_ir_202605172030.png"
      },
      {
        "date": "2026-05-17T20:40:00Z",
        "provider": "eumetsat",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/app_sat_ir_202605172040.png"
      }
    ],
    "visual": [
      {
        "date": "2026-05-17T18:40:00Z",
        "provider": "eumetsat",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/app_sat_vis_202605171840.png"
      },
      {
        "date": "2026-05-17T18:50:00Z",
        "provider": "eumetsat",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/app_sat_vis_202605171850.png"
      },
      {
        "date": "2026-05-17T19:00:00Z",
        "provider": "eumetsat",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/app_sat_vis_202605171900.png"
      },
      {
        "date": "2026-05-17T19:10:00Z",
        "provider": "eumetsat",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/app_sat_vis_202605171910.png"
      },
      {
        "date": "2026-05-17T19:20:00Z",
        "provider": "eumetsat",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/app_sat_vis_202605171920.png"
      },
      {
        "date": "2026-05-17T19:30:00Z",
        "provider": "eumetsat",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/app_sat_vis_202605171930.png"
      },
      {
        "date": "2026-05-17T19:40:00Z",
        "provider": "eumetsat",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/app_sat_vis_202605171940.png"
      },
      {
        "date": "2026-05-17T19:50:00Z",
        "provider": "eumetsat",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/app_sat_vis_202605171950.png"
      },
      {
        "date": "2026-05-17T20:00:00Z",
        "provider": "eumetsat",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/app_sat_vis_202605172000.png"
      },
      {
        "date": "2026-05-17T20:10:00Z",
        "provider": "eumetsat",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/app_sat_vis_202605172010.png"
      },
      {
        "date": "2026-05-17T20:20:00Z",
        "provider": "eumetsat",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/app_sat_vis_202605172020.png"
      },
      {
        "date": "2026-05-17T20:30:00Z",
        "provider": "eumetsat",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/app_sat_vis_202605172030.png"
      },
      {
        "date": "2026-05-17T20:40:00Z",
        "provider": "eumetsat",
        "url": "https://metapi.ana.lu/api/v1/metapp/image/app_sat_vis_202605172040.png"
      }
    ]
  },
  "data": {
    "history": [
      {
        "date": "2026-05-12T00:00:00",
        "minTemp": 2.9,
        "maxTemp": 3.6,
        "precipitation": 0,
        "meanTemp": 3.3,
        "sunshine": 0
      },
      {
        "date": "2026-05-12T01:00:00",
        "minTemp": 2.3,
        "maxTemp": 3,
        "precipitation": 0,
        "meanTemp": 2.5,
        "sunshine": 0
      },
      {
        "date": "2026-05-12T02:00:00",
        "minTemp": 1.8,
        "maxTemp": 2.6,
        "precipitation": 0,
        "meanTemp": 2.2,
        "sunshine": 0
      },
      {
        "date": "2026-05-12T03:00:00",
        "minTemp": 1.7,
        "maxTemp": 2.2,
        "precipitation": 0,
        "meanTemp": 2,
        "sunshine": 0
      },
      {
        "date": "2026-05-12T04:00:00",
        "minTemp": 1.7,
        "maxTemp": 2.4,
        "precipitation": 0,
        "meanTemp": 2.1,
        "sunshine": 0
      },
      {
        "date": "2026-05-12T05:00:00",
        "minTemp": 1.3,
        "maxTemp": 2.5,
        "precipitation": 0,
        "meanTemp": 2,
        "sunshine": 12
      },
      {
        "date": "2026-05-12T06:00:00",
        "minTemp": 2.4,
        "maxTemp": 3.4,
        "precipitation": 0,
        "meanTemp": 2.8,
        "sunshine": 18
      },
      {
        "date": "2026-05-12T07:00:00",
        "minTemp": 3.4,
        "maxTemp": 4.5,
        "precipitation": 0,
        "meanTemp": 3.9,
        "sunshine": 48
      },
      {
        "date": "2026-05-12T08:00:00",
        "minTemp": 4.4,
        "maxTemp": 5.2,
        "precipitation": 0,
        "meanTemp": 4.9,
        "sunshine": 6
      },
      {
        "date": "2026-05-12T09:00:00",
        "minTemp": 5.1,
        "maxTemp": 6.4,
        "precipitation": 0,
        "meanTemp": 5.7,
        "sunshine": 36
      },
      {
        "date": "2026-05-12T10:00:00",
        "minTemp": 6.1,
        "maxTemp": 7.6,
        "precipitation": 0,
        "meanTemp": 6.7,
        "sunshine": 0
      },
      {
        "date": "2026-05-12T11:00:00",
        "minTemp": 6.8,
        "maxTemp": 7.6,
        "precipitation": 0,
        "meanTemp": 7.2,
        "sunshine": 12
      },
      {
        "date": "2026-05-12T12:00:00",
        "minTemp": 7.3,
        "maxTemp": 8.8,
        "precipitation": 0,
        "meanTemp": 8.1,
        "sunshine": 18
      },
      {
        "date": "2026-05-12T13:00:00",
        "minTemp": 7.7,
        "maxTemp": 9.8,
        "precipitation": 0,
        "meanTemp": 8.2,
        "sunshine": 18
      },
      {
        "date": "2026-05-12T14:00:00",
        "minTemp": 8.3,
        "maxTemp": 9.9,
        "precipitation": 0,
        "meanTemp": 8.9,
        "sunshine": 24
      },
      {
        "date": "2026-05-12T15:00:00",
        "minTemp": 8.9,
        "maxTemp": 9.8,
        "precipitation": 0,
        "meanTemp": 9.3,
        "sunshine": 0
      },
      {
        "date": "2026-05-12T16:00:00",
        "minTemp": 8.8,
        "maxTemp": 9.6,
        "precipitation": 0,
        "meanTemp": 9.2,
        "sunshine": 0
      },
      {
        "date": "2026-05-12T17:00:00",
        "minTemp": 8.8,
        "maxTemp": 9.1,
        "precipitation": 0,
        "meanTemp": 9,
        "sunshine": 0
      },
      {
        "date": "2026-05-12T18:00:00",
        "minTemp": 8.8,
        "maxTemp": 9.1,
        "precipitation": 0,
        "meanTemp": 8.9,
        "sunshine": 0
      },
      {
        "date": "2026-05-12T19:00:00",
        "minTemp": 8.3,
        "maxTemp": 8.9,
        "precipitation": 0,
        "meanTemp": 8.6,
        "sunshine": 0
      },
      {
        "date": "2026-05-12T20:00:00",
        "minTemp": 8,
        "maxTemp": 8.3,
        "precipitation": 0,
        "meanTemp": 8.2,
        "sunshine": 0
      },
      {
        "date": "2026-05-12T21:00:00",
        "minTemp": 7.5,
        "maxTemp": 8,
        "precipitation": 0,
        "meanTemp": 7.8,
        "sunshine": 0
      },
      {
        "date": "2026-05-12T22:00:00",
        "minTemp": 7.2,
        "maxTemp": 7.5,
        "precipitation": 0,
        "meanTemp": 7.4,
        "sunshine": 0
      },
      {
        "date": "2026-05-12T23:00:00",
        "minTemp": 6.9,
        "maxTemp": 7.3,
        "precipitation": 0,
        "meanTemp": 7.2,
        "sunshine": 0
      },
      {
        "date": "2026-05-13T00:00:00",
        "minTemp": 6.4,
        "maxTemp": 7.1,
        "precipitation": 0,
        "meanTemp": 6.8,
        "sunshine": 0
      },
      {
        "date": "2026-05-13T01:00:00",
        "minTemp": 6.5,
        "maxTemp": 6.9,
        "precipitation": 0,
        "meanTemp": 6.8,
        "sunshine": 0
      },
      {
        "date": "2026-05-13T02:00:00",
        "minTemp": 6.4,
        "maxTemp": 7,
        "precipitation": 0,
        "meanTemp": 6.7,
        "sunshine": 0
      },
      {
        "date": "2026-05-13T03:00:00",
        "minTemp": 6.7,
        "maxTemp": 7.3,
        "precipitation": 0,
        "meanTemp": 7,
        "sunshine": 0
      },
      {
        "date": "2026-05-13T04:00:00",
        "minTemp": 6.2,
        "maxTemp": 6.9,
        "precipitation": 0,
        "meanTemp": 6.4,
        "sunshine": 0
      },
      {
        "date": "2026-05-13T05:00:00",
        "minTemp": 6.4,
        "maxTemp": 6.7,
        "precipitation": 0,
        "meanTemp": 6.5,
        "sunshine": 0
      },
      {
        "date": "2026-05-13T06:00:00",
        "minTemp": 6.6,
        "maxTemp": 6.8,
        "precipitation": 0,
        "meanTemp": 6.7,
        "sunshine": 0
      },
      {
        "date": "2026-05-13T07:00:00",
        "minTemp": 6.7,
        "maxTemp": 7.3,
        "precipitation": 0,
        "meanTemp": 6.9,
        "sunshine": 0
      },
      {
        "date": "2026-05-13T08:00:00",
        "minTemp": 7.3,
        "maxTemp": 8.5,
        "precipitation": 0,
        "meanTemp": 7.8,
        "sunshine": 0
      },
      {
        "date": "2026-05-13T09:00:00",
        "minTemp": 8.3,
        "maxTemp": 9.3,
        "precipitation": 0,
        "meanTemp": 8.7,
        "sunshine": 0
      },
      {
        "date": "2026-05-13T10:00:00",
        "minTemp": 9.2,
        "maxTemp": 10.1,
        "precipitation": 0,
        "meanTemp": 9.5,
        "sunshine": 0
      },
      {
        "date": "2026-05-13T11:00:00",
        "minTemp": 9.5,
        "maxTemp": 11.8,
        "precipitation": 0,
        "meanTemp": 10.4,
        "sunshine": 0
      },
      {
        "date": "2026-05-13T12:00:00",
        "minTemp": 10.6,
        "maxTemp": 12.2,
        "precipitation": 0,
        "meanTemp": 11.2,
        "sunshine": 6
      },
      {
        "date": "2026-05-13T13:00:00",
        "minTemp": 8,
        "maxTemp": 12.3,
        "precipitation": 0.6,
        "meanTemp": 10.4,
        "sunshine": 0
      },
      {
        "date": "2026-05-13T14:00:00",
        "minTemp": 8.6,
        "maxTemp": 11.9,
        "precipitation": 0,
        "meanTemp": 10.1,
        "sunshine": 6
      },
      {
        "date": "2026-05-13T15:00:00",
        "minTemp": 10.2,
        "maxTemp": 11.4,
        "precipitation": 0,
        "meanTemp": 11,
        "sunshine": 12
      },
      {
        "date": "2026-05-13T16:00:00",
        "minTemp": 9.1,
        "maxTemp": 10.4,
        "precipitation": 0.1,
        "meanTemp": 9.8,
        "sunshine": 12
      },
      {
        "date": "2026-05-13T17:00:00",
        "minTemp": 8.5,
        "maxTemp": 9.6,
        "precipitation": 0.4,
        "meanTemp": 8.9,
        "sunshine": 0
      },
      {
        "date": "2026-05-13T18:00:00",
        "minTemp": 8.6,
        "maxTemp": 9.1,
        "precipitation": 0,
        "meanTemp": 8.9,
        "sunshine": 0
      },
      {
        "date": "2026-05-13T19:00:00",
        "minTemp": 6.6,
        "maxTemp": 8.5,
        "precipitation": 1.7,
        "meanTemp": 7.2,
        "sunshine": 18
      },
      {
        "date": "2026-05-13T20:00:00",
        "minTemp": 6.3,
        "maxTemp": 6.7,
        "precipitation": 0,
        "meanTemp": 6.4,
        "sunshine": 0
      },
      {
        "date": "2026-05-13T21:00:00",
        "minTemp": 6.4,
        "maxTemp": 6.6,
        "precipitation": 0,
        "meanTemp": 6.5,
        "sunshine": 0
      },
      {
        "date": "2026-05-13T22:00:00",
        "minTemp": 5.3,
        "maxTemp": 6.6,
        "precipitation": 0,
        "meanTemp": 6,
        "sunshine": 0
      },
      {
        "date": "2026-05-13T23:00:00",
        "minTemp": 5.1,
        "maxTemp": 5.6,
        "precipitation": 0,
        "meanTemp": 5.3,
        "sunshine": 0
      },
      {
        "date": "2026-05-14T00:00:00",
        "minTemp": 5.7,
        "maxTemp": 6,
        "precipitation": 0,
        "meanTemp": 5.8,
        "sunshine": 0
      },
      {
        "date": "2026-05-14T01:00:00",
        "minTemp": 5.5,
        "maxTemp": 5.7,
        "precipitation": 0,
        "meanTemp": 5.6,
        "sunshine": 0
      },
      {
        "date": "2026-05-14T02:00:00",
        "minTemp": 5.3,
        "maxTemp": 5.7,
        "precipitation": 0.5,
        "meanTemp": 5.5,
        "sunshine": 0
      },
      {
        "date": "2026-05-14T03:00:00",
        "minTemp": 5.3,
        "maxTemp": 5.5,
        "precipitation": 0.3,
        "meanTemp": 5.4,
        "sunshine": 0
      },
      {
        "date": "2026-05-14T04:00:00",
        "minTemp": 5.3,
        "maxTemp": 5.5,
        "precipitation": 0,
        "meanTemp": 5.5,
        "sunshine": 0
      },
      {
        "date": "2026-05-14T05:00:00",
        "minTemp": 5.2,
        "maxTemp": 5.3,
        "precipitation": 0,
        "meanTemp": 5.3,
        "sunshine": 0
      },
      {
        "date": "2026-05-14T06:00:00",
        "minTemp": 5,
        "maxTemp": 5.3,
        "precipitation": 0.7,
        "meanTemp": 5.2,
        "sunshine": 0
      },
      {
        "date": "2026-05-14T07:00:00",
        "minTemp": 4.5,
        "maxTemp": 5,
        "precipitation": 1.2,
        "meanTemp": 4.8,
        "sunshine": 0
      },
      {
        "date": "2026-05-14T08:00:00",
        "minTemp": 4.6,
        "maxTemp": 6.7,
        "precipitation": 0,
        "meanTemp": 5.6,
        "sunshine": 48
      },
      {
        "date": "2026-05-14T09:00:00",
        "minTemp": 6.3,
        "maxTemp": 8.1,
        "precipitation": 0,
        "meanTemp": 7.1,
        "sunshine": 18
      },
      {
        "date": "2026-05-14T10:00:00",
        "minTemp": 4.6,
        "maxTemp": 9,
        "precipitation": 1.2,
        "meanTemp": 6.9,
        "sunshine": 0
      },
      {
        "date": "2026-05-14T11:00:00",
        "minTemp": 7.3,
        "maxTemp": 9.4,
        "precipitation": 0.1,
        "meanTemp": 8.2,
        "sunshine": 6
      },
      {
        "date": "2026-05-14T12:00:00",
        "minTemp": 5.4,
        "maxTemp": 8.6,
        "precipitation": 1.7,
        "meanTemp": 6.9,
        "sunshine": 0
      },
      {
        "date": "2026-05-14T13:00:00",
        "minTemp": 8.9,
        "maxTemp": 9.9,
        "precipitation": 0,
        "meanTemp": 9.3,
        "sunshine": 6
      },
      {
        "date": "2026-05-14T14:00:00",
        "minTemp": 8.6,
        "maxTemp": 11.1,
        "precipitation": 0,
        "meanTemp": 9.7,
        "sunshine": 36
      },
      {
        "date": "2026-05-14T15:00:00",
        "minTemp": 9.3,
        "maxTemp": 10.8,
        "precipitation": 0,
        "meanTemp": 10,
        "sunshine": 18
      },
      {
        "date": "2026-05-14T16:00:00",
        "minTemp": 9.2,
        "maxTemp": 11,
        "precipitation": 0,
        "meanTemp": 10.1,
        "sunshine": 30
      },
      {
        "date": "2026-05-14T17:00:00",
        "minTemp": 9.2,
        "maxTemp": 10.5,
        "precipitation": 0,
        "meanTemp": 9.7,
        "sunshine": 6
      },
      {
        "date": "2026-05-14T18:00:00",
        "minTemp": 6.8,
        "maxTemp": 9.4,
        "precipitation": 0,
        "meanTemp": 8.1,
        "sunshine": 6
      },
      {
        "date": "2026-05-14T19:00:00",
        "minTemp": 6.4,
        "maxTemp": 7.1,
        "precipitation": 0,
        "meanTemp": 6.6,
        "sunshine": 0
      },
      {
        "date": "2026-05-14T20:00:00",
        "minTemp": 5.2,
        "maxTemp": 6.4,
        "precipitation": 0,
        "meanTemp": 6.1,
        "sunshine": 0
      },
      {
        "date": "2026-05-14T21:00:00",
        "minTemp": 5,
        "maxTemp": 5.5,
        "precipitation": 0,
        "meanTemp": 5.3,
        "sunshine": 0
      },
      {
        "date": "2026-05-14T22:00:00",
        "minTemp": 5.3,
        "maxTemp": 6,
        "precipitation": 0,
        "meanTemp": 5.6,
        "sunshine": 0
      },
      {
        "date": "2026-05-14T23:00:00",
        "minTemp": 5.7,
        "maxTemp": 5.9,
        "precipitation": 0,
        "meanTemp": 5.8,
        "sunshine": 0
      },
      {
        "date": "2026-05-15T00:00:00",
        "minTemp": 5.4,
        "maxTemp": 5.8,
        "precipitation": 0,
        "meanTemp": 5.7,
        "sunshine": 0
      },
      {
        "date": "2026-05-15T01:00:00",
        "minTemp": 5.3,
        "maxTemp": 5.6,
        "precipitation": 0,
        "meanTemp": 5.5,
        "sunshine": 0
      },
      {
        "date": "2026-05-15T02:00:00",
        "minTemp": 5.2,
        "maxTemp": 5.7,
        "precipitation": 0,
        "meanTemp": 5.5,
        "sunshine": 0
      },
      {
        "date": "2026-05-15T03:00:00",
        "minTemp": 4.8,
        "maxTemp": 5.2,
        "precipitation": 0,
        "meanTemp": 4.9,
        "sunshine": 0
      },
      {
        "date": "2026-05-15T04:00:00",
        "minTemp": 4.6,
        "maxTemp": 4.9,
        "precipitation": 0,
        "meanTemp": 4.7,
        "sunshine": 0
      },
      {
        "date": "2026-05-15T05:00:00",
        "minTemp": 4.5,
        "maxTemp": 4.7,
        "precipitation": 0,
        "meanTemp": 4.6,
        "sunshine": 0
      },
      {
        "date": "2026-05-15T06:00:00",
        "minTemp": 4.7,
        "maxTemp": 5.2,
        "precipitation": 0,
        "meanTemp": 4.9,
        "sunshine": 0
      },
      {
        "date": "2026-05-15T07:00:00",
        "minTemp": 5.1,
        "maxTemp": 6.3,
        "precipitation": 0,
        "meanTemp": 5.8,
        "sunshine": 24
      },
      {
        "date": "2026-05-15T08:00:00",
        "minTemp": 6.1,
        "maxTemp": 8.3,
        "precipitation": 0,
        "meanTemp": 7.3,
        "sunshine": 54
      },
      {
        "date": "2026-05-15T09:00:00",
        "minTemp": 7.5,
        "maxTemp": 8.2,
        "precipitation": 0,
        "meanTemp": 7.8,
        "sunshine": 42
      },
      {
        "date": "2026-05-15T10:00:00",
        "minTemp": 6.9,
        "maxTemp": 9.5,
        "precipitation": 0.1,
        "meanTemp": 8.1,
        "sunshine": 18
      },
      {
        "date": "2026-05-15T11:00:00",
        "minTemp": 7.5,
        "maxTemp": 10,
        "precipitation": 0,
        "meanTemp": 8.9,
        "sunshine": 42
      },
      {
        "date": "2026-05-15T12:00:00",
        "minTemp": 8,
        "maxTemp": 11.1,
        "precipitation": 0,
        "meanTemp": 9.2,
        "sunshine": 30
      },
      {
        "date": "2026-05-15T13:00:00",
        "minTemp": 10.5,
        "maxTemp": 12.6,
        "precipitation": 0,
        "meanTemp": 11.5,
        "sunshine": 54
      },
      {
        "date": "2026-05-15T14:00:00",
        "minTemp": 11,
        "maxTemp": 12.9,
        "precipitation": 0,
        "meanTemp": 11.7,
        "sunshine": 36
      },
      {
        "date": "2026-05-15T15:00:00",
        "minTemp": 10.9,
        "maxTemp": 13.2,
        "precipitation": 0,
        "meanTemp": 11.8,
        "sunshine": 18
      },
      {
        "date": "2026-05-15T16:00:00",
        "minTemp": 9.8,
        "maxTemp": 11.1,
        "precipitation": 0,
        "meanTemp": 10.4,
        "sunshine": 0
      },
      {
        "date": "2026-05-15T17:00:00",
        "minTemp": 10.2,
        "maxTemp": 11.2,
        "precipitation": 0,
        "meanTemp": 10.7,
        "sunshine": 0
      },
      {
        "date": "2026-05-15T18:00:00",
        "minTemp": 9.7,
        "maxTemp": 10.6,
        "precipitation": 0,
        "meanTemp": 10.1,
        "sunshine": 0
      },
      {
        "date": "2026-05-15T19:00:00",
        "minTemp": 8.5,
        "maxTemp": 9.7,
        "precipitation": 0,
        "meanTemp": 9.2,
        "sunshine": 0
      },
      {
        "date": "2026-05-15T20:00:00",
        "minTemp": 7.1,
        "maxTemp": 8.6,
        "precipitation": 0,
        "meanTemp": 7.7,
        "sunshine": 0
      },
      {
        "date": "2026-05-15T21:00:00",
        "minTemp": 6,
        "maxTemp": 7.1,
        "precipitation": 0,
        "meanTemp": 6.5,
        "sunshine": 0
      },
      {
        "date": "2026-05-15T22:00:00",
        "minTemp": 5.5,
        "maxTemp": 6.4,
        "precipitation": 0,
        "meanTemp": 5.9,
        "sunshine": 0
      },
      {
        "date": "2026-05-15T23:00:00",
        "minTemp": 4.7,
        "maxTemp": 5.5,
        "precipitation": 0,
        "meanTemp": 5.1,
        "sunshine": 0
      },
      {
        "date": "2026-05-16T00:00:00",
        "minTemp": 4.2,
        "maxTemp": 4.8,
        "precipitation": 0,
        "meanTemp": 4.6,
        "sunshine": 0
      },
      {
        "date": "2026-05-16T01:00:00",
        "minTemp": 3,
        "maxTemp": 4.3,
        "precipitation": 0,
        "meanTemp": 3.7,
        "sunshine": 0
      },
      {
        "date": "2026-05-16T02:00:00",
        "minTemp": 2.8,
        "maxTemp": 3.7,
        "precipitation": 0,
        "meanTemp": 3.3,
        "sunshine": 0
      },
      {
        "date": "2026-05-16T03:00:00",
        "minTemp": 3.4,
        "maxTemp": 3.7,
        "precipitation": 0,
        "meanTemp": 3.5,
        "sunshine": 0
      },
      {
        "date": "2026-05-16T04:00:00",
        "minTemp": 3.7,
        "maxTemp": 4,
        "precipitation": 0,
        "meanTemp": 3.9,
        "sunshine": 0
      },
      {
        "date": "2026-05-16T05:00:00",
        "minTemp": 3.9,
        "maxTemp": 4.2,
        "precipitation": 0,
        "meanTemp": 4,
        "sunshine": 12
      },
      {
        "date": "2026-05-16T06:00:00",
        "minTemp": 3.6,
        "maxTemp": 5.2,
        "precipitation": 0,
        "meanTemp": 4.4,
        "sunshine": 60
      },
      {
        "date": "2026-05-16T07:00:00",
        "minTemp": 5.3,
        "maxTemp": 7,
        "precipitation": 0,
        "meanTemp": 6.2,
        "sunshine": 60
      },
      {
        "date": "2026-05-16T08:00:00",
        "minTemp": 6.6,
        "maxTemp": 8.9,
        "precipitation": 0,
        "meanTemp": 7.8,
        "sunshine": 60
      },
      {
        "date": "2026-05-16T09:00:00",
        "minTemp": 8.4,
        "maxTemp": 9.7,
        "precipitation": 0,
        "meanTemp": 8.8,
        "sunshine": 42
      },
      {
        "date": "2026-05-16T10:00:00",
        "minTemp": 8.6,
        "maxTemp": 9.9,
        "precipitation": 0,
        "meanTemp": 9,
        "sunshine": 0
      },
      {
        "date": "2026-05-16T11:00:00",
        "minTemp": 8.6,
        "maxTemp": 10.4,
        "precipitation": 0,
        "meanTemp": 9.2,
        "sunshine": 0
      },
      {
        "date": "2026-05-16T12:00:00",
        "minTemp": 9.2,
        "maxTemp": 11.3,
        "precipitation": 0,
        "meanTemp": 9.9,
        "sunshine": 6
      },
      {
        "date": "2026-05-16T13:00:00",
        "minTemp": 9.2,
        "maxTemp": 10.7,
        "precipitation": 0,
        "meanTemp": 9.9,
        "sunshine": 6
      },
      {
        "date": "2026-05-16T14:00:00",
        "minTemp": 10,
        "maxTemp": 11.5,
        "precipitation": 0,
        "meanTemp": 10.7,
        "sunshine": 6
      },
      {
        "date": "2026-05-16T15:00:00",
        "minTemp": 10.3,
        "maxTemp": 11,
        "precipitation": 0,
        "meanTemp": 10.6,
        "sunshine": 0
      },
      {
        "date": "2026-05-16T16:00:00",
        "minTemp": 9.9,
        "maxTemp": 11.1,
        "precipitation": 0,
        "meanTemp": 10.4,
        "sunshine": 18
      },
      {
        "date": "2026-05-16T17:00:00",
        "minTemp": 10.1,
        "maxTemp": 11.3,
        "precipitation": 0,
        "meanTemp": 10.6,
        "sunshine": 36
      },
      {
        "date": "2026-05-16T18:00:00",
        "minTemp": 6.5,
        "maxTemp": 10.3,
        "precipitation": 0.6,
        "meanTemp": 7.7,
        "sunshine": 0
      },
      {
        "date": "2026-05-16T19:00:00",
        "minTemp": 6.5,
        "maxTemp": 6.9,
        "precipitation": 0,
        "meanTemp": 6.7,
        "sunshine": 0
      },
      {
        "date": "2026-05-16T20:00:00",
        "minTemp": 6.4,
        "maxTemp": 6.7,
        "precipitation": 0,
        "meanTemp": 6.6,
        "sunshine": 0
      },
      {
        "date": "2026-05-16T21:00:00",
        "minTemp": 5.7,
        "maxTemp": 6.8,
        "precipitation": 0,
        "meanTemp": 6.3,
        "sunshine": 0
      },
      {
        "date": "2026-05-16T22:00:00",
        "minTemp": 5,
        "maxTemp": 5.8,
        "precipitation": 0,
        "meanTemp": 5.4,
        "sunshine": 0
      },
      {
        "date": "2026-05-16T23:00:00",
        "minTemp": 4.8,
        "maxTemp": 5.8,
        "precipitation": 0,
        "meanTemp": 5.3,
        "sunshine": 0
      }
    ],
    "forecast": [
      {
        "date": "2026-05-18",
        "minTemp": 8,
        "maxTemp": 14,
        "precipitation": 7
      },
      {
        "date": "2026-05-19",
        "minTemp": 6,
        "maxTemp": 13,
        "precipitation": 2.5
      },
      {
        "date": "2026-05-20",
        "minTemp": 10,
        "maxTemp": 16,
        "precipitation": 3
      },
      {
        "date": "2026-05-21",
        "minTemp": 10,
        "maxTemp": 18,
        "precipitation": 0
      },
      {
        "date": "2026-05-22",
        "minTemp": 11,
        "maxTemp": 22,
        "precipitation": 0
      },
      {
        "date": "2026-05-23",
        "minTemp": 11,
        "maxTemp": 22,
        "precipitation": 1
      },
      {
        "date": "2026-05-24",
        "minTemp": 12,
        "maxTemp": 22,
        "precipitation": 1
      },
      {
        "date": "2026-05-25",
        "minTemp": 13,
        "maxTemp": 23,
        "precipitation": 0
      },
      {
        "date": "2026-05-26",
        "minTemp": 13,
        "maxTemp": 24,
        "precipitation": 1
      },
      {
        "date": "2026-05-27",
        "minTemp": 13,
        "maxTemp": 24,
        "precipitation": 1
      }
    ]
  }
}
  """
  mock_response_data = json.loads(mock_response_data_str)

  respx_mock.get('https://metapi.ana.lu/api/v1/metapp/weather', params={'lat': 49.6116, 'long': 6.1319, 'langcode': 'en'}).mock(
    return_value=httpx.Response(200, json=mock_response_data)
  )

  client = AsyncMeteoLuxClient()
  weather_response = await client.get_weather(lat=49.6116, long=6.1319, langcode='en')

  assert isinstance(weather_response, WeatherResponse)
  assert weather_response.city.name == 'Luxembourg'
  assert weather_response.forecast.current.temperature.temperature == 10


@pytest.mark.asyncio
async def test_get_observations_metadata_hvd_success(respx_mock) -> None:
  """
  Test the successful response of get_observations_metadata_hvd.
  """
  mock_response_data_str = """
  {
  "licence": [
    "Creative Commons",
    "https://creativecommons.org/public-domain/cc0/"
  ],
  "docUrl": "/docs",
  "data": [
    {
      "id": "string",
      "name": "string",
      "description": "string",
      "dataType": "realtime",
      "unit": "m",
      "category": "Wind",
      "performanceCategory": "A",
      "qualityCode": 0,
      "timeOffsets": "PT0H",
      "timeResolution": "PT1M",
      "sensorLevels": {
        "levelType": "height_above_ground",
        "unit": "m",
        "value": 0
      }
    }
  ],
  "totalItemCount": 1,
  "qualityCodes": {
    "0": "Value is controlled and found O.K."
  },
  "performanceCategory": {
    "A": "The sensor type fulfills the requirements from WMO/CIMOs on measurement accuracy, calibration and maintenance."
  }
}
  """
  mock_response_data = json.loads(mock_response_data_str)

  respx_mock.get('https://metapi.ana.lu/api/v1/hvd/observations/metadata').mock(return_value=httpx.Response(200, json=mock_response_data))

  client = AsyncMeteoLuxClient()
  metadata = await client.get_observations_metadata_hvd()

  assert isinstance(metadata, ObservationMetadataResponse)
  assert metadata.total_item_count == 1
  assert metadata.data[0].name == 'string'
  assert metadata.data[0].unit == 'm'


@pytest.mark.asyncio
async def test_error_handling(respx_mock) -> None:
  """
  Test that an HTTP error status code raises an httpx.HTTPStatusError.
  """
  respx_mock.get('https://metapi.ana.lu/api/v1/atc/report').mock(return_value=httpx.Response(404, json={'detail': 'Not Found'}))

  client = AsyncMeteoLuxClient()
  with pytest.raises(NotFoundError):
    await client.get_atc_report()
