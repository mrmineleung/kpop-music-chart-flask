import json
from json import JSONDecodeError
from extensions import mongo


def get_chart(chart_name: str, chart_type: str):
    def _get_melon_chart(chart_type: str):
        if chart_type == 'TOP100':
            try:
                with open('melon_chart.json', 'r') as json_file:
                    data = json.load(json_file)
                return data
            except JSONDecodeError | FileNotFoundError:
                return None
                # return mongo.db.rankings.find_one({'type': chart_type, })
        elif chart_type == 'HOT100':
            try:
                with open('melon_chart_hot100.json', 'r') as json_file:
                    data = json.load(json_file)
                return data
            except JSONDecodeError | FileNotFoundError:
                return None
        elif chart_type == 'DAY':
            try:
                with open('melon_chart_day.json', 'r') as json_file:
                    data = json.load(json_file)
                return data
            except JSONDecodeError | FileNotFoundError:
                return None
        else:
            return None



    charts = {'melon': _get_melon_chart, 'bugs': None, 'flo': None, 'youtube': None, 'spotify': None}

    data = charts[chart_name](chart_type)
    return data

