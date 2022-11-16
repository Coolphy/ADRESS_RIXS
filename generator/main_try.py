import scripts_generator as sg
import copy

def run(num):

    path = "C:\\Researches\\Scripts\\plotRIXS\\generator\\"
    atom = 'Fe'
    file_name = path.replace('\\','/') + atom + f'_{num:04d}_d1.h5'
    return file_name

def moveby_samz(sample):
    current_samz = sample.pos['samz']
    sample.set('samz',current_samz+0.005)
    return sample


sg.init()

sg.current.load(run(75))
# wrong copy with
# sampleA = current

H375 = sg.create()
H375 = copy.deepcopy(sg.current)
H375.set('samt',112.3)
H375.set('phi',4)
H375.set('samz',-2.195)
H375.set('samy',3.13)
H375.set('tilt',2.5)

K375 = copy.deepcopy(copy.deepcopy(H375))
H375.set('samt',112.3)
K375.set('phi',-86)
K375.set('samz',-1.69)
K375.set('samy',3.2)
K375.set('tilt',-1.4)

sg.drive(H375)
sg.acquire(1)
moveby_samz(H375)
sg.drive(K375)
sg.acquire(1)
moveby_samz(K375)
sg.drive(K375)
sg.acquire(1)
moveby_samz(K375)
sg.drive(H375)
sg.acquire(1)
moveby_samz(H375)

sg.fprint(r'C:\Researches\Scripts\plotRIXS\generator\text.txt')

import sys

for path in sys.path:
    print(path)