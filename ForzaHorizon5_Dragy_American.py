import socket
import struct
import tkinter as tk
import time
import threading

ascii_art = """
███████╗██╗  ██╗███████╗    ██████╗ ██████╗  █████╗  ██████╗██╗   ██╗
██╔════╝██║  ██║██╔════╝    ██╔══██╗██╔══██╗██╔══██╗██╔════╝╚██╗ ██╔╝
█████╗  ███████║███████╗    ██║  ██║██████╔╝███████║██║  ███╗╚████╔╝ 
██╔══╝  ██╔══██║╚════██║    ██║  ██║██╔══██╗██╔══██║██║   ██║ ╚██╔╝  
██║     ██║  ██║███████║    ██████╔╝██║  ██║██║  ██║╚██████╔╝  ██║   
╚═╝     ╚═╝  ╚═╝╚══════╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝   ╚═╝                                                                                                                     
"""

print(ascii_art)
# UDP Settings
UDP_IP = "127.0.0.1"
UDP_PORT = 5300
BUFFER_SIZE = 1500

# Reading the data format
data_types = {
    'IsRaceOn': 's32',
    'TimestampMS': 'u32',
    'EngineMaxRpm': 'f32',
    'EngineIdleRpm': 'f32',
    'CurrentEngineRpm': 'f32',
    'AccelerationX': 'f32',
    'AccelerationY': 'f32',
    'AccelerationZ': 'f32',
    'VelocityX': 'f32',
    'VelocityY': 'f32',
    'VelocityZ': 'f32',
    'AngularVelocityX': 'f32',
    'AngularVelocityY': 'f32',
    'AngularVelocityZ': 'f32',
    'Yaw': 'f32',
    'Pitch': 'f32',
    'Roll': 'f32',
    'NormalizedSuspensionTravelFrontLeft': 'f32',
    'NormalizedSuspensionTravelFrontRight': 'f32',
    'NormalizedSuspensionTravelRearLeft': 'f32',
    'NormalizedSuspensionTravelRearRight': 'f32',
    'TireSlipRatioFrontLeft': 'f32',
    'TireSlipRatioFrontRight': 'f32',
    'TireSlipRatioRearLeft': 'f32',
    'TireSlipRatioRearRight': 'f32',
    'WheelRotationSpeedFrontLeft': 'f32',
    'WheelRotationSpeedFrontRight': 'f32',
    'WheelRotationSpeedRearLeft': 'f32',
    'WheelRotationSpeedRearRight': 'f32',
    'WheelOnRumbleStripFrontLeft': 's32',
    'WheelOnRumbleStripFrontRight': 's32',
    'WheelOnRumbleStripRearLeft': 's32',
    'WheelOnRumbleStripRearRight': 's32',
    'WheelInPuddleDepthFrontLeft': 'f32',
    'WheelInPuddleDepthFrontRight': 'f32',
    'WheelInPuddleDepthRearLeft': 'f32',
    'WheelInPuddleDepthRearRight': 'f32',
    'SurfaceRumbleFrontLeft': 'f32',
    'SurfaceRumbleFrontRight': 'f32',
    'SurfaceRumbleRearLeft': 'f32',
    'SurfaceRumbleRearRight': 'f32',
    'TireSlipAngleFrontLeft': 'f32',
    'TireSlipAngleFrontRight': 'f32',
    'TireSlipAngleRearLeft': 'f32',
    'TireSlipAngleRearRight': 'f32',
    'TireCombinedSlipFrontLeft': 'f32',
    'TireCombinedSlipFrontRight': 'f32',
    'TireCombinedSlipRearLeft': 'f32',
    'TireCombinedSlipRearRight': 'f32',
    'SuspensionTravelMetersFrontLeft': 'f32',
    'SuspensionTravelMetersFrontRight': 'f32',
    'SuspensionTravelMetersRearLeft': 'f32',
    'SuspensionTravelMetersRearRight': 'f32',
    'CarOrdinal': 's32',
    'CarClass': 's32',
    'CarPerformanceIndex': 's32',
    'DrivetrainType': 's32',
    'NumCylinders': 's32',
    'HorizonPlaceholder': 'hzn',
    'PositionX': 'f32',
    'PositionY': 'f32',
    'PositionZ': 'f32',
    'Speed': 'f32',
    'Power': 'f32',
    'Torque': 'f32',
    'TireTempFrontLeft': 'f32',
    'TireTempFrontRight': 'f32',
    'TireTempRearLeft': 'f32',
    'TireTempRearRight': 'f32',
    'Boost': 'f32',
    'Fuel': 'f32',
    'DistanceTraveled': 'f32',
    'BestLap': 'f32',
    'LastLap': 'f32',
    'CurrentLap': 'f32',
    'CurrentRaceTime': 'f32',
    'LapNumber': 'u16',
    'RacePosition': 'u8',
    'Accel': 'u8',
    'Brake': 'u8',
    'Clutch': 'u8',
    'HandBrake': 'u8',
    'Gear': 'u8',
    'Steer': 's8',
    'NormalizedDrivingLine': 's8',
    'NormalizedAIBrakeDifference': 's8'
}

