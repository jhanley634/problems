#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.


# from https://stackoverflow.com/questions/77933809/neato-output-for-mrecord-produces-significant-overlap


import graphviz

a = [
    [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
    [[0, 0], [0, 0], [0, 0], [0, 0], [0, 18.442211], [0, 1.5577889]],
]
e = [
    [0, 7.8787879, 15.353535, 0, 0, 31.212121],
    [0, 0, 0, 0, 0, 0],
    [11.392405, 0, 0, 22.025316, 46.582278, 0],
]
f = [88.607595, 12.121212, 64.646465, 37.974684, 84.97551, 67.23009]
w = [45.555556, 0, 0, 60, 150, 100]
Cuntreat = (100, 250, 80, 200, 150, 130)
Ctreat = (650, 200)
Cfresh = 1
plants = range(len(Cuntreat))
treatments = range(len(Ctreat))

graph = graphviz.Digraph(
    name="treatment_flow",
    format="svg",
    engine="neato",
    graph_attr={
        "rankdir": "LR",
        "overlap": "false",
        "splines": "true",
    },
)

graph.node(name="fresh", label="Freshwater")
graph.node(name="waste", label="Wastewater")
for plant in plants:
    graph.node(
        name=str(plant),
        shape="Mrecord",
        label="{"
        "{"
        "<fresh_in> fresh|"
        "<untreat_in> untreated|"
        "<treat_in> treated"
        "}|"
        r"Plant \N|"
        "{"
        "<waste_out> waste|"
        "<untreat_out> untreated|"
        + "|".join(
            f"<treat_{treatment}_out> treatment {treatment}" for treatment in treatments
        )
        + "}"
        "}",
    )

for i, a_slice in enumerate(a):
    for j, a_row in enumerate(a_slice):
        for treatment, (contam, flow) in enumerate(zip(Ctreat, a_row)):
            if flow > 0:
                graph.edge(
                    tail_name=f"{i}:treat_{treatment}_out",
                    head_name=f"{j}:treat_in",
                    label=f"{flow:.1f} ({contam*flow:.1f})",
                )
for i, (e_row, contam) in enumerate(zip(e, Cuntreat)):
    for j, flow in enumerate(e_row):
        if flow > 0:
            graph.edge(
                tail_name=f"{i}:untreat_out",
                head_name=f"{j}:untreat_in",
                label=f"{flow:.1f} ({contam*flow:.1f})",
            )
for j, flow in enumerate(f):
    if flow > 0:
        graph.edge(
            tail_name="fresh",
            head_name=f"{j}:fresh_in",
            label=f"{flow:.1f} ({Cfresh*flow:.1f})",
        )
for i, (flow, contam) in enumerate(zip(w, Cuntreat)):
    if flow > 0:
        graph.edge(
            tail_name=f"{i}:waste_out",
            head_name="waste",
            label=f"{flow:.1f} ({contam*flow:.1f})",
        )

graph.view()
