---
authors: Michael Puckett <michael@puckett.contact>
status: DRAFT
dateReceived: 2023-04-10
---

# FEP-5bf0: Collection sorting and filtering

## Summary

This proposal would allow Collections to have a `streams` property, as Actors do. The streams would be additional Collections that are sorted or filtered versions of the original Collection.

Additionally, metadata about the sorting/filtering could be indicated using new proposed additions to the ActivityStreams vocabulary: `orderedBy`, `reversed`, `filteredProperty`, and `filteredValue`.

## Implementation

Sorted Collections would always be of the type `Collection` so as not to violate the purpose of OrderedCollections, but would use `orderedItems` instead of `items`. The `reversed` property would indicate that a sorted Collection is in the reverse order.

The `filteredProperty` and `filteredValue` attributes would indicate the specific property being filtered and its corresponding value. These attributes can be represented as strings that reference properties from the Activity Vocabulary (e.g., `type` and `Person`).

When multiple filters are applied, both `filteredProperty` and `filteredValue` would be arrays of strings.

When applying filters to properties within nested objects, dot notation would identify the targeted property for filtering (e.g., `object.type`).

## Motivations

Some ActivityPub clients rely only on C2S protocols for accessing Collections and displaying the nested items.

Currently, in order to support filtering or sorting, these clients need to retrieve all paginated items, assemble them, manually sort or filter them, and then re-paginate them.

This proposal would allow servers to perform these kinds of operations, either at runtime or ahead of time, to ease the burden on clients.

Regarding S2S protocols: other servers should be free to explore the Collections, but they can be easily ignored, along with the new properties.

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
      "summary": "Hashtags, Ordered by Name (A -> Z)",
      "type": "Collection",
      "totalItems": 100,
      "first": "https://example.social/hashtags/ordered/name/page/1",
      "last": "https://example.social/hashtags/ordered/name/page/2",
      "orderedBy": "name"
    },
    {
      "id": "https://example.social/hashtags/ordered/name/reversed",
      "url": "https://example.social/hashtags/ordered/name/reversed",
      "name": "Hashtags",
      "summary": "Hashtags, Ordered by Name (Z -> A)",
      "type": "Collection",
      "totalItems": 100,
      "first": "https://example.social/hashtags/ordered/name/reversed/page/1",
      "last": "https://example.social/hashtags/ordered/name/reversed/page/2",
      "orderedBy": "name",
      "reversed": true
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
      "filteredProperty": "type",
      "filteredValue": "Like"
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
      "filteredProperty": ["type", "object.type"],
      "filteredValue": ["Create", "Note"]
    }
  ]
}
```

Note that this example using an Actor's Inbox may be more suitably linked via an Actor's `streams` instead of on the Inbox itself but is designed to show how filters might work.

## Security

Servers could in theory make available a templated URL endpoint that allows for arbitrary sorting or filtering. This should be discouraged, as it could lead to database injections. Instead, only predetermined sorted/filtered Collections should be made available via the `streams` property.

## References

- [ActivityPub] Christine Lemmer Webber, Jessica Tallon, [ActivityPub](https://www.w3.org/TR/activitypub/), 2018

## Copyright

CC0 1.0 Universal (CC0 1.0) Public Domain Dedication

To the extent possible under law, the authors of this Fediverse Enhancement Proposal have waived all copyright and related or neighboring rights to this work.
