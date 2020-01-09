class metrics_evaluator(object):

    def __init__(self, route_dictionaries: list):
        self.route_dictionaries = route_dictionaries

    def evaluate(self):

        self.check_input_corretness()

        # Get the metrics
        metrics = list(self.route_dictionaries[0].keys())
        metrics.remove('route')
        metrics.remove('vehicle')

        best_routes = self.route_dictionaries

        # Compare the list elements using one metric at time
        for metric in metrics:
            best_routes = self._evaluate_metric(best_routes, metric)

            # In case there is only one route stop the computation before the loop ends
            if len(best_routes) == 1:
                break

        # Return the first elements in case there are, after the evaluation, routes with the same metrics values
        return best_routes[0]

    # Check if all the data structures are the one expected by the class
    def check_input_corretness(self):
        # Check that the route dictionaries list is not empty
        if (len(self.route_dictionaries) == 0):
            raise Exception('Route dictionaries is empty')
        
        # Check that route dictionaries is a list
        if (not isinstance(self.route_dictionaries, list)):
            raise Exception('Route dictionaries is not a list but ' + str(type(self.route_dictionaries)))

        # Check that the route dictionaries contains dictionaries
        if (not isinstance(self.route_dictionaries[0], dict)):
            raise Exception('Route dictionaries does not contain dictionaries but ' + str(type(self.route_dictionaries[0])))

    # Evaluate the list of dictionary on a single metric
    def _evaluate_metric(self, routes: list, metric: str):
        best_routes_partial = []

        # Find the highest metric value in the dictionary
        metric_values = [x[metric] for x in routes]
        max_value = max(metric_values)

        # Consider only the dictionaries having a metric value that is quite the same(5% of uncertainty for percentage values)
        # Don't apply any uncertainty mechanism on non percentage metrics
        if max_value <= 1:
            uncertainty = 0.05
            max_value -= uncertainty

            for route in routes:
                if route[metric] >= max_value:
                    best_routes_partial.append(route)
        else:
            # the metric is not a percentage value, don't apply the uncertainty
            for route in routes:
                if route[metric] >= max_value:
                    best_routes_partial.append(route)

        return best_routes_partial