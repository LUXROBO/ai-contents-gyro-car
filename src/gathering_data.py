import os
import sys
import time
import numpy as np
import pandas as pd
import sounddevice as sd
import soundfile as sf
import modi

from pandas import DataFrame
from IPython.display import clear_output,display
from matplotlib import pyplot as plt
from sklearn.preprocessing import Normalizer,MaxAbsScaler
from multiprocessing import Process

wav_path = '/home/pi/workspace/ai-contents-gyro-car/src/img/'


def play_beep(wavfile):
    data, fs = sf.read(wav_path + wavfile, dtype="float32")
    sd.play(data, fs)
    sd.wait()


class DataGathering:
    def record_motion(self, btn, gyro):
        clear_output(wait=True)
        print('데이터 수집을 시작합니다.')
        print('ready')
        time.sleep(1)
        print('3')
        time.sleep(1)
        print('2')
        time.sleep(1)
        p = Process(target=play_beep, args=('sound02.wav',))
        p.start()
        print('1')
        time.sleep(1)
        print('start!')
        self.l = []
        self.X = None
        self.X_df = None
        self.X_sc = None
        while True:
            time.sleep(0.01)

            self.aX = gyro.acceleration_x
            self.aY = gyro.acceleration_y
            self.aZ = gyro.acceleration_z

            self.roll = gyro.roll
            self.pitch = gyro.pitch
            self.yaw = gyro.yaw
            self.l.append((self.aX,self.aY,self.aZ,self.roll,self.pitch,self.yaw))

            print("데이터 수집 중. 수집을 종료하려면 버튼을 누르세요.")
            print(
                '현재 자이로 센서 데이터',
                self.aX, self.aY, self.aZ, self.roll, self.pitch, self.yaw
            )
            clear_output(wait=True)

            if btn.clicked:
                p.join()
                p = Process(target=play_beep, args=('sound04.wav',))
                p.start()
                self.X = np.array(self.l)[5:-5]
                if len(self.X) > 50:
                    itr = len(self.X) // 25
                    self.X_tr = self.X[::itr][:25]

                    self.X_df = pd.DataFrame(
                        self.X_tr,
                        columns=['aX', 'aY', 'aZ', 'roll', 'pitch', 'yaw']
                    )
                    self.X_df.plot()
                    plt.show()

                    scaler = MaxAbsScaler()
                    scaler.fit(self.X_df)
                    self.X_sc = DataFrame(
                        scaler.transform(self.X_df),
                        columns=['aX', 'aY', 'aZ', 'roll', 'pitch', 'yaw']
                    )
                    time.sleep(0.01)

                else:
                    print('데이터 길이가 너무 짧습니다. 데이터가 저장되지 않았습니다.')
                    time.sleep(1)
                    print('조금만 천천히 그려보세요.')
                    time.sleep(1)
                # 전처리 필요
                # 최대 길이에 맞출 경우, 1 처럼 모션 시간이 짧은 데이터는 
                # 결측값이 존재하게 됨. 이부분을 평균값으로 처리할지,
                # 이전값으로 처리할지에 대한 부분

                p.join()
                break
        return self.X_sc

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
            print(
                filename, "데이터의 ", str(record_index + 1), 
                "번째 데이터 수집을 시작하려면 버튼을 클릭하세요. ",
                "데이터 수집을 종료하려면 버튼을 더블클릭하세요.", end='\r'
            )
            time.sleep(0.1)
            if btn.clicked:
                clear_output(wait=True)
                print(str(record_index+1), ' 번째 데이터 수집을 시작합니다.')
                print('ready')
                time.sleep(0.5)
                print('3')
                time.sleep(0.5)
                print('2')
                time.sleep(0.5)
                print('1')
                time.sleep(0.5)
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
                    self.roll = gyro.roll
                    self.pitch = gyro.pitch
                    self.yaw = gyro.yaw
                    self.l.append(
                        (self.aX,self.aY,self.aZ,self.roll,self.pitch,self.yaw)
                    )
                    print(
                        str(record_index+1), 
                        " 번째 데이터 수집 중. 수집을 종료하려면 버튼을 누르세요."
                    )
                    print(
                        '현재 자이로 센서 데이터',
                        self.aX, self.aY, self.aZ,
                        self.roll, self.pitch, self.yaw
                    )
                    clear_output(wait=True)

                    if btn.clicked:
                        dg = DataFrame(self.l)
                        self.X = np.array(self.l)[5:-5]
                        if len(self.X) > 50:
                            itr = len(self.X) // 25
                            self.X_tr = self.X[::itr][:25]

                            self.X_df = pd.DataFrame(
                                self.X_tr,
                                columns=['aX', 'aY', 'aZ', 'roll', 'pitch', 'yaw']
                            )
                            self.X_df.plot()
                            plt.show()
                            scaler = MaxAbsScaler()
                            scaler.fit(self.X_df)
                            self.X_sc = DataFrame(
                                scaler.transform(self.X_df),
                                columns=['aX', 'aY', 'aZ', 'roll', 'pitch', 'yaw']
                            )
                            time.sleep(0.1)

                        else:
                            print('데이터 길이가 너무 짧습니다. 데이터가 저장되지 않았습니다.')
                            time.sleep(1)
                            print('조금만 천천히 그려보세요.')
                            time.sleep(1)
                            break
                        # 전처리 필요
                        # 최대 길이에 맞출 경우, 1 처럼 모션 시간이 짧은 데이터는 
                        # 결측값이 존재하게 됨. 이부분을 평균값으로 처리할지,
                        # 이전값으로 처리할지에 대한 부분

                        filepath = "../data/" + filename + ".csv"
                        with open(filepath, 'a') as f:
                            f.write('\n')

                        if record_index == 0:
                            self.X_sc.to_csv(filepath, mode='a', header=True)
                        else:
                            self.X_sc.to_csv(filepath, mode='a', header=False)

                        print(str(record_index+1), '번째 데이터가 저장되었습니다.')
                        time.sleep(0.1)
                        break
    
    # print number of collected data
    def check_data(self):
        frame = DataFrame(columns = ["파일 이름", "수집된 데이터 개수"])
        path = "../data"
        try:
            os.removedirs(path+"/.ipynb_checkpoints")
        except:
            pass
        file_list = os.listdir(path)
        print(file_list)

        for i in range(len(file_list)):
            df = pd.read_csv("../data/" + file_list[i], engine='python' )
            record_index = int((df.shape[0]+1) / 25)
            frame.loc[i+1] = [file_list[i],record_index]

        display(frame)


def main():
    bundle = modi.MODI(3)
    gyro = bundle.gyros[0]
    btn = bundle.buttons[0]
    dg = DataGathering()

    i = 1
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
