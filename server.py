#!/usr/bin/env python3

import asyncio
import random
import websockets
import threading
import time

event_loop = None
websocket = None
server_ready = threading.Semaphore(value=0)


def server_thread_body():
    """ The body of the thread where asyncio event loop lives
    """
    global event_loop, server_ready
    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    start_server = websockets.serve(receive, '127.0.0.1', 5678)
    event_loop.run_until_complete(start_server)
    print ('Server started')
    server_ready.release()
    event_loop.run_forever()


async def receive(new_websocket, path):
    """ Setup a connection and receive data from the client

    The coroutine is invoked by the websocket server when the page
    is loaded (when the page requests for a websocket)

    After that it is an infinite coroutine run on the websocket server.
    It awaits for any messages, and process them when arrive.
    """
    global websocket
    print(f"Server accessed at path: '{path}'")
    websocket = new_websocket
    while True:
        data = await websocket.recv()
        print (f"Received: {data}")


async def send(data):
    """ Send `data` to the client
    """
    global websocket
    print(f"Sent: {data}")
    await websocket.send(data)


def send_append(data):
    """ Append sending `data` to the client

    This function is a wrapper that injects a `Task` into `event_loop`
    It is necessary to ensure proper thread synchronization
    """
    global event_loop
    event_loop.create_task(send(data))


server_thread = threading.Thread(target=server_thread_body)
server_thread.daemon = True
server_thread.start()
# We wait here for the server to start
server_ready.acquire()
print('Main synchronous loop start')


while True:
    time.sleep(2.0)
    if websocket is None:
        print ('Waiting for websocket (open the `index.html` in browser)')
    else:
        data = "{:0>9}".format(random.randint(0,999999999))
        event_loop.call_soon_threadsafe(send_append, data)

