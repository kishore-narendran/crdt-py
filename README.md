# Conflict-free Replicated Data Types (CRDTs) for Python

A library, that provides Conflict-free Replicated Data Types (CRDTs) for distributed Python applications. The intent of this middleware is to provide a simple interface for handling CRDTs and to use them in Python applications. For more information on CRDT, read [here](https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type).

[Sai Teja Ranuva](https://github.com/saitejar) and I created this library for our CS 237 - Distributed Systems Middleware class, at University of California, Irvine in the Spring of 2016.

##Installation

1. Install Virtualenv, by following the instructions [here](https://virtualenv.pypa.io/en/latest/installation.html)
2. Clone this repository
3. Run the command `virtualenv crdt-py` when in the folder that has the cloned repository
4. Change directory to the project `cd crdt-py`
5. Run the activate script `source bin/activate`
6. Install the dependencies `pip install -r requirements.txt`

NOTE - When done using and developing for this project, run the command `deactivate`

##Dependencies

1. This project needs a running copy of [Redis](http://redis.io/) locally. Get a copy of Redis, [here](http://redis.io/download).
