# SPDX-License-Identifier: GPL-2.0-or-later

import bpy

from .....base_rig import BaseRig
from .....utils.naming import strip_org, make_deformer_name
from .....utils.widgets import layout_widget_dropdown, create_registered_widget
from .....utils.switch_parent import SwitchParentBuilder

from .utils import get_parent_list, set_parent_list, resolve_parent_bones


# ---------------------------------------------------------------------------
# Operators
# ---------------------------------------------------------------------------

class SNORKI_OT_parent_add(bpy.types.Operator):
    """Add all other selected pose bones as switchable parents"""
    bl_idname  = "snorki_rigify.parent_add"
    bl_label   = "Add Selected Bone as Parent"
    bl_options = {'UNDO', 'INTERNAL'}

    def execute(self, context):
        pb = context.active_pose_bone
        if not pb:
            self.report({'WARNING'}, "No active pose bone.")
            return {'CANCELLED'}

        selected = [b.name for b in context.selected_pose_bones if b != pb]
        if not selected:
            self.report({'WARNING'}, "Select another bone to add as parent.")
            return {'CANCELLED'}

        params = pb.rigify_parameters
        lst = get_parent_list(params)

        changed = False
        for name in selected:
            if name not in lst:
                lst.append(name)
                changed = True

        if changed:
            set_parent_list(params, lst)
        return {'FINISHED'}


class SNORKI_OT_parent_remove(bpy.types.Operator):
    """Remove this entry from the parent list"""
    bl_idname  = "snorki_rigify.parent_remove"
    bl_label   = "Remove Parent"
    bl_options = {'UNDO', 'INTERNAL'}

    index: bpy.props.IntProperty()

    def execute(self, context):
        pb = context.active_pose_bone
        if not pb:
            return {'CANCELLED'}
        lst = get_parent_list(pb.rigify_parameters)
        if 0 <= self.index < len(lst):
            lst.pop(self.index)
            set_parent_list(pb.rigify_parameters, lst)
        return {'FINISHED'}


# ---------------------------------------------------------------------------
# Rig class
# ---------------------------------------------------------------------------

class Rig(BaseRig):
    """
    Prop bone with ORG / DEF / CTRL stack and switchable parent.
    The control bone gets the same name as the metarig bone.
    Extra parents are picked interactively in pose mode.
    """

    class CtrlBones(BaseRig.CtrlBones):
        master: str

    bones: BaseRig.ToplevelBones[str, 'Rig.CtrlBones', BaseRig.MchBones, str]

    def find_org_bones(self, pose_bone) -> str:
        return pose_bone.name

    def initialize(self):
        self.org_name = strip_org(self.bones.org)
        self.prop_make_deform = self.params.prop_make_deform

    # ---------------------------------------------------------------- bones

    def generate_bones(self):
        org = self.bones.org

        self.bones.ctrl.master = self.copy_bone(org, self.org_name, parent=True)

        if self.prop_make_deform:
            self.bones.deform = self.copy_bone(
                org, make_deformer_name(self.org_name), bbone=True)

        self._build_parent_switch(self.bones.ctrl.master)

    def _build_parent_switch(self, ctrl_name: str):
        pbuilder = SwitchParentBuilder(self.generator)

        org_parent = self.get_bone_parent(self.bones.org)
        extra = ([org_parent] if org_parent else []) + \
                resolve_parent_bones(self.obj.data.edit_bones, get_parent_list(self.params))

        pbuilder.build_child(
            self, ctrl_name,
            context_rig=self.rigify_parent, allow_self=True,
            prop_name=f"Parent ({ctrl_name})",
            extra_parents=extra,
            select_parent=org_parent,
            controls=lambda: self.bones.ctrl.flatten(),
        )

    # --------------------------------------------------------------- parenting

    def parent_bones(self):
        self.set_bone_parent(self.bones.org, self.bones.ctrl.master)
        if self.prop_make_deform:
            self.set_bone_parent(self.bones.deform, self.bones.org)

    # ------------------------------------------------------------- configure

    def configure_bones(self):
        self.copy_bone_properties(self.bones.org, self.bones.ctrl.master)

    # --------------------------------------------------------------- rig

    def rig_bones(self):
        self.make_constraint(self.bones.org, 'COPY_TRANSFORMS',
                             self.bones.ctrl.master, insert_index=0)

    # -------------------------------------------------------------- widgets

    def generate_widgets(self):
        create_registered_widget(self.obj, self.bones.ctrl.master, self.params.widget_type)

    # ----------------------------------------------------------- parameters

    @classmethod
    def add_parameters(cls, params):
        params.prop_make_deform = bpy.props.BoolProperty(
            name="Deform",
            default=True,
            description="Create a deform bone for the prop"
        )
        params.widget_type = bpy.props.StringProperty(
            name="Widget Type",
            default='cube',
            description="Choose the widget to create for the control bone"
        )
        params.extra_parents = bpy.props.StringProperty(
            name="Extra Parents",
            default="",
            description="JSON list of extra switchable parent bone names"
        )

    @classmethod
    def parameters_ui(cls, layout, params):
        layout.prop(params, "prop_make_deform")
        layout.separator()
        layout_widget_dropdown(layout, params, "widget_type")
        layout.separator()

        layout.label(text="Extra Parent Bones:")
        box = layout.box()

        lst = get_parent_list(params)
        if not lst:
            box.label(text="No extra parents.", icon='INFO')
        else:
            for i, name in enumerate(lst):
                row = box.row(align=True)
                row.label(text=name, icon='BONE_DATA')
                op = row.operator("snorki_rigify.parent_remove", text="", icon='X')
                op.index = i

        box.operator("snorki_rigify.parent_add", icon='EYEDROPPER')
        box.label(text="Select this bone + target bone, then click Add.", icon='INFO')
        layout.label(text="'None' and 'root' are always included.", icon='INFO')


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

classes = (
    SNORKI_OT_parent_add,
    SNORKI_OT_parent_remove,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


# ---------------------------------------------------------------------------
# Sample
# ---------------------------------------------------------------------------

def create_sample(obj):
    bpy.ops.object.mode_set(mode='EDIT')
    arm = obj.data
    bones = {}

    bone = arm.edit_bones.new('prop')
    bone.head[:] = 0.0000, 0.0000, 1.0000
    bone.tail[:] = 0.0000, 0.0000, 1.2000
    bone.roll = 0.0000
    bone.use_connect = False
    bones['prop'] = bone.name

    bpy.ops.object.mode_set(mode='OBJECT')
    pbone = obj.pose.bones[bones['prop']]
    pbone.rigify_type = 'snorki.switchable_parent'
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'

    bpy.ops.object.mode_set(mode='EDIT')
    for bone in arm.edit_bones:
        bone.select = False
        bone.select_head = False
        bone.select_tail = False
    for b in bones:
        bone = arm.edit_bones[bones[b]]
        bone.select = True
        bone.select_head = True
        bone.select_tail = True
        arm.edit_bones.active = bone
        if bcoll := arm.collections.active:
            bcoll.assign(bone)

    return bones
