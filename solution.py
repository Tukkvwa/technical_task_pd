import pandas as pd
import numpy as np
import seaborn as sns


df = pd.read_csv('match_data.csv')
df.rename(columns={'Pitch_x': 'x', 'Pitch_y' : 'y',
                   'participation_id' : 'id' , 'Time (s)': 
                   'time', 'Speed (m/s)': 'speed'}, inplace=True)

df = df[(df['x'] > -52.5) &
        (df['x'] < 52.5) &
        (df['y'] > -34) &
        (df['y'] < 34)]

df.sort_values(by=['id', 'time'], inplace=True)

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
max_speed = lboard3.groupby('id').max().sort_values('speed', ascending=False)
