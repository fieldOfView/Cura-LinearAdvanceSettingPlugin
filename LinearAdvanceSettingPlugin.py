# Copyright (c) 2018 fieldOfView
# The LinearAdvanceSettingPlugin is released under the terms of the AGPLv3 or higher.

from UM.Extension import Extension
from UM.Application import Application
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
            "default_value": 0,
            "settable_per_mesh": False,
            "settable_per_extruder": False,
            "settable_per_meshgroup": False
        }

        ContainerRegistry.getInstance().containerLoadComplete.connect(self._onContainerLoadComplete)


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
