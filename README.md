# Minimal websocket/asyncio demo

This is what I think a minimal websocket/asyncio demo that allows for **synchronous** execution on the server side, because it delegates the `asyncio` event loop to a thread. It's nothing special, really, but it is build from well known blocks in the way that it works. It does not support multiple client access and the termination is quite ungraceful at times (these were not on the feature list).
