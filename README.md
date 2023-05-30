# CS:GO Match Data Analysis

This project is about analyzing Counter-Strike: Global Offensive (CS:GO) match data to find out insights about team strategies and weapon choices.

## Prerequisites

The script requires the following Python packages:

- pandas
- argparse
- shapely
- matplotlib
- seaborn
- numpy

## Files

- `main.py`: The main script to run.

## Class: ProcessGameState

The class `ProcessGameState` in `main.py` is responsible for handling the data analysis. Its features include:

- File ingestion and ETL
- Checking whether or not each row falls within a provided boundary
- Extracting the weapon classes from the inventory JSON column
- Analyzing team strategies based on entries through a specific boundary
- Calculating the average timer for a team entering a specific bombsite with at least two rifles or SMGs
- Plotting a heatmap to visualize player locations

## Execution

The script can be executed via command line using the following command:

```shell
python main.py --filepath YOUR_FILE_PATH --z_bounds 'lower,upper' --xy_polygon 'x1,y1 x2,y2 x3,y3'
