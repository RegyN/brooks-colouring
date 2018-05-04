# coding=utf-8
from Graph import Graph


def main():
    graf = Graph("data_test_uvw.txt")
    # rank = graf.get_delta()
    # isCycle = graf.is_cycle()
    # isFC = graf.is_fully_connected()
    # isBiconnected = graf.is_biconnected()
    # a = graf.find_biconnected()
    # u, v, w = graf.find_uvw()
    # labels = graf.label_from_uvw(u, v, w)
    # colors = graf.colouring_from_labels(labels)
    colors = graf.find_brooks_colouring()
    print (colors)


main()