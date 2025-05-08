# M-TA-Prioritized-MAPD
Multi-Agent Pickup and Delivery

Implementation of the [TA-Prioritized](https://dl.acm.org/doi/10.5555/3306127.3331816) algorithm with a modified deadlock avoidance method for a significant improvement of the larger instances' makespans. This implementation does not compute the solution for the travelling salesman problem, but instead loads the solution provided by the author.



[![Demo CountPages alpha](https://j.gifs.com/5QoqDY.gif)](https://youtu.be/LY9a7Q_aBT4)
## Agent types
**Orange cells:** Agent parking locations<br/>
**Blue cells:** Task endpoints (pickup/delivery)<br/>
**Black cells:** Wall/blocked cell<br/>

## Requirements
Requires [Mesa](https://mesa.readthedocs.io/en/master/index.html) to run the simulation.<br/>
Install with PIP:
```
pip install Mesa==0.8.7
```


 
