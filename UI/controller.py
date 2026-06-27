import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self.year=None
        self.forma=None

    def handle_graph(self, e):
        if self.year is not None and self.forma is not None:
            self._model.buildGraph(self.year,self.forma)
            n,a,max5= self._model.getDettagli()
            if n is not None and a is not None and max5 is not None:
                self._view.txt_result1.controls.clear()
                self._view.txt_result1.controls.append(ft.Text(f"Grafo correttamente creato con {n} nodi e {a} archi!\n"
                                                               f"Di seguito i 5 archi di peso maggiore:"))
                for a in max5:
                    self._view.txt_result1.controls.append(ft.Text(f"{a[0].id} --> {a[1].id} (peso: {a[2]['weight']})"))
            else:
                self._view.txt_result1.controls.clear()
                self._view.txt_result1.controls.append(ft.Text(f"Non siamo riusciti a creare il grafo"))
        else:
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(ft.Text(f"Iserire un anno e un aforma corretta"))
        self._view.update_page()

    def handle_path(self, e):
        camm,punto=self._model.bestCammino()
        if camm is not None and punto is not None:
            self._view.txt_result2.controls.clear()
            self._view.txt_result2.controls.append(ft.Text(f"Il cammino migliore è lungo {len(camm)} e conta {punto} punti!\n"
                                                           f"Di seguito i nodi del cammino"))
            for c in camm:
                self._view.txt_result2.controls.append(ft.Text(f"{c.id}"))
        else:
            self._view.txt_result2.controls.clear()
            self._view.txt_result2.controls.append( ft.Text(f"Non siamo riusciti a trovare il cammino migliore"))
        self._view.update_page()

    def fillDDyear(self):
        year=self._model.getAllYear()
        for i in year:
            self._view.ddyear.options.append(ft.dropdown.Option(data=i,text=i,on_click=self.readYear))

        self._view.update_page()
    def fillDDShape(self):
        if self.year is not None:
            stati=self._model.getShape(self.year)
            for s in stati:
                self._view.ddshape.options.append(ft.dropdown.Option(data=s,text=s,on_click=self.readState))
            self._view.update_page()
        else:
            return



    def readYear(self,e):
        if e.control.data is None:
            self.year=None
        else:
            self.year=e.control.data
            self.fillDDShape()

    def readState(self,e):
        if e.control.data is None:
            self.forma=None
        else:
            self.forma=e.control.data