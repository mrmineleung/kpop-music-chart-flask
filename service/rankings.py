from extensions import mongo


def get_latest_ranking(chart_name: str, chart_type: str):
    return mongo.db.rankings.find_one({'chart': chart_name, 'type': chart_type}, sort=[('date', -1)])
