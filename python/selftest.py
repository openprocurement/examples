from datetime import datetime, timedelta
import json

from munch import munchify
from restkit import errors
import yaml

from openprocurement_client.client import TendersClient

TENDER_JSON="""{
  "data": {
    "tenderPeriod": {
      "endDate": "2016-06-01T18:47:47.136678"
    },
    "title": "футляри до державних нагород",
    "minimalStep": {
      "currency": "UAH",
      "amount": 35
    },
    "enquiryPeriod": {
      "endDate": "2016-05-25T18:47:47.136678"
    },
    "procurementMethodType": "belowThreshold",
    "value": {
      "currency": "UAH",
      "amount": 500
    },
    "procuringEntity": {
      "contactPoint": {
        "name": "Державне управління справами",
        "telephone": "0440000000"
      },
      "identifier": {
        "scheme": "UA-EDR",
        "id": "00037256",
        "uri": "http://www.dus.gov.ua/"
      },
      "name": "Державне управління справами",
      "address": {
        "countryName": "Україна",
        "postalCode": "01220",
        "region": "м. Київ",
        "streetAddress": "вул. Банкова, 11, корпус 1",
        "locality": "м. Київ"
      }
    },
    "items": [
      {
        "description": "футляри до державних нагород",
        "classification": {
          "scheme": "CPV",
          "id": "44617100-9",
          "description": "Cartons"
        },
        "additionalClassifications": [
          {
            "scheme": "ДКПП",
            "id": "17.21.1",
            "description": "папір і картон гофровані, паперова й картонна тара"
          }
        ],
        "deliveryAddress": {
          "countryName": "Україна",
          "postalCode": "79000",
          "region": "м. Київ",
          "streetAddress": "вул. Банкова 1",
          "locality": "м. Київ"
        },
        "deliveryDate": {
          "startDate": "2016-07-20T18:47:47.136678",
          "endDate": "2016-07-23T18:47:47.136678"
        },
        "unit": {
          "code": "44617100-9",
          "name": "item"
        },
        "quantity": 5
      }
    ]
  }
}
"""

def tender_listing(client):
    print("\nList of tenders:")
    print("\n".join("{} {}".format(t.id, t.dateModified) for t in client.get_tenders()))

def create_tender(client):
    #with open('tender.json') as data_file:    
    #    tender = munchify(json.load(data_file))
    tender = munchify(json.loads(TENDER_JSON))
    print("")
    print("Creating tender:")
    now=datetime.now()
    tender.data.enquiryPeriod.endDate = (now+timedelta(days=1)).isoformat()
    tender.data.tenderPeriod.endDate = (now+timedelta(days=2)).isoformat()
    try:
        result=client.create_tender(tender)
        print(yaml.safe_dump(result, allow_unicode=True))
    except errors.Unauthorized, e:
        print("Unauthorized")
        print(yaml.safe_dump(json.loads(e.message)))

def main():
    client = TendersClient('', 'https://lb.api-sandbox.openprocurement.org', api_version='2.2')
    #client = TendersClient('f94f208e696846dcbe18dbfcea67b330', 'http://localhost:6543', api_version='2.2')   
    tender_listing(client)
    create_tender(client)

if __name__ == "__main__":
    main()
