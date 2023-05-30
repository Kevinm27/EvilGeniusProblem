import pandas as pd
import argparse
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
import numpy as np
class ProcessGameState:
   def __init__(self, z_bounds, xy_polygon):
      self.data = None
      self.z_bounds = z_bounds
      self.xy_polygon = Polygon(xy_polygon)

   def readParquetIntoPanda(self, fullFilePath):
      try:
         self.data = pd.read_parquet(fullFilePath, engine='pyarrow')
      except Exception as e:
         print(f"Error reading parquet file: {e}")
         return

   def checkBoundaries(self, data_to_check):
      if data_to_check is None:
         print("Data not loaded yet.")
         return None
      
       # Drop any rows with missing or NaN values in any column
      data_to_check = data_to_check.dropna()

      #print(self.data)
      data_in_z = data_to_check[(data_to_check['z'] >= self.z_bounds[0]) & (data_to_check['z'] <= self.z_bounds[1])]

      in_boundary = data_in_z.apply(
         lambda row: self.xy_polygon.contains(Point(row['x'], row['y'])) if pd.notnull(row['x']) and pd.notnull(row['y']) else False,
         axis=1
      )

      return data_in_z[in_boundary]

   def extractWeaponClassesIntoCol(self):
      if self.data is None:
         print("Data not loaded yet.")
         return

      def weapon_count(inventory):
         if inventory is None:
            return 0
         count = 0
        # print("Inventory: ", inventory)  # debugging line
         for item in inventory:
            if item is not None and 'weapon_class' in item:
          #        print("Item: ", item)  # debugging line
                  if item['weapon_class'] in ['Rifle', 'SMG']:
                     count += 1
         #print("Count: ", count)  # debugging line
         return count


      
      self.data['weapon_count'] = self.data['inventory'].apply(weapon_count)

   def check_team_weapons(self, round_num, team='Team2'):
    # Get all the data for the specific round and team
    round_data = self.data[
        (self.data['round_num'] == round_num) 
        & (self.data['team'] == team)
    ]

    # Sum up the weapon counts for the team in this round
    total_weapons = round_data['weapon_count'].sum()

    return total_weapons >= 2

   def ave_time(self, team='Team2', side='T', bombsite='BombsiteB'):
      if self.data is None:
         print("Data not loaded yet.")
         return

      # Get a list of all the unique round numbers
      rounds = self.data['round_num'].unique()

      # Filter out rounds where the team does not have at least two rifles or SMGs
      valid_rounds = [round_num for round_num in rounds if self.check_team_weapons(round_num, team)]

      # Filter for the specific team, side, bombsite and valid rounds
      team_boundary_entries = self.data[
         (self.data['team'] == team) 
         & (self.data['side'] == side) 
         & (self.data['round_num'].isin(valid_rounds))
         & (self.data['area_name'] == bombsite)
      ]

      # Get the earliest time per valid round
      earliest_times = team_boundary_entries.groupby('round_num')['seconds'].min()

      # Calculate the average of these times
      average_time = earliest_times.mean()

      return average_time

   def team_strategy(self, team='Team2', side='T'):
      if self.data is None:
         print("Data not loaded yet.")
         return

      # Filter for the specific team and side
      team_data = self.data[(self.data['team'] == team) & (self.data['side'] == side)]

      # Group by round and player, then apply checkBoundaries to each group
      team_data_grouped = team_data.groupby(['round_num', 'player'])
      player_entries = team_data_grouped.apply(lambda group: self.checkBoundaries(group).head(1)).reset_index(drop=True)

      # Count unique rounds where a player enters the boundary
      unique_boundary_entries = player_entries['round_num'].nunique()

      # Count total unique rounds
      total_unique_rounds = team_data['round_num'].nunique()

      # Calculate the percentage of unique rounds where a player enters the boundary
      percentage = unique_boundary_entries / total_unique_rounds if total_unique_rounds > 0 else 0
      #print(unique_boundary_entries)
      #print(total_unique_rounds)
      #print(percentage)
      return percentage > 0.5

   def plot_heatmap(self, team='Team2', side='CT', bombsite='BombsiteB'):
      # Filter data for Team2 and CT side in BombsiteB
      team_data = self.data[(self.data['team'] == 'Team2') & (self.data['side'] == 'CT') & (self.data['area_name'] == 'BombsiteB')]

      # Extract x and y coordinates
      x = team_data['x']
      y = team_data['y']

      # Compute 2D histogram using np.histogram2d
      bins = (200, 200) # Increase this for a finer grid
      hist, xedges, yedges = np.histogram2d(x, y, bins=bins)

      # Create a new figure and set its size
      fig, ax = plt.subplots(figsize=(10,10))

      # Overlay the heatmap
      heatmap = ax.imshow(hist, cmap='hot', interpolation='nearest', origin='lower', 
               extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]], alpha=0.5, aspect='auto')

      # Add a colorbar
      cbar = fig.colorbar(heatmap)
      cbar.ax.set_ylabel('# of Occurences', rotation=-90, va="bottom")

      # Show the plot
      plt.show()















if __name__ == "__main__":
   parser = argparse.ArgumentParser()

   parser.add_argument('--filepath', type=str, required=True,
                       help="Full path to the parquet file")
   parser.add_argument('--z_bounds', type=lambda s: [int(item) for item in s.split(',')], default=[0,0],
                       help="Z Bounds in the format 'lower,upper'")
   parser.add_argument('--xy_polygon', type=lambda s: [tuple(map(int, item.split(','))) for item in s.split(' ')], default=[(0,0)],
                       help="XY Polygon vertices in the format 'x1,y1 x2,y2;...'")

   args = parser.parse_args()

   # Add some input validation here
   if len(args.z_bounds) != 2:
      print("Error: z_bounds must contain exactly two integers.")
      exit(1)

   if len(args.xy_polygon) < 3:
      print("Error: xy_polygon must contain at least three points.")
      exit(1)

   pg = ProcessGameState(args.z_bounds, args.xy_polygon)
   pg.readParquetIntoPanda(args.filepath)
   pd.set_option('display.max_columns', 20)
   pg.extractWeaponClassesIntoCol()

   in_boundary = pg.checkBoundaries(pg.data)

   #print(len(in_boundary))
   print("In Boundary? : " + str(pg.team_strategy()))
   print(str(pg.ave_time()) + "s on average per round" )
   pg.plot_heatmap()
