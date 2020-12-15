import sys
sys.path.insert(0, '/home/pi/workspace/ai-contents-gyro-car/src')

from gesture_detection import DetectGesture
import modi
import time
import board
import neopixel
import sounddevice as sd
import soundfile as sf
from multiprocessing import Process

wav_path = '/home/pi/workspace/ai-contents-gyro-car/src/img/'

def play_beep(wavfile):
#     data, fs = sf.read('/usr/src/rpi-daemon-py/sound/beep.wav', dtype="float32")
    data, fs = sf.read(wav_path + wavfile, dtype="float32")
    sd.play(data, fs)
    sd.wait()


if __name__ == "__main__":
    # 네트워크 모듈의 uuid를 확인해주세요.
    bundle_ble = modi.MODI(conn_mode="ble", uuid="5BCAF0B0") # 예시(uuid="ABCD1234")

    gyro = bundle_ble.gyros[0]
    btn = bundle_ble.buttons[0]
    
    bundle_can = modi.MODI()
    mot = bundle_can.motors[0]
    
    dg = DetectGesture()
    
    p = Process(target=play_beep, args=('sound01.wav',))
    p.start()
  
#     play_beep('sound01.wav')
    
    while True:
        time.sleep(0.1)
#         print("버튼을 더블클릭하면 출발합니다")
        if btn.double_clicked:
            print("출발!")
            mot.speed = 35, -35
            time.sleep(0.1)
            while True:
#                 print("버튼을 눌러 데이터를 수집해보세요. 멈추려면 버튼을 더블클릭하세요.", end='\r')
                if btn.clicked:
                    pred = dg.predict(gyro, btn) #pred 변수에, 예측값을 받아와 저장합니다.
                    time.sleep(0.1)
                    # 사용자 코드 영역
                    # =======================================================
                    if pred == 'back':
                        mot.speed = -30,30
                        time.sleep(0.1)
                        print('car : back!')
                    elif pred == 'go':
                        mot.speed = 30, -30
                        time.sleep(0.1)
                        print('car : go!')
                    elif pred == 'left':
                        mot.speed = 30, 30
                        time.sleep(0.1)
                        print('car : left!')
                    elif pred == 'right':
                        mot.speed = -30, -30
                        time.sleep(0.1)
                        print('car : right!')
                        
                    p1 = Process(target=play_beep, args=('button8.wav',))
                    p1.start()   
                    p1.join()
                    #=======================================================

                time.sleep(0.1)
                if btn.double_clicked:
                    print("stop!")
                    mot.speed = 0, 0
                    time.sleep(0.1)
                    break
    p.join()
    