# Byte size for each data type
jumps = {
    's32': 4,
    'u32': 4,
    'f32': 4,
    'u16': 2,
    'u8': 1,
    's8': 1,
    'hzn': 12
}

def get_data(data):
    return_dict = {}
    passed_data = data
    for i in data_types:
        d_type = data_types[i]
        jump = jumps[d_type]
        current = passed_data[:jump]
        
        decoded = 0
        if d_type == 's32':
            decoded = int.from_bytes(current, byteorder='little', signed=True)
        elif d_type == 'u32':
            decoded = int.from_bytes(current, byteorder='little', signed=False)
        elif d_type == 'f32':
            decoded = struct.unpack('f', current)[0]
        elif d_type == 'u16':
            decoded = struct.unpack('H', current)[0]
        elif d_type == 'u8':
            decoded = struct.unpack('B', current)[0]
        elif d_type == 's8':
            decoded = struct.unpack('b', current)[0]
        
        return_dict[i] = decoded
        passed_data = passed_data[jump:]
    return return_dict

# Tkinter GUI for overlay
class SpeedOverlay:
    def __init__(self, root):
        self.root = root
        self.root.geometry("150x125+0+0")
        self.root.title("Speed Timer")
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(1)
        self.root.config(bg='black')

        # Labels for times, boost, and status
        self.label_boost = tk.Label(root, text="Boost: 0.00 psi", font=("Helvetica", 10, "bold"), fg="white", bg="black")
        self.label_boost.pack()

        self.label_status = tk.Label(root, text="Ready to measure", font=("Helvetica", 10, "bold"), fg="white", bg="black")
        self.label_status.pack()

        self.label_times = tk.Label(root, text="0-60: N/A\n60-130: N/A\n130-190: N/A", font=("Helvetica", 10, "bold"), fg="white", bg="black", justify="left")
        self.label_times.pack()


    def update_times(self, t_0_60, t_60_130, t_130_190):
        self.label_times.config(text=f"0-60: {t_0_60:.2f}s\n60-130: {t_60_130:.2f}s\n130-190: {t_130_190:.2f}s")

    def update_boost(self, boost_psi):
        self.label_boost.config(text=f"Boost: {boost_psi :.2f} psi")

    def reset_times(self):
        # Reset times to N/A in the overlay
        self.label_times.config(text="0-60: N/A\n60-130: N/A\n130-190: N/A")
        self.label_status.config(text="Ready to measure")

    def update_status(self, status):
        self.label_status.config(text=status)

# Socket setup
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# Timing variables using time.perf_counter for higher precision
start_0_60, start_60_130, start_130_190 = None, None, None
t_0_60, t_60_130, t_130_190 = None, None, None

def measure_speed(overlay):
    global start_0_60, start_60_130, start_130_190, t_0_60, t_60_130, t_130_190

    while True:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        returned_data = get_data(data)
        speed_kmh = returned_data['Speed'] * 3.6
        speed_mph = speed_kmh * 0.621371  # Convert km/h to mph
        boost_value = returned_data['Boost']

        # Update boost in overlay 
        overlay.update_boost(boost_value)

        # Measure 0-60 mph time (about 0-100 km/h)
        if speed_mph > 10 and start_0_60 is None:
            start_0_60 = time.perf_counter()  # Use high-precision timer
            overlay.update_status("Measuring")
        elif speed_mph >= 60 and start_0_60 and not t_0_60:
            t_0_60 = time.perf_counter() - start_0_60  # Calculate with precision
            print(f"0-60 mph: {t_0_60:.2f} seconds")

        # Measure 60-130 mph time
        if speed_mph >= 60 and start_60_130 is None:
            start_60_130 = time.perf_counter()  # Start timer for 60-130
        elif speed_mph >= 130 and start_60_130 and not t_60_130:
            t_60_130 = time.perf_counter() - start_60_130  # Measure with precision
            print(f"60-130 mph: {t_60_130:.2f} seconds")

        # Measure 130-190 mph time
        if speed_mph >= 130 and start_130_190 is None:
            start_130_190 = time.perf_counter()  # Start timer for 130-190
        elif speed_mph >= 190 and start_130_190 and not t_130_190:
            t_130_190 = time.perf_counter() - start_130_190  # Measure with precision
            print(f"130-190 mph: {t_130_190:.2f} seconds")

        # Reset all times if speed goes below 10 mph
        if speed_mph < 10:
            start_0_60, start_60_130, start_130_190 = None, None, None
            t_0_60, t_60_130, t_130_190 = None, None, None
            overlay.reset_times()

        # Update times in overlay
        overlay.update_times(t_0_60 or 0, t_60_130 or 0, t_130_190 or 0)

        time.sleep(0.005)  # Reduce delay for more frequent updates

if __name__ == "__main__":
    root = tk.Tk()
    overlay = SpeedOverlay(root)

    # Run speed measurement in a separate thread
    threading.Thread(target=measure_speed, args=(overlay,), daemon=True).start()

    root.mainloop()
