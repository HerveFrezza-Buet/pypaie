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

class Maladie(Cotisation):
    def __init__(self, regime = regles.REGIME_GENERAL):
        super().__init__('Maladie')
        self.regime = regime
        
    def cotise(self, assiettes, mode):
        self.cotis_non_majoree, self.cotis_majoree, self.cotis_salariale = regles.calcul_cotis_maladie(assiettes.securite_sociale, mode, self.regime)
        
    def _cotisation_salariale(self):
        return self.cotis_salariale
    
    def _cotisation_employeur(self):
        if self.cotis_majoree == None:
            return self.cotis_non_majoree
        else:
            return self.cotis_non_majoree +  self.cotis_majoree

    def lignes(self):
        res = [{'label': 'Cotisation maladie',
                'employeur': self.cotis_non_majoree}]
        if self.cotis_majoree != None:
            res.append({'label': 'Cotisation maladie majorée',
                        'employeur': self.cotis_majoree})
        if self.cotis_salariale != None:
            res.append({'label': 'Cotisation maladie ALSACE-MOSELLE',
                        'salarial': self.cotis_salariale})
        return res
            
        
class Chomage(Cotisation):
    def __init__(self):
        super().__init__('Chômage')
        
    def _cotisation_employeur(self):
        return self.cotis_chomage + self.cotis_ags
    
    def cotise(self, assiettes, mode):
        self.cotis_chomage = regles.taux_chomage_patronal * assiettes.securite_sociale
        self.cotis_ags     = regles.taux_ags_patronal * assiettes.securite_sociale
    
    def lignes(self):
        return [{'label': "Cotisation assurance chômage",
                 'employeur': self.cotis_chomage},
                {'label': "cotisation AGS garantie des salaires",
                 'employeur': self.cotis_ags}]

class Retraite(Cotisation):
    def __init__(self, label):
        super().__init__(label)

class RetraiteTranches(Retraite):
    def __init__(self, label, tag_A, tag_B):
        super().__init__(label)
        self.tag_A = tag_A
        self.tag_B = tag_B
        
    def _cotisation_salariale(self):
        return self.cotis_sal_A + self.cotis_sal_B
    
    def _cotisation_employeur(self):
        return self.cotis_pat_A + self.cotis_pat_B
        
    def lignes(self):
        return [{'label': f'{self.label} {self.tag_A}',
                 'salarial': self.cotis_sal_A,
                 'employeur': self.cotis_pat_A},
                {'label': f'{self.label} {self.tag_B}',
                 'salarial': self.cotis_sal_B,
                 'employeur': self.cotis_pat_B}]

class Vieillesse(RetraiteTranches):
    def __init__(self):
        super().__init__('Vieillesse', 'plafonnée', 'déplafonnée')
    
    def cotise(self, assiettes, mode):
        self.cotis_sal_A, self.cotis_pat_A, self.cotis_sal_B, self.cotis_pat_B = regles.calcul_cotis_vieillesse(assiettes.securite_sociale)

class IRCANTEC(RetraiteTranches):
    def __init__(self):
        super().__init__('IRCANTEC', 'tranche A', 'tranche B')
    
    def cotise(self, assiettes, mode):
        self.cotis_sal_A, self.cotis_pat_A, self.cotis_sal_B, self.cotis_pat_B = regles.calcul_cotis_ircantec(assiettes.securite_sociale)

class AGIRC_ARRCO(RetraiteTranches):
    def __init__(self):
        super().__init__('AGIRC-ARRCO', 'tranche 1', 'tranche 2')
    
    def cotise(self, assiettes, mode):
        self.cotis_sal_A, self.cotis_pat_A, self.cotis_sal_B, self.cotis_pat_B = regles.calcul_cotis_agirc_arrco(assiettes.securite_sociale)
        

class AllocationsFamiliales(Cotisation):
    def __init__(self, taux_reduit = False):
        super().__init__('Allocations familiales')
        self.taux_reduit = taux_reduit
        
    def cotise(self, assiettes, mode):
        self.taux_reduit_effectif, self.cotis = regles.calcul_cotis_allocations_familiales(assiettes.securite_sociale, self.taux_reduit)
        
    def _cotisation_employeur(self):
        return self.cotis

    def lignes(self):
        if self.taux_reduit_effectif:
            label_taux = '(taux réduit)'
        else:
            label_taux = '(taux plein)'
        return [{'label': f'{self.label} {label_taux}',
                'employeur': self.cotis}]

    
class FNAL(Cotisation):
    def __init__(self, nb_salaries=regles.seuil_nb_salaries_fnal):
        super().__init__("Fond National d'Aide au Logement")
        self.nb_salaries = nb_salaries
        
    def cotise(self, assiettes, mode):
        self.cotis = regles.calcul_cotis_fnal(assiettes.securite_sociale, self.nb_salaries)
        
    def _cotisation_employeur(self):
        return self.cotis

    def lignes(self):
        return [{'label': self.label,
                'employeur': self.cotis}]

