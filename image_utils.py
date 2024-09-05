def show_image(title, image):
    """Helper function to display images using OpenCV."""
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def manual_transformation(image):
    """Allows the user to manually select four points for perspective transformation."""
    clone = image.copy()
    points = []

    def select_point(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            points.append((x, y))
            cv2.circle(clone, (x, y), 5, (0, 255, 0), -1)
            cv2.imshow("Select points", clone)
        if len(points) == 4:
            cv2.destroyAllWindows()

    cv2.imshow("Select points", clone)
    cv2.setMouseCallback("Select points", select_point)
    cv2.waitKey(0)

    if len(points) == 4:
        points = np.array(points, dtype="float32")
        (tl, tr, br, bl) = points
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))
        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype="float32")
        M = cv2.getPerspectiveTransform(points, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
        return warped
    else:
        print("You need to select exactly four points!")
        return None
