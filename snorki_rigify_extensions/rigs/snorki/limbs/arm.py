# SPDX-License-Identifier: GPL-2.0-or-later

import bpy

from ......rigs.limbs.arm import Rig as ArmRig
from ......utils.switch_parent import SwitchParentBuilder

from ..utils import get_parent_list, set_parent_list, resolve_parent_bones


# ---------------------------------------------------------------------------
# Operators
# ---------------------------------------------------------------------------

class SNORKI_OT_arm_parent_add(bpy.types.Operator):
    """Add all other selected pose bones as extra IK hand parents"""
    bl_idname  = "snorki_rigify.arm_parent_add"
    bl_label   = "Add Selected Bone as IK Parent"
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
        lst = get_parent_list(params, 'extra_ik_parents')

        changed = False
        for name in selected:
            if name not in lst:
                lst.append(name)
                changed = True

        if changed:
            set_parent_list(params, lst, 'extra_ik_parents')
        return {'FINISHED'}


class SNORKI_OT_arm_parent_remove(bpy.types.Operator):
    """Remove this entry from the IK parent list"""
    bl_idname  = "snorki_rigify.arm_parent_remove"
    bl_label   = "Remove IK Parent"
    bl_options = {'UNDO', 'INTERNAL'}

    index: bpy.props.IntProperty()

    def execute(self, context):
        pb = context.active_pose_bone
        if not pb:
            return {'CANCELLED'}
        lst = get_parent_list(pb.rigify_parameters, 'extra_ik_parents')
        if 0 <= self.index < len(lst):
            lst.pop(self.index)
            set_parent_list(pb.rigify_parameters, lst, 'extra_ik_parents')
        return {'FINISHED'}


# ---------------------------------------------------------------------------
# Rig subclass — registered as snorki.limbs.arm
# ---------------------------------------------------------------------------

class Rig(ArmRig):
    """
    Human arm rig with extra switchable IK hand parents.
    Identical to limbs.arm with an added parent picker in the UI.
    """

    def build_ik_parent_switch(self, pbuilder: SwitchParentBuilder):
        self.register_switch_parents(pbuilder)

        ctrl = self.bones.ctrl

        def master(): return self.bones.ctrl.master
        def controls(): return [ctrl.master] + self.get_all_ik_controls()

        extra = resolve_parent_bones(
            self.obj.data.edit_bones,
            get_parent_list(self.params, 'extra_ik_parents')
        )

        pbuilder.build_child(
            self, ctrl.ik, prop_bone=master, select_parent='root',
            prop_id='IK_parent', prop_name='IK Parent', controls=controls,
            extra_parents=extra,
        )

        pbuilder.build_child(
            self, ctrl.ik_pole, prop_bone=master, extra_parents=self.get_ik_pole_parents,
            prop_id='pole_parent', prop_name='Pole Parent', controls=controls,
            no_fix_rotation=True, no_fix_scale=True,
        )

    # ----------------------------------------------------------- parameters

    @classmethod
    def add_parameters(cls, params):
        super().add_parameters(params)

        params.extra_ik_parents = bpy.props.StringProperty(
            name="Extra IK Parents",
            default="",
            description="JSON list of extra IK hand parent bone names"
        )

    @classmethod
    def parameters_ui(cls, layout, params):
        super().parameters_ui(layout, params, end='Hand')

        layout.separator()
        layout.label(text="Extra IK Hand Parents:")
        box = layout.box()

        lst = get_parent_list(params, 'extra_ik_parents')
        if not lst:
            box.label(text="No extra parents.", icon='INFO')
        else:
            for i, name in enumerate(lst):
                row = box.row(align=True)
                row.label(text=name, icon='BONE_DATA')
                op = row.operator("snorki_rigify.arm_parent_remove", text="", icon='X')
                op.index = i

        box.operator("snorki_rigify.arm_parent_add",
                     text="Add Selected Bone as IK Parent", icon='EYEDROPPER')
        box.label(text="Select upper_arm bone + target, then click Add.", icon='INFO')


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

classes = (
    SNORKI_OT_arm_parent_add,
    SNORKI_OT_arm_parent_remove,
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

def create_sample(obj, limb=False):
    from ......rigs.limbs.arm import create_sample as arm_sample
    bones = arm_sample(obj, limb)
    bpy.ops.object.mode_set(mode='OBJECT')
    for bone_name in bones.values():
        pb = obj.pose.bones.get(bone_name)
        if pb and pb.rigify_type in ('limbs.arm', 'limbs.super_limb'):
            pb.rigify_type = 'snorki.limbs.arm'
            break
    bpy.ops.object.mode_set(mode='EDIT')
    return bones
