import json

def csv_to_records(text: str) -> list[dict]:
    if not text.strip():
        return []
    lines = [line for line in text.splitlines() if line.strip()]
    if not lines:
        return []
    headers = [h.strip() for h in lines[0].split(',')]
    records = []
    for line in lines[1:]:
        values = [v.strip() for v in line.split(',')]
        records.append(dict(zip(headers, values)))
    return records

def parse_settings(lines: list[str]) -> dict:
    result = {}
    current_list_key = None
    
    def cast_val(val: str):
        v_lower = val.lower()
        if v_lower in ('true', 'yes'): return True
        if v_lower in ('false', 'no'): return False
        try: return int(val)
        except ValueError: pass
        try: return float(val.replace(',', '.'))
        except ValueError: pass
        return val

    for line in lines:
        if '#' in line:
            line = line.split('#', 1)[0]
        
        line = line.rstrip()
        if not line:
            continue
            
        stripped = line.lstrip()
        if stripped.startswith('- '):
            if current_list_key is not None:
                item_val = stripped[2:].strip()
                result[current_list_key].append(cast_val(item_val))
            continue
            
        if ':' in line:
            key, val = line.split(':', 1)
            key = key.strip()
            val = val.strip()
            
            if not val:
                result[key] = []
                current_list_key = key
            else:
                current_list_key = None
                result[key] = cast_val(val)
                
    return result

def merge_by_key(rows: list[dict], extra: dict, key: str = 'id') -> list[dict]:
    merged = []
    for row in rows:
        new_row = {}
        row_key = row.get(key)
        if row_key in extra:
            new_row.update(extra[row_key])
        new_row.update(row)
        merged.append(new_row)
    return merged

def records_to_json(records: list[dict]) -> str:
    return json.dumps(records, ensure_ascii=False, indent=2, sort_keys=True)
