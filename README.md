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

Při testování na datasetu MNIST shluky nevznikaly správně. Kód přeložený pomocí Numba a paralelizovaný pomocí prange() 
běžel v řádech minut. Kód ve standardním, neparalelizovaném Pythonu běžel PODSTATNĚ déle -- na finální čas lineárního
kódu jsem proto ani nečekal.

To, zdali algoritmus správně pracuje a tvoří clustery, jsem ověřil na datasetu z přiloženého paperu ( Thavikulwat, Precha. “Affinity Propagation: A Clustering Algorithm for Computer-Assisted Business Simulations and Experiential Exercises.” Developments in Business Simulation and Experiential Learning 35 (2014): n. pag.)

Výsledkem byly dva správně určené shluky. Jelikož se však jednalo o velmi malý dataset, rozdíl v rychlostí běhu lineárního
a paralelního řešení byl nepatrný.