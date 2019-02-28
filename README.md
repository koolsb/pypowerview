## Status

# pypowerview
Python3 interface implementation for Powerview Hub

## Notes
This is for use with [Home-Assistant](http://home-assistant.io)

## Usage
```python
from pypowerview import PowerView

# Connect via IP
pv = PowerView('192.168.1.50')

# Return an array of shade objects
shades = pv.get_shades()

# Return first shade in array
shade = shades[0]

# Return attributes of shade
print(shade.id)
print(shade.name)
print(shade.position) # Position represented 0 (close) to 100 (open)

# Update shade position

pv.get_status(shade)

# Close shade

pv.close_shade(shade)

# Open Shade

pv.open_shade(shade)

# Stop shade in motion

pv.stop_shade(shade)

# Set shade to specific position (0 - 100)

pv.set_shade_position(shade, 55)
```
