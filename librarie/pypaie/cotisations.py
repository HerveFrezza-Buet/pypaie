from . import regles
from . import ligne

class Cotisation(ligne.Ligne):
    def __init__(self, label):
        super().__init__(label)

class CSG_CRDS(Cotisation):
    def __init__(self):
        super().__init__('CSG-CRDS')

    def _cotisation_salariale(self):
        return self.deductible + self.non_deductible + self.crds

    def cotise(self, assiettes, mode):
        base = regles.calcul_assiette_csg_crds(assiettes.csg)
        self.non_deductible = regles.taux_csg_imp_salarial    * base
        self.deductible     = regles.taux_csg_nonimp_salarial * base
        self.crds           = regles.taux_crds_salarial       * base
    
    def lignes(self):
        return [{'label': 'CSG non-déductible',
                 'salarial': self.non_deductible},
                {'label': 'CSG déductible',
                 'salarial': self.deductible},
                {'label': 'CRDS',
                 'salarial': self.crds}]
    


