# Import mavutil
from pymavlink import mavutil
import time


class SensorsCollector:

    def __init__(self, master):

        self.master = master
        self.prev_imu_reading = "0" * 36
        self.prev_pressure_reading = "0" * 6
        self.prev_temp_reading = "0" * 6


    def __zfill(self, num):
        return "0" * (6 - len(num)) + num

    def get_IMU(self):
        msg = self.master.recv_match(type="SCALED_IMU2")
        if not msg:
            return None
        
        imu_dic = msg.to_dict()

        imu_values = [imu_dic["xacc"] , imu_dic["yacc"] , imu_dic["zacc"] , imu_dic["xgyro"] , imu_dic["ygyro"] , imu_dic["zgyro"]]

        # pad the values to be 6byte each
        imu_values = [self.__zfill(str(imu_values[i])) for i in range(len(imu_values))]
        # convert the list to string and remove the brackets
        imu_values =''.join(map(str, imu_values))

        # save the last imu values so that it be used when current read value is none
        self.prev_imu_reading = imu_values

        return imu_values  # xacc yacc zacc xgyro ygro zgyro

    def get_SCALED_PRESSURE2(self):
        msg = self.master.recv_match(type="SCALED_PRESSURE2")
        if not msg:
            return None
        
        pressure_dic = msg.to_dict()
        pressure_value = int((pressure_dic["press_abs"]))
        pressure_value = round(pressure_value, 2) / 1000

        # pad the values to be 6byte
        pressure_value = self.__zfill(str(pressure_value))
        # save the last pressure value so that it be used when current read value is none
        self.prev_pressure_reading = pressure_value

        return pressure_value  # pressure

    def get_SCALED_PRESSURE3(self):
        msg = self.master.recv_match(type="SCALED_PRESSURE3")
        if not msg:
            return None

        temp_value = msg.to_dict()["temperature"]
        temp_value = round(temp_value, 1) / 100

        # pad the values to be 6byte
        temp_value = self.__zfill(str(temp_value))
        # save the last temp value so that it be used when current read value is none
        self.prev_temp_reading = temp_value

        return temp_value  # temp

    def read_sensors(self):

        sensors_readings = ""

        # read imu sensor
        imu_reading = self.get_IMU()

        sensors_readings += (
            imu_reading if imu_reading is not None else self.prev_imu_reading
        )

        # read pressure sensor
        pressure_reading = self.get_SCALED_PRESSURE2()
  
        sensors_readings += (
            pressure_reading
            if pressure_reading is not None
            else self.prev_pressure_reading
        )

        # read temprature sensor
        temp_reading = self.get_SCALED_PRESSURE3()
        sensors_readings += (
            temp_reading if temp_reading is not None else self.prev_temp_reading
        )

        return sensors_readings


if "__main__" == __name__:

    master = mavutil.mavlink_connection("COM22",115200)
    master.wait_heartbeat()

    sensors_collector = SensorsCollector(master)

    while True:

        sensors_readings = sensors_collector.read_sensors()
        #print(sensors_readings)

        time.sleep(0.01)