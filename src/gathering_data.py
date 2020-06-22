import modi
import time
import numpy as np
import pandas as pd
from IPython.display import clear_output

class DataGathering(object):

    def record_motion(self, btn, gyro):
        print('recording')
        print('ready')
        time.sleep(0.3)
        print('3')
        time.sleep(0.3)
        print('2')
        time.sleep(0.3)
        print('1')
        time.sleep(0.3)
        print('start!')
        self.l = []
        self.X = None
        self.X_df = None
        while True:
            time.sleep(0.01)

            self.aX = gyro.get_acceleration_x()
            self.aY = gyro.get_acceleration_y()
            self.aZ = gyro.get_acceleration_z()
            self.gX = gyro.get_angular_vel_x()
            self.gY = gyro.get_angular_vel_y()
            self.gZ = gyro.get_angular_vel_z()
            self.roll = gyro.get_roll()
            self.pitch = gyro.get_pitch()
            self.yaw = gyro.get_yaw()
            self.vi = gyro.get_vibration()
            self.l.append((self.aX,self.aY,self.aZ,self.gX,self.gY,self.gZ,self.roll,self.pitch,self.yaw,self.vi))
            print('aX, aY, aZ, gX, gY, gZ, roll, pitch, yaw, vi', self.aX, self.aY, self.aZ,
                                                                self.gX, self.gY, self.gZ,
                                                                self.roll, self.pitch, self.yaw,
                                                                self.vi)
            clear_output(wait=True)


            if btn.get_clicked():
                self.X = np.array(self.l)[5:-5]
                print(self.X)
                if len(self.X) > 50:
                    self.X_tr = self.X[::2][:25]

                    self.X_df = pd.DataFrame(self.X_tr,
                                             columns=['aX', 'aY', 'aZ', 'gX', 'gY', 'gZ', 'roll', 'pitch', 'yaw', 'vi'])

                else:
                    print('data is too short')
                    #raise ValueError('data is too short')
                # 전처리 필요
                # 최대 길이에 맞출 경우, 1 처럼 모션 시간이 짧은 데이터는 결측값이 존재하게 됨. 이부분을 평균값으로 처리할지, 이전값으로 처리할지에 대한 부분

                # self.X_df = pd.DataFrame(self.X_tr, columns=['aX', 'aY', 'aZ', 'gX', 'gY', 'gZ', 'roll', 'pitch', 'yaw', 'vi'])
                break
        return self.X_df


    def normalization():
        pass





def main():
    bundle = modi.MODI(3)
    gyro = bundle.gyros[0]
    btn = bundle.buttons[0]
    i = 1
    dg = DataGathering()

    while True:
        df = dg.record_motion(btn, gyro)
        filename = '../data/new.csv' # go 를 모을 데이터 명으로 바꾼 다음 실행
        with open(filename, 'a') as f:
            f.write('\n')
        df.to_csv(filename, mode='a', header=False)
        i += 1
        print("collected data : ", i)

    


if __name__ == "__main__":
    main()