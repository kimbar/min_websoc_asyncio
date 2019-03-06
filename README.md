# Minimal websocket/asyncio demo

This is what I think a minimal websocket/asyncio demo that allows for **synchronous** execution on the server side, because it delegates the `asyncio` event loop to a thread. It's nothing special, really, but it is build from well known blocks in the way that it works. It does not support multiple client access and the termination is quite ungraceful at times (these were not on the feature list).

## How to run

Run the `server.py` file with Python >=3.7 and open the `index.html` page in a browser on the same machine. Firefox 65.0.2 (64 bit) was tested, but any modern browser should work.

## How it works, step by step

The Python process spawns a thread on which an `asyncio` event loop is run. On this event loop a `websockets` server is setup. When the `index.html` is opened in a browser it creates a websocket that connects to local machine 5678 port. This triggers server's `receive` coroutine on the Python side. This coroutine awaits for any messages sent from client via the websocket.

Because the event loop is run on a separate thread, the main thread on the Python side can be utilised in traditional synchronous way. Each 2 seconds a random number is send to the client, by creating an `asyncio.Task` on the server event loop in a thread-safe manner.

The client side displays the random numbers in boxes with checkboxes. Clicking on the checkboxes sends a message via the websocket that can be received on the Python side in the websocket server.
