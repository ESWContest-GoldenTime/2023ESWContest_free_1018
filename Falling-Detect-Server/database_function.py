import tempfile
import cv2
import io

# Firebase Server
import firebase_admin
from firebase_admin import storage, credentials, messaging, initialize_app

# SQL server
import mysql.connector


def mysql_config(args):
    
# Connect to MySQL database
    connection = mysql.connector.connect(
        host=args.host,
        port=args.port,
        user=args.user,
        password=args.password,
        database=args.database
    )

    # Create a cursor object
    cursor = connection.cursor()
    print("MySQL Connection Succeed!")

    return connection, cursor


def firebase_config(args):
    #firebase server connection 
    cred = credentials.Certificate(args.certificate)

    if not firebase_admin._apps:
        app = firebase_admin.initialize_app(cred, {
            'storageBucket': args.storage_url,
        })

        bucket = storage.bucket(app = app)

    else:
        bucket = storage.bucket()

    print("Firebase Connection Succeed!")


    # token needed for firebase connected application
    fcm_token = args.fcm_token
    
    return fcm_token, bucket



def push_mySQL(cursor, connection, data, table_name = "raw_images"):
    # SQL query to insert the image into the table
    # The table name is "raw_images"
    
    sql = "INSERT INTO {} (frame_name, encoded_frame) VALUES (%s, %s)".format(table_name)

    for binary_data in data.get_all_frames():
        
        values = ("Webcam Image", binary_data)
        # Execute the SQL query
        cursor.execute(sql, values)


    # Commit the transaction
    connection.commit()
    
def send_to_token(registration_token):
    # See documentation on defining a message payload.
    message = messaging.Message(
        notification=messaging.Notification(
            title='Falling Detected!!',
            body='Please check the video',
        ),
        token=registration_token,
    )

    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)
    

def frames_to_video_buffer(frames, fps=30):
    # Check if there are any frames
    if not frames:
        raise ValueError("No frames provided for video creation")

    
    frames = [frame[:, :, ::-1] for frame in frames]
    # Determine the width and height from the first frame
    h, w, _ = frames[0].shape
    size = (w, h)


    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=True) as temp_video_file:
    # Define the codec and create VideoWriter object writing into the buffer
        out = cv2.VideoWriter(temp_video_file.name, cv2.VideoWriter_fourcc(*'avc1'), fps, size)

        for i, frame in enumerate(frames):
            # print(i)
            print(frame)
            out.write(frame)

        out.release()
        video_buffer = io.BytesIO(temp_video_file.read())  # Move buffer position to the beginning
    
    return video_buffer


def upload_video_firebase(video_buffer, destination_name, bucket):
    # Upload the video
    video_buffer.seek(0)
    
    # Upload the video
    blob = bucket.blob(destination_name)
    blob.upload_from_file(video_buffer)
    
    print("Video uploaded.")


def download_video_firebase(source_name, destination_path, bucket):
    """
    Download a video from Firebase Storage.

    Args:
    - source_name (str): The name of the video in Firebase Storage (same as the name you used to upload).
    - destination_path (str): The local path where you want to save the downloaded video.
    - bucket (storage.bucket.Bucket): The Firebase Storage bucket instance.

    Returns:
    None
    """
    
    # Create a blob reference
    blob = bucket.blob(source_name)
    
    # Download the video to the destination path
    blob.download_to_filename(destination_path)

    print(f"Video downloaded to {destination_path}.")
    
# example usage
# download_video('videos/example_Ironman.mp4',"/home/briankim/Development/Dataset/ironman.mp4", bucket)