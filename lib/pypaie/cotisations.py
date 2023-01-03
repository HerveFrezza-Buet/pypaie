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
        base, base_hs = regles.calcul_assiette_csg_crds(assiettes.csg, assiettes.csg_hs)
        self.non_deductible  = regles.taux_csg_imp_salarial    * base
        self.deductible      = regles.taux_csg_nonimp_salarial * base
        self.non_deductible += regles.taux_csg_total_salarial  * base_hs
        self.crds            = regles.taux_crds_salarial       * (base + base_hs)
    
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
        a = assiettes.securite_sociale + assiettes.securite_sociale_hs
        self.cotis_non_majoree, self.cotis_majoree, self.cotis_salariale = regles.calcul_cotis_maladie(a, mode, self.regime)
        
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
        a = assiettes.securite_sociale + assiettes.securite_sociale_hs
        self.cotis_chomage = regles.taux_chomage_patronal * a
        self.cotis_ags     = regles.taux_ags_patronal * a
    
    def lignes(self):
        return [{'label': "Cotisation assurance chômage",
                 'employeur': self.cotis_chomage},
                {'label': "cotisation AGS garantie des salaires",
                 'employeur': self.cotis_ags}]

class Retraite(Cotisation):
    def __init__(self, label):
        super().__init__(label)

class Prefon(Retraite):
    def __init__(self, montant):
        super().__init__('Préfon-Retraite')
        self.montant = montant
        
    def _cotisation_salariale(self):
        return self.montant
        
    def cotise(self, assiettes, mode):
        pass
        
    def lignes(self):
        return [{'label': self.label,
                 'salarial': self.montant}]

class ATI(Retraite):
    def __init__(self):
        super().__init__('Contribution ATI')
        
    def _cotisation_employeur(self):
        return self.cotis
        
    def cotise(self, assiettes, mode):
        a = assiettes.securite_sociale + assiettes.securite_sociale_hs
        self.cotis = regles.taux_ati_patronal * a
        
    def lignes(self):
        return [{'label': self.label,
                'employeur': self.cotis}]

class CNRACL(Retraite):
    def __init__(self):
        super().__init__('CRNACL')
        
    def _cotisation_salariale(self):
        return self.cotis_s
        
    def _cotisation_employeur(self):
        return self.cotis_e
        
    def cotise(self, assiettes, mode):
        a = assiettes.securite_sociale + assiettes.securite_sociale_hs
        self.cotis_s = regles.taux_cnracl_salarial * a
        self.cotis_e = regles.taux_cnracl_patronal * a
        
    def lignes(self):
        return [{'label': self.label,
                 'salarial': self.cotis_s,
                 'employeur': self.cotis_e}]
    
class RAFP(Retraite):
    def __init__(self):
        super().__init__('RAFP')
        
    def _cotisation_salariale(self):
        return self.cotis_s
        
    def _cotisation_employeur(self):
        return self.cotis_e
        
    def cotise(self, assiettes, mode):
        self.cotis_s = regles.taux_rafp_salarial * assiettes.rafp
        self.cotis_e = regles.taux_rafp_patronal * assiettes.rafp
        
    def lignes(self):
        return [{'label': self.label,
                 'salarial': self.cotis_s,
                 'employeur': self.cotis_e}]

class PensionCivile(Retraite):
    def __init__(self):
        super().__init__('Pension civile (PC)')
        
    def _cotisation_salariale(self):
        return self.cotis_s
        
    def _cotisation_employeur(self):
        return self.cotis_e
        
    def cotise(self, assiettes, mode):
        a = assiettes.securite_sociale + assiettes.securite_sociale_hs
        self.cotis_s = regles.taux_pc_salarial * a
        self.cotis_e = regles.taux_pc_patronal * a
        
    def lignes(self):
        return [{'label': self.label,
                 'salarial': self.cotis_s,
                 'employeur': self.cotis_e}]



