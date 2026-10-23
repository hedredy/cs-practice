import sys
from logstats import count_levels, top_errors, format_report

lines = sys.stdin.read().splitlines()
if lines:
    filename = lines[0].strip()
    
    with open(filename, "r", encoding="utf-8") as f:
        counts = count_levels(f)
        
    with open(filename, "r", encoding="utf-8") as f:
        errors = top_errors(f, 3)
        
    total = sum(counts.values())
    error_count = counts.get("ERROR", 0)
    broken_count = counts.get("BROKEN", 0)
    
    print(total)
    print(error_count)
    print(broken_count)
    
    report_text = format_report(counts, errors)
    with open("report.txt", "w", encoding="utf-8") as out:
        out.write(report_text)