# PA
Pro implementaci úkolů do PA jsem se rozhodl použít Python a vyzkoušet vícero způsobů, jakými lze kód paralelizovat --
automaticky pomocí překladače Numba a manuálně pomocí knihovny Multiprocessing. V případě středních či velkých vstupů paralelizace
pokaždé přinesla masivní zlepšení, v případě malých vstupů byla kvůli přidané režii paralelizace +- stejně výkonná jako lineární kód.
I s použitím paralelizace jsou však výsledné algoritmy řádově pomalejší než odpovídající  implementace v jazycích jako
C++, Rust či Go...

## 1. Single Row Facility Layout Problem

Použité knihovny: Itertools, Multiprocessing, Time.

V jednom procesu a bez použití techniky Branch and Bound běžel algoritmus 103 sekund a došel k řešení:

- Best permutation: [0, 4, 1, 9, 6, 3, 7, 2, 5, 8]
- Best distance: 5596. 

S využitím Multiprocessingu (8 procesů) a techniky Branch and Bound běžel program 9 sekund a došel k totožným výsledkům.


## 2. Affinity Propagation

Použité knihovny: Pandas, Numpy, Numba, Scipy, Time.

Při testování na redukovaném datasetu MNIST se ukázala paralelizace pomocí Numby jako podstatně rychlejší -- algoritmus běžel
6 sekund. Lineární kód pak běžel 50 sekund. Shlukování však neproběhlo podle skutečných tříd, a proto jsem se rozhodl 
ověřit správnost ještě na základě dat z přiloženého paperu.

````
 Thavikulwat, Precha. “Affinity Propagation: A Clustering Algorithm for Computer-Assisted Business Simulations and Experiential Exercises.” Developments in Business Simulation and Experiential Learning 35 (2014): n. pag. 
````

Na základě těchto dat jsem ověřil, že algoritmus funguje správně:
````
Criterion matrix:
 [[  5. -16. -15. -11. -21.]
 [  5. -15. -25. -15. -25.]
 [  5. -26. -15. -17. -25.]
 [ -9. -29. -30.  -5. -10.]
 [-14. -34. -33.  -5. -10.]]
Clusters:
 {0: [0, 1, 2], 3: [3, 4]}
````
Paralelizace však zde kvůli režijním nákladům a velmi malému rozsahu dat nebyla tak efektivní.