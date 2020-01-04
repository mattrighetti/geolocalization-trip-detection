from Utils.metrics_evaluator import metrics_evaluator
import pytest
from shapely.geometry import Point
import numpy as np


#Test that an Exception is raised when the routes_dictionaries list is empty
def test_routes_dictionaries_emptiness():
    route_list = []

    evaluator = metrics_evaluator(route_list)
    with pytest.raises(Exception):
        assert evaluator.evaluate()

#Test that an Exception is raised when the routes_dictionaries is not a list
def test_routes_dictionaries_list_mismatch():
    route_a, route_b, route_c, route_d, route_e, route_f = create_routes()

    routes_list = np.array(route_a)

    evaluator = metrics_evaluator(routes_list)
    with pytest.raises(Exception):
        assert evaluator.evaluate()

#Test that an Exception is raised when the list in routes_dictionaries does not contain dictionaries
def test_routes_dictionaries_type_mismatch():
    route_list = [1,2,4]

    evaluator = metrics_evaluator(route_list)
    with pytest.raises(Exception):
        assert evaluator.evaluate()

# Test the selection method on the first metric
def test_percentage_user():
    route_a, route_b, route_c, route_d, route_e, route_f = create_routes()
    route_list = [route_a, route_b]
    evaluator = metrics_evaluator(route_list)
    assert evaluator.evaluate() == route_a
    assert route_a['vehicle'] == 'BUS'

# Test the selection method on the second metric
def test_number_user_coordinates():
    route_a, route_b, route_c, route_d, route_e, route_f = create_routes()
    route_list = [route_c, route_b]
    evaluator = metrics_evaluator(route_list)
    assert evaluator.evaluate() == route_b
    assert route_b['vehicle'] == 'BUS'


# Test the selection method on the third metric
def test_percentage_poly():
    route_a, route_b, route_c, route_d, route_e, route_f = create_routes()
    route_list = [route_d, route_b]
    evaluator = metrics_evaluator(route_list)
    assert evaluator.evaluate() == route_d
    assert route_d['vehicle'] == 'BUS'


# Test the selection method on the fourth metric
def test_number_polygons():
    route_a, route_b, route_c, route_d, route_e, route_f = create_routes()
    route_list = [route_d, route_e]
    evaluator = metrics_evaluator(route_list)
    assert evaluator.evaluate() == route_e
    assert route_e['vehicle'] == 'BUS'


# Test with all the routes. the function returns only the first of the two optimal dictionaries (c nad f)
def test_all():
    route_a, route_b, route_c, route_d, route_e, route_f = create_routes()
    route_list = [route_a, route_b, route_c, route_d, route_e, route_f]
    evaluator = metrics_evaluator(route_list)
    assert evaluator.evaluate() == route_c
    assert route_c['vehicle'] == 'BUS'



def create_routes():
    route_a = {
        'route': None,
        'vehicle': 'BUS',
        'percentage_user': 0.89,
        'number_user_coordinates': 10,
        'percentage_poly': 0.90,
        'number_polygons': 6
    }
    route_b = {
        'route': None,
        'vehicle': 'BUS',
        'percentage_user': 0.80,
        'number_user_coordinates': 100,
        'percentage_poly': 0.60,
        'number_polygons': 60
    }
    route_c = {
        'route': None,
        'vehicle': 'BUS',
        'percentage_user': 0.84,
        'number_user_coordinates': 10,
        'percentage_poly': 0.90,
        'number_polygons': 70
    }
    route_d = {
        'route': None,
        'vehicle': 'BUS',
        'percentage_user': 0.82,
        'number_user_coordinates': 100,
        'percentage_poly': 0.88,
        'number_polygons': 60
    }

    route_e = {
        'route': None,
        'vehicle': 'BUS',
        'percentage_user': 0.82,
        'number_user_coordinates': 100,
        'percentage_poly': 0.84,
        'number_polygons': 70
    }
    
    route_f = {
        'route': None,
        'vehicle': 'BUS',
        'percentage_user': 0.84,
        'number_user_coordinates': 10,
        'percentage_poly': 0.90,
        'number_polygons': 70
    }
    return route_a, route_b, route_c, route_d, route_e, route_f
