from pathlib import Path
import os

import streamlit as st, json, glob, networkx as nx, html
from pyvis.network import Network

cwd = Path.cwd()
out_dir = f"{cwd}/dist"
os.makedirs(out_dir, exist_ok=True)
event_files = glob.glob(f"{cwd}/openlineage_events/event-*.json")
print("Found events:")
[print(f"\t{event_file}") for event_file in event_files]
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
class HtmlFragment:
    def __init__(self, html: str) -> None:
        self.html = html

    def _repr_html_(self) -> str:
        return self.html

# st.markdown(graph_html, unsafe_allow_html=True)
st.write(HtmlFragment(graph_html), unsafe_allow_html=True)

