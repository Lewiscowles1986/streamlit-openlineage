from pathlib import Path
import os

import streamlit as st, json, glob, networkx as nx
import streamlit.components.v1 as components
from pyvis.network import Network

cwd = Path.cwd()
out_dir = f"{cwd}/dist"
os.makedirs(out_dir, exist_ok=True)
event_files = glob.glob(f"{cwd}/openlineage_events/event-*.json")
print("Found events:")
for event_file in event_files:
    print(f"\t{event_file}")
events = [json.load(open(p)) for p in event_files]

G = nx.DiGraph()
for e in events:
    job = e["job"]["name"]
    for inp in e.get("inputs", []):
        G.add_edge(inp["name"], job)
    for out in e.get("outputs", []):
        G.add_edge(job, out["name"])

net = Network(height="750px", width="100%", directed=True)
net.from_nx(G)
net.save_graph(f"{out_dir}/lineage.html")

st.title("OpenLineage Graph (no DB)")

graph_html = open(f"{out_dir}/lineage.html").read()
components.html(graph_html, height=750)
