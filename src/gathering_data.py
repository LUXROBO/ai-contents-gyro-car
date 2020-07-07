import modi
import time
import numpy as np
import pandas as pd
from IPython.display import clear_output
import sys

class DataGathering(object):

    def record_motion(self, btn, gyro):
        clear_output(wait=True)
        print('데이터 수집을 시작합니다.')
        print('ready')
        time.sleep(1)
        print('3')
        time.sleep(1)
        print('2')
        time.sleep(1)
        print('1')
        time.sleep(1)
        print('start!')
        self.l = []
        self.X = None
        self.X_df = None
        while True:
            time.sleep(0.01)

            self.aX = gyro.acceleration_x
            self.aY = gyro.acceleration_y
            self.aZ = gyro.acceleration_z
            self.gX = gyro.angular_vel_x
            self.gY = gyro.angular_vel_y
            self.gZ = gyro.angular_vel_z
            self.roll = gyro.roll
            self.pitch = gyro.pitch
            self.yaw = gyro.yaw
            self.vi = gyro.vibration
            self.l.append((self.aX,self.aY,self.aZ,self.gX,self.gY,self.gZ,self.roll,self.pitch,self.yaw,self.vi))
            # print('aX, aY, aZ, gX, gY, gZ, roll, pitch, yaw, vi', self.aX, self.aY, self.aZ,
            #                                                     self.gX, self.gY, self.gZ,
            #                                                     self.roll, self.pitch, self.yaw,
            #                                                     self.vi)
            print("데이터 수집 중. 수집을 종료하려면 버튼을 누르세요.")
            print('현재 자이로 센서 데이터', self.aX, self.aY, self.aZ, self.gX, self.gY, self.gZ,
                                                                  self.roll, self.pitch, self.yaw, self.vi)
            clear_output(wait=True)


            if btn.clicked:
                self.X = np.array(self.l)[5:-5]
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

    def gathering_motion(self, btn, gyro, filename):
        while True:
            # exit trigger
            if btn.double_clicked:
                clear_output(wait=True)
                print("데이터 수집을 종료합니다.")
                time.sleep(0.1)
                break

            #check csv file and return index of data
            try:
                df = pd.read_csv("../data/" + filename + ".csv")
                record_index = int((df.shape[0]+1) / 25)
            except:
                record_index = 0

            #collect data
            print(filename, "데이터의 ", str(record_index + 1), "번째 데이터 수집을 시작하려면 버튼을 클릭하세요. ",
                                         "데이터 수집을 종료하려면 버튼을 더블클릭하세요.", end='\r')
            time.sleep(0.1)
            if btn.clicked:
                clear_output(wait=True)
                print(str(record_index+1), ' 번째 데이터 수집을 시작합니다.')
                print('ready')
                time.sleep(1)
                print('3')
                time.sleep(1)
                print('2')
                time.sleep(1)
                print('1')
                time.sleep(1)
                print('start!')
                clear_output(wait=True)
                self.l = []
                self.X = None
                self.X_df = None
                while True:
                    time.sleep(0.01)

                    self.aX = gyro.acceleration_x
                    self.aY = gyro.acceleration_y
                    self.aZ = gyro.acceleration_z
                    self.gX = gyro.angular_vel_x
                    self.gY = gyro.angular_vel_y
                    self.gZ = gyro.angular_vel_z
                    self.roll = gyro.roll
                    self.pitch = gyro.pitch
                    self.yaw = gyro.yaw
                    self.vi = gyro.vibration
                    self.l.append((self.aX,self.aY,self.aZ,self.gX,self.gY,self.gZ,self.roll,self.pitch,self.yaw,self.vi))
                    print(str(record_index+1), " 번째 데이터 수집 중. 수집을 종료하려면 버튼을 누르세요.")
                    print('현재 자이로 센서 데이터', self.aX, self.aY, self.aZ, self.gX, self.gY, self.gZ,
                                                                          self.roll, self.pitch, self.yaw, self.vi)
                    clear_output(wait=True)


                    if btn.clicked:
                        self.X = np.array(self.l)[5:-5]
                        #print(self.X)
                        if len(self.X) > 50:
                            self.X_tr = self.X[::2][:25]

                            self.X_df = pd.DataFrame(self.X_tr,
                                                     columns=['aX', 'aY', 'aZ', 'gX', 'gY', 'gZ', 'roll', 'pitch', 'yaw', 'vi'])

                        else:
                            print('데이터 길이가 너무 짧습니다. 다시 그려보세요.')
                            #raise ValueError('data is too short')
                        # 전처리 필요
                        # 최대 길이에 맞출 경우, 1 처럼 모션 시간이 짧은 데이터는 결측값이 존재하게 됨. 이부분을 평균값으로 처리할지, 이전값으로 처리할지에 대한 부분

                        # self.X_df = pd.DataFrame(self.X_tr, columns=['aX', 'aY', 'aZ', 'gX', 'gY', 'gZ', 'roll', 'pitch', 'yaw', 'vi'])
                        filepath = "../data/" + filename + ".csv"

                        with open(filepath, 'a') as f:
                            f.write('\n')
                        self.X_df.to_csv(filepath, mode='a', header=False)
                        print(str(record_index+1), '번째 데이터가 저장되었습니다.')
                        time.sleep(1)
                        clear_output(wait=True)
                        break


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