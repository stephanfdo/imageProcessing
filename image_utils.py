def show_image(title, image):
    """Helper function to display images using OpenCV."""
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
