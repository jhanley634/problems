#! /usr/bin/env python
# Copyright 2022 John Hanley. MIT licensed.
# based on
# https://medium.com/analytics-vidhya/interative-map-with-osm-directions-and-networkx-582c4f3435bc
from pathlib import Path

from ipyleaflet import AwesomeIcon, Map, Marker, basemaps
from osmnx.graph import graph_from_place
import matplotlib.pyplot as plt
import osmnx as ox
import seaborn as sns
import typer


def _set_nearest_node(graph, marker):
    marker.nearest_node = ox.get_nearest_node(graph, marker.location)


def show_locale(place_name='Kamppi, Helsinki, Finland'):
    out_file = Path('~/Desktop').expanduser() / place_name.replace(', ', '-')
    graph = graph_from_place(place_name)
    # fig, ax = ox.plot_graph(graph); print(fig, ax)
    nodes, edges = ox.graph_to_gdfs(graph)
    center = (60.16607, 24.93116)
    m = Map(center=center, basemap=basemaps.CartoDB.Positron, zoom=15)
    to_marker_style = AwesomeIcon(
        name='circle',
        icon_color='white',
        marker_color='red',
        spin=False
    )
    from_marker = Marker(location=center)
    to_marker = Marker(location=center, icon=to_marker_style)
    m.add(from_marker)
    m.add(to_marker)

    print(nodes)
    print(edges)
    sns.scatterplot(data=nodes, x='x', y='y',
                    hue='highway', legend='full')
    plt.savefig(out_file)


if __name__ == '__main__':
    typer.run(show_locale)
