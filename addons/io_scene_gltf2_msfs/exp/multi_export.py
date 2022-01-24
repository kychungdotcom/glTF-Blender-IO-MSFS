# Copyright 2021-2022 The glTF-Blender-IO-MSFS authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import re
import bpy
from bpy_extras.io_utils import ExportHelper


# Objects
class MultiExportLOD(bpy.types.PropertyGroup):
    object: bpy.props.PointerProperty(name="", type=bpy.types.Object)
    enabled: bpy.props.BoolProperty(name="", default=False)

    lod_value: bpy.props.IntProperty(name="", default=0, min=0)  # TODO: add max
    flatten_on_export: bpy.props.BoolProperty(name="", default=False)
    keep_instances: bpy.props.BoolProperty(name="", default=False)
    file_name: bpy.props.StringProperty(name="", default="")

class MultiExporterPropertyGroup(bpy.types.PropertyGroup):
    collection: bpy.props.StringProperty(name="", default="")
    expanded: bpy.props.BoolProperty(name="", default=True)
    lods: bpy.props.CollectionProperty(type=MultiExportLOD)
    folder_name: bpy.props.StringProperty(name="", default="")

# Presets
class MultiExporterPresetLayer(bpy.types.PropertyGroup):
    collection: bpy.props.PointerProperty(name="", type=bpy.types.Collection)

    enabled: bpy.props.BoolProperty(name="", default=False)

class MultiExporterPreset(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="", default="")
    folder_name: bpy.props.StringProperty(name="", default="")

    enabled: bpy.props.BoolProperty(name="", default=False)
    expanded: bpy.props.BoolProperty(name="", default=True)
    layers: bpy.props.CollectionProperty(type=MultiExporterPresetLayer)

class MSFSMultiExporterProperties:
    bpy.types.Scene.msfs_multi_exporter_current_tab = bpy.props.EnumProperty(items=
            (("OBJECTS", "Objects", ""),
            ("PRESETS", " Presets", "")),
    )

def update_lods():
    property_collection = bpy.context.scene.msfs_multi_exporter_collection

    # Remove deleted collections and objects
    for i, property_group in enumerate(property_collection):
        if property_group.collection:
            for j, lod in enumerate(property_group.lods):
                if not lod.object.name in bpy.context.scene.objects:
                    property_collection[i].lods.remove(j)
        else:
            property_collection.remove(i)

    # Search all objects in scene to find LOD groups
    lod_groups = {}
    for obj in bpy.context.scene.objects:
        matches = re.findall("(?i)x\d_|_lod[0-9]+", obj.name) # If an object starts with xN_ or ends with _LODN, treat as an LOD
        if matches:
            filtered_string = obj.name
            for match in matches:
                filtered_string = filtered_string.replace(match, "")
            
            if filtered_string in lod_groups.keys():
                lod_groups[filtered_string].append(obj)
            else:
                lod_groups[filtered_string] = [obj]
        else:
            lod_groups[obj.name] = [obj] # If not in a LOD group, just create a "fake" group to add the object to

    # Add collection if not already in property group
    for _, (collection, objects) in enumerate(lod_groups.items()):
        if not collection in [property_group.collection for property_group in property_collection]:
            collection_prop_group = property_collection.add()
            collection_prop_group.collection = collection
            collection_prop_group.folder_name = collection
        else:
            for property_group in property_collection:
                if property_group.collection == collection:
                    collection_prop_group = property_group
                    break
        
        for obj in objects:
            # If the object is at the root level (no parent)
            if obj.parent is None:
                if not obj in [lod.object for lod in collection_prop_group.lods]:
                    obj_item = collection_prop_group.lods.add()
                    obj_item.object = obj
                    obj_item.file_name = obj.name

class MSFS_OT_ChangeTab(bpy.types.Operator):
    bl_idname = "msfs.multi_export_change_tab"
    bl_label = "Change tab"

    current_tab: bpy.types.Scene.msfs_multi_exporter_current_tab

    def execute(self, context):
        context.scene.msfs_multi_exporter_current_tab = self.current_tab
        return {"FINISHED"}

