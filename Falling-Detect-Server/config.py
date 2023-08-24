import argparse

def argument_parser():
    parser = argparse.ArgumentParser(description='Human Fall Detection Demo.')
    
    parser.add_argument('-C', '--camera', default="rtsp://192.168.200.117:8555/unicast",  # required=True,  # default=2,
                        help='Source of camera or video file path.')
    
    
    parser.add_argument('--detection_input_size', type=int, default=384,
                        help='Size of input in detection model in square must be divisible by 32 (int).')
    parser
    parser.add_argument('--pose_input_size', type=str, default='224x160',
                        help='Size of input in pose model must be divisible by 32 (h, w)')
    parser.add_argument('--pose_backbone', type=str, default='resnet50',
                        help='Backbone model for SPPE FastPose model.')
    parser.add_argument('--show_detected', default=False, action='store_true',
                        help='Show all bounding box from detection.')
    parser.add_argument('--show_skeleton', default=True, action='store_true',
                        help='Show skeleton pose.')
    parser.add_argument('--device', type=str, default='cuda',
                        help='Device to run model on cpu or cuda.')
    
    # saving the output
    parser.add_argument('--save_video', default=False,action ='store_true',
                        help='Save the outpout file for detection and tracking')
    parser.add_argument("--saving_path",type=str,default="/home/briankim/Development/Dataset/")
    parser.add_argument("--fps",type = int,default = 30)
    
    
    # MySQL Database configure
    # parser.add_argument('--host', type=str, default="118.176.122.86",
    #                     help='MySQL Host')
    parser.add_argument('--host', type=str, default="192.168.200.116",
                        help='MySQL Host')
    parser.add_argument('--port', type=int, default=3306,
                        help='MySQL Port Number')
    parser.add_argument('--user', type=str,default="briankim",help="MySQL username")
    parser.add_argument('--password', type=str,default="DBK*0825ek",help="MySQL password")
    parser.add_argument('--database', type=str,default="fall_detection",help="MySQL database name")
    
    # Firebase configure
    parser.add_argument('--certificate',type=str,default="/home/briankim/Development/Human-Falling-Detect-Tracks/goldentime1-75942-firebase-adminsdk-3mmy8-8f095b53f2.json")
    parser.add_argument('--storage_url', type=str,default='goldentime1-75942.appspot.com')
    parser.add_argument('--fcm_token',type=str,default = "eYJicP5aR6mYbHWtMhqu3e:APA91bElYpBZ8y8uMGSg2J5TEBdNHJmTHIGx5VnemBL3LpBRPX4btc3FeWGcQTqqj2_W7ePskiTTJmUuhSEFZ3DM7xZnXGWMwrZ4Afpwwemol_w74APH8Lp5PbwoDS7nFqlmAGp56ErL")
    
    return parser