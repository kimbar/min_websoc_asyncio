#!/usr/bin/env python3

import asyncio
import random
import websockets
import threading
import time
from queue import Queue

event_loop = None
websocket = None
connection_ready = threading.Semaphore(value=0)
recievied_data = Queue()


def server_thread_body():
    """ The body of the thread where asyncio event loop lives
    """
    global event_loop
    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    start_server = websockets.serve(receive, '127.0.0.1', 5678)
    event_loop.run_until_complete(start_server)
    print ('Server started')
    event_loop.run_forever()


async def receive(new_websocket, path):
    """ Setup a connection and receive data from the client

    The coroutine is invoked by the websocket server when the page
    is loaded (when the page requests for a websocket). It releases
    the `connection_ready` semaphore what starts main synchronous loop
    of the script.

    After that it is an infinite coroutine run on the websocket server.
    It awaits for any messages, and process them when arrive.
    """
    global websocket, connection_ready, recievied_data
    print(f"Server accessed at path: '{path}'")
    websocket = new_websocket
    connection_ready.release()
    while True:
        data = await websocket.recv()
        recievied_data.put(data)


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
# We wait here for the server to start and client to connect
connection_ready.acquire()
print('Main synchronous loop start')


while True:
    data = "{:0>9}".format(random.randint(0,999999999))
    event_loop.call_soon_threadsafe(send_append, data)
    time.sleep(2.0)
    while not recievied_data.empty():
        print("Recieved: {}".format(recievied_data.get()))
