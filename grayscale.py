import cv2

# Path to the input image
input_image_path = 'red_map.png'  # Replace with your image path
# Path to the output (grayscale) image
output_image_path = 'gray_map.png'  # Replace with your desired output path

# Read the image
image = cv2.imread(input_image_path)

# Check if image was successfully read
if image is not None:
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Save the grayscale image
    cv2.imwrite(output_image_path, gray_image)
    print(f"Grayscale image saved as '{output_image_path}'.")
else:
    print(f"Error: The file '{input_image_path}' does not exist or is not an image.")
