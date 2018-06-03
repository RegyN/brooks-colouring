# coding=utf-8
from Graph import Graph
import csv
import argparse
import random as rd
import time


def save_colouring_as_csv(path, colouring):
    with open(path, 'wt') as outfile:
        outwriter = csv.writer(outfile, delimiter=' ', quotechar='"', quoting=csv.QUOTE_NONNUMERIC, lineterminator='\n')
        outwriter.writerow([max(colouring)])
        for i, colour in enumerate(colouring):
            outwriter.writerow([i, colour])


def generate_graph(verts, thresh = 0.8):
    graf = Graph()
    graf.VerticesCount = verts
    for i in range(verts):
        for j in range(verts):
            if j > i and rd.uniform(0, 1) > thresh:
                graf.add_edge(i, j)
    return graf


def test_performance(output_path):
    verts = list()
    edges = list()
    times = list()
    max = 25
    for i in range(1, max):
        print(25*i)
        grafy = list()
        for j in range(150):
            grafy.append(generate_graph(25*i))
        start = time.time()
        for j, g in enumerate(grafy):
            g.find_brooks_colouring()
        stop = time.time()

        verts.append(i*25)
        edges.append(i*i*25*25*0.2)
        times.append(stop-start)

    with open(output_path, 'wt') as outfile:
        outwriter = csv.writer(outfile, delimiter=' ', quotechar='"', quoting=csv.QUOTE_NONNUMERIC, lineterminator='\n')
        for i in range(max-1):
            outwriter.writerow([verts[i], edges[i], times[i]])


def main():
    parser = argparse.ArgumentParser(description='Find brooks coloring of a biconnected graph')
    parser.add_argument('--inputFile', default='data.txt', help='path to input csv data file')
    parser.add_argument('--outputFile', default="colouring.txt", help='path to coloring data output file')
    args = parser.parse_args()
    # graf = Graph(args.inputFile)
    # colouring = graf.find_brooks_colouring()
    # save_colouring_as_csv(args.outputFile, colouring)
    test_performance("test_results")


main()