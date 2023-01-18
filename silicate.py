import re


class Silicate():

    moleculemass = {
        "SiO2": 60.09,
        "Al2O3": 101.94,
        "Fe2O3": 159.7,
        "FeO": 71.85,
        "MnO": 70.94,
        "MgO": 40.32,
        "CaO": 56.08,
        "Na2O": 61.98,
        "K2O": 94.20,
        "H2O": 18.02,
    }

    kat_per_ox = {
        "SiO2": 1,
        "Al2O3": 2,
        "Fe2O3": 2,
        "FeO": 1,
        "MnO": 1,
        "MgO": 1,
        "CaO": 1,
        "Na2O": 2,
        "K2O": 2,
        "H2O": 2,
    }

    o_per_ox = {
        "SiO2": 2,
        "Al2O3": 3,
        "Fe2O3": 3,
        "FeO": 1,
        "MnO": 1,
        "MgO": 1,
        "CaO": 1,
        "Na2O": 1,
        "K2O": 1,
        "H2O": 1,
    }

    def __init__(self, O_per_FU, name="", SiO2=0, Al2O3=0, Fe2O3=0, FeO=0, MnO=0, MgO=0, CaO=0, Na2O=0, K2O=0, H2O=0):
        if not O_per_FU:
            raise ValueError("Missing O per formula unit")
        if SiO2 == 0:
            raise ValueError("SiO2 missing")
        self.name = name
        self.O_per_FU = O_per_FU
        self.SiO2 = SiO2
        self.Al2O3 = Al2O3
        self.Fe2O3 = Fe2O3
        self.FeO = FeO
        self.MnO = MnO
        self.MgO = MgO
        self.CaO = CaO
        self.Na2O = Na2O
        self.K2O = K2O
        self.H2O = H2O
        self.total = SiO2 + Al2O3 + Fe2O3 + FeO + MnO + MgO + CaO + Na2O + K2O + H2O
        if self.total < 97 or self.total > 103:
            raise ValueError(f"Total of {self.total} not in the range between 97 and 103 %")


        # Calculate
        chem = vars(self)
        oxigens = [chem[k] * self.o_per_ox[k] / self.moleculemass[k] for k in self.o_per_ox]
        self.kations = []

        for k in self.moleculemass:
            if k == 'Fe2O3':
                katkey = 'FeIII'
            else:
                matches = re.search(r"^([A-Z][a-z]?)", k)
                katkey = matches.group(1)
            if chem[k] != 0:
                kat = chem[k] * self.kat_per_ox[k] *  self.O_per_FU / (self.moleculemass[k] * sum(oxigens))
                setattr(self, katkey, kat)
                self.kations.append(katkey)

        # Set formula
        chem = vars(self)
        self.formula = ""
        for k in self.kations:
            self.formula = self.formula + k + f" {chem[k]:.3f} "
        self.formula = self.formula + "O " + str(self.O_per_FU)


    def __str__(self):
        return f"<Silicate> {self.name} {self.formula}"



class Olivine(Silicate):
    def __init__(self, name="", SiO2=0, FeO=0, MnO=0, MgO=0, CaO=0):
        O_per_FU = 4
        super().__init__(O_per_FU, name=name, SiO2=SiO2, FeO=FeO, MnO=MnO, MgO=MgO, CaO=CaO)
        self.formula = f"(Mg {self.Mg:.3f} Fe {self.Fe:.3f} Ca {self.Ca:.3f} Mn {self.Mn:.3f}) Si {self.Si:.3f} O 4"

    def __str__(self):
        return f"<Olivine> {self.name} {self.formula}"

    @property
    def z(self):
        return self.Si

    @property
    def y(self):
        return self.Fe + self.Mn + self.Mg + self.Ca

    @property
    def sites(self):
        return {
            "Z": {
                "Si": self.Si,
            },
            "Y": {
                "Fe": self.Fe,
                "Mn": self.Mn,
                "Mg": self.Mg,
                "Ca": self.Ca,
            }
        }


class Amphibole(Silicate):
    def __init__(self, name="", SiO2=0, Al2O3=0, Fe2O3=0, FeO=0, MnO=0, MgO=0, CaO=0, Na2O=0, K2O=0, H2O=0):
        O_per_FU = 24
        super().__init__(O_per_FU, name=name, SiO2=SiO2, Al2O3=Al2O3, Fe2O3=Fe2O3, FeO=FeO, MnO=MnO, MgO=MgO, CaO=CaO, Na2O=Na2O, K2O=K2O, H2O=H2O)
        self.formula = f"K {self.K:.3f} (Ca {self.Ca:.3f} Na {self.Na:.3f}) (Mg {self.Mg:.3f} Fe {self.Fe:.3f} Mn {self.Mn:.3f} Fe3+ {self.FeIII:.3f} Al {self.AlC:.3f}) (Al {self.AlZ:.3f}) Si {self.Si:.3f}) O 22 (OH) {self.OH:.3f}"


    @property
    def AlZ(self):
        return self.Al - (8 - self.Si)

    @property
    def AlC(self):
        return self.Al - self.AlZ

    @property
    def z(self):
        return 8

    @property
    def c(self):
        return self.AlC + self.FeIII + self.Fe + self.Mn + self.Mg

    @property
    def b(self):
        return self.Ca + self.Na

    @property
    def a(self):
        return self.K

    @property
    def OH(self):
        return self.H

    @property
    def sites(self):
        return {
            "Z": {
                "Si": self.Si,
                "Al": self.AlZ,
            },
            "C": {
                "Al": self.AlC,
                "FeIII": self.FeIII,
                "Fe": self.Fe,
                "Mn": self.Mn,
                "Mg": self.Mg,
            },
            "B": {
                "Ca": self.Ca,
                "Na": self.Na,
            },
            "A":{
                "K": self.K,
            },
            "OH": {
                "OH": self.OH,
            }
        }



# Some data

olivine_data = {
    "SiO2": 39.41,
    "FeO": 16.46,
    "MnO": 0.21,
    "MgO": 43.27,
    "CaO": 0.23,
}

amphibole_data = {
    "SiO2": 57.73,
    "Al2O3": 12.04,
    "Fe2O3": 1.16,
    "FeO": 5.41,
    "MnO": 0.1,
    "MgO": 13.03,
    "CaO": 1.04,
    "Na2O": 6.98,
    "K2O": 0.68,
    "H2O": 2.27,
}

# Main
def main():
    print("Olivine")
    olivine1 = Silicate(4, **olivine_data)
    print(olivine1)

    olivine2 = Olivine(**olivine_data)

    print(olivine2)
    print("z", olivine2.z)
    print("y", olivine2.y)
    print(olivine2.sites)
    print()

    print("Amphibole")
    amph = Amphibole(**amphibole_data)
    print(amph)
    print(amph.sites)




if __name__ == "__main__":
    main()