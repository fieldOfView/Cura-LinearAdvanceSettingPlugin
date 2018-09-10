# LinearAdvanceSettingPlugin

This plugin adds a setting named "Linear Advance Factor" to the Material category in the Custom print setup of Cura.

If the start gcode doesn't include an M900 statement to set the linear advance parameters, a single G-code line is added before the start G-code:
```
...
M900 K{material_linear_advance_factor}
...
```

Users may want to add more detailed M900 parameters in their start G-code snippet, eg:

```
...
M900 K{material_linear_advance_factor}
M900 W{line_width} H{layer_height} D{material_diameter}
...
```
