from service import charts as charts_service


def get_chart(chart_name: str, chart_type: str):
    chart_data = charts_service.get_chart(chart_name, chart_type)
    return chart_data
