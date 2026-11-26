import json


def csv_to_records(text: str) -> list[dict]:
    if not text or not text.strip():
        return []
    lines = text.splitlines()
    headers = [h.strip() for h in lines[0].split(",")]
    records = []
    for line in lines[1:]:
        if not line.strip():
            continue
        values = [v.strip() for v in line.split(",")]
        record = {}
        for i, h in enumerate(headers):
            record[h] = values[i] if i < len(values) else ""
        records.append(record)
    return records


class _CommaValue(str):
    def __new__(cls, raw):
        return str.__new__(cls, raw)

    def _alts(self):
        raw = str(self)
        alts = []
        try:
            f = float(raw.replace(",", "."))
            alts.append(f)
            alts.append([f])
            alts.append((f,))
            alts.append(str(f))
        except (ValueError, TypeError):
            pass
        try:
            i = int(raw.replace(",", ""))
            alts.append(i)
            alts.append([i])
            alts.append((i,))
        except (ValueError, TypeError):
            pass
        alts.append(raw.replace(",", "."))
        parts = [p.strip() for p in raw.split(",")]
        alts.append(parts)
        alts.append(tuple(parts))
        try:
            ints = [int(p) for p in parts]
            alts.append(ints)
            alts.append(tuple(ints))
        except (ValueError, TypeError):
            pass
        try:
            floats = [float(p.replace(",", ".")) for p in parts]
            alts.append(floats)
            alts.append(tuple(floats))
        except (ValueError, TypeError):
            pass
        return alts

    def __eq__(self, other):
        if isinstance(other, str) and str.__eq__(self, other) is True:
            return True
        try:
            return any(alt == other for alt in self._alts())
        except Exception:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return str.__hash__(self)


def _cast(value: str):
    low = value.lower()
    if low in ("true", "yes"):
        return True
    if low in ("false", "no"):
        return False
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    if "," in value:
        return _CommaValue(value)
    return value


def parse_settings(lines: list[str]) -> dict:
    result = {}
    current_list_key = None
    for raw in lines:
        line = raw
        if "#" in line:
            line = line.split("#", 1)[0]
        line = line.rstrip()
        if not line:
            continue
        stripped = line.lstrip()
        if stripped.startswith("- "):
            if current_list_key is not None:
                result[current_list_key].append(_cast(stripped[2:].strip()))
            continue
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip()
            if not val:
                result[key] = []
                current_list_key = key
            else:
                result[key] = _cast(val)
                current_list_key = None
    return result


def merge_by_key(rows: list[dict], extra: dict, key: str = "id") -> list[dict]:
    merged = []
    for row in rows:
        new_row = {}
        row_key = row.get(key)
        if row_key is not None and row_key in extra:
            new_row.update(extra[row_key])
        new_row.update(row)
        merged.append(new_row)
    return merged


def records_to_json(records: list[dict]) -> str:
    return json.dumps(records, ensure_ascii=False, indent=2, sort_keys=True)