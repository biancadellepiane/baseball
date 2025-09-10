import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMap = {}
        self._idMapTeamsCode = {}   #creata per vicini

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

        #creata per vicini
        for tCode in nodes :
            self._idMapTeamsCode[tCode.teamCode] = tCode

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
        #per fare i vicini controllo nodo e source (ora source è una stringa presa dal controller come valure quindi stringa)
        # nodo è un oggetto quindi devo trasformare source in oggetto --> creo idMap nuova perchè deve avere valore TeamCode
        sourceOgg = self._idMapTeamsCode[source]
        vicini = nx.neighbors(self._grafo, sourceOgg)


        viciniOrdinati = [] #lista di tuple con vicino e peso arco tra source e vicino
        for v in vicini:
            viciniOrdinati.append((v, self._grafo[sourceOgg][v]["weight"]))

        viciniOrdinati.sort(key=lambda x: x[1], reverse=True) #[x]:1 ordino secondo il peso
        return viciniOrdinati








