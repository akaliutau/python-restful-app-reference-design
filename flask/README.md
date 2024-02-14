# About

This is an example of the simple Flask application

* A classic CRUD service
* Message fields type validation


| Verb   | Endpoint                | Notes                                                  |
|--------|-------------------------|--------------------------------------------------------|
| GET    | service/notifications/  | Returns all notifications                              |
| GET    | service/notifications/1 | Returns a single notification                          |
| POST   | service/notifications/  | Create a new notification in the collection            |
| PATCH  | service/notifications/1 | Update one or more fields for an existing notification |
| DELETE | service/notifications/1 | Delete an existing notification                        |


# Installation

```shell
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

# Running

To start local server
```shell
# export PORT=8080 - optional
python3 service.py
```

This will start a local server:

```shell
 * Serving Flask app 'service'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.201:5000
```

Submit a test payload:

```shell
curl -H "Content-Type: application/json" \
  --request POST \
  --data '{"message": "event will start in 2 minutes", "ttl": 20, "notification_category": "Information"}' \
  http://localhost:5000/service/notifications/
```

Get all notifications:

```shell
curl -H "Content-Type: application/json"   --request GET   http://localhost:5000/service/notifications/
```
