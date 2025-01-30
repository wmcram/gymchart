from django.shortcuts import render
from plotly.offline import plot
from charts.models import MetricType


def metric_dashboard(request):
    metric_types = MetricType.objects.all()
    return render(request, 'charts/index.html', {'metric_types': metric_types})


def metric_chart(request, metric_id):
    metric = MetricType.objects.get(id=metric_id)

    data_points = metric.get_recent_data()

    x_data = [d.timestamp for d in data_points]
    y_data = [d.value for d in data_points]

    fig = {
        'data': [{
            'x': x_data,
            'y': y_data,
            'mode': 'lines+markers',
            'name': metric.display_name
        }],
        'layout': {
            'title': f'{metric.display_name} - Last 7 Days',
            'xaxis': {'title': 'Time'},
            'yaxis': {'title': 'Usage'},
            'shapes': [
                {
                    "type": "line",
                    "xref": "paper",
                    "yref": "y",
                    "x0": 0,
                    "y0": metric.capacity,
                    "x1": 1,
                    "y1": metric.capacity,
                    "line": {
                        "color": "red",
                        "dash": "dash",
                        "width": 2
                    }
                }
            ],
        },
    }

    plot_div = plot(fig, output_type='div', config={'displayModeBar': False})

    return render(request, 'charts/metric_chart.html', {'plot_div': plot_div})
