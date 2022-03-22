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
import radio_gyms.engines as Tracer

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
# 'tx_pos': array([ 0, 15,  0]),
# 'rx_pos': array([-30. ,   1.5,  45. ]),
# 'roof_edges': [array([-19.24403786,   8.5621709 ,  28.8660568 ])]}
```

## Documentation
Radio Gyms provides radio propagation engines and tools for customizations.
The official documentation can be found at ***[radio-gyms.intelek.ai](https://radio-gyms.intelek.ai)***

## Contributors
- [Supawat Tamsri](https://github.com/tamsri)
- Krysztof Cichoń

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
- [ ] v0.2.x - Theoretical Outdoor Propagation Model
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
