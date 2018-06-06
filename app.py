import logging
import json
from logging import FileHandler, Formatter

from flask import Flask, render_template

import plotly
import plotly.graph_objs as go

from manage_data import read_data

app = Flask(__name__)
app.config.from_object('config')


@app.route('/')
def home():
    return render_template('layout.html')


@app.route('/graph')
def graph():
    data = read_data()

    # Create a trace
    traces = []
    for g, d in data.groupby('Name'):
        trace = go.Scatter(
            name=g,
            x=d.Datetime,
            y=d.Temperature,
        )
        traces.append(trace)

    layout = go.Layout(
        title='Sensor Measurements',
        yaxis=dict(
            title='Temperature',
            range=[0, 40],
        ),
        xaxis=dict(
        ),
        showlegend=True)
    graph = go.Figure(data=traces, layout=layout)
    # graph = dict(
    #     data=traces,
    #     layout=dict(
    #         title='Sensor Measurements',
    #         yaxis=dict(
    #             title='Temperature'
    #         ),
    #         xaxis=dict(
    #             title='Time'
    #         )
    #     )
    # )
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
