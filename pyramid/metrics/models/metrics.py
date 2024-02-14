from enum import Enum
from marshmallow import Schema, fields
from marshmallow_enum import EnumField


class DronMetricModel:
    def __init__(self, status, speed_in_mph, altitude_in_feet, air_temperature_in_f):
        # We will automatically generate the new id
        self.mid = 0
        self.status = status
        self.speed_in_mph = speed_in_mph
        self.altitude_in_feet = altitude_in_feet
        self.air_temperature_in_f = air_temperature_in_f


class DronMetricManager:
    last_id = 0

    def __init__(self):
        self.metrics = {}

    def insert_metric(self, metric):
        self.__class__.last_id += 1
        metric.id = self.__class__.last_id
        self.metrics[self.__class__.last_id] = metric

    def get_metric(self, mid):
        return self.metrics[mid]

    def delete_metric(self, mid):
        del self.metrics[mid]


class SurferStatus(Enum):
    IDLE = 0
    LIFTOFF = 1
    FLYING = 2
    FLIGHT_FINISHED = 3
    LANDING = 4


class DronMetricSchema(Schema):
    mid = fields.Integer(dump_only=True)
    status = EnumField(enum=SurferStatus, required=True)
    speed_in_mph = fields.Integer(required=True)
    altitude_in_feet = fields.Integer(required=True)
    air_temperature_in_f = fields.Integer(required=True)
