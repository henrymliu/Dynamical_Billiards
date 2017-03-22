from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
from scipy import optimize as op
from AbstractTable import AbstractTable as abT
from matplotlib.collections import PatchCollection



class Lorentz(abT):
    """docstring for Lorentz."""
    def __init__(self, **kwargs):
        super(Lorentz,self).__init__(**kwargs)
        self.maxx = 3
        self.maxy = 3
        self.minx = -3
        self.miny = -3
        self.radius = 1
        self.length = abs(self.minx - self.maxx)
        self.height = abs(self.maxy - self.miny)

    def drawTable(self,ec='none'):
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.fig.canvas.set_window_title('Lorentz Billiards Simulation')
        self.ax.set(xlim=[(self.minx - 0.5),(self.maxx + 0.5)],ylim=[(self.miny - 0.5),
            (self.maxy + 0.5)])
        self.ax.axis('off')
        # make table
        patches=[]
        patches.append(plt.Rectangle((self.minx, self.miny), self.length, self.height, ec='none', lw=1, fc='none'))
        patches.append(plt.Circle((0, 0), self.radius))

        self.table = PatchCollection(patches)
        self.table.set_edgecolor(ec)
        self.table.set_linewidth(1)
        self.table.set_facecolor('none')
        self.ax.add_collection(self.table)
        plt.axis('equal')


    def step(self,particle, dt):

        # check for crossing boundary
        crossed_x1 = particle.state[0] < self.minx
        crossed_x2 = particle.state[0] > self.maxx
        crossed_y1 = particle.state[1] < self.miny
        crossed_y2 = particle.state[1] > self.maxy

        # reset the position to the boundary line
        if crossed_x1:
            fun = lambda y: particle.state[2] / particle.state[3] * (y - particle.state[1]) + particle.state[0] - self.minx
            root = op.brentq(fun, -0.1+self.miny, self.maxy + 0.1)
            particle.state[0] = self.minx
            particle.state[1] = root
            particle.state[2] *= -1

        elif crossed_x2:
            fun = lambda y: particle.state[2] / particle.state[3] * (y - particle.state[1]) + particle.state[0] - self.maxx
            root = op.brentq(fun, -0.1+self.miny, self.maxy + 0.1)
            particle.state[0] = self.maxx
            particle.state[1] = root
            particle.state[2] *= -1

        if crossed_y1:
            fun = lambda x: particle.state[3] / particle.state[2] * (x - particle.state[0]) + particle.state[1] - self.miny
            root = op.brentq(fun, -0.1+self.minx, self.maxx + 0.1)
            particle.state[0] = root
            particle.state[1] = self.miny
            particle.state[3] *= -1
        elif crossed_y2:
            fun = lambda x: particle.state[3] / particle.state[2] * (x - particle.state[0]) + particle.state[1] - self.maxy
            root = op.brentq(fun, -0.1+self.minx, self.maxx + 0.1)
            particle.state[0] = root
            particle.state[1] = self.maxy
            particle.state[3] *= -1

        # check for crossing boundary
        if np.hypot(particle.state[0], particle.state[1]) < self.radius:
            # circ = lambda x: np.sqrt(abs(4 - x**2)) - particle.state[3]/particle.state[2]*(x-particle.state[0])+particle.state[1]
            # root = op.fsolve(circ, particle.state[0])
            # print(root)
            # first quadrant
            # dy/dx
            # intercept = particle.state[3] * -particle.state[0] / particle.state[2] + particle.state[1]

            if abs(particle.state[3] / particle.state[2]) <= 1:
                m = particle.state[3] / particle.state[2]
                intercept = m * -particle.state[0] + particle.state[1]

                # discrimanant
                b = 2 * m * intercept
                a = m ** 2 + 1
                c = -self.radius ** 2 + intercept ** 2

                # choose root based on proximity with x
                root = -b / (2 * a)
                dis = (np.sqrt(abs(b ** 2 - 4 * a * c))) / (2 * a)
                if abs(particle.state[0] - root - dis) < abs(particle.state[0] - root + dis):
                    root += dis
                else:
                    root -= dis

                particle.state[0] = root
                particle.state[1] = m * root + intercept
                # print((particle.state[0], particle.state[1]))

                vel_norm = np.hypot(particle.state[0], particle.state[1])
                dot = (particle.state[2] * particle.state[0] + particle.state[3] * particle.state[1]) / (vel_norm ** 2)
                particle.state[2] = particle.state[2] - 2 * dot * particle.state[0]
                particle.state[3] = particle.state[3] - 2 * dot * particle.state[1]

                # particle.state[3] *= -1/2;
                # particle.state[2] *= -1;
                # print((particle.state[2], particle.state[3]))
                # print((particle.state[0], particle.state[1]))

            elif abs(particle.state[2] / particle.state[3]) <= 1:
                m = particle.state[2] / particle.state[3]
                intercept = m * -particle.state[1] + particle.state[0]
                # discriminant
                b = 2 * m * intercept
                a = m ** 2 + 1
                c = -self.radius ** 2 + intercept ** 2

                # choose root based on proximity with current y
                root = -b / (2 * a)
                dis = (np.sqrt(abs(b ** 2 - 4 * a * c))) / (2 * a)
                if abs(particle.state[1] - root - dis) < abs(particle.state[1] - root + dis):
                    root += dis
                else:
                    root -= dis
                # vel = [particle.state[0], particle.state[1]] / vel_norm

                particle.state[0] = m * root + intercept
                particle.state[1] = root
                # print((particle.state[0], particle.state[1]))

                # update velocity based on r = d - 2(r.n)r
                vel_norm = np.hypot(particle.state[0], particle.state[1])
                dot = (particle.state[2] * particle.state[0] + particle.state[3] * particle.state[1]) / (vel_norm ** 2)
                particle.state[2] = particle.state[2] - 2 * dot * particle.state[0]
                particle.state[3] = particle.state[3] - 2 * dot * particle.state[1]
                # print((particle.state[2], particle.state[3]))
                # print((particle.state[0], particle.state[1]))

if __name__ == '__main__':
    table = Lorentz()
    table.main()
