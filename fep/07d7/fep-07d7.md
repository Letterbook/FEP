---
slug: "07d7"
authors: Jennifer Moore <contact@jenniferplusplus.com>
status: DRAFT
dateReceived: 
discussionsTo: 
---
# FEP-07d7: A Custom URL Scheme and Web-Based Protocol Handlers for Linking to ActivityPub Resources

## Summary

This specification defines a custom URL scheme for use in conjuction with web-based protocol handlers registered with end-user browsers. It additionally specifies when ActivityPub servers can include these links in HTML views they generate, and how the handling server should respond to requests for these urls.

## Motivation

When a person clicks a link to some ActivityPub powered site, the browser will navigate to the resource on that site. This is often *not* what the person wanted when they have an account on a different ActivityPub aware site. In order to interact with the linked resource, the person must separately open their home site and search for the resource. This is an awkward and sometimes confusing process, especially for people who are not already familiar with the idosyncracies of navigating a federated social network.

By utilizing the built-in web-based protocol handler feature of modern web browsers, it's possible to direct links like these to the user's preferred server. The server can retrieve the resource and provide familiar and appropriate handling. Native ActivityPub clients can also take advantage of these URLs to provide similar handling. 

## Context

## Requirements

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this specification are to be interpreted as described in [RFC-2119].

### 1. Definitions

This proposal refers to ActivityPub objects as viewed and represented in multiple ways from multiple servers. For clarity, these are the terms that will be used to describe those scenarios.

Origin server means the server that has authority for the ActivityPub object. This is the server that hosts and controls access to the object, and will recieve requests for the URI used as the object's ID.

Home server means the server with which a person has an account. This is the server that a person would log into in order to send, receive, and/or browse messages on the ActivityPub network.

ActivityPub object means the JSON-LD document representing an ActivityPub Object, as described in the [ActivityPub] and [ActivityStreams] specifications.

HTML representation means an HTML document rendered to display the ActivityPub object for human use.

A client is any software that provides a human-friendly presentation of ActivityPub objects, or can interact with an ActivityPub server. For example, this could be a server's web UI or a native mobile app. This software does not necessarily utilize the C2S profile of the ActivityPub spec.

### 2. URL Scheme

When creating hyperlinks to ActivityPub resources, individuals and applications SHOULD include a link using the custom `web+ap:` scheme. This scheme can be handled by web-based or native handlers registered with browsers by end-users. Because there's no guarantee that a given browser will have any registered handler for this scheme, these links SHOULD NOT be used in place of a link that refers to the resource by ID or an alternative HTML representation of it. Links using the `web+ap:` scheme SHOULD be used as an addition to those more canonical links.

The address provided using the `web+ap:` scheme SHOULD be the same as the referenced ActivityPub object's ID. The address MAY instead be for an alternative human-readable address, or for an HTML representation of the object, as normal for the origin server.

### 3. Protocol Handlers

#### 3.1 ActivityPub Servers

#### 3.2 Clients


## Examples


## Security considerations


## References

- \[ActivityPub\] Christine Lemmer Webber, Jessica Tallon, [ActivityPub], 2018
- \[Web-based Protocol Handlers\] Mozilla Developer Network, [Web-based Protocol Handlers]
- \[HTML Living Standard\] WHATWG, [HTML], 2023

## Copyright

CC0 1.0 Universal (CC0 1.0) Public Domain Dedication

To the extent possible under law, the authors of this Fediverse Enhancement Proposal have waived all copyright and related or neighboring rights to this work.

[RFC-2119]: https://www.rfc-editor.org/rfc/rfc2119
[ActivityPub]: https://www.w3.org/TR/activitypub/
[Web-based Protocol Handlers]: https://developer.mozilla.org/en-US/docs/Web/API/Navigator/registerProtocolHandler/Web-based_protocol_handlers
[HTML]: https://html.spec.whatwg.org/multipage/system-state.html#custom-handlers
[ActivityStreams]: https://www.w3.org/TR/activitystreams-core/