import georinex as gr
import pandas as pd

rinex_file = "ISK41040.20O"
obs_data = gr.load(rinex_file)
print(obs_data)

# Read observation data
times = obs_data.time.values
print("Time series data:", times)

if "C1" in obs_data:
    C1_data = obs_data["C1"].values
    print("C1 pseudorange data for the first few epochs and satellites:")
    print(C1_data[:5, :])  # Print first few rows


C1_df = pd.DataFrame(C1_data, index=times)
print(C1_df.head())
