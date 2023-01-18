# Silicate as Python class
## Disclaimer
The purpose of this project was to get used to object orientated programming in python. It is not considered to be of any use for mineralogy. It might be incorrect or incomplete.
## About
Model silicates as python classes. An instance is initiated with the chemistry of the mineral (as wt.% of oxides). Mineral formula, cations per formula, lattice site totals and a dictionary of cations on lattice sites can be accessed as class attributes.

For now I have the classes:
- Sicicate as base class
- Olivine
- Amphibole

## Usage
```python
from silicate import Olivine

olivine_data = {
    "SiO2": 39.41,
    "FeO": 16.46,
    "MnO": 0.21,
    "MgO": 43.27,
    "CaO": 0.23,
}

olivine = Olivine("my sample", **olivine_data)

print(olivine)
# <Olivine> my sample (Mg 1.638 Fe 0.350 Ca 0.006 Mn 0.005) Si 1.001 O 4

print(olivine.formula)
# (Mg 1.638 Fe 0.350 Ca 0.006 Mn 0.005) Si 1.001 O 4

print(olivine.Mg)
# 1.6377856827011499

print(olivine.sites)
# {'Z': {'Si': 1.0009097720077973}, 'Y': {'Fe': 0.34961797811072864, 'Mn': 0.004517714782608314, 'Mg': 1.6377856827011499, 'Ca': 0.006259080389918636}}
```
## Classes
### Silicate
```python
silicate = Silicate(O_per_FU, name="", SiO2=0, Al2O3=0, Fe2O3=0, FeO=0, MnO=0, MgO=0, CaO=0, Na2O=0, K2O=0, H2O=0)
```
Arguments:
- O_per_FU: Oxigen per formula unit, required argument for the base class.
- name: optional
- SiO2, Al2O3, Fe2O3, FeO, MnO, MgO, CaO, Na2O, K2O, H2O: wt.% of oxides

Attributes:
- name
- SiO2, Al2O3, Fe2O3, FeO, MnO, MgO, CaO, Na2O, K2O, H2O: wt.% of oxides
- Si, Al, FeIII, Fe, Mn, Mg, Ca, Na, K, H: respective cations per formula unit
- formula

### Olivine
```python
olivine = Olivine(name="", SiO2=0, FeO=0, MnO=0, MgO=0, CaO=0)
```
Arguments:
- name: optional
- SiO2, FeO, MnO, MgO, CaO: wt.% of oxides

Attributes:
- name
- SiO2, FeO, MnO, MgO, CaO: wt.% of oxides
- Si, Fe, Mn, Mg, Ca: respective cations per formula unit
- z, y: total of Z and Y site, respectively
- sites: dictionary with cations mapped to lattice sites
- formula

### Amphibole
```python
amphibole = Amphibole(name="", SiO2=0, Al2O3=0, Fe2O3=0, FeO=0, MnO=0, MgO=0, CaO=0, Na2O=0, K2O=0, H2O=0)
```
Arguments:
- name: optional
- SiO2, Al2O3, Fe2O3, FeO, MnO, MgO, CaO, Na2O, K2O, H2O: wt.% of oxides

Attributes:
- name
- SiO2, Al2O3, Fe2O3, FeO, MnO, MgO, CaO, Na2O, K2O, H2O: wt.% of oxides
- Si, Al, FeIII, Fe, Mn, Mg, Ca, Na, K, H: respective cations per formula unit
- AlZ, AlC: Al on Z and C site, respectively
- z, c, b, a, OH: total of Z, C, B, A, OH sites, respectively
- sites: dictionary with cations mapped to lattice sites
- formula