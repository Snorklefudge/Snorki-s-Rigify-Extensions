# Snorki's Rigify Extensions

[![Ko-fi](https://img.shields.io/badge/Support%20me%20on-Ko--fi-FF5E5B?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ko-fi.com/snorklefudge)

A [Rigify](https://docs.blender.org/manual/en/latest/addons/rigging/rigify/index.html) feature set for Blender 5.0+ that adds custom rig types for flexible switchable parent setups on props and limbs.

---

## Rig Types

### `snorki.switchable_parent`

A full prop bone rig that generates an **ORG / DEF / MCH / CTRL** stack with a switchable parent dropdown in the rig's UI panel.

- Control bone gets the same name as the metarig bone
- Extra parent bones are added in Pose Mode
- Widget type picker with all standard Rigify widgets
- Optional deform bone
- Parent list survives rig regeneration
- If the bone is parented to other bones in the metarig, those parents are automatically included in the switch list

**Use case:** Props like weapons, bows, tools — anything that needs to switch between hands or other attachment points.

<!-- Screenshot: switchable_parent panel in Rigify Type -->
<!-- Screenshot: Parent dropdown in the generated rig UI -->

---

### `snorki.limbs.arm`

An extended version of Rigify's built-in `limbs.arm` rig, identical in every way but with an extra **IK Hand parent picker** at the bottom of the parameters panel.

- All standard arm rig features (IK/FK, pole vector, tweak bones, wrist pivot, etc.)
- Extra IK hand parents are appended at the end of the parent list
- Parent list survives rig regeneration
- You can use this to parent one hand IK to another, just make sure not to have them set to each other at the same time, otherwise both will move erratically.

**Use case:** Characters that need to grab objects or surfaces — adds custom bones like `bow`, `quiver`, or prop controls as valid IK hand parents.

<!-- Screenshot: snorki.limbs.arm extra parents panel -->
<!-- Screenshot: IK Parent dropdown with extra entries -->

---

## Installation

1. Download the latest release zip from [Releases](../../releases/latest)
2. Open Blender and make sure the **Rigify** addon is enabled
3. Go to **Edit → Preferences → Add-ons → Rigify** (expand it)
4. Under **Feature Sets**, click **Install Feature Set from File**
5. Select the downloaded zip
6. Enable the feature set in the list

The rig types will appear in the **Rigify Type** dropdown on any pose bone.

---

## Usage

### snorki.switchable_parent

1. In the metarig, select a bone and set its Rigify Type to `snorki.switchable_parent`
2. Choose a **Widget Type** from the dropdown
3. To add extra parents: in Pose Mode, **Shift-click** the target bone(s) alongside your prop bone (active), then click **Add Selected Bone as Parent**
4. Generate the rig — the Parent dropdown appears in the **Rig Main Properties** panel

### snorki.limbs.arm

1. Set your upper arm bone's Rigify Type to `snorki.limbs.arm` instead of `limbs.arm`
2. Scroll to the bottom of the parameters panel
3. Add extra IK parents the same way as above
4. Generate the rig — extra parents appear at the end of the **IK Parent** dropdown

---

## Video Tutorial

[![Watch the tutorial](https://img.shields.io/badge/YouTube-Watch%20Tutorial-red?style=for-the-badge&logo=youtube)](https://youtube.com/PLACEHOLDER)

> Tutorial coming soon!

---

## Requirements

- Blender 5.0+
- Rigify addon enabled

## License

GNU GPL v2 — see [LICENSE](LICENSE)
