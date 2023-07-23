import csv

# Open the CSV file and read its contents into a list of dictionaries
with open('moliere.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    cues = list(reader)

# Group the cues by play_name, act, and scene
grouped_cues = {}
for cue in cues:
    key = (cue['play_name'], cue['act'], cue['scene'])
    if key not in grouped_cues:
        grouped_cues[key] = []
    grouped_cues[key].append(cue)

# Sort the cues by act and scene within each play_name group
for key in grouped_cues:
    grouped_cues[key].sort(key=lambda x: (int(x['act']), int(x['scene'])))

# Print the sorted cues for each play_name
for play_name in set([cue['play_name'] for cue in cues]):
    # print(f'\n{play_name}:')
    for key in grouped_cues:
        if key[0] == play_name:
            act = key[1]
            scene = key[2]
            # print(f'  Act {act}, Scene {scene}:')
            for cue in grouped_cues[key]:
                print(f'{cue["character"]}: \n{cue["cue"]}\n')
