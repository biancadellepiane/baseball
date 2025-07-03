import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDYear(self):
        years = self._model.getAllYears()
        for y in years:
            self._view._ddAnno.options.append(ft.dropdown.Option(y))
        self._view.update_page()

        #yearsDD = [] --> perchè creo lista vuota?
        #for y in years:
            #yearsDD.append(ft.dropdown.Option(year))
        # self._update_page()

    def handleDDYearSelection(self, e):   #ha evento
        teams = self._model.getTeamsofYear(self._view._ddAnno.value)
        self._view._txtOutSquadre.controls.clear()
        self._view._txtOutSquadre.controls.append(ft.Text(f"Ho trovato {len(teams)} squadre che hanno giocato nel {self._view._ddAnno.value} "))

        #stampo
        for t in teams:
            self._view._txtOutSquadre.controls.append(ft.Text(f"{t.teamCode}"))
            self._view._ddSquadra.options.append(ft.dropdown.Option(data=t, text=t.teamCode, on_click=self.readDDTeams))
        self._view.update_page()

    def readDDTeams(self, e):
        if e.control.data is None:
            self._selectedTeam = None
        else:
            self._selectedTeam = e.control.data
        print(f"readDDTeams called -- {self._selectedTeam}")


    def handleCreaGrafo(self, e):
        year = self._view._ddAnno.value
        if year is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"Attenzione, non hai selezionato un anno", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(int(year))
        numNodi, numEdges = self._model.getGraphDetails()
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Grafo correttamente creato, con {numNodi} nodi e {numEdges} archi"))
        self._view.update_page()

    def handleDettagli(self, e):
        squadra = self._view._ddSquadra.value
        if squadra is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"Attenzione, non hai selezionato una squadra", color="red"))
            self._view.update_page()
            return

        vicini = self._model.getNeighborsSorted(squadra)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Le squadre adiacenti sono {len(vicini)}:"))
        for v in vicini:
            self._view._txt_result.controls.append(ft.Text(f"{v[0]} -- peso: {v[1]}"))
        self._view.update_page()


    def handlePercorso(self, e):
        pass