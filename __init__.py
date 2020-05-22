# Copyright (c) 2014 mato.sus304(mato.sus304@gmail.com)
#
# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy

bl_info = {
    "name": "Apply Modifier With Shape Keys",
    "author": "mate.sus304, Taremin, SAM-tak",
    "version": (1, 2),
    "blender": (2, 80, 0),
    "location": "View3D > Object > Apply",
    "description": "Apply all modifiers to mesh object respecting shape keys.",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "website":"https://sites.google.com/site/matosus304blendernotes/home",
    "category": "Object"
}

######################################################

def clear_shape_keys(Name):
    obj = bpy.context.window.view_layer.objects.active
    if obj.data.shape_keys is None:
        return True
    obj.active_shape_key_index = len(obj.data.shape_keys.key_blocks) - 1
    while len(obj.data.shape_keys.key_blocks) > 1:
        if obj.data.shape_keys.key_blocks[obj.active_shape_key_index].name == Name:
            obj.active_shape_key_index = 0
        else:
            bpy.ops.object.shape_key_remove()
    bpy.ops.object.shape_key_remove()

def clone_object(Obj):
    tmp_obj = Obj.copy()
    tmp_obj.name = "applymodifier_tmp_%s"%(Obj.name)
    tmp_obj.data = tmp_obj.data.copy()
    tmp_obj.data.name = "applymodifier_tmp_%s"%(Obj.data.name)
    bpy.context.scene.collection.objects.link(tmp_obj)
    return tmp_obj

def delete_object(Obj):
    if Obj.data.users == 1:
        Obj.data.user_clear()
    for scn in bpy.data.scenes:
        try:
            scn.collection.objects.unlink(Obj)
        except:
            pass

def copy_attributes(a, b):
    keys = dir(a)
    for key in keys:
        if not key.startswith("_") \
        and not key.startswith("error_") \
        and key != "group" \
        and key != "strips" \
        and key != "is_valid" \
        and key != "rna_type" \
        and key != "bl_rna":
            try:
                setattr(b, key, getattr(a, key))
            except AttributeError:
                pass

######################################################

def apply_modifier(target_object=None, target_modifiers=None):
    if target_object is None:
        obj_src = bpy.context.window.view_layer.objects.active
    else:
        obj_src = target_object

    if target_modifiers is None:
        target_modifiers = []
        for x in obj_src.modifiers:
            if x.show_viewport:
                target_modifiers.append(x.name)
    
    if len(target_modifiers) == 0:
        # if object has no modifier then skip
        return True
    
    # make single user
    if obj_src.data.users != 1:
        obj_src.data = obj_src.data.copy()
    
    if obj_src.data.shape_keys is None:
        # if object has no shapekeys, just apply modifier
        for x in target_modifiers:
            try:
                bpy.ops.object.modifier_apply(modifier=x)
            except RuntimeError:
                pass
        return True
    
    obj_fin = clone_object(obj_src)
    
    bpy.context.window.view_layer.objects.active = obj_fin
    clear_shape_keys('Basis')
    
    for x in target_modifiers:
        try:
            bpy.ops.object.modifier_apply(modifier=x)
        except RuntimeError:
            pass
    
    flag_on_error = False
    list_skipped = []
    
    for i in range(1, len(obj_src.data.shape_keys.key_blocks)):
        tmp_name = obj_src.data.shape_keys.key_blocks[i].name
        obj_tmp = clone_object(obj_src)
        
        bpy.context.window.view_layer.objects.active = obj_tmp
        clear_shape_keys(tmp_name)
        
        for x in target_modifiers:
            try:
                bpy.ops.object.modifier_apply(modifier=x)
            except RuntimeError:
                pass
        
        obj_tmp.modifiers.clear()

        obj_tmp.select_set(True)
        bpy.context.window.view_layer.objects.active = obj_fin
        try:
            bpy.ops.object.join_shapes()
            obj_fin.data.shape_keys.key_blocks[-1].name = tmp_name
        except:
            flag_on_error = True
            list_skipped.append(tmp_name)
            
        delete_object(obj_tmp)
    
    if flag_on_error:
        def draw(self, context):
            self.layout.label("Vertex Count Disagreement! Some shapekeys skipped.")
            for s in list_skipped:
                self.layout.label(s)

        bpy.context.window_manager.popup_menu(draw, title="Error", icon='INFO')
        
        return False
    
    # Copy shape key drivers
    if obj_src.data.shape_keys.animation_data:
        for d1 in obj_src.data.shape_keys.animation_data.drivers:
            d2 = obj_fin.data.shape_keys.driver_add(d1.data_path)
            copy_attributes(d1, d2)
            copy_attributes(d1.driver, d2.driver)

            # Remove default modifiers, variables, etc.
            for m in d2.modifiers:
                d2.modifiers.remove(m)
            for v in d2.driver.variables:
                d2.driver.variables.remove(v)

            # Copy modifiers
            for m1 in d1.modifiers:
                m2 = d2.modifiers.new(type=m1.type)
                copy_attributes(m1, m2)

            # Copy variables
            for v1 in d1.driver.variables:
                v2 = d2.driver.variables.new()
                copy_attributes(v1, v2)
                for i in range(len(v1.targets)):
                    copy_attributes(v1.targets[i], v2.targets[i])

    tmp_name = obj_src.name
    tmp_data_name = obj_src.data.name
    obj_fin.name = tmp_name + '.tmp'
    
    obj_src.data = obj_fin.data
    obj_src.data.name = tmp_data_name
    
    for x in target_modifiers:
        obj_src.modifiers.remove(obj_src.modifiers[x])

    delete_object(obj_fin)
    bpy.context.window.view_layer.objects.active = obj_src


