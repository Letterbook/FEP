---
slug: "f1d5"
authors: CJ <cjslep@gmail.com>, silverpill <silverpill@firemail.cc>
status: FINAL
dateReceived: 2020-12-13
discussionsTo: https://codeberg.org/fediverse/fep/issues/50
---
# FEP-f1d5: NodeInfo in Fediverse Software

## Summary

NodeInfo is a protocol intended to standardize upon a way to provide
server-level metadata to the public. This enables tools and clients to utilize
this metadata to assess server health or facilitate end-users choices about
servers and software to use on the Fediverse.

## History

NodeInfo was developed prior to the ActivityPub protocol targeted for use by
diaspora, friendica, and redmatrix software [ActivityPub]. Some of the original
protocols it encapsulated include diaspora, pumpio, and gnusocial.

The NodeInfo specification is incredibly strict in its schema, often requiring
regex-validation and a closed set of enumerated possible values. As an objection
to this, the NodeInfo2 fork was created as a form of criticism by removing some
validation of fields and with some logical restructuring of the metadata.
Building off of NodeInfo and NodeInfo2, ServiceInfo was briefly
explored [ServiceInfo].

This FEP does **not** attempt to document the specific protocol details. For
that, see the [NodeInfoRepository] and [NodeInfo2Repository]. It attempts to
clarify the history and identify shortcomings with the current approaches, to
bring context to developers of Fediverse Software.

## Requirements

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this specification are to
be interpreted as described in [RFC-2119].

Fediverse software SHOULD implement NodeInfo [NodeInfoRepository].

## Caveats

At the time of this FEP's writing, the current objections to the current state
of NodeInfo that have been identified by the community are below. Note that any
technical alternatives identified are meant to be illustrative and not
prescriptive:

* The `software.name` regex is unnecessarily strict. For example, no uppercase
  letters, no spaces, no non-English-alphabet, and no special characters besides
  hyphen are permitted.
* The `software.version` field is required, which is unnecessarily strict.
  Forcibly requiring software to divulge version information is potentially a
  security issue.
* The `inbound` and `outbound` elements are specified as a closed set of enums
  instead of a simple string. Protocol versioning manifests as renaming, having
  to add a new enum, which results in unclear version management.
* The Fediverse software MUST have an `openRegistrations` concept due to it
  being required.
* Lacks an extendable method for identifying and versioning other features, such
  as HTTP Signatures, webfinger, or OAuth. Whereas the specification is very
  strict, the `metadata` is too lax.
* The `usage.users` is not denormalized, such that implementations can provide
  custom pairs of `(activity counts, time period in days)` that make sense for
  the software.
* The `usage.users` assumes that user identity is tied to a specific instance of
  running software. It is unclear how to count `total` users when user identity
  is: spread across multiple servers, spread across multiple groups, or present
  within multiple collections of users. Multiple software instances could each
  have a reasonable claim to counting the user as "using" their software, which
  globally results users being counted more than once.
* The `usage.users` activity counts likewise assume that user identity is tied
  to a specific instance of running software. For the same reasons above, where
  the `total` user counts may result in duplicate counts of the same user across
  all software running, the activity counts `activeHalfYear` and `activeMonth`
  may also result in a globally inflated count.
* The `activeHalfyear` and `activeMonth` are ill-named properties for describing
  the time periods of 180 days and 30 days, respectively. A "half of one year"
  is 180 days 0% of the time and roughly 182.5 days only 75% of the time. A
  month is 30 days only 33% of the time.
* The `localPosts` and `localComments` are not denormalized into pairs of
  `(kind, counts)` for software that, for example, hosts audio files, hosts
  videos, or software that does not have comments, or does not have posts.
* The `localPosts` and `localComments` are required, which is problematic for
  software that does not have comments, or does not have posts.

## Implementations

### Servers

This list is not comprehensive:

* Mastodon
* Matrix
* Pleroma
* PeerTube
* WriteFreely
* Friendica
* Diaspora
* PixelFed
* Misskey
* Funkwhale
* Smithereen
* Plume
* GNU Social
* lemmy
* zap
* Socialhome
* epicyon
* apcore

### Clients

* [The-Federation.Info](https://the-federation.info/)
* [Hello Matrix Public Servers](https://www.hello-matrix.net/public_servers.php)

## References

- [ActivityPub] Christine Lemmer Webber, Jessica Tallon, [ActivityPub](https://www.w3.org/TR/activitypub/), 2018
- [NodeInfoRepository] Jonne Haß, [jhass/nodeinfo](https://github.com/jhass/nodeinfo), 2014
- [NodeInfo2Repository] Jason Robinson, [jaywink/nodeinfo2](https://github.com/jaywink/nodeinfo2), 2016
- [ServiceInfo] Jason Robinson, [ServiceInfo - specification for service metadata](https://web.archive.org/web/20220201002230/https://talk.feneas.org/t/serviceinfo-specification-for-service-metadata/99), 2019
- [RFC-2119] S. Bradner, [Key words for use in RFCs to Indicate Requirement Levels](https://tools.ietf.org/html/rfc2119.html), 1997

## Copyright

CC0 1.0 Universal (CC0 1.0) Public Domain Dedication

To the extent possible under law, the authors of this Fediverse Enhancement
Proposal have waived all copyright and related or neighboring rights to this
work.
