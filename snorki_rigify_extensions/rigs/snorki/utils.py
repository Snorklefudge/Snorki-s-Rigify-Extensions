# SPDX-License-Identifier: GPL-2.0-or-later

"""Shared utilities for prop rig types."""

import json


def get_parent_list(params, attr='extra_parents'):
    """Read the JSON-backed parent bone list from a params attribute."""
    raw = (getattr(params, attr, None) or "").strip()
    if not raw:
        return []
    try:
        return json.loads(raw)
    except Exception:
        return []


def set_parent_list(params, lst, attr='extra_parents'):
    """Write the parent bone list back as JSON."""
    setattr(params, attr, json.dumps(lst))


def resolve_parent_bones(edit_bones, meta_names):
    """
    Resolve a list of metarig bone names to their generated ORG- equivalents.
    Returns a list of resolved bone names, skipping any that can't be found.
    """
    result = []
    for meta_name in meta_names:
        if not meta_name:
            continue
        org_name = f"ORG-{meta_name}"
        if org_name in edit_bones:
            result.append(org_name)
        elif meta_name in edit_bones:
            result.append(meta_name)
        else:
            print(f"[Snorki Rigify Extensions] Warning: bone '{meta_name}' not found, skipping.")
    return result
