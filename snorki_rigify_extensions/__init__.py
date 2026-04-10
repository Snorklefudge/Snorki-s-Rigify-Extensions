# SPDX-License-Identifier: GPL-2.0-or-later

bl_info = {
    "name": "Snorki's Rigify Extensions",
    "author": "",
    "version": (1, 1, 0),
    "blender": (4, 0, 0),
    "description": "Adds snorki.switchable_parent and snorki.limbs.arm Rigify rig types",
    "category": "Rigging",
}

# Rigify reads this dict for the display name in preferences
rigify_info = {
    "name": "Snorki's Rigify Extensions",
    "author": "",
    "description": "Adds snorki.switchable_parent and snorki.limbs.arm Rigify rig types",
}


def register():
    from .rigs.snorki.switchable_parent import register as reg1
    from .rigs.snorki.limbs.arm import register as reg2
    reg1()
    reg2()


def unregister():
    from .rigs.snorki.switchable_parent import unregister as unreg1
    from .rigs.snorki.limbs.arm import unregister as unreg2
    unreg2()
    unreg1()
