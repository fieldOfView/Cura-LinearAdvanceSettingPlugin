# LinearAdvanceSettingPlugin

This plugin adds a setting named "Linear Advance Factor", and a number of feature-specific subsettings to the Material category in the Custom print setup of Cura. The plugin inserts M900 commands in the Gcode to set the Linear Advance Factor for Marlin-based printers (that have the LIN_ADVANCE feature enabled) or M572 to set the Pressure Advance Factor for RepRap based printers.

For more information about Linear Advance, see the Marlin documentation: http://marlinfw.org/docs/features/lin_advance.html
For more information about Pressure Advance, see the Duet documentation: https://duet3d.dozuki.com/Wiki/Pressure_advance

Users of Klipper can add the following lines to their `printer.cfg`:
```
[gcode_macro M900]
gcode:
  {% set K = params.K|default(0)|float %}
  SET_PRESSURE_ADVANCE ADVANCE={K}
```
