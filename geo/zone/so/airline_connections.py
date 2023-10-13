#! /usr/bin/env python

# Copyright 2023 John Hanley. MIT licensed.
#
# from https://codereview.stackexchange.com/questions/275384/the-shortest-path-between-airports

import matplotlib.pyplot as plt
import networkx as nx

connection_names = [
    ("ATH", "CTA"),
    ("ATH", "EDI"),
    ("ATH", "GLA"),
    ("BFS", "CGN"),
    ("BFS", "CTA"),
    ("BFS", "LTN"),
    ("BTS", "BLQ"),
    ("BTS", "STN"),
    ("CRL", "BLQ"),
    ("CRL", "BSL"),
    ("CRL", "LTN"),
    ("DUB", "LCA"),
    ("EIN", "BUD"),
    ("EIN", "MAD"),
    ("HAM", "BRS"),
    ("KEF", "CGN"),
    ("KEF", "LPL"),
    ("LCA", "HAM"),
    ("LTN", "DUB"),
    ("LTN", "MAD"),
    ("STN", "DUB"),
    ("STN", "EIN"),
    ("STN", "HAM"),
    ("STN", "KEF"),
    ("SUF", "BUD"),
    ("SUF", "LIS"),
    ("SUF", "STN"),
]


def airline_connections(interactive=False) -> None:
    g = nx.Graph(sorted(connection_names, reverse=True))
    print(nx.shortest_path(g, "ATH", "LIS"))

    nx.draw(g, node_size=1, width=0.1, with_labels=True)
    plt.savefig("/tmp/airline_connections.png")
    if interactive:
        plt.show()


if __name__ == "__main__":
    airline_connections()
