def parse_event(line: str) -> dict:
    line = line.strip()
    if not line:
        raise ValueError("Пустая строка")
    
    parts = line.split(" ", 2)
    if len(parts) != 3:
        raise ValueError("Неверный формат строки")
        
    time_str = parts[0]
    level = parts[1]
    msg = parts[2]
    
    if level not in ["DEBUG", "INFO", "WARNING", "ERROR"]:
        raise ValueError("Неизвестный уровень")
        
    return {"time": time_str, "level": level, "message": msg}
def count_levels(lines) -> dict:
    counts = {}
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            evt = parse_event(line)
            lvl = evt["level"]
            counts[lvl] = counts.get(lvl, 0) + 1
        except ValueError:
            counts["BROKEN"] = counts.get("BROKEN", 0) + 1
    return counts

def top_errors(lines, n: int) -> list[list]:
    counts = {}
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            evt = parse_event(line)
            if evt["level"] == "ERROR":
                msg = evt["message"]
                counts[msg] = counts.get(msg, 0) + 1
        except ValueError:
            pass
            
    arr = []
    for msg in counts:
        arr.append([msg, counts[msg]])
        
    arr.sort(key=lambda x: (-x[1], x[0]))
    
    res = []
    for i in range(min(n, len(arr))):
        res.append(arr[i])
    return res