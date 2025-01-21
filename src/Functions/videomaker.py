import os
import cv2


def create_simulation_video(plots_dir, output_dir):
    """
    Creates a video from the simulation plot images.
    
    Args:
        plots_dir: Directory containing the plot images
        output_dir: Directory where the video will be saved
    """
    # Get all PNG files in the plots directory and sort them numerically
    image_files = [f for f in os.listdir(plots_dir) if f.endswith('.png')]
    image_files.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))
    
    if not image_files:
        print("No image files found for video creation")
        return
    
    # Get the full path of the first image
    first_image_path = os.path.join(plots_dir, image_files[0])
    
    # Read the first image to determine dimensions
    frame = cv2.imread(first_image_path)
    if frame is None:
        print(f"Error reading image: {first_image_path}")
        return
        
    height, width, layers = frame.shape
    
    # Create the output video file
    video_path = os.path.join(output_dir, "simulation.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # Using 10 frames per second for a smooth visualization
    video = cv2.VideoWriter(video_path, fourcc, 10, (width, height))
    
    # Write each image to the video
    try:
        for image_file in image_files:
            image_path = os.path.join(plots_dir, image_file)
            frame = cv2.imread(image_path)
            if frame is not None:
                video.write(frame)
            else:
                print(f"Error reading image: {image_path}")
    finally:
        # Ensure proper cleanup of resources
        video.release()
    
    print(f"Video created successfully: {video_path}")