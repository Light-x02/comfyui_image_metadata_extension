import json
from ..meta import MetaField
from ..formatters import calc_lora_hash

def _get_selection_list(input_data):
    try:
        d = input_data[0] if input_data and isinstance(input_data[0], dict) else {}
        raw = d.get("selection_data")
        s = raw[0] if isinstance(raw, list) else raw
        if isinstance(s, (bytes, bytearray)):
            s = s.decode("utf-8", "ignore")
        if isinstance(s, str):
            s = s.strip()
            return json.loads(s) if s else []
        if isinstance(s, list):
            return s
        return []
    except Exception:
        return []

def _names_from_selection(input_data):
    items = _get_selection_list(input_data)
    out = []
    for it in items:
        try:
            if it.get("on", True):
                name = str(it.get("lora", "")).strip()
                if name and name != "None":
                    out.append(name)
        except Exception:
            pass
    return out

def _strength_model_from_selection(input_data):
    items = _get_selection_list(input_data)
    out = []
    for it in items:
        try:
            if it.get("on", True):
                val = float(it.get("strength", 1.0))
                out.append(val)
        except Exception:
            pass
    return out

def _strength_clip_from_selection(input_data):
    items = _get_selection_list(input_data)
    out = []
    for it in items:
        try:
            if it.get("on", True):
                if "strength_clip" in it:
                    val = float(it.get("strength_clip", it.get("strength", 1.0)))
                else:
                    val = float(it.get("strength", 1.0))
                out.append(val)
        except Exception:
            pass
    return out

def _selector_lora_names(node_id, obj, prompt, extra_data, outputs, input_data):
    return _names_from_selection(input_data)

def _selector_lora_hashes(node_id, obj, prompt, extra_data, outputs, input_data):
    names = _names_from_selection(input_data)
    return [calc_lora_hash(n, input_data) for n in names]

def _selector_strength_model(node_id, obj, prompt, extra_data, outputs, input_data):
    return _strength_model_from_selection(input_data)

def _selector_strength_clip(node_id, obj, prompt, extra_data, outputs, input_data):
    return _strength_clip_from_selection(input_data)

def _selector_strength_clip_zeros(node_id, obj, prompt, extra_data, outputs, input_data):
    return [0.0] * len(_names_from_selection(input_data))

CAPTURE_FIELD_LIST = {
    "LocalLoraGallery": {
        MetaField.LORA_MODEL_NAME:     {"selector": _selector_lora_names},
        MetaField.LORA_MODEL_HASH:     {"selector": _selector_lora_hashes},
        MetaField.LORA_STRENGTH_MODEL: {"selector": _selector_strength_model},
        MetaField.LORA_STRENGTH_CLIP:  {"selector": _selector_strength_clip},
    },
    "LocalLoraGalleryModelOnly": {
        MetaField.LORA_MODEL_NAME:     {"selector": _selector_lora_names},
        MetaField.LORA_MODEL_HASH:     {"selector": _selector_lora_hashes},
        MetaField.LORA_STRENGTH_MODEL: {"selector": _selector_strength_model},
        MetaField.LORA_STRENGTH_CLIP:  {"selector": _selector_strength_clip_zeros},
    },
}
