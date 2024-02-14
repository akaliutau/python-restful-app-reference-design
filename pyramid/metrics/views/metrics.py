from pyramid.httpexceptions import HTTPCreated, HTTPNotFound, HTTPBadRequest, HTTPMethodNotAllowed, HTTPNoContent
from pyramid.response import Response
from pyramid.view import view_config
from metrics.models.metrics import DronMetricModel, DronMetricManager, SurferStatus, DronMetricSchema

metric_manager = DronMetricManager()
metric_schema = DronMetricSchema()


def get_metric_or_not_found(mid):
    if id in metric_manager.metrics:
        return metric_manager.metrics[mid]
    else:
        raise HTTPNotFound("Metric {0} doesn't exist".format(mid))


"""
Metrics collection
"""


@view_config(route_name='metrics',
             accept='application/json',
             renderer='json')
def metrics_collection(request):
    if request.method == 'GET':
        metrics = metric_manager.metrics.values()
        dump_result = metric_schema.dump(metrics, many=True)
        return dump_result
    elif request.method == 'POST':
        print(len(request.json_body))
        if not request.json_body:
            raise HTTPBadRequest('No input data provided')
        errors = metric_schema.validate(request.json_body)
        if errors:
            raise HTTPBadRequest(errors)
        metric_ref = DronMetricModel(
            status=SurferStatus[request.json_body['status']],
            speed_in_mph=request.json_body['speed_in_mph'],
            altitude_in_feet=request.json_body['altitude_in_feet'],
            air_temperature_in_f=request.json_body['air_temperature_in_f'])
        metric_manager.insert_metric(metric_ref)
        dumped_metric = metric_schema.dump(metric_ref).data
        response = Response()
        response.status_code = HTTPCreated.code
        response.content_type = 'application/json; charset=UTF-8'
        response.json_body = dumped_metric
        return response
    else:
        # The method is neither GET nor POST
        raise HTTPMethodNotAllowed()


"""
Metric resource
"""


@view_config(route_name='metric',
             accept='application/json',
             renderer='json')
def metric(request):
    mid = int(request.matchdict['mid'])
    metric_ref = get_metric_or_not_found(mid)
    if request.method == 'GET':
        dumped_metric = metric_schema.dump(metric_ref).data
        return dumped_metric
    elif request.method == 'DELETE':
        metric_manager.delete_metric(mid)
        return HTTPNoContent()
    else:
        # The method is neither GET nor DELETE
        raise HTTPMethodNotAllowed()
