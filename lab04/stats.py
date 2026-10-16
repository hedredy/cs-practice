def parse_record(line: str) -> dict:
    parts = line.split(";")
    if len(parts) != 3:
        raise ValueError("Неверное количество полей")
    
    city = parts[0].strip()
    temp_str = parts[1].strip().replace(",", ".")
    date = parts[2].strip()
    
    if not city or not date:
        raise ValueError("Пустой город или дата")
    
    try:
        temp = float(temp_str)
    except ValueError:
        raise ValueError("Температура не число")
        
    return {"city": city, "temperature": temp, "date": date}

def read_valid(lines: list[str]) -> list[dict]:
    records = []
    for line in lines:
        if not line:
            continue
        try:
            records.append(parse_record(line))
        except ValueError:
            pass
    return records

def average_by_city(records: list[dict]) -> dict:
    total = {}
    count = {}
    for r in records:
        city = r["city"]
        total[city] = total.get(city, 0.0) + r["temperature"]
        count[city] = count.get(city, 0) + 1
        
    ans = {}
    for city in total:
        ans[city] = round(total[city] / count[city], 1)
    return ans

def warmest_city(records: list[dict]) -> str:
    avgs = average_by_city(records)
    best = ""
    for city in avgs:
        if best == "" or avgs[city] > avgs[best]:
            best = city
        elif avgs[city] == avgs[best] and city < best:
            best = city
    return best