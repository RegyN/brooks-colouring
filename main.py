# coding=utf-8
from Graph import Graph
from GraphPart import GraphPart
import csv
import argparse


def save_colouring_as_csv(path, colouring):
    with open(path, 'wt') as outfile:
        outwriter = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC, lineterminator='\n')
        outwriter.writerow([max(colouring)])
        for i, colour in enumerate(colouring):
            outwriter.writerow([i, colour])


def main():
    parser = argparse.ArgumentParser(description='Find brooks coloring of a biconnected graph')
    parser.add_argument('--inputFile', default='data_cycle.txt', help='path to input csv data file')
    parser.add_argument('--outputFile', default="colouring.txt", help='path to coloring data output file')
    args = parser.parse_args()
    graf = Graph(args.inputFile)
    graf_p = GraphPart()
    graf_p.add_edge(0, 1)
    graf_p.add_edge(1, 2)
    graf_p.add_edge(2, 3)
    # rank = graf.get_delta()
    isCycle = graf.is_cycle()
    isBic = graf.find_biconnected(None)
    colours = graf.colour_as_cycle()
    isPCycle = graf_p.is_cycle()
    isPFc = graf_p.is_fully_connected()
    isPBc = graf_p.is_biconnected(None)
    # pColours = graf_p.colour_as_cycle()
    # u, v, w = graf_p.find_uvw()
    # labels = graf_p.label_from_uvw(u, v, w)
    # col = graf_p.colouring_from_labels(labels)
    # isFC = graf.is_fully_connected()
    # isBiconnected = graf.is_biconnected()
    # a = graf.find_biconnected()
    # u, v, w = graf.find_uvw()
    # labels = graf.label_from_uvw(u, v, w)
    # colors = graf.colouring_from_labels(labels)
    colours = graf.find_brooks_colouring()
    print (colours)
    save_colouring_as_csv(args.outputFile, colours)


main()