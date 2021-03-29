## Explosion-Diffuser

My take on generating a combinatorial explosion and searching through it for a match using multiple optimization techniques.<br>
The combinatorial explosion stems from generation of all variations, with symbol repetition, of length `K` using a set of symbols of length `N`:
`N`<sup>`K`</sup> total number of variations. <br>

---

### Installation:

`git clone https://github.com/ginger-with-a-soul/Explosion_Diffuser-Computational_Intelligence.git` <br>
`cd ~/Explosion_Diffuser-Computational_Intelligence/runnable` <br>
`./make` <br>

---

### Parameters:
`size` - length of a variation (**MAX SIZE: 21**)<br>
`number of symbols` - number of symbols that variation can use (**MAX SIZE: 36**)<br>
_there is a hardlock in place if you try to use parameters that are larger than this and the search won't start_ <br>

---


### Algorithms:

I've implemented 2 different algorithms that affect the speed of the search drastically, which was the point of this project after all.<br><br>**Brute-force algorithm** is the slowest of them all. It goes through variations from back to front transforming current variation into the next one by incrementing it by 1. It gets really slow when the lenght of a variation is about 10-11 and the number of symbols is about 7-8.<br><br>
**Genetic algorithm with simulated annealing** is a very efficient implementation of this evolutive algorithm. It uses simulated annealing optimization that contributes to what is a very fast stochastic search algorithm. <br>

---
