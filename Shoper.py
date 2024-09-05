
def main(image_path):
    # Load the image from a file
    image = cv2.imread(image_path)

    # Resize the image and perform edge detection
    ratio = image.shape[0] / 500.0
    orig = image.copy()
    image = imutils.resize(image, height=500)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 200)

    print("STEP 1: Edge Detection")
    show_image("Original Image", image)
    show_image("Edged Image", edged)
    cv2.imwrite(os.path.join("outputImages", "gray_image.png"), gray)
    cv2.imwrite(os.path.join("outputImages", "edged_image.png"), edged)
    



  