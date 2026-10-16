import sys
from stats import average_by_city, read_valid, warmest_city

lines = sys.stdin.read().splitlines()
valid_records = read_valid(lines)

empty_lines = sum(1 for line in lines if not line)
errors = len(lines) - len(valid_records) - empty_lines

best_city = warmest_city(valid_records)
avgs = average_by_city(valid_records)

print(len(valid_records))
print(errors)
print(f"{avgs[best_city]:.1f}")
