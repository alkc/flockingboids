# FlockingBoids

A cozy project I made in 2015 (I think) in a state of perpeutal panic for the course "Theoretical Modelling in Biology (B-KUL-G0G41A)" at KU Leuven. The code and documentation is preserved here in all its frantic glory (for the purpose of maximizing nostalgia).

## What's it do?

The script implements a flock of [Boids](https://en.wikipedia.org/wiki/Boids) and a PredatorBoid (or two) to hunt them. The Boids are hunted down and eaten one by one by the PredatorBoids, until a user-defined number of Boids has been eaten, whereupon the  remaining number of boids get to breed a new generation of a flock and the simulation restarts.

If I remember correctly, the boids should have a simple genetic code that determines how strongly they adhere to any of the rules of the flocking behavior. This code can mutate, and so on.

There's a GUI, implemented through pygame, where the user can watch them die and evolve. Pretty grisly, huh?

## Dependencies

* Python (probably 3-something)
* pygame
