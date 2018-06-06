import logging
import json
from logging import FileHandler, Formatter

from flask import Flask, render_template, request
from sheets import ROW_TITLES

import plotly
import plotly.graph_objs as go

from manage_data import read_data
from datetime import datetime, timedelta
from werkzeug.contrib.cache import SimpleCache

cache = SimpleCache()

app = Flask(__name__)
app.config.from_object('config')


@app.route('/')
def home():
    return render_template('layout.html')


@app.route('/graph')
def graph():
    graph_date = request.args.get('date')
    graph_type = request.args.get('type')
    if graph_date is None:
        graph_date = datetime.now().strftime('%Y%m%d')
    if graph_type not in ROW_TITLES:
        graph_type = 'Temperature'
    date_range = [datetime.strptime(graph_date, '%Y%m%d')] * 2
    date_range[0] -= timedelta(0)
    date_range[1] += timedelta(1)
    date_range = [datetime.strftime(dt, '%Y-%m-%d') for dt in date_range]

    data = cache.get('data')
    if data is None:
        data = read_data()
        cache.set('data', data, timeout=10 * 60)

    data = data[data.Datetime.dt.strftime('%Y%m%d') == graph_date]

    # Create a trace
    traces = []
    for g, d in data.groupby('Name'):
        trace = go.Scatter(
            name=g,
            x=d.Datetime,
            y=d[graph_type],
        )
        if not d[graph_type].isnull().values.all():
            traces.append(trace)

    layout = go.Layout(
        title='Sensor Measurements',
        yaxis=dict(
            title=graph_type,
            # range=[0, 40],
        ),
        xaxis=dict(
            range=date_range,
        ),
        showlegend=True)
    graph = go.Figure(data=traces, layout=layout)
    graphJSON = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('graph.html', graphJSON=graphJSON)


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
