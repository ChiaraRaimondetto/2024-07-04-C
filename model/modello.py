import copy

from starlette.routing import Mount

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self.idMapN={}
        self._bestc = []
        self.punti = 0

    def getAllYear(self):
        return DAO.getAllYears()

    def get_all_states(self,anno):
        return DAO.get_all_states(anno)

    def buildGraph(self,anno,forma):
        self._graph.clear()
        nodi=DAO.getAllNodes(anno,forma)
        for n in nodi:
            self.idMapN[n.id]=n
        self._graph.add_nodes_from(nodi)
        self.addMyEdges(anno,forma,self.idMapN)

    def addMyEdges(self,anno,forma,idMap):
        archi=DAO.getAllEdges(anno,forma,idMap)
        for a in archi:
            self._graph.add_edge(a.si1,a.si2,weight=a.peso)

    def getShape(self,anno):
        return DAO.getShape(anno)
    def getDettagli(self):
        archi=list(self._graph.edges(data=True))
        lista=sorted(archi,key=lambda x:x[2]["weight"],reverse=True )
        return len(self._graph.nodes), len(self._graph.edges),lista[:5]

    def bestCammino(self):
        self._bestc=[]
        self.punti=0

        for n in self._graph.nodes:
            parziale=[n]
            conteggio_mesi = {}
            for i in range(1,13):
                conteggio_mesi[i]=0
            conteggio_mesi[n.datetime.month] = 1
            self.ricorsione(parziale,conteggio_mesi)

        return self._bestc,self.punti
    def ricorsione(self,parziale,conteggio_mesi):
        punti=self.calcolaPunti(parziale)
        if punti>self.punti:
            self.punti=punti
            self._bestc=copy.deepcopy(parziale)

        for n in self._graph.neighbors(parziale[-1]):
            if n.duration>parziale[-1].duration and n not in parziale and conteggio_mesi[n.datetime.month]<3:
                parziale.append(n)
                conteggio_mesi[n.datetime.month] += 1
                self.ricorsione(parziale,conteggio_mesi)
                conteggio_mesi[n.datetime.month] -= 1
                parziale.pop()
#altro metodo per vedere i mesi
   # def limiti(self,parziale,n):
   #     mesi={1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0}
   #     for p in parziale:
   #          mese=p.datetime.month
   #          mesi[mese]+=1
   #     if mesi[n.datetime.month]>=3:
   #         return False
   #     else:
   #         return True

    def calcolaPunti(self,parziale):

        punti = 100 * (len(parziale))
        for i in range(1,len(parziale)):
            if parziale[i].datetime.month==parziale[i-1].datetime.month:
                punti+=200
        return punti





