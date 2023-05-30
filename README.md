#Data Analysis of CSGO Match: EvilGeniusProblem

This repository contains the analysis of Counter-Strike: Global Offensive (CS:GO) matches. 

The analysis is carried out through a Python class, ProcessGameState, which provides a flexible and efficient solution for handling game state data.

ProcessGameState Class
The class handles the following tasks:

File ingestion and ETL: It manages the loading and transformation of match data.

Boundary Check: The class includes a function to determine whether each data row (representing a player's position) falls within a provided boundary. The function has been designed to be highly efficient and minimize runtime.

Weapon Class Extraction: It parses the inventory JSON column to extract weapon classes.

Analysis Performed
Using the ProcessGameState class, we answer several key questions about game strategy:

Team2 T-side Strategy: Determine if entering via a specific boundary is a common strategy used by Team2 when they are on the Terrorist (T) side.

Average Entry Time: Calculate the average timer that Team2, on T side, enters "BombsiteB" with at least 2 rifles or SMGs.

Team2 CT-side Strategy: Investigate Team2's Counter-Terrorist (CT) side strategy, specifically their waiting positions inside "BombsiteB". This includes a heatmap visualization.

Non-Technical Stakeholders Support
Most of our stakeholders, such as the CS:GO coaching staff, aren't tech-savvy enough to run the code themselves. Therefore, we propose a solution that allows our coaching staff to request or acquire the output themselves with minimal technical knowledge. This solution is expected to be implemented in less than a week.
