import json, csv
with open('merged.json', 'r') as f:
    merged_l = json.load(f)
with open('merged.csv', 'w') as f:
    dict_writer = csv.DictWriter(f, fieldnames=merged_l[0].keys())
    dict_writer.writeheader()
    dict_writer.writerows(merged_l)