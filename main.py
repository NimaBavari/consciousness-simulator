import asyncio
import base64
import datetime
import json
import logging
import sys

import aioredis
import websockets

from constants import DECAY_DIFF_PER_SEC, RADIUS_REL_SIZE, REDIS_CLIENT_PARAMS

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
logger.addHandler(handler)

redis_client = aioredis.StrictRedis(**REDIS_CLIENT_PARAMS)


async def autostore(t, ip, freq, event):
    dataload = base64.b64encode(str({"time": t, "IP": ip, "freq": freq, "event": event}).encode("utf-8"))
    await redis_client.lpush("store", dataload)


async def autoload(t, freq):
    for mem_in_base64 in await redis_client.lrange("store", 0, -1):
        mem = eval(base64.b64decode(mem_in_base64).decode("utf-8"))
        freq_in_past = freq / (1 - DECAY_DIFF_PER_SEC) ** (t - mem["time"])
        if 1 - RADIUS_REL_SIZE < mem["freq"] / freq_in_past < 1 + RADIUS_REL_SIZE:
            return {k: v for k, v in mem.items() if k != "freq"}
    return {"time": 0, "IP": "N/A", "event": 0}


async def handler(ws_protocol):
    client_ip = "%s:%d" % ws_protocol.remote_address
    while True:
        chunk = await ws_protocol.recv()
        chunk_decoded = json.loads(chunk)
        event = chunk_decoded["event"]
        freq = chunk_decoded["freq"]
        current_time = datetime.datetime.now().timestamp()
        await autostore(current_time, client_ip, freq, event)
        output = await autoload(current_time, freq)
        output_encoded = json.dumps(output).encode("utf-8")
        await ws_protocol.send(output_encoded)


async def serve():
    async with websockets.serve(handler, "0.0.0.0", 8080):
        logger.log(logging.INFO, "Serving...")
        await asyncio.Future()
    logger.log(logging.INFO, "Websocket closed.")


if __name__ == "__main__":
    try:
        asyncio.run(serve())
    except (KeyboardInterrupt, RuntimeError):
        logger.log(logging.INFO, "Shutting down the consciousness gracefully...")
    except websockets.exceptions.ConnectionClosedOK:
        logger.log(logging.INFO, "A client brain disconnected.")