class MSFS_PT_MultiExporter(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = ""
    bl_parent_id = "FILE_PT_operator"
    bl_options = {'HIDE_HEADER'}

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator

        return context.scene.msfs_ExtAsoboProperties.enabled and operator.bl_idname == "EXPORT_SCENE_OT_multi_gltf"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        current_tab = context.scene.msfs_multi_exporter_current_tab

        row = layout.row(align=True)
        row.operator(MSFS_OT_ChangeTab.bl_idname, text="Objects",
                     depress=(current_tab == "OBJECTS")).current_tab = "OBJECTS"
        row.operator(MSFS_OT_ChangeTab.bl_idname, text="Presets",
                     depress=(current_tab == "PRESETS")).current_tab = "PRESETS"

class MultiExportGLTF2(bpy.types.Operator, ExportHelper):
    """Export scene as glTF 2.0 file"""
    bl_idname = 'export_scene.multi_gltf'
    bl_label = 'Multi-Export glTF 2.0'

    filename_ext = ''

    filter_glob: bpy.props.StringProperty(default='*.glb;*.gltf', options={'HIDDEN'})

    def invoke(self, context, event):
        update_lods() # Handle this here instead of using depsgraph_update_post so that we don't have much of a performance hit
        return ExportHelper.invoke(self, context, event)

    def execute(self, context):
        folder_path = os.path.dirname(self.filepath)

        property_collection = context.scene.msfs_multi_exporter_collection

        for collection in property_collection:
            export_path = os.path.join(folder_path, collection.folder_name)
            if not os.path.exists(export_path):
                export_path = os.mkdir(export_path)
            for lod in collection.lods:
                for obj in bpy.context.selected_objects:
                    obj.select_set(False)

                def select_recursive(obj):
                    obj.select_set(True)
                    for child in obj.children:
                        select_recursive(child)

                select_recursive(lod.object)

                if lod.enabled:
                    bpy.ops.export_scene.gltf(
                        export_format="GLTF_SEPARATE",
                        export_selected=True,
                        filepath=os.path.join(export_path, lod.file_name)
                    )

        return {"FINISHED"}

class MSFS_OT_RemovePreset(bpy.types.Operator):
    bl_idname = "msfs.multi_export_remove_preset"
    bl_label = "Remove preset"

    preset_index: bpy.props.IntProperty()

    def execute(self, context):
        presets = bpy.context.scene.msfs_multi_exporter_presets
        presets.remove(self.preset_index)

        return {"FINISHED"}

class MSFS_OT_AddPreset(bpy.types.Operator):
    bl_idname = "msfs.multi_export_add_preset"
    bl_label = "Add preset"

    def execute(self, context):
        presets = bpy.context.scene.msfs_multi_exporter_presets
        preset = presets.add()
        preset.name = f"Preset {len(presets)}"

        return {"FINISHED"}

class MSFS_OT_EditLayers(bpy.types.Operator):
    bl_idname = "msfs.multi_export_edit_layers"
    bl_label = "Edit layers"

    preset_index: bpy.props.IntProperty()

    def execute(self, context):
        return {"FINISHED"}

    def invoke(self, context, event):
        preset = bpy.context.scene.msfs_multi_exporter_presets[self.preset_index]

        for i, layer in enumerate(preset.layers):
            if not layer.collection in list(bpy.data.collections):
                preset.layers.remove(i)

        for collection in bpy.data.collections:
            if not collection in [layer.collection for layer in preset.layers]:
                layer = preset.layers.add()
                layer.collection = collection

        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout

        preset = bpy.context.scene.msfs_multi_exporter_presets[self.preset_index]

        for layer in preset.layers:
            box = layout.box()
            row = box.row()
            row.label(text=layer.collection.name)
            row.prop(layer, "enabled", text="Enabled")


class MSFS_PT_MultiExporterPresetsView(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = ""
    bl_parent_id = "FILE_PT_operator"
    bl_options = {'HIDE_HEADER'}

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator

        return context.scene.msfs_multi_exporter_current_tab == "PRESETS" and operator.bl_idname == "EXPORT_SCENE_OT_multi_gltf"

    def draw(self, context):
        layout = self.layout

        layout.operator(MSFS_OT_AddPreset.bl_idname, text="Add Preset")

        presets = bpy.context.scene.msfs_multi_exporter_presets
        for i, preset in enumerate(presets):
            row = layout.row()
            box = row.box()
            box.prop(preset, "expanded", text=preset.name,
                        icon="DOWNARROW_HLT" if preset.expanded else "RIGHTARROW", icon_only=True, emboss=False)

            if preset.expanded:
                box.prop(preset, "enabled", text="Enabled")
                box.prop(preset, "name", text="Name")
                box.prop(preset, "folder_name", text="Folder")

                box.operator(MSFS_OT_EditLayers.bl_idname, text="Edit Layers").preset_index = i

                box.operator(MSFS_OT_RemovePreset.bl_idname, text="Remove").preset_index = i

class MSFS_PT_MultiExporterObjectsView(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = ""
    bl_parent_id = "FILE_PT_operator"
    bl_options = {'HIDE_HEADER'}

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator

        return context.scene.msfs_multi_exporter_current_tab == "OBJECTS" and operator.bl_idname == "EXPORT_SCENE_OT_multi_gltf"

    def draw(self, context):
        layout = self.layout

        property_collection = context.scene.msfs_multi_exporter_collection
        total_lods = 0
        for prop in property_collection:
            total_lods += len(prop.lods)
        if total_lods == 0:
            box = layout.box()
            box.label(text="No LODs found in scene")
        else:
            for prop in property_collection:
                row = layout.row()
                if len(prop.lods) > 0:
                    box = row.box()
                    box.prop(prop, "expanded", text=prop.collection,
                             icon="DOWNARROW_HLT" if prop.expanded else "RIGHTARROW", icon_only=True, emboss=False)
                    if prop.expanded:
                        box.prop(prop, "folder_name", text="Folder")

                        col = box.column()
                        for lod in prop.lods:
                            row = col.row()
                            row.prop(lod, "enabled", text=lod.object.name)
                            subrow = row.column()
                            subrow.prop(lod, "lod_value", text="LOD Value")
                            subrow.prop(lod, "flatten_on_export", text="Flatten on Export")
                            subrow.prop(lod, "keep_instances", text="Keep Instances")
                            subrow.prop(lod, "file_name", text="Name")

def menu_func_export(self, context):
    self.layout.operator(MultiExportGLTF2.bl_idname, text='Multi-Export glTF 2.0 (.gltf)')

def register():
    bpy.types.Scene.msfs_multi_exporter_collection = bpy.props.CollectionProperty(type=MultiExporterPropertyGroup)
    bpy.types.Scene.msfs_multi_exporter_presets = bpy.props.CollectionProperty(type=MultiExporterPreset)

    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)

def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)

def register_panel():
    # Register the panel on demand, we need to be sure to only register it once
    # This is necessary because the panel is a child of the extensions panel,
    # which may not be registered when we try to register this extension
    try:
        bpy.utils.register_class(MSFS_PT_MultiExporter)
    except Exception:
        pass

    # If the glTF exporter is disabled, we need to unregister the extension panel
    # Just return a function to the exporter so it can unregister the panel
    return unregister_panel


def unregister_panel():
    try:
        bpy.utils.unregister_class(MSFS_PT_MultiExporter)
    except Exception:
        pass