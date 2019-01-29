

# API Design Challenge

## Instruction

This is an single endpoint API that will return a list of users filtered by gender, age, or distance from an origin.

This program uses `Python 3.7` with `Flask 1.0.2` and `PostgreSQL 11.1`

### To run this program locally

__1. Start up a virtual environment__  
`python3 -m venv venv`  
`source ./venv/bin/activate`  

__2. Install dependencies__  
`pip install -r requirements.txt`

__3. Create database__  
`createdb rsapi`

__4. Populate database from users.csv__  
`python generate.py`

__5. To run program__  
`flask run`  
or  
`python app.py`

__6. Make a request to the API__

`curl http://localhost:5000/users?gender=f&dist=100&origin=37.774929,-122.419416&min_age=21&max_age=29`

### Coming soon
 * Basic CRUD operations
 * Data model refactor to improve search when paginating
 * Authentication
 * Refactor distance calculations to use Haversine

## The Challenge

### What’s Required

Write an API endpoint that returns a filtered set of users from the csv provided below.

* Your API endpoint URL is /users ✓
* Your API responds in the above format with valid GeoJSON ✓
* Your API should correctly filter any combination of API parameters ✓
* Your API should utilize a datastore ✓
* Your API should support paginating the number of resulting users ✓

### API Structure

| Parameter | Description                                    |
| --------- | ---------------------------------------------- |
| gender    | Your gender preference: m (male) or f (female) |
| dist      | Maximum match distance in miles                |
| origin    | lat/long string of your location               |
| min_age   | Minimum age preference                         |
| max_age   | Maximum age preference                         |
| page      | Page number                                    |
| per_page  | Items per page                                 |

Given the following request:

GET `/users?gender=f&dist=100&origin=37.774929,-122.419416&min_age=21&max_age=29`

The expected response should contain the following:

```json
{
  "metadata": {
    "path": "/users",
    "query": {
      "gender": "f",
      "dist": 100,
      "origin": "37.774929,-122.419416",
      "min_age": 21,
      "max_age": 29
    }
  },
  "num_results": 1,
  "results": [
    {
      "type": "user",
      "locationHistory": {
        "type": "FeatureCollection",
        "features": [
          {
            "type": "Feature",
            "properties": {
              "city": "Oakland"
            },
            "geometry": {
              "type": "Point",
              "coordinates": [-122.08007812499999, 37.78808138412046]
            }
          },
          {
            "type": "Feature",
            "properties": {
              "city": "San Francisco"
            },
            "geometry": {
              "type": "Point",
              "coordinates": [-120.498046875, 36.24427318493909]
            }
          }
        ]
      },
      "properties": {
        "id": 1,
        "name": "Taylor Swift",
        "age": 27,
        "gender": "f"
      }
    }
  ]
}
```

All query parameters are optional. If a query parameter is missing or the value is invalid, you should skip the related filter.

All minimum and maximum fields should be inclusive (e.g. min_age=21&max_age=23 should return users with an age of 21, 22, or 23).
