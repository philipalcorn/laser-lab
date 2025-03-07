
from pylablib.core.gui.utils import get_relative_position
from pylablib.devices import Thorlabs
import pylablib as pll
from pylablib.devices.Thorlabs import kinesis
from pylablib.devices.Thorlabs import TLCamera
from pylablib.devices import uc480
from pylablib.devices.uc480.uc480 import TAcquiredFramesStatus


import numpy as np
import os
import cv2
import time
from thorlabs_tsi_sdk.tl_camera import TLCameraSDK, OPERATION_MODE

camera_enable = True
motor_enable = False

swap_motors = False

print(Thorlabs.list_kinesis_devices())




#print(uc480.list_cameras())
#print(list_instruments())

#basically stops the motors from runnign while I am working on the camera
if(motor_enable):
    motor_x_id = int(kinesis.list_kinesis_devices()[1][0])
    motor_y_id = int(kinesis.list_kinesis_devices()[0][0])

    if (swap_motors):
        motor_x_id = int(kinesis.list_kinesis_devices()[0][0])
        motor_y_id = int(kinesis.list_kinesis_devices()[1][0])

    motor_x = kinesis.KinesisMotor(motor_x_id)
    motor_y = kinesis.KinesisMotor(motor_y_id)

    #motorx = kinesis.KinesisMotor(27002966) # the brush motor Id would need to
    #motory = kinesis.KinesisMotor(27002991)# be changed if the motors get replaced

    #move to zero zero before moving to start position
    motor_x.home(0)
    motor_x.wait_for_stop()
    motor_y.home(0)
    motor_y.wait_for_stop()

    print("Home Position: Currently at (",motor_x.get_position(),",",motor_y.get_position(),")")

    motor_x.move_to(2)
    motor_x.wait_for_stop()
    motor_y.move_to(2)
    motor_y.wait_for_stop()
    print("move_to() position: \n",motor_x.get_position(),",",motor_y.get_position(),",")


#cam =Thorlabs.ThorlabsTLCamera(serial="4103252793")
if(camera_enable):
    cam = uc480.UC480Camera(cam_id=0)

    cam.open()
    print(cam.get_detector_size())
    if(not cam.is_opened()):
        #Throw Error
        pass

    cam.setup_acquisition(nframes=100)
    cam.start_acquisition()
    cam.wait_for_frame()
    image = cam.read_newest_image()
    cam.stop_acquisition()
    cam.close()
    #image = cam.snap(timeout=5.0, return_info=True)
    if image is not None:
        plt.imshow(image)
        plt.show()
    else:
        print("Failed to capture an image")

    print(cam.get_frame_format())
    #'list': list of 2d arraws
    cam.close()
    #cam.setup_acquisition(nframes=100)
