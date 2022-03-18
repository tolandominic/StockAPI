import plotly.express as px


def line(x, y, title):
    return px.line(x=x, y=y, title=title, markers=True)
