from pyzbar.pyzbar import decode
from playsound import playsound
import pandas as pd
import cv2
import time
import urllib.request
import numpy as np


class BarCodeScanner:
    def __init__(self):
        self.url = 'http://192.168.0.155:8080/shot.jpg'
        self.cod_decode()
        self.cod = None

    def cod_decode(self):
        while True:
            time.sleep(2)
            result_decode = self.get_cod()
            if result_decode:
                playsound('beep.mp3')
                for result in result_decode:
                    cod = str(result.data).split("'")[1]
                    self.add_clip_board(cod)
                    print(result)

            if cv2.waitKey(1) == ord('q'):
                break

        cv2.destroyAllWindows()

    def get_cod(self):
        img_resp = urllib.request.urlopen(self.url)
        img_np = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        img = cv2.imdecode(img_np, cv2.IMREAD_GRAYSCALE)
        cv2.imshow('Leitor', img)
        img_code = img
        result_decode = decode(img_code)

        return result_decode

    def add_clip_board(self, text):
        df = pd.DataFrame([text])
        df.to_clipboard(index=False, header=False)


app = BarCodeScanner()
