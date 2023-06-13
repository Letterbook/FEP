Feature: Dereferencing URIs with webfinger as described in fep-4adb

  Scenario: User found
    Given Webfinger response:
      """
      {
        "links": [
          {
            "href": "https://having.examples.rocks/endpoints/mooo",
            "rel": "self",
            "type": "application/activity+json"
          }
        ],
        "subject": "acct:moocow@having.examples.rocks"
      }
      """
    When Looking up "acct:moocow@having.examples.rocks"
    Then Lookup at "https://having.examples.rocks/.well-known/webfinger?resource=acct%3Amoocow%40having.examples.rocks"
    Then ActivityPub Object Id is "https://having.examples.rocks/endpoints/mooo"

  Scenario: User found multiple options
    Given Webfinger response:
      """
      {
        "links": [
          {
            "href": "https://having.examples.rocks/themoocow",
            "rel": "http://webfinger.net/rel/profile-page",
            "type": "text/html"
          },
          {
            "href": "https://having.examples.rocks/endpoints/mooo",
            "rel": "self",
            "type": "application/activity+json"
          }
        ],
        "subject": "acct:moocow@having.examples.rocks"
      }
      """
    When Looking up "acct:moocow@having.examples.rocks"
    Then Lookup at "https://having.examples.rocks/.well-known/webfinger?resource=acct%3Amoocow%40having.examples.rocks"
    Then ActivityPub Object Id is "https://having.examples.rocks/endpoints/mooo"

  Scenario: User not found
    Given Webfinger response with 404
    When Looking up "acct:moocow@having.examples.rocks"
    Then Lookup at "https://having.examples.rocks/.well-known/webfinger?resource=acct%3Amoocow%40having.examples.rocks"
    Then None is returned
