from gesture_detection import DetectGesture
import modi
import time


def main():
    bundle = modi.MODI(3)
    gyro = bundle.gyros[0]
    btn = bundle.buttons[0]
    mot = bundle.motors[0]
    dg = DetectGesture()

    while True:
        time.sleep(0.1)
        if btn.get_double_clicked():
            print("start!")
            #mot.set_speed(25, -25)
            time.sleep(0.1)
            while True:


                if btn.get_clicked():
                    pred = dg.predict(gyro, btn)
                    time.sleep(0.1)
                    print("prediction : ", pred)
                    # 사용자 코드 영역
                    # =======================================================
                    if pred == 'back':
                        #mot.set_speed(-23,23)
                        time.sleep(0.1)
                        print('car : back!')
                    elif pred == 'go':
                        #mot.set_speed(23, -23)
                        time.sleep(0.1)
                        print('car : go!')
                    elif pred == 'left':
                        #mot.set_speed(23, 23)
                        time.sleep(0.1)
                        print('car : left!')
                    elif pred == 'right':
                        #mot.set_speed(-23, -23)
                        time.sleep(0.1)
                        print('car : right!')




                #=======================================================


                time.sleep(0.1)
                if btn.get_double_clicked():
                    print("stop!")
                    mot.set_speed(0, 0)
                    time.sleep(0.1)
                    break


if __name__ == "__main__":
    main()