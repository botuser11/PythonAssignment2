import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def load_data(file_path):
    # Step 1: Load the dataset
    return pd.read_csv(file_path)

def filter_data_by_bounding_box(grow_data, lon_min, lon_max, lat_min, lat_max):
    # Step 3: Filter data within the bounding box
    valid_data = grow_data[
        (grow_data["Longitude"] >= lon_min) & (grow_data["Longitude"] <= lon_max) &
        (grow_data["Latitude"] >= lat_min) & (grow_data["Latitude"] <= lat_max)
    ]
    valid_data.dropna(subset=["Latitude", "Longitude"], inplace=True)
    return valid_data

def plot_valid_data(valid_data, map_image_path, lon_min, lon_max, lat_min, lat_max):
    # Step 4: Load the map image
    map_image = mpimg.imread(map_image_path)

    # Plot valid sensor points only
    fig, ax = plt.subplots(figsize=(10, 12))
    ax.imshow(map_image, extent=[lon_min, lon_max, lat_min, lat_max], aspect='auto')
    ax.scatter(
        valid_data["Longitude"],
        valid_data["Latitude"],
        color="red",
        s=50,
        alpha=0.7,
        label="Valid Sensor Locations"
    )
    plt.legend()
    plt.title("GROW Sensor Locations in the UK (Cleaned)")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.savefig('finalPlot.png')
    plt.show()

def check_and_swap_columns(data):
    """This function checks if the Latitude and Longitude columns are swapped by mistake.
       If Latitude contains values that seem like Longitude (values outside the expected range for Latitude),
       it swaps the columns to correct the mistake."""
    
    # If Latitude values are outside the typical range for Latitude (-90 to 90), swap the columns
    if data["Latitude"].min() < -180 or data["Latitude"].max() > 180:
        print("Warning: Latitude and Longitude columns appear to be swapped. Fixing...")
        
        # Swap the Latitude and Longitude columns
        data.rename(columns={"Latitude": "Temp", "Longitude": "Latitude"}, inplace=True)
        data.rename(columns={"Temp": "Longitude"}, inplace=True)
    
    return data

def main():
    # File paths and bounding box
    file_path = "GrowLocations.csv"
    map_image_path = "map7.png"
    lon_min, lon_max = -10.592, 1.6848
    lat_min, lat_max = 50.681, 57.985

    # Load data
    grow_data = load_data(file_path)
    
    # Check for swapped columns and fix if needed
    grow_data = check_and_swap_columns(grow_data)
    
    # Filter data by bounding box
    valid_data = filter_data_by_bounding_box(grow_data, lon_min, lon_max, lat_min, lat_max)
    
    # Debugging: Print counts
    print(f"Total points before filtering: {len(grow_data)}")
    print(f"Total points after filtering: {len(valid_data)}")
    
    # Plot valid data only
    plot_valid_data(valid_data, map_image_path, lon_min, lon_max, lat_min, lat_max)

if __name__ == '__main__':
    main()
