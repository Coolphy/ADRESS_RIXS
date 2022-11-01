import scripts_generator as sg
import copy

def run(num):

    path = "C:\\Researches\\Scripts\\plotRIXS\\test\\"
    atom = 'Cr'
    file_name = path.replace('\\','/') + atom + f'_{num:04d}_d1.h5'
    return file_name


sg.init()

print(sg.current.pos)

sampleA = sg.create()
sampleA.load(run(26))

# wrong copy with
# sampleA = current
sampleB = copy.deepcopy(sampleA)

sg.drive(sampleA)
sg.acquire(5)
sampleA.set('samt',50)
sg.drive(sampleA)
sg.acquire(5)
sampleA.set('energy',300)
sg.drive(sampleA)
sg.acquire(5)

sg.fprint(r'C:\Researches\Scripts\plotRIXS\generator\text.txt')