from metrics.views.metrics import metric, metrics_collection


def includeme(config):
    # Define the routes for metrics
    config.add_route('metrics', '/metrics/')
    config.add_route('metric', '/metrics/{mid:\\d+}/')
    # Match the metrics views with the appropriate routes
    config.add_view(metrics_collection,
                    route_name='metrics',
                    renderer='json')
    config.add_view(metric,
                    route_name='metric',
                    renderer='json')
