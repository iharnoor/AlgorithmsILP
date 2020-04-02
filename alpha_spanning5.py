from copy import deepcopy
import csv
import networkx as nx
import matplotlib.pyplot as plt

alpha = 0.05


def printGraph(graph, imageFile):
    FG = nx.Graph()
    for edge in graph:
        FG.add_edge(edge[0], edge[1], weight=edge[2])
    # FG.add_weighted_edges_from(answer)
    nx.draw(FG, with_labels=True, arrows=True)
    plt.savefig(imageFile)  # save as png
    plt.show()  # display
    # print(FG.edges())


# Read in the graph from file
# vertices = set of vertices
# edges = list of edges
# list = the adjacency list in dictionary format, key is the vertex and value is the set of outgoing vertices
vertices = set()
edges = []
list = {}
answer = []
with open('distancesnew.txt') as f:
    line_no = 0
    for line in f:
        if line_no:
            line = line.strip()
            print(line)
            s, d, cost = line.split(',')
            # convert cost to likelihood
            edges.append((s, d, 1.0 / float(cost)))
            if not s in list:
                list[s] = set()
            if not d in list:
                list[d] = set()
            list[s].add(d)
            list[d].add(s)
            vertices.add(s)
            vertices.add(d)
        line_no += 1


# simple recursive DFS algorithm
def dfs(s, list, visited, cc):
    visited.add(s)
    cc.append(s)
    if s in list:
        for node in list[s]:
            if node not in visited:
                dfs(node, list, visited, cc)


# check whether the graph is connected, and returns the connected components
def connected(list, vertices):
    visited = set()
    number_comp = 0
    comps = []
    for node in vertices:
        if node not in visited:
            cc = []
            dfs(node, list, visited, cc)
            number_comp += 1
            comps.append(cc)
    return number_comp == 1, comps

    # the actual algoirithm below


import matplotlib.pyplot
from matplotlib.pyplot import *
import numpy
from numpy import arange


def performILP():
    figure()
    x = arange(-100, 200, 10)
    y = arange(-100, 200, 10)
    y1 = 150.0 - x
    y2 = 25.0 - 0.625 * x
    y3 = 35 - 2.5 * x

    xlim(-100, 200)
    ylim(-100, 200)
    hlines(0, -100, 200, color='k')
    vlines(0, -100, 200, color='k')
    grid(True)

    xlabel('x-axis')
    ylabel('y-axis')

    plot(x, y1, color='b')
    plot(x, y2, color='r')
    plot(x, y3, color='m')

    title('Obj')
    # legend
    x = [0.0, 40.0, 150.0, 0.0]
    y = [25.0, 0.0, 0.0, 150.0]
    fill(x, y, 'r')


# method for alpha spanning network computation
def alpha_spanning(list, edges, vertices):
    # create copies of the adjacency list and edges since they will be modified
    list_temp = deepcopy(list)
    edges_temp = deepcopy(edges)

    # sort edges in ascending order of likelihood
    sorted_edges = sorted(edges_temp, key=lambda x: x[2])

    # print("\n \n Printing the Graph\n")
    # for edge in sorted_edges:
    #     print(edge)

    # cross_edges are the list of edges that go from one connected component to other
    cross_edges_possible = []
    cross_edges = []
    comps = []
    # iterate through edges in sorted order, and add to cross_edges if removing it still leaves the graph connected, otherwise break the iterations
    for edge in sorted_edges:
        s, d, c = edge
        list_temp[s].remove(d)
        list_temp[d].remove(s)
        # get the connected components
        cross_edges_possible.append(edge)
        con, comps = connected(list_temp, vertices)
        if not con:
            break

    comp_number = 0
    vertex_component = {}
    for comp in comps:
        for v in comp:
            vertex_component[v] = comp_number
        comp_number = comp_number + 1

    for edge in cross_edges_possible:
        s, d, cost = edge
        if vertex_component[s] != vertex_component[d]:
            cross_edges.append(edge)
            edges_temp.remove(edge)
        else:
            list_temp[s].add(d)
            list_temp[d].add(s)

    # print("\n \n Printing the cross edges\n")
    # for edge in cross_edges:
    #     print(edge)

    # calculate total likelihood of the cross edges
    total_likelihood = 0.0
    for edge in cross_edges:
        total_likelihood += edge[2]

    # multiple by alpha
    total_likelihood_alpha = total_likelihood * alpha

    # with the cross edges sorted in descending order of likelihood
    # keep adding it to the answer list until the summation of likelihood equals or surpasses the
    # total_likelihood_alpha
    total_likelihood_alpha_reached = 0.0
    for edge in sorted(cross_edges, key=lambda x: x[2], reverse=True):
        total_likelihood_alpha_reached = total_likelihood_alpha_reached + edge[2]
        answer.append(edge)
        if total_likelihood_alpha_reached >= total_likelihood_alpha:
            break

    # now recurse the same process within each connected component
    # (we don;t need to do that if a connected component does not have at least 2 vertices
    for comp in comps:
        if len(comp) > 1:
            comp_edges = get_edges_for_component(comp, edges_temp)
            alpha_spanning(list_temp, comp_edges, comp)


# utility method for getting list of edges within only a connected component
def get_edges_for_component(comp, edges):
    result_edges = []
    for edge in edges:
        s, d, cost = edge
        if s in comp and d in comp:
            result_edges.append(edge)
    return result_edges


if __name__ == '__main__':
    # printGraph(edges, "input_graph.png")
    alpha_spanning(list, edges, vertices)
    # for row in answer:
    #     print(row)
    # print (answer);
    # print (answer);
    answer = sorted(answer, key=lambda x: x[2])
    with open('graph.csv', 'w') as csvfile:
        fieldnames = ['source', 'target', 'weight']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in answer:
            writer.writerow({'source': row[0], 'target': row[1], 'weight': row[2]})

    print(len(answer))
    print("Done")
    printGraph(answer, "output_graph.png")

f = open("output5.txt", "w+")
f.close()
