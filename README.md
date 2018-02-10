# LinearAdvanceSettingPlugin

This plugin adds a setting named "Linear Advance Factor" to the Material category in the Custom print setup of Cura. By itself this setting has no effect on the created gcode, but the value of the setting can be used in the start gcode snippet, eg:

```
...
M900 K{material_linear_advance_factor}
M900 W{line_width} H{layer_height} D{material_diameter}
...
```
