def parse_record(line: str) -> dict:
    parts = line.split(";")
    if len(parts) != 3:
        raise ValueError("Неверное количество полей")
    
    city = parts[0]
    temp_str = parts[1]
    date = parts[2]
    
    if not city or not date:
        raise ValueError("Пустой город или дата")
    
    try:
        temp = float(temp_str)
    except ValueError:
        raise ValueError("Температура не число")
        
    return {"city": city, "temperature": temp, "date": date}
