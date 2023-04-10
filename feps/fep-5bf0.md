---
authors: Michael Puckett <michael@puckett.contact>
status: DRAFT
dateReceived: 2023-04-10
---

# FEP-5bf0: Collection sorting and filtering

## Summary

This proposal would allow Collections to have a `streams` property, as Actors do. The streams would be additional Collections that are sorted or filtered versions of the original Collection.

The property that determines the sort order and/or the filtered property should be made available, possibly via the `context` property. The examples below use [Schema.org's `PropertyValue`](https://schema.org/PropertyValue) for lack of a better vocabulary.

Sorted Collections would always be of the type `OrderedCollection`. The `current` property would indicate a sorted Collection with a reverse-ordered sort.

## Motivations

Some ActivityPub clients rely only on C2S protocols for accessing Collections and displaying the nested items.

Currently, in order to support filtering or sorting, these clients need to retrieve all paginated items, assemble them, manually sort or filter them, and then re-paginate them.

This proposal would allow servers to perform these kinds of operations to ease the burden on clients.

## Examples

### Sorting

Hashtags will typically be entered into a database according to the order of creation, however it is more useful for them to be displayed alphabetically.

```json
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "id": "https://example.social/hashtags",
  "url": "https://example.social/hashtags",
  "name": "Hashtags",
  "type": "Collection",
  "totalItems": 100,
  "first": "https://example.social/hashtags/page/1",
  "last": "https://example.social/hashtags/page/2",
  "streams": [
    {
      "id": "https://example.social/hashtags/ordered/name",
      "url": "https://example.social/hashtags/ordered/name",
      "name": "Hashtags",
      "summary": "Hashtags, Ordered by Name",
      "type": "OrderedCollection",
      "totalItems": 100,
      "first": "https://example.social/hashtags/ordered/name/page/1",
      "last": "https://example.social/hashtags/ordered/name/page/2",
      "current": "https://example.social/hashtags/ordered/name/reverse",
      "context": [
        {
          "type": "https://schema.org/PropertyValue",
          "https://schema.org/name": "sortedByProperty",
          "https://schema.org/value": "name"
        }
      ]
    }
  ]
}
```

### Filtering

Here, an Actor's Inbox returns all Activities posted by the Actor, and the server also provides filtered versions for client consumption.

The first filtered stream returns only the Like Activities.

The second filtered stream filters Activities by their type and their nested Object's type to return only created Notes.

```json
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "id": "https://example.social/@alyssa/inbox",
  "url": "https://example.social/@alyssa/inbox",
  "name": "Inbox",
  "type": "OrderedCollection",
  "totalItems": 1000,
  "first": "https://example.social/@alyssa/inbox/page/1",
  "last": "https://example.social/@alyssa/inbox/page/2",
  "streams": [
    {
      "id": "https://example.social/@alyssa/inbox/likes",
      "url": "https://example.social/@alyssa/inbox/likes",
      "name": "Likes",
      "summary": "Incoming Likes to Alyssa's Inbox",
      "type": "OrderedCollection",
      "totalItems": 100,
      "first": "https://example.social/@alyssa/inbox/likes/page/1",
      "last": "https://example.social/@alyssa/inbox/likes/page/2",
      "current": "https://example.social/@alyssa/inbox/likes/reverse",
      "context": [
        {
          "type": "https://schema.org/PropertyValue",
          "https://schema.org/name": "filteredByProperty",
          "https://schema.org/value": "type"
        },
        {
          "type": "https://schema.org/PropertyValue",
          "https://schema.org/name": "filteredByValue",
          "https://schema.org/value": "Like"
        }
      ]
    },
    {
      "id": "https://example.social/@alyssa/inbox/notes",
      "url": "https://example.social/@alyssa/inbox/notes",
      "name": "Notes",
      "summary": "Incoming Notes to Alyssa's Inbox",
      "type": "OrderedCollection",
      "totalItems": 100,
      "first": "https://example.social/@alyssa/inbox/notes/page/1",
      "last": "https://example.social/@alyssa/inbox/notes/page/2",
      "current": "https://example.social/@alyssa/inbox/notes/reverse",
      "context": [
        {
          "type": "https://schema.org/PropertyValue",
          "https://schema.org/name": "filteredByProperty",
          "https://schema.org/value": "type"
        },
        {
          "type": "https://schema.org/PropertyValue",
          "https://schema.org/name": "filteredByValue",
          "https://schema.org/value": "Create"
        },
        {
          "type": "https://schema.org/PropertyValue",
          "https://schema.org/name": "filteredByProperty",
          "https://schema.org/value": "object.type"
        },
        {
          "type": "https://schema.org/PropertyValue",
          "https://schema.org/name": "filteredByProperty",
          "https://schema.org/value": "Note"
        }
      ]
    }
  ]
}
```

## Security

Servers could in theory make available a templated URL endpoint that allows for arbitrary sorting or filtering. This should be discouraged, as it could lead to database injections. Instead, only predetermined sorted/filtered Collections should be made available via the `streams` property.

## References

- [ActivityPub] Christine Lemmer Webber, Jessica Tallon, [ActivityPub](https://www.w3.org/TR/activitypub/), 2018
- [ABC] Alyssa P.Hacker, [An example proposal](http://example.org/abc.html), 2020

## Copyright

CC0 1.0 Universal (CC0 1.0) Public Domain Dedication

To the extent possible under law, the authors of this Fediverse Enhancement Proposal have waived all copyright and related or neighboring rights to this work.
