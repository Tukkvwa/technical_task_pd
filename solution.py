import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.ndimage import gaussian_filter


df = pd.read_csv('match_data.csv')
df.rename(columns={'Pitch_x': 'x', 'Pitch_y' : 'y',
                   'participation_id' : 'id' , 'Time (s)': 
                   'time', 'Speed (m/s)': 'speed'}, inplace=True)
pitch_dimensions = {'x': (-52.5, 52.5), 'y': (-34, 34)}

df = df[(df['x'] > -52.5) &
        (df['x'] < 52.5) &
        (df['y'] > -34) &
        (df['y'] < 34)]

df.sort_values(by=['id', 'time'], inplace=True)
df = df.round({"x": 1, "y": 1})

plt.figure(figsize = (10,8))
df['x'] = pd.cut(df['x'], bins=60, labels=False)
df['y'] = pd.cut(df['y'], bins=40, labels=False)

position_counts = df.groupby(['x', 'y']).size().sort_values(ascending=False).reset_index(name='counts')
#print(position_counts.iloc[1:])

pos_smooth = gaussian_filter(position_counts.iloc[1:].pivot(index='x', columns='y', values='counts'), sigma=1)
#pos_smooth = gaussian_filter(position_counts.pivot(index='x', columns='y', values='counts'), sigma=1)
sns.heatmap(pos_smooth, cmap='coolwarm', cbar=False)

#print(position_counts)
plt.show()

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