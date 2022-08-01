---
authors: silverpill <silverpill@firemail.cc>
status: DRAFT
dateReceived: 2022-08-01
---
# FEP-e232: Object Links

## Summary

This document proposes a way to represent text-based links to [ActivityPub] objects which are similar to mentions. One example of such link is inline quote within the value of the `content` property, but this proposal is not limited to any particular use case.

## Requirements

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC-2119].

## Object links

If object's content has links to other objects, that object MAY have the `tag` property, where each link is represented as a `Link` object, as suggested by [Activity Vocabulary]. The properties of this `Link` object are:

- `type` (REQUIRED): the type MUST be `Link`.
- `mediaType` (REQUIRED): the media type SHOULD be `application/activity+json`.
- `href` (REQUIRED): the href property MUST contain the URI of the referenced object.
- `name` (OPTIONAL): if link is a quote, its representation SHOULD have the `name` property whose value starts with `RE:`, followed by referenced object's URI.

Example:

```json
{
    "type": "Note",
    "content: "This is a quote:<br>RE: https://example.com/objects/123",
    "tag": [
        {
            "type": "Link",
            "mediaType": "application/activity+json",
            "href": "https://example.com/objects/123",
            "name": "RE: https://example.com/objects/123"
        }
    ]
}
```

## Implementations

TBD

## References

- [ActivityPub] Christopher Lemmer Webber, Jessica Tallon, [ActivityPub](https://www.w3.org/TR/activitypub/), 2018
- [RFC-2119] S. Bradner, [Key words for use in RFCs to Indicate Requirement Levels](https://tools.ietf.org/html/rfc2119.html), 1997
- [Activity Vocabulary], James M Snell, Evan Prodromou, [Activity Vocabulary](https://www.w3.org/TR/activitystreams-vocabulary/), 2017

## Copyright

CC0 1.0 Universal (CC0 1.0) Public Domain Dedication 

To the extent possible under law, the authors of this Fediverse Enhancement Proposal have waived all copyright and related or neighboring rights to this work.