class RetraiteTranches(Retraite):
    def __init__(self, label, tag_A, tag_B):
        super().__init__(label)
        self.tag_A = tag_A
        self.tag_B = tag_B
        
    def _cotisation_salariale(self):
        return self.cotis_sal_A + self.cotis_sal_A_hs + self.cotis_sal_B + self.cotis_sal_B_hs
    
    def _cotisation_employeur(self):
        return self.cotis_pat_A + self.cotis_pat_A_hs + self.cotis_pat_B + self.cotis_pat_B_hs
        
    def lignes(self):
        res = []
        if self.cotis_sal_A > 0 or self.cotis_pat_A > 0:
            res.append({'label': f'{self.label} {self.tag_A}',
                        'salarial': self.cotis_sal_A + self.cotis_sal_A_hs,
                        'employeur': self.cotis_pat_A + self.cotis_pat_A_hs})
        if self.cotis_sal_B > 0 or self.cotis_pat_B > 0:
            res.append({'label': f'{self.label} {self.tag_B}',
                        'salarial': self.cotis_sal_B + self.cotis_sal_B_hs,
                        'employeur': self.cotis_pat_B + self.cotis_pat_B_hs})
        return res

class Vieillesse(RetraiteTranches):
    def __init__(self):
        super().__init__('Vieillesse', 'plafonnée', 'déplafonnée')
    
    def cotise(self, assiettes, mode):
        self.cotis_sal_A, self.cotis_sal_A_hs, self.cotis_pat_A, self.cotis_pat_A_hs, self.cotis_sal_B, self.cotis_sal_B_hs, self.cotis_pat_B, self.cotis_pat_B_hs = regles.calcul_cotis_vieillesse(assiettes.securite_sociale, assiettes.securite_sociale_hs)

class IRCANTEC(RetraiteTranches):
    def __init__(self):
        super().__init__('IRCANTEC', 'tranche A', 'tranche B')
    
    def cotise(self, assiettes, mode):
        self.cotis_sal_A, self.cotis_sal_A_hs, self.cotis_pat_A, self.cotis_pat_A_hs, self.cotis_sal_B, self.cotis_sal_B_hs, self.cotis_pat_B, self.cotis_pat_B_hs = regles.calcul_cotis_ircantec(assiettes.ircantec, assiettes.ircantec_hs)

class AGIRC_ARRCO(RetraiteTranches):
    def __init__(self):
        super().__init__('AGIRC-ARRCO', 'tranche 1', 'tranche 2')
    
    def cotise(self, assiettes, mode):
        self.cotis_sal_A, self.cotis_sal_A_hs, self.cotis_pat_A, self.cotis_pat_A_hs, self.cotis_sal_B, self.cotis_sal_B_hs, self.cotis_pat_B, self.cotis_pat_B_hs = regles.calcul_cotis_agirc_arrco(assiettes.securite_sociale, assiettes.securite_sociale_hs)
        

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

class PatronaleTauxSecuriteSociale(Cotisation):
    def __init__(self, label, taux):
        super().__init__(label)
        self.taux = taux
        
    def cotise(self, assiettes, mode):
        self.cotis = assiettes.securite_sociale * self.taux * .01
        
    def _cotisation_employeur(self):
        return self.cotis

    def lignes(self):
        return [{'label': self.label + f' (taux={self.taux}%)',
                'employeur': self.cotis}]

class AccidentsTravail(PatronaleTauxSecuriteSociale):
    def __init__(self, taux):
        super().__init__("Accidents du travail", taux)

class Mobilite(PatronaleTauxSecuriteSociale):
    def __init__(self, taux):
        super().__init__("Versement mobilité", taux)
        
class CNSA(Cotisation):
    def __init__(self):
        super().__init__("Caisse Nationale de Solidarité pour l'Autonomie")
        
    def cotise(self, assiettes, mode):
        self.cotis = assiettes.securite_sociale * regles.taux_cnsa_patronal
        
    def _cotisation_employeur(self):
        return self.cotis

    def lignes(self):
        return [{'label': self.label,
                'employeur': self.cotis}]

