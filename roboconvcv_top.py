import time
import cv2
from roboconvcv_imgframe import Frame, PiCam
from roboconvcv_database import DBConnection
from roboconvcv_ssc32 import SSC32RoboticArm
from roboconvcv_conveyor import ConveyorBelt
import roboconvcv_constants as constants
import threading

if __name__ == '__main__':
    db = DBConnection()
    robo_arm = SSC32RoboticArm(constants.ssc32_serial_port,
                               constants.ssc32_baud_rate)
    conveyor = ConveyorBelt()
    camera = PiCam()
    conveyor.start()

    command = False


    def listener():
        query = "SELECT * FROM command"
        db.execute("USE Proyek6_IEE3031")
        while True:
            db.execute(query)
            command_post = db.c.fetchall()
            print(command_post[0])
            time.sleep(0.3)
            global command


    def main_funct():

        frame_count = 0
        reset_count = 0

        prev_img = []

        prev_c_x, prev_c_y = 0, 0
        c_x, c_y = 0, 0
        global command
        print(f"Command: {command}")
        if command:
            robo_arm.reset_ready(2)

            for frame in camera.cam.capture_continuous(camera.raw_cap,
                                                       format="bgr",
                                                       use_video_port=True):
                img = Frame(frame.array)

                if frame_count <= 1:
                    prev_img = Frame(frame.array)

                if frame_count % constants.cv_frames_before_refresh == 0:
                    reset_count += 1
                    prev_img = Frame(frame.array)

                canny_diff = img.canny_difference(prev_img)
                magnitude = img.fast_sum_image(canny_diff)
                c_x, c_y = img.centroid(canny_diff)

                cv2.circle(canny_diff, (c_x, c_y), 5, (255, 255, 255), -1)
                cv2.line(canny_diff,
                         (0, 0),
                         (100, 100),
                         (0, 0, 255), 5)

                cv2.imshow("Difference Frame", canny_diff)
                cv2.imshow("Canny Frame", img.canny_edges)

                centroid_pos_condition = constants.cv_hard_lower_bound < c_x < constants.cv_hard_upper_bound
                magnitude_size_condition = constants.cv_magnitude_lower_boundary < magnitude < constants. \
                    cv_magnitude_upper_boundary

                print(f"FRAME: {frame_count}")
                print(f" > Movement Magnitude : {magnitude_size_condition} : ", end=" ")
                print(
                    f"{constants.cv_magnitude_lower_boundary} < {magnitude} < {constants.cv_magnitude_upper_boundary}")
                print(f" > Centroid: {centroid_pos_condition} : ", end=" ")
                print(f"{constants.cv_lower_bound} < "
                      f"{constants.cv_hard_lower_bound} < "
                      f"{c_x} < "
                      f"{constants.cv_hard_upper_bound} < "
                      f"{constants.cv_upper_bound}")

                if constants.cv_lower_bound < c_x < constants.cv_upper_bound:
                    print(" >> close to center")
                    conveyor.change_dc(constants.conveyor_low_dc)

                    if centroid_pos_condition and magnitude_size_condition:
                        print(" >>> at center", end=" ")
                        print(constants.cv_hard_lower_bound,
                              c_x,
                              constants.cv_hard_upper_bound)
                        conveyor.change_dc(constants.conveyor_stop_dc)

                        time.sleep(0.5)
                        robo_arm.grab_drop_ready(1)

                        magnitude = 0
                        c_x, c_y = 0, 0
                        camera.raw_cap.truncate(0)
                        time.sleep(0.5)
                        continue

                else:

                    conveyor.change_dc(constants.conveyor_high_dc)

                prev_c_x, prev_c_y = c_x, c_y

                camera.raw_cap.truncate(0)
                frame_count += 1

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cv2.destroyAllWindows()
            exit()


    print("meng")
    threading.Thread(target=listener).start()
    print("thread1")
    threading.Thread(target=main_funct).start()
    print("thread2")
