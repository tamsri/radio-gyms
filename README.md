# Radio Gyms

![Radio Gyms](https://github.com/intelek-ai/radio-gyms/blob/master/assets/logo.png)

Radio Gyms is an open-source bundle of AI environments for radio communications. The simulations are composed of Open AI Gym and various theoretical radio propagation models, specifically for AI research in telecommunications. 

## Installation

```commandline
pip install radio_gyms
```

## Examples
### 1. Calling Primitive Ray Tracer for Outdoor Propagation
Radio gyms provides the toolkit for building wireless communication simulations. 
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
## Documentation
Radio Gyms provides radio propagation engines and tools for customizations.
The official documentation can be found at ***[radio-gyms.intelek.ai](https://radio-gyms.intelek.ai)***

## Contributors
- [Supawat Tamsri](https://github.com/tamsri)
- [Krzysztof Cichoń](https://scholar.google.pl/citations?user=GmzK3-oAAAAJ)

[//]: # (## Citation)

[//]: # (```)

[//]: # (@article{)

[//]: # (	title={Radio Gyms},)

[//]: # (	author={Supawat Tamsri and Krysztof Cichoń},)

[//]: # (	year={2022})

[//]: # (})

[//]: # (```)

## Community
Feel free to suggest an idea or contribute with us.
* [Discord](https://discord.gg/Rp2KhXcpPh)

## Road Map
- [x] v0.1.x - Radio Ray Tracer
- [x] v0.2.x - Theoretical Outdoor Propagation Model
- [ ] v0.3.x - Radio Transmitter and Receiver Controller
- [ ] v0.4.x - Visualization for desktop
- [ ] v0.5.x - Visualization for notebook
- [ ] v0.6.x - Outdoor Simulation
- [ ] v1.0.0 - Radio Gym 01: Beam Steering
- [ ] v1.5.0 - Radio Gym 02: Beam-forming Control by Antenna Array
- [ ] v2.x.x - FDTD Model
- [ ] v3.1.0 - Radio Gym 03: Indoor Environment
- [ ] v3.2.0 - Radio Gym 04: Complex Transmission Control


## License
**© Intelek AI [MIT](https://github.com/intelek-ai/radio-gyms/blob/master/LICENSE)**.
