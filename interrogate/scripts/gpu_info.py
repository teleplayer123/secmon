import cupy
from pprint import pprint

device = cupy.cuda.Device(0)
dev_attrs = device.attributes

pprint(dev_attrs)
