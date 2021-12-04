from flask import Flask
from flask import request, Response, render_template, redirect, url_for
import serial
import webbrowser
from multiprocessing import Process, Queue
import time

app = Flask(__name__)
app.config["SECRET_KEY"]= 'a65643b9b52d637a11b3182e923e5703'

class SerialProcess:
    actions = {}

    def __init__(self):
        self.ser = serial.Serial("/dev/tty.usbmodem14101", 9600)
        self.queue = Queue()
        self.serialIOProcess = Process(target=self.serial_io_loop, args=(self.queue,))

    def serial_io_loop(self, queue):
        while 1:
            if (self.ser.in_waiting > 0):
                out = self.ser.readline().decode("utf-8")
                queue.put(out)
                print(out)

    def start_process(self):
        self.serialIOProcess.start()

    def end_process(self):
        self.serialIOProcess.terminate()



@app.route("/enableserial", methods=["POST", "GET"])
def enable():
    if request.method == "POST":
        print(serialP.ser)
        #serialP.start_process()
        return ""




@app.route("/serialdata")
def data():
    if not serialP.queue.empty():
        return serialP.queue.get()
    return ""

@app.route("/console")
def dashboard():
    return render_template("serial.html")

if __name__ == '__main__':

    serialP = SerialProcess()
    serialP.start_process()

    try:
        command = 'g'
        while (command is not 'e'):
            #Process generally do not receive signals, including KeyboardInterrupt
            # so this helps with killing the process properly
            command = input()
            b = bytes(command, 'utf-8')
            serialP.ser.write(b)
            time.sleep(1)
        serialP.end_process()

    except KeyboardInterrupt:
        serialP.end_process()


    #app.run(host="0.0.0.0", port="8081")