class OBJECT_OT_apply_all_modifiers(bpy.types.Operator):
    """Apply All Modifier to Selected Mesh Object"""
    bl_idname = "object.apply_all_modifiers"
    bl_label = "Apply All Modifiers With Shape Keys"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        targets = []
        for x in bpy.context.selected_objects:
            targets.append(x.name)
        
        bpy.ops.object.select_all(action='DESELECT')
        for x in targets:
            apply_modifier(target_object=bpy.data.objects[x])
        
        for x in targets:
            bpy.data.objects[x].select_set(True)
        
        return {'FINISHED'}


class OBJECT_OT_apply_selected_modifier(bpy.types.Operator):
    """Apply Selected Modifier to Active Mesh Object"""
    bl_idname = "object.apply_selected_modifier"
    bl_label = "Apply Selected Modifier With Shape Keys"
    bl_options = {'REGISTER', 'UNDO'}
    
    flags : bpy.props.BoolVectorProperty(name="Targets", description="Flags for applyee modifiers", size=32)

    modifier_names = None
    
    @classmethod
    def poll(cls, context):
        obj = context.object
        return obj and obj.type == 'MESH'
    
    def execute(self, context):
        obj = bpy.context.window.view_layer.objects.active
        
        if self.modifier_names and len(self.modifier_names) > 0:
            bpy.ops.object.select_all(action='DESELECT')
            str_targets = []
            for i in range(len(self.modifier_names)):
                if self.flags[i] and obj.modifiers[self.modifier_names[i]]:
                    str_targets.append(self.modifier_names[i])
            
            apply_modifier(target_object=obj, target_modifiers=str_targets)
            
            obj.select_set(True)
        else:
            self.modifier_names = tuple(i.name for i in obj.modifiers)
            self.flags = tuple(False for i in range(32))
        return {'FINISHED'}
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
    def draw(self, context):
        obj = context.object
        
        layout = self.layout
        col = layout.column()

        for i in range(len(self.modifier_names)):
            col.prop(self, "flags", text=self.modifier_names[i], index=i)


# Registration

def apply_modifier_buttons(self, context):
    self.layout.separator()
    self.layout.operator(
        OBJECT_OT_apply_all_modifiers.bl_idname,
        text="Apply All Modifiers With Shape Keys")
    self.layout.operator(
        OBJECT_OT_apply_selected_modifier.bl_idname,
        text="Apply Selected Modifier With Shape Keys")

def register():
    bpy.utils.register_class(OBJECT_OT_apply_all_modifiers)
    bpy.utils.register_class(OBJECT_OT_apply_selected_modifier)
    bpy.types.VIEW3D_MT_object_apply.append(apply_modifier_buttons)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_apply_all_modifiers)
    bpy.utils.unregister_class(OBJECT_OT_apply_selected_modifier)
    bpy.types.VIEW3D_MT_object_apply.remove(apply_modifier_buttons)

if __name__ == "__main__":
    register()
