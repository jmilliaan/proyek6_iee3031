import cv2
from roboconvcv_imgframe import Frame, PiCam
from roboconvcv_database import DBConnection
from roboconvcv_ssc32 import SSC32RoboticArm
from roboconvcv_conveyor import ConveyorBelt
import roboconvcv_constants as constants

db = DBConnection()
robo_arm = SSC32RoboticArm(constants.ssc32_serial_port, constants.ssc32_baud_rate)
conveyor = ConveyorBelt()
camera = PiCam()

frame_count = 0
reset_count = 0

prev_img = []

prev_c_x, prev_c_y = 0, 0
c_x, c_y = 0, 0

if __name__ == '__main__':
    robo_arm.reset_ready(1)
    conveyor.start()
    for frame in camera.cam.capture_continuous(camera.raw_cap,
                                               format="bgr",
                                               use_video_port=True):

        img = Frame(frame.array)
        canny_diff = img.canny_difference(prev_img)
        c_x, c_y = img.centroid(canny_diff)

        if frame_count <= 1:
            prev_img = Frame(frame.array)

        centroid_vec_x = c_x - prev_c_x
        centroid_vec_y = c_y - prev_c_y

        if abs(centroid_vec_x) < constants.cv_vector_min_x:
            centroid_vec_x = 0

        if abs(centroid_vec_y) < constants.cv_vector_min_y:
            centroid_vec_y = 0

        print(" > Mvmnt Mag:", img.frame_magnitude)
        print(constants.cv_lower_bound,
              constants.cv_hard_lower_bound,
              c_x,
              constants.cv_hard_upper_bound,
              constants.cv_upper_bound)

        if reset_count > 1:
            if constants.cv_lower_bound < c_x < constants.cv_upper_bound:
                conveyor.change_dc(constants.conveyor_low_dc)
                print("  >> close to center")
                if constants.cv_hard_lower_bound < c_x < constants.cv_hard_upper_bound:
                    conveyor.change_dc(constants.conveyor_stop_dc)
                    print("  >> at center")
                    robo_arm.grab_drop_ready(2)
            else:
                conveyor.change_dc(constants.conveyor_high_dc)

        if frame_count % constants.cv_frames_before_refresh == 0:
            reset_count += 1
            prev_img = Frame(frame.array)
            c_x, c_y = 0, 0

        cv2.circle(canny_diff, (c_x, constants.cv_half_y_dim), 5, (255, 255, 255), -1)
        cv2.imshow("Difference Frame", canny_diff)
        prev_c_x, prev_c_y = c_x, c_y

        camera.raw_cap.truncate(0)
        frame_count += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    exit()
