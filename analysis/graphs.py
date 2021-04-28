import mysql.connector
import networkx as nx;
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout
from operator import itemgetter

fig = plt.figure(figsize=(12,12))
ax = plt.subplot(111)
ax.set_title('Graph - Shapes', fontsize=10)

# https://networkx.org/documentation/stable/tutorial.html
G = nx.Graph()

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
)

cursor = db.cursor() #object to execute SQL statements and interact with SQL server
cursor.execute("USE website_vulnerabilities")

cursor.execute("SELECT ip_addr, sender_ttl, receiver_source FROM traceroute")

sorty_boi = sorted(cursor, key=lambda tup: (tup[0], int(tup[1])))

starting_ip = None
last_start_ip = None
target_ip = None
last_vertex = None

#sorty_boi = sorty_boi[:5000]

for record in sorty_boi:
    if target_ip != record[0]:
        target_ip = record[0]
        last_vertex = record[2]
    else:
#        print(target_ip)
#        print(last_vertex," ",record[2])
        G.add_edge(last_vertex, record[2], color='r', weight=20, target_ip=target_ip)
        last_vertex = record[2]

#print(nx.betweenness_centrality(G))
#print(type(nx.betweenness_centrality(G)))
betweenness = nx.betweenness_centrality(G)
print(betweenness)
print(sorted(betweenness.items(), key = itemgetter(1), reverse = True)[:30])

#for record in sorty_boi:
#    if last_start_ip is None or last_start_ip != record[0]:
#       # if last_start_ip is not None and last_start_ip != record[0]:
#       #     G.add_edge(last_vertex, "SINK", source_vertex=last_vertex)
#        last_start_ip = record[0]
#    if record[0] != starting_ip:
#        starting_ip = record[0]j
#        last_vertex = starting_ip
#        G.add_edge("SOURCE", last_vertex, source_vertex="SOURCE")
#    if last_vertex == record[2]:
#        G.add_edge(last_vertex, record[2],color='r', weight=30, source_vertex=record[0])
#    last_vertex=record[2]


#print(len(list(nx.edge_disjoint_paths(G, "SOURCE", "SINK"))))
#print(list(nx.articulation_points(G)))

#pos = graphviz_layout(G, prog="dot")
#nx.draw_networkx(G, pos, node_size=5, with_labels=False)
#plt.savefig("Graph.png", format="PNG")
