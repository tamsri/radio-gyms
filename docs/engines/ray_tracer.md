# Tracer
Tracer is an engine to trace the possible propagation paths from the scene. 

## Import
```python
from radio_gyms.engines import Tracer
```

## Construction
inputs 
 - object_file_path: str,  the .obj file path for tracing
 - ref_max: number, the maximum reflection bounce tracing
```python
SCENE_PATH = "./my_map.obj"
tracer = Tracer(SCENE_PATH, 2)
```

## Methods
### trace_outdoor
Trace the paths from the given transmitting point to the the given receiving point.
inputs
 - tx_pos: Tuple[float,float,float], transmitting position
 - rx_pos: Tuple[float, float, flaot], receiving position
output
 - result, trace result object
---
### direct_path
Check the given transmitting point and the given receiving point are in line-of-sight.
inputs
 - tx_pos: Tuple[float, float, float], transmitting position
 - rx_pos: Tuple[float, float, float], receiving position
#### output
 - result: boolean
----
### trace_reflection
Trace the reflection points between the given transmitting point and the given receiving point.
#### inputs
 - tx_pos: Tuple[float, float, float], transmitting position
 - rx_pos: Tuple[float, float, float], receiving position 
#### output
 - result, reflection result object 
---
### trace_single_reflect
Trace the single reflection points between the given transmitting point and the given receiving point.
#### inputs
 - tx_pos: Tuple[float, float, float], transmitting position
 - rx_pos: Tuple[float, float, float], receiving position
#### output
 - result, list of single reflected points
---
### trace_double_reflect
Trace the double reflection points between the given transmitting point and the given receiving point.
#### inputs
 - tx_pos: Tuple[float, float, float], transmitting position
 - rx_pos: Tuple[float, float, float], receiving position
#### output
 - result, list of double reflected points
---
### trace_roof_edges
Trace the roof edges from the transmitting position to the receiving position. The top of positions must be an open sky.
inputs
 - tx_pos: Tuple[float, float, float], transmitting position
 - rx_pos: Tuple[float, float, float], receiving position
output
 - result, list of roof edges
---
### is_outdoor
Check the given position is outdoor.
#### input
 - pos: Tuple[float, float, float], position
#### output
 - result: boolean, indicate if the given position is outdoor
---
### terrain_height
Provide the terrain height of the given position
#### input
 - x: float, x-coordinate point
 - z: float, z-coordinate point
#### output
 - y: float, height of the terrain

---
### get_terrain_depth
     def(self, x: float, z: float):
        upper = np.array([x, 1000, z])
        lower_ray = (upper, np.array([0, -1, 0]))
        nearest_hit = self.map.is_intersect(lower_ray)
        if nearest_hit == -1:
            return 0
        return 1000 - nearest_hit

    def (self, x_n, z_n):
        x_min, x_max = self.min_bound[0], self.max_bound[2]
        z_min, z_max = self.min_bound[0], self.max_bound[2]
        assert x_min < x_max
        assert z_min < z_max
        depth_map = []
        for x in np.linspace(x_min, x_max, x_n):
            for z in np.linspace(z_min, z_max, z_n):
                height = self.terrain_height(x, z)
                if height != -1:
                    depth_map.append({'x': x, 'z': z, 'height': height})
        return pd.DataFrame(depth_map)