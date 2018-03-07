# FlockingBoids

A silly project I made in 2015/2016 (I think) in a state of perpeutal panic for the course "Theoretical Modelling in Biology (B-KUL-G0G41A)" at KU Leuven. The code and documentation is preserved here in all its frantic glory (entirely out of nostalgia).

For the purpose of actual science (studying the evolution of flocking) it's not a very good or realistic simulation. But it sure as hell was fun to code up in two-and-a-half months. Up to that point my Python code was mostly crappy bioinformatics scripts and simple crappy web apps -- this, on the other hand, was my first real crappy Python program.

I should probably mention here that the quality of my Python code has improved since I finished this back in early 2016 :x

## What's it do?

The script implements a flock of [Boids](https://en.wikipedia.org/wiki/Boids) and a PredatorBoid (or two) to hunt them. The Boids are hunted down and eaten one by one by the PredatorBoids, until a user-defined number of Boids has been eaten, whereupon the  remaining number of boids get to breed a new generation of a flock and the simulation restarts.

If I remember correctly, the boids should have a simple genetic code that determines how strongly they adhere to any of the rules of the flocking behavior. This code can mutate, and so on.

There's a GUI, implemented through pygame, where the user can watch them die and evolve. Pretty grisly, huh?

## Dependencies

* Python 2. I _think._
* Some version of pygame.
