from flask import Blueprint, Response, jsonify, request
from facade import charts as charts_facade

api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')


@api_v1.route('/charts/<string:chart_name>')
def get_chart_data(chart_name: str):
    return {'chart': chart_name}


@api_v1.route('/charts/<string:chart_name>/types/<string:chart_type>')
def get_chart_data_by_type(chart_name: str, chart_type: str):
    response = charts_facade.get_chart(chart_name, chart_type)
    if not response:
        return Response(status=200)
    return response
