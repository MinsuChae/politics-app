import json
import os

_data = None
_parties = None
_parties_by_slug = None

def _load_json():
    global _data, _parties, _parties_by_slug
    try:
        official_data = 'data/data.json'
        unofficial_data = 'data/sample_data.json'
        
        path = unofficial_data
        if os.path.exists(official_data):
            path = official_data

        with open(path, 'r', encoding='utf-8') as f:
                _data = json.load(f)
                
        _parties = _data.get("parties", [])
        _parties_by_slug = {party["slug"]: party for party in _parties}
    except Exception as e:
        pass

_load_json()

def get_all_candidates():
    out = []
    for slug, party in _parties_by_slug.items():
        for cand in party["candidates"]:
            entry = cand.copy()
            entry["party_slug"] = slug
            entry["party_name"] = party["name"]
            out.append(entry)
    return out

data = lambda: _data
parties = lambda: _parties
parties_by_slug = lambda: _parties_by_slug

def reload_data():
    _load_json()