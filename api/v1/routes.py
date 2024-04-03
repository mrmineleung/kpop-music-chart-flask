from flask import Blueprint, Response, request
from flask_cors import cross_origin

from facade import charts as charts_facade
from facade import playlists as playlists_facade

from enumerations import Charts

api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')


@api_v1.route('/charts')
@cross_origin()
def get_charts():
    return charts_facade.get_charts()


@api_v1.route('/charts/<string:chart_name>')
@cross_origin()
def get_chart_type(chart_name: str):
    if Charts.contains(chart_name) is False:
        return Response(status=200)
    return charts_facade.get_chart_type(Charts(chart_name))


@api_v1.route('/charts/<string:chart_name>/types/<string:chart_type>')
@cross_origin()
def get_chart_data_by_type(chart_name: str, chart_type: str):
    response = charts_facade.get_chart(chart_name, chart_type, request.args)
    if not response:
        return Response(status=200)
    return response


@api_v1.route('/charts/<string:chart_name>/types/<string:chart_type>/playlist')
@cross_origin()
def get_playlist_by_type(chart_name: str, chart_type: str):
    response = playlists_facade.get_playlist(chart_name, chart_type, request.args)
    if not response:
        return Response(status=200)
    return response
