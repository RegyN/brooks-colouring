# coding=utf-8
from Graph import Graph
import csv
import argparse


def save_colouring_as_csv(path, colouring):
    with open(path, 'wb') as outfile:
        outwriter = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        outwriter.writerow([max(colouring)])
        for i, colour in enumerate(colouring):
            outwriter.writerow([i, colour])


def main():
    parser = argparse.ArgumentParser(description='Find brooks coloring of a biconnected graph')
    parser.add_argument('--inputFile', default='data_cycle.txt', help='path to input csv data file')
    parser.add_argument('--outputFile', default="colouring.txt", help='path to coloring data output file')
    args = parser.parse_args()
    graf = Graph(args.inputFile)
    # rank = graf.get_delta()
    # isCycle = graf.is_cycle()
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