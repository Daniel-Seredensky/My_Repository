import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import os
from PIL import Image
import math
import random


class Terra:
  def __init__(self):
    self.light = [-1,-1,40]
    self.x_data = None
    self.y_data = None
    self.terrain_data = None
    self.generate_terrain()
    self.create_moon()
    self.generate_trees()
    self.AllData=[self.terrain_data,self.Trees]


  def generate_terrain(self):
    size = 35
    x_WaveLengths = np.random.rand(size)*(1/3.5)
    x_coef = np.random.rand(size)-.2
    y_coef = np.random.rand(size)-.2
    y_WaveLengths = np.random.rand(size)*(1/3.5)
    orderx = np.random.rand(size)
    ordery = np.random.rand(size)
    self.x_data = np.linspace(0,14*(math.pi+1),301)
    self.y_data = np.linspace(0,14*(math.pi+1),301)
    self.terrain_data = {}

    def x_func(x):
      sum = 0
      index = -1
      for waveL,coef,order in zip(x_WaveLengths,x_coef,orderx):
        if order>.5:
          sum += coef*math.sin(waveL*x)
        else:
          sum+= coef*math.cos(waveL*x)
        index*=-1
      return sum

    def y_func(y):
      sum = 0
      index = -1
      for waveL,coef,order in zip(y_WaveLengths,y_coef,ordery):
        if order>.5:
          sum += coef*math.cos(waveL*y)
        else:
          sum += coef*math.sin(waveL*y)
        index*=-1
      return sum

    for x in self.x_data:
      for y in self.y_data:
        z = x_func(x)+y_func(y)
        if z > 2:
          self.terrain_data[(x,y,z)] = "ground"
        else:
          self.terrain_data[(x,y,2)] = "water"


  def create_tree(self,origin_x,origin_y,origin_z):
    tree_data = {}
    coef = np.random.rand() + .5
    for z in np.linspace(0,4,50):
      if z < 2:
        r = .2
        for theta in np.linspace(0,2*math.pi,50):
          x = r*math.cos(theta) + origin_x
          y = r*math.sin(theta) + origin_y
          tree_data[tuple((x,y,origin_z+z))] = "bark"
      else:
        for theta in np.linspace(0,2*math.pi,35):
          x = coef*(z-4)*math.cos(theta) + origin_x
          y = coef*(z-4)*math.sin(theta) + origin_y
          tree_data[tuple((x,y,z+origin_z))] = "leaf"
    return tree_data

  def generate_trees(self):
    self.Trees = []
    data = [key for key,val in self.terrain_data.items() if val == "ground"]
    for i in range(50):
      x,y,z = random.choice(data)
      self.Trees.append(self.create_tree(x,y,z))


  def create_moon(self):
    r = 1.5
    theta_vals = phi_vals = np.linspace(0,math.pi,101)
    for theta in theta_vals:
      for phi in phi_vals:
        x = r*math.sin(theta)*math.cos(phi) + self.light[0]
        y = r*math.sin(theta)*math.sin(phi) + self.light[1]
        z = r*math.cos(theta) + self.light[2]
        self.terrain_data[(x,y,z)] = "moon"




  def plot(self):
    terrain = np.array([list(key) for key,val in self.terrain_data.items() if val == "ground" ])
    x,y,z = terrain[:,0],terrain[:,1],terrain[:,2]
    fig = go.Figure(data=[go.Scatter3d(x=x, y=y, z=z,mode = "markers")])
    fig.update_traces(marker=dict(color="darkgreen",opacity=1,size = 1))
    terrain = np.array([list(key) for key,val in self.terrain_data.items() if val == "water" ])
    x,y,z = terrain[:,0],terrain[:,1],terrain[:,2]
    fig.add_trace(go.Scatter3d(x=x, y=y, z=z,marker=dict(color="blue",opacity=1,size = 1)))
    terrain = np.array([list(key) for key,val in self.terrain_data.items() if val == "moon" ])
    x,y,z = terrain[:,0],terrain[:,1],terrain[:,2]
    fig.add_trace(go.Scatter3d(x=x, y=y, z=z,marker=dict(color="gray",opacity=1,size = 1)))
    for tree in self.Trees:
      bark_data = np.array([list(key) for key,val in tree.items() if val == "bark" ])
      x,y,z = bark_data[:,0],bark_data[:,1],bark_data[:,2]
      fig.add_trace(go.Scatter3d(x=x, y=y, z=z,marker=dict(color="brown",opacity=1,size = 1)))
      leaf_data = np.array([list(key) for key,val in tree.items() if val == "leaf" ])
      x,y,z = leaf_data[:,0],leaf_data[:,1],leaf_data[:,2]
      fig.add_trace(go.Scatter3d(x=x, y=y, z=z,marker=dict(color="green",opacity=1,size = 1)))
    fig.show()


terra = Terra()
terra.plot()

