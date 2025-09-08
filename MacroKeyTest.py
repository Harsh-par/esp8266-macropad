import serial
import time
import webbrowser
import serial.tools.list_ports
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import wmi

# Variables for Port connection
SerialPort = None
BaudRate = 115200
RetryConnectSeconds = 3

Esp8266_vid = 6790
Esp8266_pid = 29987

# Variables for Audio
try:
    AudioDevices = AudioUtilities.GetSpeakers()
    AudioInterface = AudioDevices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    Volume = AudioInterface.QueryInterface(IAudioEndpointVolume)
except Exception:
    Volume = None

# Variables for Screen brightness
try:
    BrightnessInterface = wmi.WMI(namespace='wmi')
    BrightnessMethods = BrightnessInterface.WmiMonitorBrightnessMethods()[0]
except Exception:
    BrightnessMethods = None

def FindPort():
    try:
        DevicePorts = serial.tools.list_ports.comports()
        for Port in DevicePorts:
            if Port.vid == Esp8266_vid and Port.pid == Esp8266_pid:
                try:
                    _SerialPort = serial.Serial(Port.device, BaudRate, timeout=1)
                    print(f"Connected to : {Port.device}")
                    return _SerialPort
                except (OSError, serial.SerialException):
                    pass
    except Exception:
        pass
    return None

def IncreaseVolume(VolumeStep=0.1):
    if Volume:
        CurrentVolume = Volume.GetMasterVolumeLevelScalar()
        Volume.SetMasterVolumeLevelScalar(min(1.0, CurrentVolume + VolumeStep), None)

def DecreaseVolume(VolumeStep=0.1):
    if Volume:
        CurrentVolume = Volume.GetMasterVolumeLevelScalar()
        Volume.SetMasterVolumeLevelScalar(max(0.0, CurrentVolume - VolumeStep), None)

def MuteAudio():
    if Volume:
        Volume.SetMute(not Volume.GetMute(), None)

def IncreaseBrightness(BrightnessStep=10):
    if BrightnessMethods:
        try:
            Brightness = BrightnessInterface.WmiMonitorBrightness()[0].CurrentBrightness
            new = min(100, Brightness + BrightnessStep)
            BrightnessMethods.WmiSetBrightness(new, 0)
        except Exception:
            pass

def DecreaseBrightness(BrightnessStep=10):
    if BrightnessMethods:
        try:
            Brightness = BrightnessInterface.WmiMonitorBrightness()[0].CurrentBrightness
            new = max(0, Brightness - BrightnessStep)
            BrightnessMethods.WmiSetBrightness(new, 0)
        except Exception:
            pass

while True:
    try:
        if SerialPort is None or not SerialPort.is_open:
            if SerialPort:
                try:
                    SerialPort.close()
                except:
                    pass
                SerialPort = None

            SerialPort = FindPort()
            if SerialPort is None:
                time.sleep(RetryConnectSeconds)
                continue

        SerialInput = SerialPort.readline().decode(errors='ignore').strip()
        if not SerialInput:
            continue

        print(f"Received: {SerialInput}")

        if SerialInput == "Button Pressed : 1":
            webbrowser.open("https://chat.openai.com/")
        elif SerialInput == "Button Pressed : 2":
            webbrowser.open("https://discord.com/channels/@me")
        elif SerialInput == "Button Pressed : 3":
            webbrowser.open("https://www.youtube.com/")

        elif SerialInput == "Button Pressed : 4":
            webbrowser.open("https://mail.google.com/")
        elif SerialInput == "Button Pressed : 5":
            webbrowser.open("https://google.com/")
        elif SerialInput == "Button Pressed : 6":
            webbrowser.open("https://docs.google.com/")

        elif SerialInput == "Button Pressed : 7":
            IncreaseVolume()
        elif SerialInput == "Button Pressed : 8":
            DecreaseVolume()
        elif SerialInput == "Button Pressed : 9":
            MuteAudio()

        elif SerialInput == "Button Pressed : 10":
            IncreaseBrightness()
        elif SerialInput == "Button Pressed : 11":
            DecreaseBrightness()
        elif SerialInput == "Button Pressed : 12":
            pass

        elif SerialInput == "Button Pressed : 13":
            pass
        elif SerialInput == "Button Pressed : 14":
            pass
        elif SerialInput == "Button Pressed : 15":
            pass

    except (serial.SerialException, OSError):
        if SerialPort:
            try:
                SerialPort.close()
            except:
                pass
        SerialPort = None
        time.sleep(RetryConnectSeconds)
    except Exception:
        time.sleep(1)
