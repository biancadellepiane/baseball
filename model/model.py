import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMap = {}

    def getAllYears(self):
        return DAO.getAllYears()

    def getTeamsofYear(self, year):
        return DAO.getTeamsofYear(year)

    def buildGraph(self, year):
        self._grafo.clear()
        nodes = DAO.getTeamsofYear(year)
        self._idMap = {}
        for t in nodes:
            self._idMap[t.ID] = t

        self._grafo.add_nodes_from(nodes)

        #per gli archi non serve una query perchè COLLEGANO TUTTE LE COPPIE DISTINTE quindi ciclo i nodi
        for n1 in self._grafo.nodes:
            for n2 in self._grafo.nodes:
                if n1 != n2:
                    self._grafo.add_edge(n1, n2, weight=0) #inizio a inizializzare peso

        salaries = DAO.getSalaryOfTeam(year, self._idMap)
        for a in self._grafo.edges:
            self._grafo[a[0]][a[1]]["weight"] += salaries[a[0]] + salaries[a[1]]


    def getGraphDetails(self):
        return self._grafo.number_of_nodes(), self._grafo.number_of_edges()

    def getNeighborsSorted(self, source):#source = squadra di partenza selezionata
        source = [n for n in self._grafo.nodes if n.teamCode == source][0]
        #Scorro n nodi del grafo e prendo il primo [0] che ha l'attributo teamCode = source (siccome source è una stringa del temCode)
        vicini = nx.neighbors(self._grafo, source) #lista
        #prima di controllare i vicini --> passa il nodo source e controlla se sta dentro al grafo
        # ERRORE (source era una stringa e nodi nel grafo un oggetto --> non comparabili) - soluzione riga 42

        #return vicini

        viciniOrdinati = [] #lista di tuple con vicino e peso arco tra source e vicino
        for v in vicini:
            viciniOrdinati.append((v, self._grafo[source][v]["weight"]))

        viciniOrdinati.sort(key=lambda x: x[1], reverse=True) #[x]:1 ordino secondo il peso
        return viciniOrdinati








