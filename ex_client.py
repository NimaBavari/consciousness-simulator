"""Example client brain."""
import asyncio
import json
import logging
import random
import sys

import websockets

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
logger.addHandler(handler)


def feeder():
    # Customize it according to your needs
    while True:
        yield {"event": random.randint(0, 2**64 - 1), "freq": random.uniform(0, 1000)}


async def ws_client(host, port, gen):
    logger.log(logging.INFO, "Connecting to ws://%s:%d." % (host, port))
    async with websockets.connect("ws://%s:%s" % (host, port)) as conn:
        for chunk in gen:
            logger.log(logging.INFO, "Sending %s to the server." % chunk)
            encoded_chunk = json.dumps(chunk).encode("utf-8")
            await conn.send(encoded_chunk)
            data = await conn.recv()
            decoded_data = json.loads(data)
            logger.log(logging.INFO, "Received %s from the server." % decoded_data)
            # yield decoded_data  # for further processing
        logger.log(logging.INFO, "Connection is being closed.")


try:
    asyncio.run(ws_client("127.0.0.1", 8080, feeder()))
except websockets.exceptions.ConnectionClosedError:
    logger.log(logging.INFO, "Server was stopped.")
except KeyboardInterrupt:
    logger.log(logging.INFO, "Disconnected.")
