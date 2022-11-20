from . import revenus

class Bulletin:
    def __init__(self):
        self.bruts_salariaux = []
        self.brut_salarial = 0.

        self.revenus_divers = []

    def percoit(self, revenu):
        """
        Ajoute un revenu
        """
        if revenu['type'] == revenus.TYPE_BRUT_SALARIAL:
            self.bruts_salariaux.append(revenu)
            self.brut_salarial += revenu['montant']
            return
        
        if revenu['type'] == revenus.TYPE_INDEMNITE:
            self.revenus_divers.append(revenu)
            return
        

        raise ValueError(f'Bulletin.percoit (+=) : type de revenu -- {revenu["type"]} -- non géré.')

    def __iadd__(self, revenu):
        self.percoit(revenu)
        return self


