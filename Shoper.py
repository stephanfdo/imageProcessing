
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
    
       # Find contours and select the largest one
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

    screenCnt = None
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            screenCnt = approx
            break

    # If no contour with four points is detected, ask for manual input
    if screenCnt is None:
        print("No contour with four points detected. Please manually select the corners.")
        warped = manual_transformation(orig)
        if warped is not None:
            processed_image = sharpen_and_close(warped)
            cv2.imwrite(os.path.join("outputImages", "processed_image.png"), processed_image)

            show_image("processed Image", processed_image)
            text_extraction(processed_image)
    else:
        print("STEP 2: Find contours of paper")
        cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
        show_image("Outline", image)

        warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
        processed_image = sharpen_and_close(warped)
        text_extraction(processed_image)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Please provide the image path as a command-line argument.")




  