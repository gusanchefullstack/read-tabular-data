import numpy as np
import pandas as pd


def decoding_secret(url):
    #Extract first table from Google Doc
    tables = pd.read_html(url, encoding="utf-8")
    df = tables[0]
    df.columns = pd.Index(df.iloc[0].astype(str))
    df = df[1:].reset_index(drop=True)  
    
    # Get the highest coordinate
    max_x = df['x-coordinate'].astype(int).max()
    max_y = df['y-coordinate'].astype(int).max()

    # Generate a empty matrix to map coordinates
    rows = max_y + 1
    cols = max_x + 1
    matrix = np.full((rows, cols), " ", dtype="<U1")

    # Captures coordinates from table (tabular data) and create tuples
    existing_coordinates = []
    for character in df.values:
        existing_coordinates.append([int(character[0]), int(character[2]), character[1]])

    # Fill the matrix mirroring cartesian plane
    for (x,y,symbol) in existing_coordinates:
        matrix[y,x] = symbol

    #Display symbols reading first column and last row and so on
    rows = len(matrix)
    cols = len(matrix[0])

    for r in range(rows - 1, -1, -1):
        for c in range(0, cols):
            print(matrix[r][c], end="")
        print()
