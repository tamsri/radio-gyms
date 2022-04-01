# Getting Starated

## Installation

```shell
pip install radio-gyms
```


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
lines = lines + OutdoorResultToLines(result, tx_pos, rx_pos)
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
