# Copyright (c) 2023 Aldo Hoeben / fieldOfView
# The LinearAdvanceSettingPlugin is released under the terms of the AGPLv3 or higher.

from . import LinearAdvanceSettingPlugin


def getMetaData():
    return {}

def register(app):
    return {"extension": LinearAdvanceSettingPlugin.LinearAdvanceSettingPlugin()}
