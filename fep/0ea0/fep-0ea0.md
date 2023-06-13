---
slug: "0ea0"
authors: silverpill <silverpill@firemail.cc>
status: DRAFT
dateReceived: 2023-04-18
discussionsTo: https://codeberg.org/fediverse/fep/issues/88
---
# FEP-0ea0: Payment Links

## Summary

This FEP describes a way to attach payment information to [ActivityPub](https://www.w3.org/TR/activitypub/) actors and objects. That information might be a link to donation page, a link for buying an artwork, or anything else that can be represented with a URI.

## Payment links

Payment link is an object with the following properties:

- `type` (REQUIRED): the type MUST be `Link`.
- `name` (RECOMMENDED): the `name` property SHOULD contain a human-readable description of the payment link.
- `href` (REQUIRED): the `href` property MUST contain a payment URI. This can be a URL of a website, or any other kind of URI, such as [payto URI](https://datatracker.ietf.org/doc/html/rfc8905).
- `rel` (REQUIRED):  the `rel` property MUST contain the string `payment` or an array containing that string. The `payment` relation type is defined in [Link Relations Registry](https://www.iana.org/assignments/link-relations/link-relations.xhtml).

Payment links MUST be added to `attachment` array of an actor or an object.

## Examples

Payment link attached to an actor:

```json
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "type": "Person",
  "id": "https://example.tld/users/alice",
  "inbox": "https://example.tld/users/alice/inbox",
  "outbox": "https://example.tld/users/alice/outbox",
  "attachment": [
    {
      "type": "Link",
      "name": "Donate",
      "href": "payto://iban/DE75512108001245126199",
      "rel": "payment"
    }
  ]
}
```

Payment link attached to an object:

```json
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "type": "Image",
  "id": "https://example.tld/photos/123",
  "attributedTo": "https://example.tld/users/alice",
  "name": "Painting of a cat",
  "attachment": [
    {
      "type": "Link",
      "name": "Buy",
      "href": "https://example.tld/photos/123/order",
      "rel": [
        "payment",
        "https://example.tld/ns#buy"
      ]
    }
  ]
}
```

## Payment links as actor metadata

(This section is non-normative.)

Implementers may treat payment links attached to actor object in the same way as actor metadata fields. In that case, `name` translates into field label and `href` translates into field value.

## References

- [ActivityPub] Christine Lemmer Webber, Jessica Tallon, [ActivityPub](https://www.w3.org/TR/activitypub/), 2018
- [Link Relations Registry] IANA, [Link Relations](https://www.iana.org/assignments/link-relations/link-relations.xhtml), 2005

## Copyright

CC0 1.0 Universal (CC0 1.0) Public Domain Dedication

To the extent possible under law, the authors of this Fediverse Enhancement Proposal have waived all copyright and related or neighboring rights to this work.
