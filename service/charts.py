import json
from json import JSONDecodeError

from extensions import mongo


def get_available_charts():
    return mongo.db.rankings.distinct('chart', {})


def get_available_chart_type(chart_name: str):
    return mongo.db.rankings.distinct('type', {"chart": chart_name})


def get_chart(chart_name: str, chart_type: str):
    charts = {'melon': _get_melon_chart, 'billboard': _get_billboard_chart, 'bugs': None, 'flo': None, 'youtube': None,
              'spotify': None}

    data = charts[chart_name](chart_type)
    return data


def _get_billboard_chart(chart_type: str):
    if chart_type is not None:
        try:
            with open(f'billboard_chart_{chart_type.lower()}.json', 'r') as json_file:
                data = json.load(json_file)
            return data
        except (JSONDecodeError, FileNotFoundError):
            return None
    else:
        return None


def _get_melon_chart(chart_type: str):
    if chart_type is not None:
        try:
            with open(f'melon_chart_{chart_type.lower()}.json', 'r') as json_file:
                data = json.load(json_file)
            return data
        except (JSONDecodeError, FileNotFoundError):
            return None
    else:
        return None


if __name__ == '__main__':
    print(get_chart('melon', 'TOP100'))
