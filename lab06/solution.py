import os
from pathlib import Path

def count_by_extension(paths: list[str]) -> dict[str, int]:
    counts = {}
    for p in paths:
        ext = Path(p).suffix.lower()
        if ext.startswith('.'):
            ext = ext[1:]
        counts[ext] = counts.get(ext, 0) + 1
    return counts

def deepest_path(paths: list[str]) -> str:
    if not paths:
        return ""
    return sorted(paths, key=lambda x: (-x.count('/'), x))[0]

def human_size(n_bytes: int) -> str:
    if n_bytes < 1024:
        return f"{n_bytes} Б"
    for unit in ['КБ', 'МБ', 'ГБ', 'ТБ']:
        n_bytes /= 1024
        if n_bytes < 1024:
            return f"{n_bytes:.1f} {unit}"
    return f"{n_bytes:.1f} ПБ"
