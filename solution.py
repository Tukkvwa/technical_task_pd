import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.ndimage import gaussian_filter
from collections import defaultdict


df = pd.read_csv('match_data.csv')
df.rename(columns={'Pitch_x': 'x', 'Pitch_y' : 'y',
                   'participation_id' : 'id' , 'Time (s)': 
                   'time', 'Speed (m/s)': 'speed'}, inplace=True)

df = df[(df['x'] > -52.5) &
        (df['x'] < 52.5) &
        (df['y'] > -34) &
        (df['y'] < 34) &
        (df['speed'] > 0)]

def time_spent(target_id, proximity_threshold=5):

    time_groups = df.groupby('time')
    time_with_others = defaultdict(int)

    for time, group in time_groups:
        # Get target's coordinates at this time
        target_data = group[group['id'] == target_id]
        if target_data.empty:
            continue  # target_id not present at this time
        
        x_target = target_data['x'].values[0]
        y_target = target_data['y'].values[0]
        
        # Compute Euclidean distance from target to all others at this time
        group['distance'] = np.sqrt(
            (group['x'] - x_target) ** 2 + 
            (group['y'] - y_target) ** 2
        )
        
        # Filter IDs within proximity threshold (excluding itself)
        nearby_ids = group[(group['distance'] <= proximity_threshold) & 
                           (group['id'] != target_id)]['id'].tolist()
        
        # Increment time spent with each nearby ID (assuming 0.1 time unit per row)
        for other_id in nearby_ids:
            time_with_others[other_id] += 0.1

    # Find the ID that spent the most time with target_id
    print(time_with_others)

time_spent('ball')
"""
lboard1 = df[df['id'] != 'ball'][['id', 'x', 'y']] 
total_distances = (
    lboard1.groupby('id')
    .apply(lambda x: np.sqrt((x['x'].diff()**2) +
                             (x['y'].diff()**2)).sum(),
                             include_groups=False)
    .reset_index(name='total_distance')
    .sort_values('total_distance', ascending=False) 
    .reset_index(drop=True)
)


lboard2 = df[(df['id'] != 'ball') &
             (df['speed'] > 5.5) &
             (df['speed'] < 6.97)][['id', 'x', 'y']]

total_distances = (
    lboard2.groupby('id')
    .apply(lambda x: np.sqrt((x['x'].diff()**2) +
                             (x['y'].diff()**2)).sum(),
                             include_groups=False)
    .reset_index(name='total_distance')
    .sort_values('total_distance', ascending=False) 
    .reset_index(drop=True)
)

lboard3 = df[df['id'] != 'ball'][['id', 'speed']]
max_speed = lboard3.groupby('id').max().sort_values('speed', ascending=False)"
"""