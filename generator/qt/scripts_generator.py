import h5py
import numpy as np
import copy


class manipulator:
    def __init__(self):
        self.motor = {}
        self.motor["samx"] = 0.0
        self.motor["samy"] = 0.0
        self.motor["samz"] = 0.0
        self.motor["samt"] = 0.0
        self.motor["phi"] = 0.0
        self.motor["tilt"] = 0.0
        # self.motor['temperature'] = 0

    def write(self, key):
        command_string = ""
        command_string = command_string + "moveto {0} {1:.3f}".format(
            key, self.motor[key]
        )
        return command_string


class beamline:
    def __init__(self):
        self.motor = {}
        self.motor["energy"] = 0.0
        self.motor["polar"] = 0
        self.motor["split"] = 0
        self.motor["exposure"] = 0
        # self.motor['slits'] = 10

    def write(self, key):
        command_string = ""
        if key == "energy":
            command_string = command_string + "set {0}={1:.2f}".format(
                key, self.motor[key]
            )
        elif key == "polar":
            polar_string = polar_mode_to_string(int(self.motor[key]))
            command_string = command_string + "set {0}={1}".format(key, polar_string)
        elif key == "split":
            command_string = command_string + "set {0}={1:d}".format(
                key, int(self.motor[key])
            )
        elif key == "exposure":
            seconds = int(self.motor[key])
            m, s = divmod(seconds, 60)
            # h, m = divmod(m, 60)
            command_string = command_string + "set {0}={1:02d}:{2:02d}".format(
                key, m, s
            )
        return command_string


class temperature:
    def __init__(self):
        self.temperature = {}
        self.temperature["TEMP"] = 0
        self.temperature["TEMP-B"] = 0
        self.temperature["FM"] = 0
        self.temperature["HT-RNG"] = 0

    def set(self, val):
        self.temperature["TEMP-B"] = val


class slits:
    def __init__(self) -> None:
        pass


class shutter:
    def __init__(self):
        self.shutter = {}
        self.shutter["SPVG1"] = 0
        self.shutter["SH1"] = 1

    def close(self):
        self.shutter["SPVG1"] = 0
        self.shutter["SH1"] = 1

    def open(self):
        self.shutter["SPVG1"] = 1
        self.shutter["SH1"] = 0

    def write(self):
        command_string = ""
        command_string = command_string + "caput X03MA-ES2-SPVG1:WT_SET {:d}\n".format(
            self.shutter["SPVG1"]
        )
        command_string = command_string + "caput X03MA-OP-SH1:WT_SET {:d}\n".format(
            self.shutter["SH1"]
        )
        return command_string


class create:
    def __init__(self):
        self.manipulator = manipulator()
        self.beamline = beamline()
        self.pos = {}
        self.pos.update(self.manipulator.motor)
        self.pos.update(self.beamline.motor)
        self.pos["polar"] = polar_mode_to_string(self.beamline.motor["polar"])

    def print(self):
        print(self.pos)

    def set(self, key, val):
        manipulator_list = ["samx", "samy", "samz", "samt", "phi", "tilt"]
        beamline_list = ["energy", "polar", "split", "exposure"]
        if key in manipulator_list:
            self.manipulator.motor[key] = val
        elif key in beamline_list:
            self.beamline.motor[key] = val
        elif key == "acquire":
            self.acquire = val
        else:
            print(f"# Wrong key {key}")
        self.pos.update(self.manipulator.motor)
        self.pos.update(self.beamline.motor)
        self.pos["polar"] = polar_mode_to_string(self.beamline.motor["polar"])


def polar_mode_to_string(polar_mode):
    if polar_mode == 0:
        polar_string = "LH"
    elif polar_mode == 1:
        polar_string = "LV"
    elif polar_mode == 2:
        polar_string = "C+"
    elif polar_mode == 3:
        polar_string = "C-"
    return polar_string


def drive(object):
    global command_text
    command_string = ""
    manipulator_list = ["samx", "samy", "samz", "samt", "phi", "tilt"]
    beamline_list = ["energy", "polar", "split", "exposure"]

    for key in manipulator_list:
        if abs(object.manipulator.motor[key] - current.manipulator.motor[key]) < 0.001:
            pass
        else:
            command_string = (
                command_string + "{}".format(object.manipulator.write(key)) + "\n"
            )
            current.set(key, object.manipulator.motor[key])
    if command_string == "":
        command_string = "moveby samz 0.005\n"

    for key in beamline_list:
        if abs(object.beamline.motor[key] - current.beamline.motor[key]) < 0.005:
            pass
        else:
            command_string = (
                command_string + "{}".format(object.beamline.write(key)) + "\n"
            )
            current.set(key, object.beamline.motor[key])
    # print(command_string)
    command_text = command_text + command_string


def acquire(num, moveby=1):
    global command_text
    command_string = ""
    if moveby == 1:
        command_string = command_string + "acquire\n"
        for x in range(num - 1):
            command_string = command_string + "moveby samz 0.005\n"
            current.set("samz", current.manipulator.motor["samz"] + 0.005)
            command_string = command_string + "acquire\n"
    else:
        for x in range(num):
            command_string = command_string + "acquire\n"
    # print(command_string)
    command_text = command_text + command_string


def init():
    global current, command_text
    current = create()
    command_text = ""


def fprint(file_name):
    global command_text
    # f = open(file_name, "w")
    # f.write(command_text)
    # f.close()
    print(command_text)

    return command_text


def load(sample_dict):
    for index in sample_dict:
        if index == 0:
            sample = create()
        for driver in sample_dict[index]:
            if sample_dict[index][driver] is not None:
                sample.set(driver, sample_dict[index][driver])

        drive(sample)
        acquire(int(sample_dict[index]["acquire"]))


if __name__ == "__main__":
    init()
    # current.print()
