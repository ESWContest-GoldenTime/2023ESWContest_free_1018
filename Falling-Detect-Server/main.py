import os
import io
import cv2
import time
import torch
import numpy as np
import time

from functools import partial

from Detection.Utils import ResizePadding
from CameraLoader import CamLoader, CamLoader_Q
from DetectorLoader import TinyYOLOv3_onecls

from PoseEstLoader import SPPE_FastPose
from fn import draw_single

from Track.Tracker import Detection, Tracker
from ActionsEstLoader import TSSTG

# Main Configure
from config import argument_parser

# Video Buffer Object
from Video_Buffer import VideoBuffer

# Database function
from database_function import mysql_config, firebase_config, push_mySQL, send_to_token, frames_to_video_buffer, upload_video_firebase

# Image utils
from utils import preproc, kpt2bbox

def main(args):
    
    # Database configure
    connection, cursor = mysql_config(args)
    fcm_token, bucket = firebase_config(args)
    
    device = args.device

    # DETECTION MODEL.
    inp_dets = args.detection_input_size
    detect_model = TinyYOLOv3_onecls(inp_dets, device=device)

    # POSE MODEL.
    inp_pose = args.pose_input_size.split('x')
    inp_pose = (int(inp_pose[0]), int(inp_pose[1]))
    pose_model = SPPE_FastPose(args.pose_backbone, inp_pose[0], inp_pose[1], device=device)

    # Tracker.
    max_age = 30
    tracker = Tracker(max_age=max_age, n_init=3)

    # Actions Estimate.
    action_model = TSSTG()

    # Resizing function for the model
    resize_fn = ResizePadding(inp_dets, inp_dets)


    # DataLoader -> no ground truth or other metadata, only the image itself
    cam_source = args.camera
    
    
    
    if type(cam_source) is str and os.path.isfile(cam_source):
        # Use loader thread with Q for video file.
        preproc_with_resize = partial(preproc, resize_fn=resize_fn)
        cam = CamLoader_Q(cam_source, queue_size=1000, preprocess=preproc_with_resize).start()
        
    else:
        # Use normal thread loader for webcam.
        preproc_with_resize = partial(preproc, resize_fn=resize_fn)
        cam = CamLoader(int(cam_source) if cam_source.isdigit() else cam_source,
                        preprocess=preproc_with_resize).start()

    #frame_size = cam.frame_size
    #scf = torch.min(inp_size / torch.FloatTensor([frame_size]), 1)[0]


    if args.save_video:
        os.makedirs(args.saving_path,exist_ok=True)
        save_path = os.path.join(args.saving_path,"human_output.mp4")
        codec = cv2.VideoWriter_fourcc(*'avc1')
        writer = cv2.VideoWriter(save_path, codec, args.fps, (inp_dets * 2, inp_dets * 2))


    fps_time = 0
    t = 0
    
    # From here, the every frame is grabbed
    
    
    # video buffer object for saving the actual images and the encoded byte data
    video_buffer = VideoBuffer()
    byte_buffer = VideoBuffer()
    
    # Save the number of frames, after falling
    frames_after_falling = 0
    
    
    # Default
    Falling_Detected = False
    
    # For database testing
    
    # Falling_Detected = True
    
    while cam.grabbed():
        
        current_time = time.time()
        t += 1
        frame = cam.getitem()
        
        image = frame.copy() # image has the copy of an image => original image
        #image = frame.deepcopy() 
        
        # Detect humans bbox in the frame with detector model.
        detected = detect_model.detect(frame, need_resize=False, expand_bb=10)

        # Predict each tracks bbox of current frame from previous frames information with Kalman filter.
        tracker.predict()
        # Merge two source of predicted bbox together.
        for track in tracker.tracks:
            det = torch.tensor([track.to_tlbr().tolist() + [0.5, 1.0, 0.0]], dtype=torch.float32)
            detected = torch.cat([detected, det], dim=0) if detected is not None else det

        detections = []  # List of Detections object for tracking.
        if detected is not None:
            #detected = non_max_suppression(detected[None, :], 0.45, 0.2)[0]
            # Predict skeleton pose of each bboxs.Human-Falling-Detect-Tracks
            track_id = track.track_id
            bbox = track.to_tlbr().astype(int)
            center = track.get_center().astype(int)

            action = 'pending..'
            clr = (0, 255, 0)

            # Use 30 frames time-steps to prediction.
            if len(track.keypoints_list) == 30:
                pts = np.array(track.keypoints_list, dtype=np.float32)
                out = action_model.predict(pts, frame.shape[:2])
                action_name = action_model.class_names[out[0].argmax()]
                action = '{}: {:.2f}%'.format(action_name, out[0].max() * 100)

                if action_name == 'Fall Down':
                    clr = (255, 0, 0)
                    a = np.zeros_like(image, dtype=np.uint8)
                    a[:, :, 0] = 50  # Increase the red channel by 50
                    image = np.clip(image + a, 0, 255)
                    frame = np.clip(frame + a, 0, 255)
                    Falling_Detected = True

                
                elif action_name == 'Lying Down':
                    clr = (255, 200, 0)



            # # VISUALIZE.
            if track.time_since_update == 0:
                if args.show_skeleton:
                    frame = draw_single(frame, track.keypoints_list[-1])
                frame = cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 1)
                frame = cv2.putText(frame, str(track_id), (center[0], center[1]), cv2.FONT_HERSHEY_COMPLEX,
                                    0.4, (255, 0, 0), 2)
                frame = cv2.putText(frame, action, (bbox[0] + 5, bbox[1] + 15), cv2.FONT_HERSHEY_COMPLEX,
                                    0.4, clr, 1)


        # For 
        # print("time consumed for making visualization: " + str(time.time() - current_time))
        # # Show Frame.
        frame = cv2.resize(frame, (0, 0), fx=2., fy=2.)
        frame = cv2.putText(frame, '%d, FPS: %f' % (t, 1.0 / (time.time() - fps_time)),
                            (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        frame = frame[:, :, ::-1]
        fps_time = time.time()
        print("time consumed for total frame : " + str(time.time() - current_time))
        
        
        
        video_buffer.add_frame(image)

        # encode the data for mySQL
        is_success, encoded_image = cv2.imencode(".jpg", image)


        if is_success:
           # append the videos into the object afther converting the encoded image to bytes
            binary_data = encoded_image.tobytes()
            byte_buffer.add_frame(binary_data)

        print(f"frames after falling:{frames_after_falling}")
        
        if Falling_Detected and frames_after_falling < 240:
            frames_after_falling +=1
        
    
        elif frames_after_falling == 240:
            
            # Send the byte images in the video_buffer
            Video = frames_to_video_buffer(video_buffer.get_all_frames())
            
            # Send Alarm using firebase
            send_to_token(fcm_token)
            
            # Send the Video to firebase
            upload_video_firebase(Video, 'videos/example_song.mp4', bucket = bucket)
            
            # Send the Video to MySQL
            push_mySQL(cursor,connection,byte_buffer)
            
            # Reset the video and byte buffer
            video_buffer.clear()
            byte_buffer.clear()
            
            # Reset the interruption
            Falling_Detected = False
            frames_after_falling = 0
            
            print("Data pushed")
        
        
        if args.save_video:
            writer.write(frame)
            print("time consumed for write video : " + str(time.time() - current_time))
        
        
        # visualize the video if possible
        try:
            cv2.imshow('frame', frame)
            print("time consumed for imshow : " + str(time.time() - current_time) + "\n")
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
        except Exception as e:
            print(f"Caught exception of type {type(e)}: {e}")
            pass

    # Clear resource.
    cam.stop()
    if args.save_video:
        writer.release()

    cv2.destroyAllWindows()

        
    # Close the cursor and connection
    cursor.close()
    connection.close()
  
    print("Main Function Finished")



if __name__ == '__main__':
    
    # Check if X-forwarding is not connected
    if not os.environ.get('DISPLAY'):
        os.environ['QT_QPA_PLATFORM'] = 'offscreen'
        
        
    parser = argument_parser()
    args = parser.parse_args()

    main(args)
