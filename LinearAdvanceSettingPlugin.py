# Copyright (c) 2018 fieldOfView
# The LinearAdvanceSettingPlugin is released under the terms of the AGPLv3 or higher.

from UM.Extension import Extension
from UM.Application import Application
from UM.Logger import Logger
from UM.Settings.SettingDefinition import SettingDefinition
from UM.Settings.DefinitionContainer import DefinitionContainer
from UM.Settings.ContainerRegistry import ContainerRegistry

from UM.i18n import i18nCatalog
i18n_catalog = i18nCatalog("LinearAdvanceSettingPlugin")

class LinearAdvanceSettingPlugin(Extension):
    def __init__(self):
        super().__init__()

        self._application = Application.getInstance()

        self._i18n_catalog = None
        self._advance_control_enabled_setting_key = "linear_advance_control_enabled"
        self._advance_control_enabled_setting_dict = {
            "label": "Enable Linear Advance Factor Control",
            "description": "Enables adjusting the Linear Advance Factor.",
            "type": "bool",
            "default_value": False,
            "resolve": "any(extruderValues('linear_advance_control_enabled'))",
            "settable_per_mesh": False,
            "settable_per_extruder": True,
            "settable_per_meshgroup": False
        }
        self._advance_control_print_setting_key = "linear_advance_factor_print"
        self._advance_control_print_setting_dict = {
            "label": "Base Linear Advance Factor",
            "description": "The Linear Advance Factor (mm of filament compression needed per 1mm/s extrusion speed) with which printing happens.",
            "unit": "mm/mm⋅s",
            "type": "float",
            "minimum_value": 0.0,
            "maximum_value_warning": 2.0,
            "default_value": 0,
            "enabled": "resolveOrValue('linear_advance_control_enabled')",
            "settable_per_mesh": False,
            "settable_per_extruder": True,
            "settable_per_meshgroup": False
        }
        self._advance_control_infill_setting_key = "linear_advance_factor_infill"
        self._advance_control_infill_setting_dict = {
            "label": "Infill Linear Advance Factor",
            "description": "The Linear Advance Factor with which infill is printed.",
            "unit": "mm/mm⋅s",
            "type": "float",
            "minimum_value": 0.0,
            "maximum_value_warning": 2.0,
            "default_value": 0,
            "value": "linear_advance_factor_print",
            "enabled": "resolveOrValue('linear_advance_control_enabled') and infill_sparse_density > 0",
            "limit_to_extruder": "infill_extruder_nr",
            "settable_per_mesh": False,
            "settable_per_extruder": True,
            "settable_per_meshgroup": False
        }
        self._advance_control_wall_setting_key = "linear_advance_factor_wall"
        self._advance_control_wall_setting_dict = {
            "label": "Wall Linear Advance Factor",
            "description": "The Linear Advance Factor with which the walls are printed.",
            "unit": "mm/mm⋅s",
            "type": "float",
            "minimum_value": 0.0,
            "maximum_value_warning": 2.0,
            "default_value": 0,
            "value": "linear_advance_factor_print",
            "enabled": "resolveOrValue('linear_advance_control_enabled')",
            "settable_per_mesh": False,
            "settable_per_extruder": True,
            "settable_per_meshgroup": False
        }
        self._advance_control_wall_0_setting_key = "linear_advance_factor_wall_0"
        self._advance_control_wall_0_setting_dict = {
            "label": "Outer Wall Linear Advance Factor",
            "description": "The Linear Advance Factor with which the outermost walls are printed.",
            "unit": "mm/mm⋅s",
            "type": "float",
            "minimum_value": 0.0,
            "maximum_value_warning": 2.0,
            "default_value": 0,
            "value": "linear_advance_factor_wall",
            "enabled": "resolveOrValue('linear_advance_control_enabled')",
            "limit_to_extruder": "wall_0_extruder_nr",
            "settable_per_mesh": False,
            "settable_per_extruder": True,
            "settable_per_meshgroup": False
        }
        self._advance_control_wall_x_setting_key = "linear_advance_factor_wall_x"
        self._advance_control_wall_x_setting_dict = {
            "label": "Inner Wall Linear Advance Factor",
            "description": "The Linear Advance Factor with which all inner walls are printed.",
            "unit": "mm/mm⋅s",
            "type": "float",
            "minimum_value": 0.0,
            "maximum_value_warning": 2.0,
            "default_value": 0,
            "value": "linear_advance_factor_wall",
            "enabled": "resolveOrValue('linear_advance_control_enabled')",
            "limit_to_extruder": "wall_x_extruder_nr",
            "settable_per_mesh": False,
            "settable_per_extruder": True,
            "settable_per_meshgroup": False
        }
        self._advance_control_topbottom_setting_key = "linear_advance_factor_topbottom"
        self._advance_control_topbottom_setting_dict = {
            "label": "Top/Bottom Skin Linear Advance Factor",
            "description": "The Linear Advance Factor with which top/bottom skin layers are printed.",
            "unit": "mm/mm⋅s",
            "type": "float",
            "minimum_value": 0.0,
            "maximum_value_warning": 2.0,
            "default_value": 0,
            "value": "linear_advance_factor_print",
            "enabled": "resolveOrValue('linear_advance_control_enabled')",
            "limit_to_extruder": "top_bottom_extruder_nr",
            "settable_per_mesh": False,
            "settable_per_extruder": True,
            "settable_per_meshgroup": False
        }
        self._advance_control_support_setting_key = "linear_advance_factor_support"
        self._advance_control_support_setting_dict = {
            "label": "Support Linear Advance Factor",
            "description": "The Linear Advance Factor with which the support structure is printed.",
            "unit": "mm/mm⋅s",
            "type": "float",
            "minimum_value": 0.0,
            "maximum_value_warning": 2.0,
            "default_value": 0,
            "value": "linear_advance_factor_print",
            "enabled": "resolveOrValue('linear_advance_control_enabled') and (support_enable or support_tree_enable)",
            "limit_to_extruder": "support_extruder_nr",
            "settable_per_mesh": False,
            "settable_per_extruder": True,
            "settable_per_meshgroup": False
        }
        self._advance_control_support_interface_setting_key = "linear_advance_factor_support_interface"
        self._advance_control_support_interface_setting_dict = {
            "label": "Support Interface Linear Advance Factor",
            "description": "The Linear Advance Factor with which the roofs and floors of support are printed.",
            "unit": "mm/mm⋅s",
            "type": "float",
            "minimum_value": 0.0,
            "maximum_value_warning": 2.0,
            "default_value": 0,
            "value": "linear_advance_factor_support",
            "enabled": "resolveOrValue('linear_advance_control_enabled') and support_interface_enable and (support_enable or support_tree_enable)",
            "limit_to_extruder": "support_interface_extruder_nr",
            "settable_per_mesh": False,
            "settable_per_extruder": True,
            "settable_per_meshgroup": False
        }
        self._advance_control_prime_tower_setting_key = "linear_advance_factor_prime_tower"
        self._advance_control_prime_tower_setting_dict = {
            "label": "Prime Tower Linear Advance Factor",
            "description": "The Linear Advance Factor with which the prime tower is printed.",
            "unit": "mm/mm⋅s",
            "type": "float",
            "minimum_value": 0.0,
            "maximum_value_warning": 2.0,
            "default_value": 0,
            "value": "linear_advance_factor_print",
            "enabled": "resolveOrValue('prime_tower_enable') and resolveOrValue('linear_advance_control_enabled')",
            "settable_per_mesh": False,
            "settable_per_extruder": True,
            "settable_per_meshgroup": False
        }
        self._advance_control_skirt_brim_setting_key = "linear_advance_factor_skirt_brim"
        self._advance_control_skirt_brim_setting_dict = {
            "label": "Skirt/Brim Linear Advance Factor",
            "description": "The Linear Advance Factor with which the skirt and brim are printed.",
            "unit": "mm/mm⋅s",
            "type": "float",
            "minimum_value": 0.0,
            "maximum_value_warning": 2.0,
            "default_value": 0,
            "value": "linear_advance_factor_print",
            "enabled": "resolveOrValue('linear_advance_control_enabled') and (resolveOrValue('adhesion_type') == 'skirt' or resolveOrValue('adhesion_type') == 'brim' or resolveOrValue('draft_shield_enabled') or resolveOrValue('ooze_shield_enabled'))",
            "limit_to_extruder": "adhesion_extruder_nr",
            "settable_per_mesh": False,
            "settable_per_extruder": True,
            "settable_per_meshgroup": False
        }

        ContainerRegistry.getInstance().containerLoadComplete.connect(self._onContainerLoadComplete)
        self._application.getOutputDeviceManager().writeStarted.connect(self._filterGcode)

    def _onContainerLoadComplete(self, container_id):
        container = ContainerRegistry.getInstance().findContainers(id = container_id)[0]
        if not isinstance(container, DefinitionContainer):
            # skip containers that are not definitions
            return
        if container.getMetaDataEntry("type") == "extruder":
            # skip extruder definitions
            return

        material_category = container.findDefinitions(key="material")
        if material_category:
            # Enable Linear Advance Factor Control
            advance_control_enabled_setting = container.findDefinitions(key=self._advance_control_enabled_setting_key)
            if not advance_control_enabled_setting:
                self._insertSettingIntoContainer(container, material_category, self._advance_control_enabled_setting_key, self._advance_control_enabled_setting_dict)

            # Base Linear Advance Factor
            advance_control_print_setting = container.findDefinitions(key=self._advance_control_print_setting_key)
            if not advance_control_print_setting:
                advance_control_print_setting = self._insertSettingIntoContainer(container, material_category, self._advance_control_print_setting_key, self._advance_control_print_setting_dict)
            
            # Infill Linear Advance Factor
            advance_control_infill_setting = container.findDefinitions(key=self._advance_control_infill_setting_key)
            if not advance_control_infill_setting:
                self._insertSettingIntoContainer(container, advance_control_print_setting, self._advance_control_infill_setting_key, self._advance_control_infill_setting_dict)
            
            # Wall Linear Advance Factor
            advance_control_wall_setting = container.findDefinitions(key=self._advance_control_wall_setting_key)
            if not advance_control_wall_setting:
                advance_control_wall_setting = self._insertSettingIntoContainer(container, advance_control_print_setting, self._advance_control_wall_setting_key, self._advance_control_wall_setting_dict)
            
            # Outer Wall Linear Advance Factor
            advance_control_wall_0_setting = container.findDefinitions(key=self._advance_control_wall_0_setting_key)
            if not advance_control_wall_0_setting:
                self._insertSettingIntoContainer(container, advance_control_wall_setting, self._advance_control_wall_0_setting_key, self._advance_control_wall_0_setting_dict)
            
            # Inner Wall Linear Advance Factor
            advance_control_wall_x_setting = container.findDefinitions(key=self._advance_control_wall_x_setting_key)
            if not advance_control_wall_x_setting:
                self._insertSettingIntoContainer(container, advance_control_wall_setting, self._advance_control_wall_x_setting_key, self._advance_control_wall_x_setting_dict)
            
            # Top/Bottom Skin Linear Advance Factor
            advance_control_topbottom_setting = container.findDefinitions(key=self._advance_control_topbottom_setting_key)
            if not advance_control_topbottom_setting:
                self._insertSettingIntoContainer(container, advance_control_print_setting, self._advance_control_topbottom_setting_key, self._advance_control_topbottom_setting_dict)

            # Support Linear Advance Factor
            advance_control_support_setting = container.findDefinitions(key=self._advance_control_support_setting_key)
            if not advance_control_support_setting:
                advance_control_support_setting = self._insertSettingIntoContainer(container, advance_control_print_setting, self._advance_control_support_setting_key, self._advance_control_support_setting_dict)
                
            # Support Interface Linear Advance Factor
            advance_control_support_interface_setting = container.findDefinitions(key=self._advance_control_support_interface_setting_key)
            if not advance_control_support_interface_setting:
                self._insertSettingIntoContainer(container, advance_control_support_setting, self._advance_control_support_interface_setting_key, self._advance_control_support_interface_setting_dict)
                
            # Prime Tower Linear Advance Factor
            advance_control_prime_tower_setting = container.findDefinitions(key=self._advance_control_prime_tower_setting_key)
            if not advance_control_prime_tower_setting:
                self._insertSettingIntoContainer(container, advance_control_print_setting, self._advance_control_prime_tower_setting_key, self._advance_control_prime_tower_setting_dict)
                
            # Skirt/Brim Linear Advance Factor
            advance_control_skirt_brim_setting = container.findDefinitions(key=self._advance_control_skirt_brim_setting_key)
            if not advance_control_skirt_brim_setting:
                self._insertSettingIntoContainer(container, advance_control_print_setting, self._advance_control_skirt_brim_setting_key, self._advance_control_skirt_brim_setting_dict)

    def _insertSettingIntoContainer(self, container, category, setting_key: str, setting_dict: dict) -> SettingDefinition:
        if not isinstance(category, SettingDefinition):
            if len(category) > 0:
                category = category[0]
                Logger.log("d", "Insertion: rewrited, %s", category.key)

        Logger.log("d", "Insertion: %s . %s", category.key, setting_key)

        setting_definition = SettingDefinition(setting_key, container, category, self._i18n_catalog)
        setting_definition.deserialize(setting_dict)

        # add the setting to the already existing material settingdefinition
        # private member access is naughty, but the alternative is to serialise, nix and deserialise the whole thing,
        # which breaks stuff
        category._children.append(setting_definition)
        container._definition_cache[setting_key] = setting_definition
        container._updateRelations(setting_definition)

        return setting_definition

    def _getFirstSubstringBetween(self, input_data: str, start: str, end: str = None) -> str:
        start_index = input_data.find(start)
        if start_index == -1:
            return None
        start_index += len(start)
        if not end:
            return input_data[start_index:]
        end_index = input_data.find(end, start_index)
        if end_index == -1:
            return input_data[start_index:]
        return input_data[start_index:end_index]

    def _filterGcode(self, output_device):
        scene = self._application.getController().getScene()

        global_container_stack = self._application.getGlobalContainerStack()
        used_extruder_stacks = self._application.getExtruderManager().getUsedExtruderStacks()
        if not global_container_stack or not used_extruder_stacks:
            return

        # check if linear advance settings are already applied
        start_gcode = global_container_stack.getProperty("machine_start_gcode", "value")
        if "M900 " in start_gcode:
            Logger.log("d", "Start GCode already includes a linear advance snippet")
            return

        # get setting from Cura
        some_factors_set = False
        for extruder_stack in used_extruder_stacks:
            linear_advance_factor = extruder_stack.getProperty(self._advance_control_print_setting_key, "value")
            if linear_advance_factor != 0:
                some_factors_set = True
        if not some_factors_set:
            Logger.log("d", "No used extruders specify a linear advance factor")
            return

        gcode_dict = getattr(scene, "gcode_dict", {})
        if not gcode_dict: # this also checks for an empty dict
            Logger.log("w", "Scene has no gcode to process")
            return

        gcode_type_to_setting_dict = {
            "WALL-OUTER": self._advance_control_wall_0_setting_key,
            "WALL-INNER": self._advance_control_wall_x_setting_key,
            "SKIN": self._advance_control_topbottom_setting_key,
            "SUPPORT": self._advance_control_support_setting_key,
            "SUPPORT-INTERFACE": self._advance_control_support_interface_setting_key,
            "SKIRT": self._advance_control_skirt_brim_setting_key,
            "FILL": self._advance_control_infill_setting_key,
            "PRIME-TOWER": self._advance_control_prime_tower_setting_key
        }

        dict_changed = False

        for plate_id in gcode_dict:
            gcode_list = gcode_dict[plate_id]
            if len(gcode_list) < 2:
                Logger.log("w", "Plate %s does not contain any layers", plate_id)
                continue

            if ";LINEARADVANCEPROCESSED\n" not in gcode_list[0]:
                for layer_nr, layer in enumerate(gcode_list):
                    lines = layer.split("\n")
                    lines_changed = False
                    for line_nr, line in enumerate(lines):
                        if line.startswith(";TYPE:"):
                            # Changed line type
                            line_type = self._getFirstSubstringBetween(line, ":")
                            settings_key = gcode_type_to_setting_dict[line_type]

                            for extruder_stack in used_extruder_stacks:
                                linear_advance_factor = extruder_stack.getProperty(settings_key, "value")
                                if linear_advance_factor != 0:
                                    extruder_nr = extruder_stack.getProperty("extruder_nr", "value")
                                    lines.insert(line_nr + 1, "M900 K%f T%d ;added by LinearAdvanceSettingPlugin" % (linear_advance_factor, extruder_nr))
                                    lines_changed = True
                    if lines_changed:
                        gcode_list[layer_nr] = "\n".join(lines)
                        dict_changed = True

                gcode_list[0] += ";LINEARADVANCEPROCESSED\n"
                gcode_dict[plate_id] = gcode_list
                
            else:
                Logger.log("d", "Plate %s has already been processed", plate_id)
                continue

        if dict_changed:
            setattr(scene, "gcode_dict", gcode_dict)