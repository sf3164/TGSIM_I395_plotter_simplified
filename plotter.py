#simplified version
import pandas as pd
import plotly.graph_objects as go
import os
import matplotlib.colors as mcolors
import tkinter as tk
from tkinter import ttk, messagebox

# File Paths
#TRAJECTORY_FILE = "TGSIM_I395.csv"
TRAJECTORY_FILE = "updated_TGSIM_I395.csv" #use the updated dataset with (corrected lane id and) flipped and rotated
#CENTERLINE_FILE = os.path.join("boundaries", "I395_boundaries.csv")
CENTERLINE_FILE = os.path.join("boundaries", "updated_I395_boundaries.csv") #use the updated flipped and rotataed boundary that is flipped
'''
def swap_x_y_columns(df):
    """Swap the values of xloc_kf and yloc_kf columns in-place while keeping column names."""
    if "xloc_kf" in df.columns and "yloc_kf" in df.columns:
        df["xloc_kf"], df["yloc_kf"] = df["yloc_kf"].copy(), df["xloc_kf"].copy()
'''



# === Load trajectory data ===
traj_df2 = pd.read_csv(TRAJECTORY_FILE)

# Apply the swap to the trajectory dataframe
#swap_x_y_columns(traj_df2)

# Initialize main window
root = tk.Tk()
root.title("Simplified Vehicle Plotter")

selected_run = tk.StringVar()

# ---- Plotting Function ----
def plot_selected_vehicles():
    try:
        #run_index = int(selected_run.get())
        input_text = vehicle_entry.get().strip()

        if not input_text:
            raise ValueError("No vehicle IDs provided.")
        
        # Get data for selected run
        #run_data = traj_df[traj_df["run_index"] == run_index]
        run_data = traj_df2
        if run_data.empty:
            raise ValueError(f"No data for Run {run_index}.")

        # Compute the max ranges
        #max_x = traj_df[(traj_df["run_index"] == run_index)]['xloc_kf'].max()
        #max_y = traj_df[(traj_df["run_index"] == run_index)]['yloc_kf'].max()


        max_x = traj_df['xloc_kf'].max()
        max_y = traj_df['yloc_kf'].max()
        # Parse and validate vehicle IDs
        input_ids = input_text.split(",")
        vehicle_ids = []
        invalid_format = []
        not_found = []

        for vid in input_ids:
            vid = vid.strip()
            if not vid.isdigit():
                invalid_format.append(vid)
            else:
                vid_int = int(vid)
                if vid_int not in run_data["id"].unique():
                    not_found.append(vid)
                else:
                    vehicle_ids.append(vid_int)

        # Raise combined error if any problems
        if invalid_format or not_found:
            error_msg = ""
            if invalid_format:
                error_msg += f"❌ Invalid format (not numeric): {', '.join(invalid_format)}\n"
            if not_found:
                error_msg += f"❌ Not found: {', '.join(not_found)}"
            raise ValueError(error_msg)

        # Filter trajectory
        filtered_traj = run_data[run_data["id"].isin(vehicle_ids)]
        '''
        # Load centerline
        centerline_file = os.path.join(CENTERLINE_FOLDER, f"I395_boundaries.csv")
        if not os.path.exists(centerline_file):
            raise FileNotFoundError(f"Missing centerline: {centerline_file}")
        '''
        centerline_df = pd.read_csv(CENTERLINE_FILE)

        # Plotting
        color_list = list(mcolors.TABLEAU_COLORS.values())
        fig = go.Figure()

        # Plot all lane centerlines
        # Plot all lane centerlines
        for lane in centerline_df.columns:
            if lane.startswith("x"):
                lane_number_raw = lane[1]  # e.g., "1", "2", ...


                lane_centerline_column_x = f"x{lane_number_raw}"
                lane_centerline_column_y = f"y{lane_number_raw}"
        
                if lane_centerline_column_x in centerline_df.columns and lane_centerline_column_y in centerline_df.columns:
                    lane_centerline = centerline_df[[lane_centerline_column_x, lane_centerline_column_y]].dropna()
        
                    # Compute logical lane number using your formula
                    try:
                        lane_index = int(lane_number_raw)
                        logical_lane_number = -1 * (6 - lane_index)
                        label_text = f"Lane {logical_lane_number}<br>right boundary"
                    except:
                        logical_lane_number = lane_number_raw  # fallback if conversion fails
                        label_text = f"Lane {logical_lane_number}<br>right boundary"
        
                    # Plot the lane boundary
                    fig.add_trace(go.Scatter(
                        #x=lane_centerline[lane_centerline_column_x]*0.3,
                        #y=lane_centerline[lane_centerline_column_y]*0.3,
                        x=lane_centerline[lane_centerline_column_x]*0.3,
                        y=lane_centerline[lane_centerline_column_y]*0.3,
                        mode="lines",
                        line=dict(color="#D3D3D3", width=1.5),
                        name=f"Lane {logical_lane_number}<br>right boundary"
                    ))
        
                    # Add label at the end of the centerline
                    max_x_idx = lane_centerline[lane_centerline_column_x].idxmax()
                    end_x = lane_centerline.at[max_x_idx, lane_centerline_column_x]*0.3
                    end_y = lane_centerline.at[max_x_idx, lane_centerline_column_y]*0.3

                    fig.add_trace(go.Scatter(
                        #x=[end_x],
                        #y=[end_y],
                        x=[end_x],
                        y=[end_y],
                        mode="text",
                        text=[label_text],
                        textposition="top center",
                        showlegend=False
                    ))

        # Plot each vehicle
        for i, vid in enumerate(vehicle_ids):
            veh_data = filtered_traj[filtered_traj["id"] == vid]
            hover = [
                f"ID: {vid}<br>Time: {t}s<br>Lane: {int(l)}<br>Speed: {s:.2f} m/s<br>Accel: {a:.2f} m/s²"
                for t, l, s, a in zip(veh_data["time"], veh_data["lane_kf"], veh_data["speed_kf"], veh_data["acceleration_kf"])
            ]
            fig.add_trace(go.Scatter(
                x=veh_data["xloc_kf"],
                y=veh_data["yloc_kf"],
                mode="markers",
                name=f"Vehicle {vid}",
                marker=dict(size=5),
                text=hover,
                hoverinfo="text",
                line=dict(color=color_list[i % len(color_list)], width=2)
            ))

        fig.update_layout(
            title=f"Trajectories",
            xaxis=dict(range=[0, max_x]),
            yaxis=dict(range=[0, max_x]),
            xaxis_title="X",
            yaxis_title="Y",
            template="plotly_white"
        )

        fig.write_html("I395_Simplified_plot.html")
        fig.show()

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ---- UI Elements ----

'''
tk.Label(root, text="Select Run Index:").grid(row=0, column=0)
run_menu = ttk.Combobox(root, textvariable=selected_run, values=[str(r) for r in sorted(traj_df["run_index"].unique())], state="readonly")
run_menu.grid(row=0, column=1)
'''

tk.Label(root, text="Enter Vehicle IDs (comma-separated):").grid(row=1, column=0)
vehicle_entry = tk.Entry(root, width=40)
vehicle_entry.grid(row=1, column=1)

tk.Button(root, text="Plot", command=plot_selected_vehicles).grid(row=2, column=0, columnspan=2, pady=10)
root.mainloop()
