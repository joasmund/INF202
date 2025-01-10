import cv2 # requires opencv-python

# Get the list of image files in the directory
images = [f"tmp/img_{i}.png" for i in range(0,20)]

# determine dimension from first image
frame = cv2.imread(images[0])
height, width, layers = frame.shape

## Define the codec and create a VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # or 'XVID', 'DIVX', 'mp4v' etc.
video = cv2.VideoWriter("video.mp4", fourcc, 5, (width, height))  # 5 frames per second

for image in images:
    video.write(cv2.imread(image))

cv2.destroyAllWindows()
video.release()
