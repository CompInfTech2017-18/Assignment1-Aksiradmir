
# coding: utf-8


from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib import lines as line
from scipy.integrate import odeint

g=-1.

class Plotter: 
    def __init__(self, title, xlabel, ylabel): 
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title(title) 
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)

    def plot(self, x, y, color): 
        return self.ax.plot(x, y, color)

    def show(self):
        plt.show()




class Matdot:
    def __init__(self, x, y, vx, vy, plotter):
        self.x0=x
        self.y0=y
        self.vx0=vx
        self.vy0=vy
        self.plotter=plotter
    def evoX(self,t):
        x=self.x0+self.vx0*t
        return x
    def evoY(self,t):
        y=self.y0+self.vy0*t+0.5*g*t**2
        return y
    def evolution(self):
        time=np.linspace(0.,5.,50)
        xx=self.evoX(time)
        yy=self.evoY(time)
        plotter.plot(xx, yy, 'b')


class Solid(Matdot):
    def __init__(self, x, y, vx, vy, w, r, plotter):
        self.w=-w
        self.r=r
        self.plotter=plotter
        Matdot.__init__(self,x,y,vx,vy,plotter)
    def evo1X(self,t):
        x=self.evoX(t)+self.r*np.cos(self.w*t)
        return x
    def evo1Y(self,t):
        y=self.evoY(t)+self.r*np.sin(self.w*t)
        return y
    def evo2X(self,t):
        x=self.evoX(t)-self.r*np.cos(self.w*t)
        return x
    def evo2Y(self,t):
        y=self.evoY(t)-self.r*np.sin(self.w*t)
        return y
    def evolutionX(self):
        time=np.linspace(0.,5.,50)
        xx1=self.evo1X(time)
        yy1=self.evo1Y(time)
        plotter.plot(xx1, yy1, 'r')
        xx2=self.evo2X(time)
        yy2=self.evo2Y(time)
        plotter.plot(xx2, yy2, 'g')
        for i in range(50):
           l=line.Line2D([xx1[i],xx2[i]], [yy1[i],yy2[i]], lw=2, color='k')
           self.plotter.ax.add_line(l)
        
class Dipol(Solid):
    def __init__(self, x, y, vx, vy, w, r, q, m, E, plotter):
        self.q=q
        self.E=E
        self.m=m
        Solid.__init__(self, x, y, vx, vy, w, r, plotter)
    def evodip(self):
        time=np.linspace(0.,5.,50)
        def func(y,t):
            fi,b = y
            return [b, (self.m*self.r)/(self.q*self.E)*np.sin(fi)]
        psi=odeint(func,[0,self.w],time)[:,0]
        xx1=self.evoX(time)+self.r*np.cos(psi)
        yy1=self.evoY(time)+self.r*np.sin(psi)
        xx2=self.evoX(time)-self.r*np.cos(psi)
        yy2=self.evoY(time)-self.r*np.sin(psi)
        plotter.plot(xx1, yy1, 'r')
        plotter.plot(xx2, yy2, 'g')
        for i in range(50):
           l=line.Line2D([xx1[i],xx2[i]], [yy1[i],yy2[i]], lw=2, color='k')
           self.plotter.ax.add_line(l)

plotter = Plotter('Solid', 'x', 'y')
#matdot=Matdot(5.,20.,5.,0.,plotter)
solid=Solid(5.,20.,5.,0.,1.,2.,plotter)
dipol=Dipol(5.,20.,5.,0.,1.,2.,1.,1.,1.,plotter)
#matdot.evolution()
solid.evolution()
#solid.evolutionX()
dipol.evodip()
plotter.show()

