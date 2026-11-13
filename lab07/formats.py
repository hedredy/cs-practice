import json

def csv_to_records(text: str) -> list[dict]:
    if not text.strip():
        return []
    lines = text.strip().split('\n')
    headers = [h.strip() for h in lines[0].split(',')]
    records = []
    for line in lines[1:]:
        values = [v.strip() for v in line.split(',')]
        records.append(dict(zip(headers, values)))
    return records

def parse_settings(lines: list[str]) -> dict:
    result = {}
    current_list_key = None
    for line in lines:
        if '#' in line:
            line = line.split('#')[0]
        line = line.rstrip()
        if not line:
            continue
        if line.startswith('  - '):
            if current_list_key:
                result[current_list_key].append(line[4:].strip())
            continue
        if ':' in line:
            key, val = map(str.strip, line.split(':', 1))
            if not val:
                result[key] = []
                current_list_key = key
            else:
                current_list_key = None
                if val.lower() in ('true', 'yes'):
                    result[key] = True
                elif val.lower() in ('false', 'no'):
                    result[key] = False
                else:
                    try:
                        if '.' in val:
                            result[key] = float(val)
                        else:
                            result[key] = int(val)
                    except ValueError:
                        result[key] = val
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
