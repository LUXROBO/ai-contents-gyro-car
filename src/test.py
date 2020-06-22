import modi
import time

bundle = modi.MODI(3)

gyro = bundle.gyros[0]


while True:
    aX = gyro.get_acceleration_x()
    aY = gyro.get_acceleration_y()
    aZ = gyro.get_acceleration_z()
    gX = gyro.get_angular_vel_x()
    gY = gyro.get_angular_vel_y()
    gZ = gyro.get_angular_vel_z()
    roll = gyro.get_roll()
    pitch = gyro.get_pitch()
    yaw = gyro.get_yaw()
    vi = gyro.get_vibration()
    time.sleep(0.01)

    print('aX, aY, aZ, gX, gY, gZ, roll, pitch, yaw, vi', aX, aY, aZ,
          #gX, gY, gZ,
          roll, pitch, yaw,
          #vi
          )