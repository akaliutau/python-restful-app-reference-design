import logging
from datetime import datetime

import colorlog
from flask import Flask
from flask_restful import abort, Api, fields, marshal_with, reqparse, Resource
from pytz import utc

from http_status import HttpStatus
from models import NotificationModel

notification_fields = {
    'nid': fields.Integer,
    'uri': fields.Url('notification_endpoint'),
    'message': fields.String,
    'ttl': fields.Integer,
    'creation_date': fields.DateTime,
    'notification_category': fields.String,
    'displayed_times': fields.Integer,
    'displayed_once': fields.Boolean
}


class Notification(Resource):

    @staticmethod
    def abort_if_notification_not_found(nid: int):
        if nid not in notification_manager.notifications:
            abort(
                HttpStatus.not_found_404.value,
                message="Notification {0} not found".format(nid))

    @marshal_with(notification_fields)
    def get(self, nid: int):
        self.abort_if_notification_not_found(nid)
        return notification_manager.get_notification(nid)

    def delete(self, nid: int):
        self.abort_if_notification_not_found(nid)
        notification_manager.delete_notification(nid)
        return '', HttpStatus.no_content_204.value

    @marshal_with(notification_fields)
    def patch(self, nid: int):
        self.abort_if_notification_not_found(nid)
        notification = notification_manager.get_notification(nid)
        parser = reqparse.RequestParser()
        parser.add_argument('message', type=str)
        parser.add_argument('ttl', type=int)
        parser.add_argument('displayed_times', type=int)
        parser.add_argument('displayed_once', type=bool)
        args = parser.parse_args()

        if 'message' in args and args['message'] is not None:
            notification.message = args['message']
        if 'ttl' in args and args['ttl'] is not None:
            notification.ttl = args['ttl']
        if 'displayed_times' in args and args['displayed_times'] is not None:
            notification.displayed_times = args['displayed_times']
        if 'displayed_once' in args and args['displayed_once'] is not None:
            notification.displayed_once = args['displayed_once']
        return notification


class NotificationList(Resource):

    @marshal_with(notification_fields)
    def get(self):
        return [v for v in notification_manager.notifications.values()]

    @marshal_with(notification_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('message', type=str, required=True, help='Message cannot be blank!')
        parser.add_argument('ttl', type=int, required=True, help='Time to live cannot be blank!')
        parser.add_argument('notification_category', type=str, required=True,
                            help='Notification category cannot be blank!')
        args = parser.parse_args()
        notification = NotificationModel(
            message=args['message'],
            ttl=args['ttl'],
            creation_date=datetime.now(utc),
            notification_category=args['notification_category']
        )
        notification_manager.insert_notification(notification)
        return notification, HttpStatus.created_201.value


class NotificationManager:
    last_id = 0

    def __init__(self):
        self.notifications = {}

    def insert_notification(self, notification):
        self.__class__.last_id += 1
        notification.id = self.__class__.last_id
        self.notifications[self.__class__.last_id] = notification

    def get_notification(self, nid: int):
        return self.notifications[nid]

    def delete_notification(self, nid: int):
        del self.notifications[nid]


notification_manager = NotificationManager()

app = Flask(__name__)
service = Api(app=app)
service.add_resource(NotificationList, '/service/notifications/')
service.add_resource(Notification, '/service/notifications/<int:nid>', endpoint='notification_endpoint')

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s %(asctime)s [%(filename)s] %(levelname)s %(message)s',
    log_colors={
        'INFO': 'black',
        'DEBUG': 'cyan',
        'WARNING': 'yellow',
        'ERROR': 'red'
    }
))

log = app.logger
log.addHandler(handler)
log.setLevel(logging.DEBUG)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
