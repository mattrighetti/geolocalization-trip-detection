from Utils.metrics_evaluator import metrics_evaluator

# Test the selection method on the first metric
def test_percentage_user():
    route_a, route_b, route_c, route_d, route_e, route_f = create_routes()
    route_list = [route_a, route_b]
    evaluator = metrics_evaluator(route_list)
    assert evaluator.evaluate() == route_a

# Test the selection method on the second metric
def test_number_user_coordinates():
    route_a, route_b, route_c, route_d, route_e, route_f = create_routes()
    route_list = [route_c, route_b]
    evaluator = metrics_evaluator(route_list)
    assert evaluator.evaluate() == route_b

# Test the selection method on the third metric
def test_percentage_poly():
    route_a, route_b, route_c, route_d, route_e, route_f = create_routes()
    route_list = [route_d, route_b]
    evaluator = metrics_evaluator(route_list)
    assert evaluator.evaluate() == route_d

# Test the selection method on the fourth metric
def test_number_polygons():
    route_a, route_b, route_c, route_d, route_e, route_f = create_routes()
    route_list = [route_d, route_e]
    evaluator = metrics_evaluator(route_list)
    assert evaluator.evaluate() == route_e

# Test with all the routes. the function returns only the first of the two optimal dictionaries (c nad f)
def test_all():
    route_a, route_b, route_c, route_d, route_e, route_f = create_routes()
    route_list = [route_a, route_b, route_c, route_d, route_e, route_f]
    evaluator = metrics_evaluator(route_list)
    assert evaluator.evaluate() == route_c


def create_routes():
    route_a = {
        "route": None,
        "percentage_user": 0.89,
        "number_user_coordinates": 10,
        "percentage_poly": 0.90,
        "number_polygons": 6
    }
    route_b = {
        "route": None,
        "percentage_user": 0.80,
        "number_user_coordinates": 100,
        "percentage_poly": 0.60,
        "number_polygons": 60
    }
    route_c = {
        "route": None,
        "percentage_user": 0.84,
        "number_user_coordinates": 10,
        "percentage_poly": 0.90,
        "number_polygons": 70
    }
    route_d = {
        "route": None,
        "percentage_user": 0.82,
        "number_user_coordinates": 100,
        "percentage_poly": 0.88,
        "number_polygons": 60
    }

    route_e = {
        "route": None,
        "percentage_user": 0.82,
        "number_user_coordinates": 100,
        "percentage_poly": 0.84,
        "number_polygons": 70
    }
    
    route_f = {
        "route": None,
        "percentage_user": 0.84,
        "number_user_coordinates": 10,
        "percentage_poly": 0.90,
        "number_polygons": 70
    }
    return route_a, route_b, route_c, route_d, route_e, route_f
