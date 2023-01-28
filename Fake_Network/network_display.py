# display the network with networkx

import sqlite3
import networkx as nx
import matplotlib.pyplot as plt


def display_graph(db_file, degree_centrality_threshold):
    # Connect to the database file
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    # Create an empty graph
    G = nx.Graph()

    # Get all the contacts from the database
    c.execute("SELECT * FROM contacts")
    contacts = c.fetchall()

    # Add the contacts as nodes to the graph
    for contact in contacts:
        G.add_node(contact[0], name=contact[1] + ' ' + contact[2], location=contact[6], like = contact[4], dislike = contact[5])

    # Get all the connections from the database
    c.execute("SELECT * FROM connections")
    connections = c.fetchall()

    # Add the connections as edges to the graph
    for connection in connections:
        G.add_edge(connection[0], connection[1])

    # Compute the centrality measures
    degree_centrality = nx.degree_centrality(G)

    # Remove the nodes that have a degree centrality below the threshold
    nodes_to_remove = [node for node in degree_centrality if degree_centrality[node] < degree_centrality_threshold]
    G.remove_nodes_from(nodes_to_remove)

    # Create the labels for the nodes
    labels = {}
    for node in G.nodes():
        # labels[node] = G.nodes[node]['name'] + '\n'
        labels[node] = G.nodes[node]
    pos = nx.kamada_kawai_layout(G)
    # Draw the graph
    nx.draw(G, with_labels=True, labels=labels, node_size=1000, node_color='skyblue', font_size=8, pos=pos)
    plt.show()

    # Close the connection
    conn.close()

display_graph('../raw_data/network.db', 0.001)
