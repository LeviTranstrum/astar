# Pseudocode
import cv2
import numpy as np
import hashlib
import json

# Load image
image = cv2.imread('./gray_map.png')

# Define tile size
tile_width, tile_height = 16, 16  # tile size

def load_known_tiles(file_path):
    """Load the known tiles dictionary with pixel data from a JSON file."""
    try:
        with open(file_path, 'r') as file:
            # Load the data from JSON
            data = json.load(file)
            # Convert lists back to numpy arrays
            known_tiles = {tile_type: [np.array(tile) for tile in tiles] for tile_type, tiles in data.items()}
            return known_tiles
    except FileNotFoundError:
        print(f"No existing tile file found. Starting with an empty dictionary.")
        return {}
    except json.JSONDecodeError:
        print(f"File {file_path} is not a valid JSON. Starting with an empty dictionary.")
        return {}

def image_hash(image):
    """Compute a hash for an image."""
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Flatten the image to a 1D array
    flattened = gray_image.flatten()
    # Compute the hash of the array
    return hashlib.sha256(flattened).hexdigest()

def is_similar(tile_image, known_tile_image):
    errors = 0
    for i in range(tile_image.shape[0]):
        for j in range(tile_image.shape[1]):
            if tile_image[i][j] != known_tile_image[i][j]:
                return False

def recognize_tile(tile_image, known_tiles):
    """Recognize the tile by comparing its pixels to the list of known tiles."""

    recognized_tile_type = None

    # Compare the tile image with each known tile
    for tile_type, tiles_data in known_tiles.items():
        for known_tile_data in tiles_data:
            known_tile_image = np.array(known_tile_data)
            # Here you would call your similarity function
            difference = is_similar(tile_image, known_tile_image)
            if difference < min_difference:
                min_difference = difference
                recognized_tile_type = tile_type

    return recognized_tile_type


def add_new_tile_data(tile_type, tile_data, known_tiles):
    """Add the pixel data for a new tile type."""
    if tile_type in known_tiles:
        # Add the new tile data to the existing list for this tile type
        known_tiles[tile_type].append(tile_data.tolist())  # Convert numpy array to list
    else:
        # Create a new entry for this tile type with the new tile data
        known_tiles[tile_type] = [tile_data.tolist()]  # Convert numpy array to list

def save_json(data, file_path):
    """Save the known tiles dictionary with pixel data to a JSON file."""
    # Convert numpy arrays to lists for JSON serialization
    serializable_data = {tile_type: [tile.tolist() for tile in tiles] for tile_type, tiles in data.items()}
    
    with open(file_path, 'w') as file:
        json.dump(serializable_data, file, indent=4)

def show_large_image(title, image, scale=16):
    """Show an image in a larger resolution."""
    # Calculate the new size
    large_image = cv2.resize(image, (image.shape[1] * scale, image.shape[0] * scale), interpolation=cv2.INTER_NEAREST)
    # Show the resized image
    cv2.imshow(title, large_image)
    cv2.waitKey(0)  # Wait for key press
    cv2.destroyAllWindows()  # Close the window when a key is pressed

def show_surrounding_tiles(image, x, y, tile_width, tile_height, scale=16):
    """Show the tile and the surrounding tiles with a red square around the current tile."""
    # Calculate the region to extract
    start_x = max(x - tile_width, 0)
    end_x = min(x + tile_width * 2, image.shape[1])
    start_y = max(y - tile_height, 0)
    end_y = min(y + tile_height * 2, image.shape[0])
    
    # Extract the region
    region = image[start_y:end_y, start_x:end_x].copy()  # Create a copy of the region

    # Calculate the position of the current tile within the region
    tile_pos_x = x - start_x
    tile_pos_y = y - start_y
    
    # Draw a red square around the current tile
    red_color = (0, 0, 255)  # Red in BGR
    thickness = 1  # Thickness of the rectangle lines
    top_left = (tile_pos_x -1 , tile_pos_y -1)
    bottom_right = (tile_pos_x + tile_width, tile_pos_y + tile_height)
    cv2.rectangle(region, top_left, bottom_right, red_color, thickness)

    # Show the extracted region in a larger resolution
    show_large_image('Surrounding Tiles', region, scale)


# Loop through each tile in the image
map_array = []
known_tiles = load_known_tiles('known_tiles.json')
for y in range(0, image.shape[0], tile_height):
    row = []
    for x in range(0, image.shape[1], tile_width):
        # Extract tile image
        print("Extracting tile...")
        tile = image[y:y+tile_height, x:x+tile_width]
        
        # Attempt to recognize the tile
        print("Recognizing tile...")
        tile_type = recognize_tile(tile, known_tiles)
        
        if tile_type in known_tiles:
            # Add known tile to the map array
            print("Tile is known! Adding to map array")
            row.append(known_tiles[tile_type])
        else:
            # Unknown tile encountered
            print("Unknown tile...")
            # Show the tile and ask for input to add to known_tiles
            show_surrounding_tiles(image, x, y, tile_width, tile_height)
            cv2.waitKey(0)  # Wait for key press
            # Manual input for tile type
            tile_type = input('Enter tile type: ')
            add_new_tile_data(tile_type, tile, known_tiles)  # Pass the numpy array of the tile
            row.append(tile_type)
            # Save the tile to the known tiles dictionary
            save_json(known_tiles, 'known_tiles.json')  # Save the updated dictionary            
            # Stop the loop
            break

    map_array.append(row)
    if 'unknown' in row:
        break  # Stop if unknown tile encountered

# Convert map array to a numpy array
map_array = np.array(map_array)

save_json(map_array, 'map_array.json')