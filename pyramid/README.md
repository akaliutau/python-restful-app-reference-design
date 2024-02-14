# About

This is an example of the simple Pyramid application

* A classic CRUD service
* Message fields type validation

| Verb   | Endpoint    | Notes                                 |
|--------|-------------|---------------------------------------|
| GET    | metrics/    | Returns all metrics                   |
| GET    | metrics/1   | Returns a single metric               |
| POST   | metrics/    | Create a new metric in the collection |
| DELETE | metrics/1   | Delete an existing metric             |


# Installation

```shell
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
pip install -e ".[testing]"
```

# Running

To start local server

```shell
pserve development.ini
```

```shell
curl -H "Content-Type: application/json" --request GET http://localhost:6543/metrics/
```