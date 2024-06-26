#! /usr/bin/env _TYPER_STANDARD_TRACEBACK=1 python
# Copyright 2022 John Hanley. MIT licensed.
# based on
# https://medium.com/analytics-vidhya/interative-map-with-osm-directions-and-networkx-582c4f3435bc
from pathlib import Path

from geopandas.geodataframe import GeoDataFrame
from ipyleaflet import AwesomeIcon, Map, Marker, basemaps
from osmnx.graph import graph_from_place
from xyzservices.lib import Bunch
import matplotlib.pyplot as plt
import osmnx as ox
import seaborn as sns
import typer


def show_locale(place_name: str = "Kamppi, Helsinki, Finland") -> None:
    out_file = Path("~/Desktop").expanduser() / place_name.replace(", ", "-")
    graph = graph_from_place(place_name)
    # fig, ax = ox.plot_graph(graph); print(fig, ax)
    nodes, edges = ox.graph_to_gdfs(graph)
    center = (60.16607, 24.93116)
    # pyright would say: "CartoDB" is not a known member of module "xyzservices.providers"
    # (reportAttributeAccessIssue)
    carto_db = getattr(basemaps, "CartoDB")
    assert isinstance(carto_db, Bunch)
    m = Map(center=center, basemap=carto_db.Positron, zoom=15)
    to_marker_style = AwesomeIcon(
        name="circle", icon_color="white", marker_color="red", spin=False
    )
    from_marker = Marker(location=center)
    to_marker = Marker(location=center, icon=to_marker_style)
    m.add(from_marker)
    m.add(to_marker)

    print(edges)
    print(nodes)
    assert isinstance(nodes, GeoDataFrame)
    sns.scatterplot(
        data=nodes,
        x="x",
        y="y",
        hue="highway",
        legend="full",
    )
    plt.savefig(out_file)


if __name__ == "__main__":
    typer.run(show_locale)
