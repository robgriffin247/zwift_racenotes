import os
import pandas as pd
from file_read.fit_reader import fit_df

fit_files = [file for file in os.listdir("data") if file.endswith(".fit")]

for f in fit_files:
    print(fit_df(f"data/{f}"))    