print("Spiker System Modules - Starting to Import")
import serial
import numpy as np
import pandas as pd
import time
import warnings
from serial.tools import list_ports
print("Spiker System Modules - Finished Importing")

import joblib
from utils.function_live_stream import process_low_pass_fft, process_gaussian_fft, live_streamer_KNN


class SpikerBox:
    def __init__(self, interface, baudrate=230400, inputBufferSize=8000, data_queue=None, simulate=False):
        self.interface = interface
        self.baudrate = baudrate
        self.inputBufferSize = inputBufferSize
        self.serial_port = None
        self.timeout = self.inputBufferSize / 6666.0 # 0.5 seconds of data, 20000 = 1 second
        self.stop_requested = False
        self.simulate = simulate
        warnings.simplefilter(action='ignore', category=FutureWarning)

    @staticmethod
    def get_ports():
        ports = [port.device for port in list_ports.comports()]
        # for port in ports:
        #     if port == '/dev/cu.BLTH' or '/dev/cu.Bluetooth-Incoming-Port':
        #         ports.remove(port)
        return ports

    def init_serial(self, port):
        self.serial_port = serial.Serial(port=port, baudrate=self.baudrate, timeout=self.timeout)
    
    def generate_random_data(self):
        return np.random.randint(400, 600, self.inputBufferSize).tolist()

    def read_arduino(self):
        if self.simulate:
            data = self.generate_random_data()
        else:
            data = self.serial_port.read(self.inputBufferSize)
        out = [(int(byte)) for byte in data]
        return out

    def process_data(self, data):
        data_in = np.array(data)
        result = []
        i = 1
        while i < len(data_in) - 1:
            if data_in[i] > 127:
                intout = (np.bitwise_and(data_in[i], 127)) * 128
                i += 1
                intout += data_in[i]
                result.append(intout)
            i += 1
        return result
    
    def continuously_read(self):
        model_path = "utils/model.joblib"
        model = None
        try:
            model = joblib.load(model_path)
        except Exception as e:
            print(f"Failed to load the model from {model_path}: {e}")


        event_window = []

        if not self.serial_port is None:
            row_counter = 0
            try:
                while not self.stop_requested:
                    state = ""
                    data = self.read_arduino()
                    processed_data = self.process_data(data)

                    if len(processed_data)>0:
                        T = self.inputBufferSize/20000.0*np.linspace(0,1,len(processed_data))
                        sigma_gauss = 25
                        data_temp_filtered0 = process_gaussian_fft(T, processed_data, sigma_gauss)
                        data_temp_filtered = process_low_pass_fft(T,data_temp_filtered0,10)

                        time_indices = list(range(row_counter, row_counter + len(data_temp_filtered)))
                        time_indices = [index / 10000 for index in time_indices]

                        row_counter += len(data_temp_filtered)
                        df = pd.DataFrame({
                            'Time': time_indices,
                            'Frequency': data_temp_filtered
                        })

                    
                        row_counter = 0

                        chunk_std = df['Frequency'].std()

                        if chunk_std > 10:
                            event_window.append(df)

                        else:
                            if event_window:       
                                event_window = pd.concat(event_window)
                                # print(len(event_window))
                                for i in range(len(event_window)):
                                    event_window['Time'].iloc[i] = i/10000
                                parameters = (live_streamer_KNN(model, event_window))
                                prediction = (model.predict(parameters))
                                # print("hi", event_window['Time'].iloc[-1])
                                self.interface.game_frame.video_frame.latency = (event_window['Time'].iloc[-1])
                                time.sleep(0.2)

                                print(prediction)

                            event_window = []


                        try:
                            if prediction == [0]:
                                state = "no event"
                            elif prediction == [1]:
                                state = "left"
                            elif prediction == [2]:
                                state = "right"
                            elif prediction == [3]:
                                state = "eyebrow"
                            elif prediction == [4]:
                                state = "blink"
                            prediction = 0

                        except:
                            print("Waiting for Event")
                        
                        if state == "left":
                            self.interface.numLookLeft += 1
                            self.interface.eyeAction = "Looked Left"
                        elif state == "right":
                            self.interface.eyeAction = "Looked Right"
                        elif state == "eyebrow": # or "eyebrow"
                            self.interface.eyeAction = "Eyebrow"
                            if self.interface.game_frame.video_frame.video_playing == True:
                                print("\nVideo was playing, now ending\n")
                                # self.interface.game_frame.distraction_frame.video_ended()
                                self.interface.trigger_handler()
                            else:
                                print("\nAttempted to end video\n")

                        # self.interface.dfAmplitudeAvg = chunk_std

                        # df.to_csv("eyebrow1.csv")

                        # time.sleep(self.timeout)
            finally:
                self.close_serial()

    def close_serial(self):
        if self.serial_port and self.serial_port.isOpen():
            self.serial_port.flushInput()
            self.serial_port.flushOutput()
            self.serial_port.close()
