import sys
import os
# author of the script was Jan Majta, it was only modified by me

atoms = {'1': 'H', '6': 'C', '8': 'O'}


class Frame:

    def __init__(self):
        self.coordinates = []
        self.energy = 'nan'
        self.status = 0
        self.degree = 0

    def __str__(self):
        coords = ['    '.join([atoms[c[1]], c[3], c[4], c[5]]) for c in self.coordinates]
        return '   {}\nscf done: {}\n{}'.format(len(self.coordinates),
                                                self.energy,
                                                '\n'.join(coords))

    def add_coord(self, line):
        self.coordinates.append(line.strip().split())


class Log_file:

    def __init__(self, fname):
        self.fname = fname
        self.frames = []

    def parse(self):
        catch_xyz = False
        with open(self.fname) as fcont:
            for line in fcont:
                if 'D(11,13,14,15)' in line:
                    degree = line.split()[3]
                if line.strip() == 'Input orientation:':
                    # first occurence
                    try:
                        self.frames.append(frame)
                        frame = Frame()
                        frame.degree = degree
                    except NameError:
                        frame = Frame()
                        frame.degree = degree
                    # after frame
                    catch_xyz = True
                    continue
                if catch_xyz:
                    if set(line.strip()) == {'-'} or \
                            'Coordinates' in line or \
                            'Number' in line:
                        continue
                    if 'Distance matrix' in line:
                        catch_xyz = False
                        continue
                    else:
                        frame.add_coord(line)
                if 'SCF Done' in line:
                    frame.energy = line.split()[4]
                if 'Stationary point found' in line:
                    frame.status = 1
        self.frames.append(frame)


if __name__ == '__main__':
    log = Log_file(sys.argv[1])
    log.parse()
    if not os.path.exists('stationary'):
        os.mkdir('stationary')
    if not os.path.exists('all'):
        os.mkdir('all')
    frame_no = 0
    for i in log.frames:
        if i.status != 0:
            with open('stationary/frame_{}_{}.xyz'.format(i.degree, frame_no), 'w') as dump:
                dump.write(str(i))
        else:
            with open('all/frame_{}_{}.xyz'.format(i.degree, frame_no), 'w') as dump:
                dump.write(str(i))
        frame_no += 1
