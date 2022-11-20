---
authors: Felix Ableitner <me@nutomic.com>
status: DRAFT
dateReceived: 2022-11-12
---
# FEP-1b12: Group federation


## Summary

Internet forums are probably the oldest form of social media. This document describes how they can be implemented with the ActivityPub protocol.

## History

Friendica released federated forums in version [2019.03](https://github.com/friendica/friendica/releases/tag/2019.03).

Lemmy published the first public beta of federated groups in [v0.8.0 (October 2020)](https://join-lemmy.org/news/2020-10-20_-_Lemmy_Release_v0.8.0_-_Federation_beta!).

## Requirements

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this specification are to be interpreted as described in [RFC-2119].

## Group actor

A federated forum is represented by a `Group` actor as specified in [Activity Vocabulary]. This actor is not directly controlled by a human, but can perform its main functionality in a fully automated way, essentially acting as a bot.

## Following a Group

Public groups SHOULD support a standard `Follow`-`Accept` workflow. This ensures compatibility with existing implementations which support `Person` following using the same vocabulary. After receiving a valid `Follow` activity, the group SHOULD automatically respond with an `Accept`, and add the sender to its followers collection.

Actors can unfollow a group by sending an `Undo/Follow` activity.

Private groups likely require a different mechanism to add followers, which is yet to be specified.

## Audience field

Every activity and object which gets published in a community MUST specify the group actor identifier in the `audience` field.

Example of a `Create/Page` activity:

```
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "type": "Create",
  "id": "https://sally.example.org/a/2"
  "actor": "https://sally.example.org",
  "audience": "https://example.com/my-forum",
  "object": {
    "type": "Page",
    "id": "https://sally.example.org/p/1",
    "attributedTo": "https://sally.example.org",
    "content": "Hello",
    "audience": "https://example.org/my-forum"
  }
}
```

Actors can send such an activity to the group inbox for publishing.


## Threads and comments

Each `Group` actor represents a single forum. Each forum usually contains many user-submitted threads, which can be represented as `Page` objects. Forums can have comments which are usually represented as `Note`, and contain a field `inReplyTo` linking the thread it belongs to. Object representations may differ based on the requirements of each application.

A thread:
```
{
    "type": "Page",
    "id": "https://sally.example.org/p/1",
    "attributedTo": "https://sally.example.org",
    "name": "Hello forum!",
    "audience": "https://example.org/my-forum"
}
```

A comment in that thread:
```
{
    "type": "Note",
    "id": "https://sally.example.org/p/3",
    "attributedTo": "https://sally.example.org",
    "inReplyTo": "https://sally.example.org/p/1",
    "content": "My first comment",
    "audience": "https://example.org/my-forum"
}
```

Groups MAY expose a collection of all threads, and a collection for each thread which contains all comments.

## The Announce activity

The main task of a group is to distribute content among its followers.

When a group receives a activity in its inbox, it SHOULD perform some automatic validation, such as checking for domain and user blocks. Groups MAY require additional validation, such as accepting content only from followers, or even manual approval from group moderators. In case an activity fails these checks, the group MAY respond to the sender with a `Reject` activity.

In case the incoming activity is valid, the group MUST wrap it in an `Announce` activity, with the original activity as object:

```
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "type": "Announce",
  "actor": "https://example.org/my-forum",
  "id": "example.org/a/5",
  "object": {
    "@context": "https://www.w3.org/ns/activitystreams",
    "type": "Create",
    "id": "https://sally.example.org/a/2"
    "actor": "https://sally.example.org",
    "audience": "https://example.org/my-forum",
    "object": {
      "type": "Page",
      "id": "https://sally.example.org/p/1",
      "content": "Hello forum!",
      "audience": "https://example.org/my-forum"
    }
  }
}
```

Implementations SHOULD ensure that activities wrapped in this way keep all their original data. In particular, software may include nonstandard fields on objects it sends. These extra fields should be kept intact by the group actor even if it cannot parse them, for the benefit of followers which use the same software.

After the group successfully verifies and wraps the received activity, it sends it to the inboxes of all group followers. Followers then use the outer `Announce` activity to determine that the content was really approved by the group. After this step the `Announce` can be discarded and only the inner activity shown to users.

This mechanism can be used to publish any possible activity type. Examples include `Announce/Like`, `Announce/Delete/Note` or `Announce/Undo/Like`. Some activity types are reserved for moderation, and SHOULD NOT be announced, unless the group has verified that it was sent by a group moderator. These reserved activities are `Block`, `Delete`, `Ignore`, `Move`, `Remove`, `Undo/Block`, `Undo/Delete`, `Undo/Ignore`, `Undo/Move`, `Undo/Remove`. Other activity types which are meant to be private MUST NOT be announced in any case: `Follow`, `Accept`,  `Join`, `Leave`.

Announced activities SHOULD also get added to the group outbox. If the group exposes collections of threads and comments, relevant items should also be added to them.

## Group moderation

Group moderators are those actors who control the group, are able to change its metadata and remove malicious content. They are listed in the group's `attributedTo` collection:

```
{
  "id": "https://example.org/my-forum",
  "type": "Group",
  "name": "Ten Forward",
  "attributedTo": "https://example.org/my-forum/moderators",
}
```

```
{
  "type": "OrderedCollection",
  "id": "https://example.org/my-forum/moderators",
  "orderedItems": [
    "https://example.org/picard",
    "https://example.org/riker"
  ]
}
```

Group moderators can be changed with `Add` and `Remove` activities. These are only valid if they are announced by the group according to its verification criteria.

```
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "type": "Announce",
  "actor": "https://example.org/my-forum",
  "id": "example.org/a/8",
  "object": {
    "id": "https://example.org/a/7",
    "type": "Add",
    "actor": "https://example.org/picard",
    "object": "http://example.org/data",
    "audience": "https://example.org/my-forum",
    "target": "https://example.org/my-forum/moderators"
  }
}
```

Moderators are responsible for the content which gets published in a community. As such they have the power to view reports received by the group (`Flag`), delete malicious posts (`Announce/Delete`), or ban users (`Announce/Block`).

## Implementations

This document is written based on existing group implementations in Lemmy, Friendica, Hubzilla, Lotide and Peertube. These already federate successfully in production since over two years.

The `audience` field and private groups are not yet implemented. Description of these aspects should serve as the basis for future changes.

## References

- [RFC-2119] S. Bradner, [Key words for use in RFCs to Indicate Requirement Levels](https://tools.ietf.org/html/rfc2119.html)
- [Activity Vocabulary], James M Snell, Evan Prodromou, [Activity Vocabulary](https://www.w3.org/TR/activitystreams-vocabulary/)

## Copyright

CC0 1.0 Universal (CC0 1.0) Public Domain Dedication

To the extent possible under law, the authors of this Fediverse Enhancement Proposal have waived all copyright and related or neighboring rights to this work.