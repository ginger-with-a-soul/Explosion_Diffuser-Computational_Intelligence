## Summary:

eXplosion Diffuser represents my take on generating a combinatorial explosion and searching through it for a match using computer vision techniques.<br>
The combinatorial explosion stems from generation of all variations, with symbol repetition, of length `K` using a set of symbols of cardinality `N`:
`N`<sup>`K`</sup> total number of variations. <br>

---

### Installation:

## Via Docker:
`docker run --name explosion-diffuser -dt -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix gingerwithasoul/explosion-diffuser:latest`

## Via Pyinstaller:
`git clone https://github.com/ginger-with-a-soul/Explosion_Diffuser-Computational_Intelligence.git` <br>
`cd Explosion_Diffuser-Computational_Intelligence/runnable` <br>
`./main` <br>

**Usage:** *press ESC when the visualizer window finishes if you want to start another run. Otherwise a new visualizer window will be opened on top of the existing one and the program will crash*

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

I've implemented 2 different algorithms that affect the speed of the search drastically, which was the point of this project after all.<br><br>**Brute-force algorithm** is the slowest of them all. It goes through variations from back to front transforming current variation into the next one by incrementing it by 1. It gets really slow when the length of a variation is about 10-11 and the number of symbols is about 7-8.<br><br>
**Genetic algorithm with simulated annealing** is a very efficient implementation of this evolutive algorithm. It uses simulated annealing optimization that contributes to what is a very fast stochastic search algorithm. <br><br>

*In the future I plan to add some other algorithms as an expansion to this project, and a better benchmark for my 2nd algorithm.*


![Main menu](https://user-images.githubusercontent.com/55445149/173895847-d3a3e7ad-0293-4fe1-a634-1eee736cf2de.png)

![Brute force](https://user-images.githubusercontent.com/55445149/173895901-eacc2857-16c4-4917-b831-9b2323c1ce91.png)

![Almost there](https://user-images.githubusercontent.com/55445149/173895959-9c1c8ec9-ec2e-4c16-925f-a4152e1256c4.png)

![Brute force found it!](https://user-images.githubusercontent.com/55445149/173895975-1734c992-860f-43a5-aae1-8fb9d89c4f1e.png)

![Genetic algorithm started](https://user-images.githubusercontent.com/55445149/173895992-f62cb231-bf95-4e5e-94d3-2e1d6286d1f3.png)

![Almost there](https://user-images.githubusercontent.com/55445149/173896011-1f11bc74-d473-4f3c-81f2-1a86885aad3d.png)

![Success!](https://user-images.githubusercontent.com/55445149/173896018-d3e6581c-2fc2-4563-aa82-086b2fccb587.png)



