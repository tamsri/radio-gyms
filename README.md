# Radio Gyms

![Radio Gyms](https://github.com/intelek-ai/radio-gyms/blob/master/assets/logo.png)

Radio Gyms is an open-source bundle of AI environments for radio communications. 
The simulations are built for AI gyms with the support of radio-related calculation modules, and theoretical radio propagation models to simulate an accurate prediction, 
specifically to perform reinforcement learning algorithms.

## Installation
### PyPi Package via pip
```shell
pip install radio_gyms
```
### Build from source
```shell
git clone https://github.com/intelek-ai/radio-gyms
cd radio-gyms
python -m pip install .
cd ..
rm -rf radio_gyms
```
### Dependencies
* python 3.8+
* numpy
* pyglet
* pywavefront
## Features
Radio gyms provides the toolkit for building wireless communication simulations including modules can be called to build and 
customize the radio propagation simulation. 
### 1. Calling Primitive Ray Tracer for Outdoor Propagation
The ray tracer can be called for computing the radio propagation paths in the following example.
```python
from radio_gyms.engines import Tracer

SCENE_FILE_PATH = "./city.obj"
tracer = Tracer(SCENE_FILE_PATH)
# position (x, y, z)
tx_pos = [0, 15, 0]
rx_pos = [-30, 1.5, 45]
# get traced result
result = tracer.trace_outdoor(tx_pos, rx_pos)
# result
# {'direct': False, 
# 'reflections': {'single': [   array([-28.94988531,   4.22886929,  62.39469675]),
#                               array([-70.80339945,   7.04682531,  15.22840999])],
#                  'double': []},
# 'roof_edges': [array([-19.24403786,   8.5621709 ,  28.8660568 ]
# 'tx_pos': array([ 0, 15,  0]),
# 'rx_pos': array([-30. ,   1.5,  45. ]),
# )]}
```
### 2. Calculate the traced result with the theoretical outdoor model
The result from the ray tracer can be calculated by the propagation models in ```radio_gyms.models```. 
In this example, ```TheoreticalOutdoorModel``` can compute the traced results to predict the signal strength 
and delay between the receiver and transmitter based on the theoretical radio propagation models.
```python
from radio_gyms.models import TheoreticalOutdoorModel
result = {
    'direct': False, 
    'reflections': {'single': [ [-28.94988531, 4.22886929, 62.39469675],
                                [-70.80339945, 7.04682531, 15.22840999]],
                    'double': []},
    'roof_edges': [[-19.24403786, 8.5621709 , 28.8660568 ]],
    'tx_pos': [ 0, 15, 0],
    'rx_pos': [-30., 1.5, 45. ],
}
model = TheoreticalOutdoorModel(result, tx_power_dbm=20)
maximum_received_power = model.calculate_max_received_power(frequency=5.4e9) 
# -72.51 dBm
impulses = model.calculate_signal_impulses(freq=5.4e9)
# [{'strength': -85.94590320344925, 'delay': 1.8653420787826134e-07},
# {'strength': -74.3214622218488, 'delay': 2.910702009034143e-07}, 
# {'strength': -77.80902883055407, 'delay': 4.125241781539828e-07}]
```
### 3. Visualize the data with window 
As we obtain the traced paths from the tracer, we can convert these paths into lines for the visualization. 
```Window()``` can be called to read the lines and the scene to visualize the scene in 3D by ```window.run()```.
```python
import numpy as np
from radio_gyms.visualizers import Window
from radio_gyms.engines.ray_tracer.tracer import Tracer
from radio_gyms.utils import OutdoorResultToLines

MAT_OBJ_PATH = "./city.obj

window = Window()
window.load_obj_to_scene(MAT_OBJ_PATH)
tracer = Tracer(MAT_OBJ_PATH)
tx_pos = np.array([0, 5, 0])
lines = []
while True:
    rx_pos = (np.random.rand(3)*2-1)*100
    rx_pos[1] = 1.2
    if tracer.is_outdoor(rx_pos):
        break
result = tracer.trace_outdoor(tx_pos, rx_pos)
lines = lines + OutdoorResultToLines(result)
window.line_sets = lines
window.run()
```
With the ```.run()``` The camera can be moved by ```W```  ```A```  ```S```  ```D``` keys and rotated by ```Q``` ```E```.
![Old Town's Visualization](https://github.com/intelek-ai/radio-gyms/blob/master/assets/examples/oldtown_freeze.gif)

### 4. Visualize the scene and radio propagation paths during running a simulation
```window.render()``` can be called to visualize the simulation frame as the simulation updates the components. 
```python
from radio_gyms.engines.ray_tracer.tracer import Tracer
from radio_gyms.visualizers import Window
from radio_gyms.utils.converters import outdoor_traced_result_to_line as OutdoorResultToLines
from radio_gyms.simulations import OldtownWalk

MAP_OBJ_PATH = "./city.obj"

window = Window()
window.load_obj_to_scene(MAP_OBJ_PATH)
tracer = Tracer(MAP_OBJ_PATH, ref_max=2) # ref_max == max reflection tracing
simulation = OldtownWalk(tracer, 1, 5)
# Run 100 episodes
for i in range(100):
    simulation.update(1) # update time in the simulation by 1 second
    results = simulation.get_results() # get result from simulation
    window.line_sets = []
    # convert the results to lines for visualizing in window
    for result in results:
        result_lines = OutdoorResultToLines(result)
        window.line_sets += result_lines
    # render the scene    
    window.render()
    window.dispatch_events()
```
![Old Town Simulation's Visualization](https://github.com/intelek-ai/radio-gyms/blob/master/assets/examples/oldtown.gif)

### 5. Visualize the scene and radio propagation paths on notebook
Radio gyms can be visualized on a notebook in 2D by using ```utils.Plotter```. 
```Plotter()``` requires definition of boundary of the map to visualize. The parameters such as points and lines can be passed to Plotter to visualize the data.

```python
from radio_gyms.engines import Tracer
from radio_gyms.utils import Plotter, OutdoorResultToLines
MAP_SCENE = "./city.obj"

tracer = Tracer(MAP_SCENE)
rx = [0, 1.2, 0]
tx = [-50, 4, 40]
result = tracer.trace_outdoor(tx, rx)
terrain_map = tracer.get_terrain_depth(64, 64)
plotter = Plotter( tracer.min_bound, tracer.max_bound, terrain_map)
plotter.rx_pos.append(rx)
plotter.tx_pos.append(tx)
plotter.lines =  OutdoorResultToLines(result)

plotter.render_top() # Display from top view
```
![Old Town Simulation's Visualization on a notebook](https://github.com/intelek-ai/radio-gyms/blob/master/assets/examples/notebook_render.png)

## Gyms
### 1. ```radio-gym-01``` : Cooperative Small Cell Power Switching (Coming soon, V1.0.0)
- #### Environment
The environment consists of mobile UEs as pedestrians walk in the old town and multiple small cells.
The small cells can sense the signal strength and delay of pedestrians where UEs only connect to the cell which provides the
strongest signal. 
- #### Reward
The reward is considered for average connected signal strength of all UEs to cells, the average signal-to-noise (SNR) of UEs 
between connected cell and disconnected cell, and the consumption transmitting power. 
- #### Action
Each cell can control its own transmitting power.

### 2. ```radio-gym-02```: Beamformer by antenna node control (Expected in v1.5)


## Documentation
Radio Gyms provides radio propagation engines and tools for customizations.
The official documentation can be found at ***[radio-gyms.intelek.ai](https://radio-gyms.intelek.ai)***

## Citations
The pre-released source code can be cited with the following bibtex entry.
```text
@misc{radiogyms2022,
  author = {Supawat Tamsri},
  title = {Radio Gyms},
  year = {2022},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/intelek-ai/radio-gyms}},
}
```

## Contributors
- [Supawat Tamsri](https://github.com/tamsri), supawat@intelek.ai
  - Founds and develops.
- [Muhammad Aamir Khan](https://scholar.google.com/citations?user=Q7YdzQEAAAAJ), aamir@intelek.ai
  - Supervises on machine learning research and AI environments.
- [Prof. Eng. Krzysztof Cichoń](https://scholar.google.com/citations?user=GmzK3-oAAAAJ), krzysztof.cichon@put.poznan.pl
  - Supervises on radio propagation and channel modelling features.
  - Validates and verifies theoretical models and simulated results.

## Community 
Feel free to suggest an environment idea or contribute with us.
* [Discord](https://discord.gg/Rp2KhXcpPh)

## Road Map
- [x] v0.1.x - Radio Ray Tracer
- [x] v0.2.x - Theoretical Outdoor Propagation Model
- [x] v0.3.x - Transmitter and Receiver Controller
- [x] v0.4.x - Visualization for desktop
- [x] v0.5.x - Visualization for notebook
- [x] v0.6.x - Outdoor Simulation
- [x] v0.7.x - Radio Gym 01: Wireless UAV Location Control
- [ ] v0.8.x - Radio Gym 02: UE Location Prediction
- [ ] v0.9.x - Radio Gym 03: Cooperative Small Cell Power Control
- [ ] v0.9.5 - Beamforming Engine
- [ ] v1.0.x - Radio Gym 04: Intelligent Beamformer
- [ ] v1.1.x - FDTD Engine

## License

The digital contents in ```/assets``` are available under Creative Commons (CC) license.

Source code is licensed under **© Intelek AI [MIT](https://github.com/intelek-ai/radio-gyms/blob/master/LICENSE)**.
