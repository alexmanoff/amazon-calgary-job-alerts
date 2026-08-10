import json
import requests

GRAPHQL_URL = "https://e5mquma77feepi2bdn4d6h3mpu.appsync-api.us-east-1.amazonaws.com/graphql"

QUERY = """
query searchJobCardsByLocation($searchJobRequest: SearchJobRequest!) {
  searchJobCardsByLocation(searchJobRequest: $searchJobRequest) {
    nextToken
    jobCards {
      jobId
      jobTitle
      jobType
      employmentType
      city
      state
      postalCode
      locationName
      totalPayRateMinL10N
      totalPayRateMaxL10N
      scheduleCount
      currencyCode
      distance
      __typename
    }
    __typename
  }
}
"""


def main():
    payload = {
        "operationName": "searchJobCardsByLocation",
        "variables": {
            "searchJobRequest": {
                "locale": "en-CA",
                "country": "Canada",
                "pageSize": 100,
                "geoQueryClause": {
                    "lat": 51.0447,
                    "lng": -114.0719,
                    "unit": "km",
                    "distance": 100,
                },
                "containFilters": [
                    {"key": "isPrivateSchedule", "val": ["false"]}
                ],
                "sorters": [
                    {"fieldName": "totalPayRateMax", "ascending": "false"}
                ],
            }
        },
        "query": QUERY,
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "*/*",
        "Accept-Language": "en-CA,en;q=0.9",
        "Content-Type": "application/json",
        "Origin": "https://hiring.amazon.ca",
        "Referer": "https://hiring.amazon.ca/app",
        "country": "Canada",
        "iscanary": "false",
    }

    response = requests.post(
        GRAPHQL_URL,
        headers=headers,
        json=payload,
        timeout=30,
    )

    print("HTTP STATUS:", response.status_code)
    print("CONTENT TYPE:", response.headers.get("content-type"))

    try:
        data = response.json()
    except ValueError:
        print("BODY START:")
        print(response.text[:3000])
        return

    if data.get("errors"):
        print("GRAPHQL ERRORS:")
        print(json.dumps(data["errors"], indent=2)[:5000])
        return

    result = (data.get("data") or {}).get("searchJobCardsByLocation") or {}
    jobs = result.get("jobCards") or []

    print("JOBS FOUND:", len(jobs))
    print("NEXT TOKEN:", bool(result.get("nextToken")))

    for job in jobs[:20]:
        print("-" * 60)
        print("ID:", job.get("jobId"))
        print("TITLE:", job.get("jobTitle"))
        print("CITY:", job.get("city"))
        print("STATE:", job.get("state"))
        print("LOCATION:", job.get("locationName"))
        print("SCHEDULES:", job.get("scheduleCount"))
        print("PAY:", job.get("totalPayRateMinL10N"), "-", job.get("totalPayRateMaxL10N"))


if __name__ == "__main__":
    main()
