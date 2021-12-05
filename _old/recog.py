import cv2
from capture_class import Frame

x_dim = 640
y_dim = 480

half_x_dim = int(x_dim / 2)
half_y_dim = int(y_dim / 2)

max_frame_difference = 255 * x_dim * y_dim

canny_min = 100
canny_max = 120

frame_count = 0

prev_c_x, prev_c_y = 0, 180
c_x, c_y = 0, 180

vector_min_x = int(x_dim / 10)
vector_min_y = int(y_dim / 10)

frames_before_refresh = 3

magnitude_threshold = 0.005


def matrix_sum(mat):
    bigmat = []
    arrsum = 0
    y_size = len(mat)
    x_size = len(mat[0])
    for i in range(y_size):
        arrsum += sum(mat[i])
    return arrsum / max_frame_difference


vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)
vid.set(3, x_dim)
vid.set(4, y_dim)

initial_ret, initial_frame = vid.read()
prev_frame = Frame(initial_frame)

while True:

    frame_count += 1

    ret, frame = vid.read()
    next_frame = Frame(frame)

    # difference between current and previous image
    diff = cv2.subtract(next_frame.blur(1), prev_frame.blur(1))
    canny_diff = cv2.Canny(diff, canny_min, canny_max)
    t_res, thresh = cv2.threshold(canny_diff, 127, 255, 0)

    thresh_mag = matrix_sum(thresh)

    # centroid calculation
    moments = cv2.moments(thresh)

    if thresh_mag > magnitude_threshold:
        if moments["m00"] != 0:
            c_x = int(moments["m10"] / moments["m00"])
            c_y = int(moments["m01"] / moments["m00"])

    centroid_vec_x = c_x - prev_c_x
    centroid_vec_y = c_y - prev_c_y

    if abs(centroid_vec_x) < vector_min_x:
        centroid_vec_x = 0
    if abs(centroid_vec_y) < vector_min_y:
        centroid_vec_y = 0

    if centroid_vec_x > 0:
        print("right")
    elif centroid_vec_x < 0:
        print("left")

    if frame_count % frames_before_refresh == 0:
        frame_count = 0
        prev_frame = Frame(frame)
    cv2.circle(thresh, (c_x, half_y_dim), 5, (255, 255, 255), -1)
    cv2.imshow("Difference Frame", thresh)
    prev_c_x, prev_c_y = c_x, c_y
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
