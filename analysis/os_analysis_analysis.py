data = open('os_analysis.txt', 'r').readlines()

counts = dict()

for pair in data:
    pair = pair.split(":")
    ip = pair[0].strip()
    version = pair[1].strip()
    if version not in counts:
        counts[version] = set()
    counts[version].add(ip)

for key in counts.keys():
    print(f"{key}: {len(counts[key])}")
