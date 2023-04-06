# Distributed Consciousness Simulator

_by Nima Bavari_

A Distributed Universal Consciousness Simulator with Decaying Autostore-Autoload Mechanism

## Idea

Similar to [Brain Simulator](https://github.com/NimaBavari/brain-simulator) but better!

Here, the universal consciousness is the server and brains are clients, and as many client brains can connect to the server as one wants. The universal consciousness -- the server --, along with serving, also plays the role of the permanent memory and uses a mechanism of key-value store but in a decaying fashion to simulate the decaying nature of the social and natural phenomena. Every connected client brain provides the server with a continuous stream of `dict`s of events and frequencies of its own and is simultaneously bombarded with a continuous stream of response `dict`s of events, timestamps and IPs of matching frequencies from the pool of everything in the permanent memory.

## Usage

Create and activate the virtualenv first by running:

```sh
python3 -m venv simenv
source simenv/bin/activate
```

Then, install the requirements:

```sh
pip install -r requirements.txt
```

Start the consciousness by running:

```sh
python main.py
```

Consciousness is now listening to client brains to connect and stream data.

An example of how client brain code should be, please view `ex_client.py`. You can bombard the server by running

```sh
python ex_client.py
```

from as many machines / terminals as you want.

## Scripts

Run

```sh
chmod +x ./lint.sh
./lint.sh
```

to lint enitre python source code in case you cause any change.

## TODO

* Add exception handling to the server module to handle scenarios such as:
  * Server and clients are running, then server is manually closed. What happens to server?
  * Server and clients are running, one of the clients is manually closed. What happens to server?
