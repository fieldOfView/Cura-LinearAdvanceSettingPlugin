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
        self._setting_key = "material_linear_advance_factor"
        self._setting_dict = {
            "label": "Linear Advance Factor",
            "description": "Sets the advance extrusion factors for Linear Advance. Note that unless this setting is used in a start gcode snippet, it has no effect!",
            "type": "float",
            "default_value": 1,
            "minimum_value": "0.001",
            "minimum_value_warning": "0.1",
            "maximum_value_warning": "2.0",
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
        linear_advance_setting = container.findDefinitions(key=self._setting_key)
        if material_category and not linear_advance_setting:
            # this machine doesn't have a Linear Advance setting yet
            material_category = material_category[0]
            linear_advance_definition = SettingDefinition(self._setting_key, container, material_category, self._i18n_catalog)
            linear_advance_definition.deserialize(self._setting_dict)

            # add the setting to the already existing meterial settingdefinition
            # private member access is naughty, but the alternative is to serialise, nix and deserialise the whole thing,
            # which breaks stuff
            material_category._children.append(linear_advance_definition)
            container._definition_cache[self._setting_key] = linear_advance_definition
            container._updateRelations(linear_advance_definition)

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
            linear_advance_factor = extruder_stack.getProperty(self._setting_key, "value")
            if linear_advance_factor != 1:
                some_factors_set = True
        if not some_factors_set:
            Logger.log("d", "No used extruders specify a linear advance factor")
            return

        gcode_dict = getattr(scene, "gcode_dict", {})
        if not gcode_dict: # this also checks for an empty dict
            Logger.log("w", "Scene has no gcode to process")
            return

        dict_changed = False

        for plate_id in gcode_dict:
            gcode_list = gcode_dict[plate_id]
            if len(gcode_list) < 2:
                Logger.log("w", "Plate %s does not contain any layers", plate_id)
                continue

            if ";LINEARADVANCEPROCESSED\n" not in gcode_list[0]:
                for extruder_stack in used_extruder_stacks:
                    linear_advance_factor = extruder_stack.getProperty(self._setting_key, "value")
                    extruder_nr = extruder_stack.getProperty("extruder_nr", "value")
                    gcode_list[1] = ("M900 K%f T%d;added by LinearAdvanceSettingPlugin\n" % (linear_advance_factor, extruder_nr)) + gcode_list[1]
                gcode_list[0] += ";LINEARADVANCEPROCESSED\n"
                gcode_dict[plate_id] = gcode_list
                dict_changed = True
            else:
                Logger.log("d", "Plate %s has already been processed", plate_id)
                continue

        if dict_changed:
            setattr(scene, "gcode_dict", gcode_dict)