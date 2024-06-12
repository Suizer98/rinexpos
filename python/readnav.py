import georinex as gr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the navigation data
nav_file = "chur1610.19n"
nav_data = gr.load(nav_file)
print(nav_data)

# Define constants
mu = 3.986005e14  # Earth's gravitational constant (m^3/s^2)
omega_e = 7.2921151467e-5  # Earth's rotation rate (rad/s)


# Function to compute satellite position from ephemeris data
def compute_satellite_position(eph, times):
    # Extract necessary ephemeris parameters
    a = eph["sqrtA"].values ** 2  # Semi-major axis
    e = eph["Eccentricity"].values
    i_0 = eph["Io"].values
    omega_0 = eph["Omega0"].values
    omega_dot = eph["OmegaDot"].values
    omega = eph["omega"].values
    M_0 = eph["M0"].values
    delta_n = eph["DeltaN"].values
    t_oe = eph["Toe"].values
    i_dot = eph["IDOT"].values

    positions = []

    # Check dimensions for debugging
    print(f"a: {a.shape}, e: {e.shape}, times: {times.shape}")

    for idx, t in enumerate(times):
        # Calculate time from ephemeris reference epoch
        t_seconds = (t - np.datetime64("1970-01-01T00:00:00")) / np.timedelta64(1, "s")
        tk = t_seconds - t_oe[idx]

        # Correct mean motion
        n_0 = np.sqrt(mu / a[idx] ** 3)
        n = n_0 + delta_n[idx]

        # Mean anomaly
        M_k = M_0[idx] + n * tk

        # Eccentric anomaly (using iterative method)
        E_k = M_k
        for _ in range(10):
            E_k = M_k + e[idx] * np.sin(E_k)

        # True anomaly
        v_k = 2 * np.arctan2(
            np.sqrt(1 + e[idx]) * np.sin(E_k / 2), np.sqrt(1 - e[idx]) * np.cos(E_k / 2)
        )

        # Argument of latitude
        phi_k = v_k + omega[idx]

        # Second harmonic perturbations
        delta_u_k = eph["Cus"].values[idx] * np.sin(2 * phi_k) + eph["Cuc"].values[
            idx
        ] * np.cos(2 * phi_k)
        delta_r_k = eph["Crs"].values[idx] * np.sin(2 * phi_k) + eph["Crc"].values[
            idx
        ] * np.cos(2 * phi_k)
        delta_i_k = eph["Cis"].values[idx] * np.sin(2 * phi_k) + eph["Cic"].values[
            idx
        ] * np.cos(2 * phi_k)

        # Corrected argument of latitude, radius, inclination
        u_k = phi_k + delta_u_k
        r_k = a[idx] * (1 - e[idx] * np.cos(E_k)) + delta_r_k
        i_k = i_0[idx] + delta_i_k + i_dot[idx] * tk

        # Positions in orbital plane
        x_k_prime = r_k * np.cos(u_k)
        y_k_prime = r_k * np.sin(u_k)

        # Corrected longitude of ascending node
        omega_k = omega_0[idx] + (omega_dot[idx] - omega_e) * tk - omega_e * t_oe[idx]

        # Earth-fixed coordinates
        x_k = x_k_prime * np.cos(omega_k) - y_k_prime * np.sin(omega_k) * np.cos(i_k)
        y_k = x_k_prime * np.sin(omega_k) + y_k_prime * np.cos(omega_k) * np.cos(i_k)
        z_k = y_k_prime * np.sin(i_k)

        positions.append([x_k, y_k, z_k])

    return np.array(positions)


# Extract times and ephemeris for satellite G01
satellite = "G01"
eph = nav_data.sel(sv=satellite).dropna(dim="time", how="all")

# Define the times at which you want to compute the satellite positions
times = eph["time"].values
positions = compute_satellite_position(eph, times)

# Ensure positions is a 2D array with shape (num_times, 3)
print("Shape of positions before reshaping:", positions.shape)

# Convert positions to pandas DataFrame for better readability
positions_df = pd.DataFrame(positions, columns=["X", "Y", "Z"], index=times)
print(positions_df.head())

# Plot the satellite positions
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.plot(positions_df["X"], positions_df["Y"], positions_df["Z"], marker="o")

ax.set_xlabel("X (meters)")
ax.set_ylabel("Y (meters)")
ax.set_zlabel("Z (meters)")
ax.set_title("Satellite G01 Orbit")

plt.show()
