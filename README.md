## Summary:

eXplosion Diffuser represents my take on generating a combinatorial explosion and searching through it for a match using computer vision techniques.<br>
The combinatorial explosion stems from generation of all variations, with symbol repetition, of length `K` using a set of symbols of cardinality `N`:
`N`<sup>`K`</sup> total number of variations. <br>

---

### Installation:

`git clone https://github.com/ginger-with-a-soul/Explosion_Diffuser-Computational_Intelligence.git` <br>
`cd Explosion_Diffuser-Computational_Intelligence/runnable` <br>
`./make` <br>

---

### Requirements:

Python 3.8+ <br>
The folder _runnable_ contains all of the packages you need already prepared using [PyInstaller](https://github.com/pyinstaller/pyinstaller). Because of that no extra installation is needed for **Linux** distos. If you want to run this on Windows or some other OS, you need to install all of the packages listed below and then you will be able to launch _main.py_ from the ***src*** directory. <br><br>
Packages used:
* [Tkinter](https://docs.python.org/3/library/tkinter.html)
* [Pygubu](https://github.com/alejandroautalan/pygubu)
* [Psutil](https://github.com/giampaolo/psutil)
* [Pygame](https://github.com/pygame/pygame)
* [Baseconvert](https://github.com/squdle/baseconvert) -> *SOURCE OF THIS ONE IS ALREADY INCLUDED (**baseconv.py** - was NOT written by me). THIS WAS DONE BECAUSE PYINSTALLER WOULD NOT COOPERATE WITH THIS PACKAGE*

---

### Parameters:
`size` - length of a variation (**MAX SIZE: 21**)<br>
`number of symbols` - number of symbols that variation can use (**MAX SIZE: 36**)<br>
_there is a hardlock in place if you try to use parameters that are larger than this and the search won't start_ <br>

---


### Algorithms:

I've implemented 2 different algorithms that affect the speed of the search drastically, which was the point of this project after all.<br><br>**Brute-force algorithm** is the slowest of them all. It goes through variations from back to front transforming current variation into the next one by incrementing it by 1. It gets really slow when the lenght of a variation is about 10-11 and the number of symbols is about 7-8.<br><br>
**Genetic algorithm with simulated annealing** is a very efficient implementation of this evolutive algorithm. It uses simulated annealing optimization that contributes to what is a very fast stochastic search algorithm. <br><br>

*In the future I plan to add some other algorithms as an expansion to this project, and a better benchmark for my 2nd algorithm.*
