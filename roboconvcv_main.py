import time
import cv2
from roboconvcv_imgframe import Frame, PiCam
from roboconvcv_database import DBConnection
from roboconvcv_ssc32 import SSC32RoboticArm
from roboconvcv_conveyor import ConveyorBelt
import roboconvcv_constants as constants

frame_count = 0
reset_count = 0

prev_img = []

prev_c_x, prev_c_y = 0, 0
c_x, c_y = 0, 0

if __name__ == '__main__':
    db = DBConnection()
    robo_arm = SSC32RoboticArm(constants.ssc32_serial_port,
                               constants.ssc32_baud_rate)
    conveyor = ConveyorBelt()
    camera = PiCam()
    conveyor.start()

    robo_arm.reset_ready(2)

    db.log_start_conv()

    for frame in camera.cam.capture_continuous(camera.raw_cap,
                                               format="bgr",
                                               use_video_port=True):
        if frame_count <= 1:
            prev_img = Frame(frame.array)

        img = Frame(frame.array)
        canny_diff = img.canny_difference(prev_img)
        c_x, c_y = img.centroid(canny_diff)

        if reset_count > 1:
            print(" > Movement Magnitude:", img.frame_magnitude)

            if constants.cv_lower_bound < c_x < constants.cv_upper_bound:
                conveyor.change_dc(constants.conveyor_low_dc)
                db.log_slow_conv()
                print(" >> close to center")

                if constants.cv_hard_lower_bound < c_x < constants.cv_hard_upper_bound:
                    conveyor.change_dc(constants.conveyor_stop_dc)
                    db.log_stop_conv()
                    db.log_ssc_take_item()
                    print(" >>> at center")
                    time.sleep(1)
                    robo_arm.grab_drop_ready(1)
                    img.frame_magnitude = 0
                    c_x, c_y = -1, -1
                    camera.raw_cap.truncate(0)
                    continue

            else:
                conveyor.change_dc(constants.conveyor_high_dc)
                db.log_start_conv()

        c_x, c_y = img.centroid(canny_diff)

        if frame_count % constants.cv_frames_before_refresh == 0:
            reset_count += 1
            prev_img = Frame(frame.array)
            c_x, c_y = 0, 0

        cv2.circle(canny_diff, (c_x, constants.cv_half_y_dim), 5, (255, 255, 255), -1)
        cv2.imshow("Difference Frame", canny_diff)
        prev_c_x, prev_c_y = c_x, c_y

        camera.raw_cap.truncate(0)
        frame_count += 1

        print(f"{frame_count}")
        print(" > Movement Magnitude:", img.frame_magnitude)
        print(constants.cv_lower_bound,
              constants.cv_hard_lower_bound,
              c_x,
              constants.cv_hard_upper_bound,
              constants.cv_upper_bound)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    exit()
