from collections import defaultdict

preferences = defaultdict(lambda: defaultdict(int))

preferences['Alice']['apples'] += 2
preferences['Bob']['oranges'] += 1
preferences['Charlie']['apples'] += 1

print(preferences)