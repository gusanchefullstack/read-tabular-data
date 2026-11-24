# import pandas as pd
# from tabulate import tabulate  # type: ignore[import-untyped]
# import numpy as np


# def main() -> None:
#     print("Hello from read-tabular-data!")

#     tables = pd.read_html("https://docs.google.com/document/d/e/2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/pub", encoding="utf-8")
#     df = tables[0]
#     df.columns = pd.Index(df.iloc[0].astype(str))
#     df = df[1:].reset_index(drop=True)  

#     print(tabulate(df, headers="keys", tablefmt="grid", showindex=False))
    
#     max_x = int(max(df['x-coordinate']))
#     max_y = int(max(df['y-coordinate']))
#     print(f"max_x = {max_x}")
#     print(f"max_y = {max_y}")

#     rows = max_y + 1
#     cols = max_x + 1
#     matrix = np.full((rows, cols), "", dtype="<U10")
#     print(matrix)
#     print("\n\n")

#     existing_coordinates = []

#     for character in df.values:
#         existing_coordinates.append([int(character[0]), int(character[2]), character[1]])
#     print(existing_coordinates)

#     for (x,y,text) in existing_coordinates:
#         matrix[y,x] = text

#     # print(matrix)

#     rows = len(matrix)
#     cols = len(matrix[0])

#     for r in range(rows - 1, -1, -1):
#         for c in range(0, cols):
#             print(matrix[r][c], end="")
#         print("\n")


    

    
