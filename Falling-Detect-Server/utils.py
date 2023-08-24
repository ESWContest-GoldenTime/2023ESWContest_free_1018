import numpy as np
import cv2

def preproc(image, resize_fn):
    """preprocess function for CameraLoader.
    """
    image = resize_fn(image)
    
    # Open CV color map is BGR instead of RGB => modification required
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    return image



def kpt2bbox(kpt, ex=20):
    """Get bbox that hold on all of the keypoints (x,y)
    kpt: array of shape `(N, 2)`,
    ex: (int) expand bounding box,
    """
    return np.array((kpt[:, 0].min() - ex, kpt[:, 1].min() - ex,
                     kpt[:, 0].max() + ex, kpt[:, 1].max() + ex))


