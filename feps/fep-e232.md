---
authors: silverpill <silverpill@firemail.cc>
status: DRAFT
dateReceived: 2022-08-01
discussionsTo: https://codeberg.org/fediverse/fep/issues/14
---
# FEP-e232: Object Links

## Summary

This document proposes a way to represent text-based links to [ActivityPub] objects which are similar to mentions. One example of such link is inline quote within the value of the `content` property, but this proposal is not limited to any particular use case.

## Requirements

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC-2119].

## Object links

It is expected that software will allow users to define object links using some kind of microsyntax, similar to `@mention` and `#hashtag` microsyntaxes. The exact way of defining object links may vary depending on the use case and is out of scope of this document.

If an object's `name`, `summary`, or `content` has qualified links to other objects, that object SHOULD have the `tag` property, where each object link is represented as a `Link` object, as suggested by [Activity Vocabulary]. The properties of this `Link` object are:

- `type` (REQUIRED): the type MUST be `Link` or a subtype.
- `mediaType` (REQUIRED): the media type MUST be `application/ld+json; profile="https://www.w3.org/ns/activitystreams"`. This specification only deals with ActivityPub objects but in practice the media type can be different and servers MAY accept object links which do not comply with the requirement. For example, a media type of `application/activity+json` SHOULD be treated as equivalent.
- `href` (REQUIRED): the href property MUST contain the URI of the referenced object.
- `name` (OPTIONAL): the `name` SHOULD match the microsyntax used in object's content.
- `rel` (OPTIONAL): if relevant, the `rel` SHOULD specify how the link is related to the current resource. Using `rel` can provide additional purpose to object links by signaling specific intended use-cases.

Example:

```json
{
    "@context": "https://www.w3.org/ns/activitystreams",
    "type": "Note",
    "content": "This is a quote:<br>RE: https://server.example/objects/123",
    "tag": [
        {
            "type": "Link",
            "mediaType": "application/ld+json; profile=\"https://www.w3.org/ns/activitystreams\"",
            "href": "https://server.example/objects/123",
            "name": "RE: https://server.example/objects/123"
        }
    ]
}
```

Note that the `content` includes the `RE: <url>` microsyntax but consuming implementations are not required to parse that in order to make the appropriate associations.

## Implementations

- (streams)
- FoundKey
- Mitra

## References

- [ActivityPub] Christine Lemmer Webber, Jessica Tallon, [ActivityPub](https://www.w3.org/TR/activitypub/), 2018
- [RFC-2119] S. Bradner, [Key words for use in RFCs to Indicate Requirement Levels](https://tools.ietf.org/html/rfc2119.html), 1997
- [Activity Vocabulary], James M Snell, Evan Prodromou, [Activity Vocabulary](https://www.w3.org/TR/activitystreams-vocabulary/), 2017

## Copyright

CC0 1.0 Universal (CC0 1.0) Public Domain Dedication 

To the extent possible under law, the authors of this Fediverse Enhancement Proposal have waived all copyright and related or neighboring rights to this work.
