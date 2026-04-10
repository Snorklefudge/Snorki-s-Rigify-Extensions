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

**Use case:** Props like weapons or tools — anything that needs to switch between hands or other attachment points.

https://github.com/user-attachments/assets/944031d0-651f-4718-8286-796200ce8f3e

---

### `snorki.limbs.arm`

An extended version of Rigify's built-in `limbs.arm` rig, identical in every way but with an extra **IK Hand parent picker** at the bottom of the parameters panel.

- All standard arm rig features (IK/FK, pole vector, tweak bones, wrist pivot, etc.)
- Extra IK hand parents are appended at the end of the parent list
- Parent list survives rig regeneration
- You can use this to parent one hand IK to another, just make sure not to have them set to each other at the same time, otherwise both will move erratically.

**Use case:** Characters that need to grab objects or surfaces — adds custom bones like `sword`, `box`, or character bones as valid IK hand parents.

https://github.com/user-attachments/assets/aa055975-a466-4046-97ee-3be13a2c5919

---

## Installation

1. Download the latest release zip from [Releases](../../releases/latest)
2. Open Blender and make sure the **Rigify** addon is enabled
3. Go to **Edit → Preferences → Add-ons → Rigify** (expand it)
4. Under **Feature Sets**, click **Install Feature Set from File**
5. Select the downloaded zip
6. Enable the feature set in the list

The rig types will appear in the **Rigify Type** dropdown on any pose bone.

<img width="543" height="523" alt="snorki_feature_set" src="https://github.com/user-attachments/assets/fc6d9782-471f-47ac-9928-17af6007a331" />

---

## Usage

### snorki.switchable_parent

1. In the metarig, select a bone and set its Rigify Type to `snorki.switchable_parent`
2. Choose a **Widget Type** from the dropdown
3. To add extra parents: in Pose Mode, **Shift-click** the target bone(s) alongside your prop bone (active), then click **Add Selected Bone as Parent**
4. Generate the rig — the Parent dropdown appears in the **Rig Main Properties** panel

<img width="572" height="356" alt="snorki_switchable_parent" src="https://github.com/user-attachments/assets/f8285ac4-a779-4c4a-80f4-d1fd6be9339d" />

### snorki.limbs.arm

1. Set your upper arm bone's Rigify Type to `snorki.limbs.arm` instead of `limbs.arm`
2. Scroll to the bottom of the parameters panel
3. Add extra IK parents the same way as above
4. Generate the rig — extra parents appear at the end of the **IK Parent** dropdown

<img width="572" height="586" alt="snorki_limbs_arm" src="https://github.com/user-attachments/assets/c02d9e0c-77f2-48c1-8577-c603fb7feb18" />

---

## Video Tutorial

[![Watch the tutorial](https://img.shields.io/badge/YouTube-Watch%20Tutorial-red?style=for-the-badge&logo=youtube)](https://youtube.com/PLACEHOLDER)

> Tutorial coming soon!

---
## Credits

Rig types developed with the help of [Claude](https://claude.ai) by Anthropic.
Based on the idea form: [tonydayo86](https://www.youtube.com/watch?v=-1MzxLW2sQw) on youtube

## Requirements

- Blender 5.0+
- Rigify addon enabled

## License

GNU GPL v2 — see [LICENSE](LICENSE)

