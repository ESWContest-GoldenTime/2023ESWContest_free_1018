import cv2
import mysql.connector
import numpy as np

# Connect to MySQL database
connection = mysql.connector.connect(
    host="192.168.200.116",
    port=3306,
    user="briankim",
    password="DBK*0825ek",
    database="fall_detection"
)

# Create a cursor object
cursor = connection.cursor()

# SQL query to select all the images from the table
sql = "SELECT encoded_frame FROM raw_images"

# Execute the SQL query
cursor.execute(sql)

# Fetch all the rows
rows = cursor.fetchall()

# Loop through the rows and display each image
for row in rows:
    # Get the image data
    image_data = row[0]

    # Convert the binary data to a numpy array
    np_array = np.frombuffer(image_data, np.uint8)

    # Decode the numpy array as an image
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    # Display the image in a window
    cv2.imshow('Image from Database', image)

    # Wait for 30ms before moving on to the next frame
    # This creates a frame rate of about 33fps
    # You can adjust this value if needed
    cv2.waitKey(30)

# Destroy all the windows created by OpenCV
cv2.destroyAllWindows()

# Close the cursor and connection
cursor.close()
connection.close()