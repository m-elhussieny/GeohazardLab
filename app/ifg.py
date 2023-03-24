import numpy as np
import  bz2, pickle
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from typing import Any, Optional, Tuple
from tensorflow.keras.models import load_model
from app.model import ViT

plt.rc('font', **{'family' : 'serif',
                  'weight' : 'light',
                  'size'   : 2})

class Interferogram():
    def __init__(self, fileName:str, modelDir:Optional[str]='') -> None:
        self.fileName = fileName
        self.cfgTF = True if modelDir.endswith('.h5') else False if modelDir else None
        self.model = load_model(modelDir, compile=False) if self.cfgTF else ViT(modelDir) if modelDir else None
        self.defo_sources = ['dyke', 'sill', 'atmo']
        

    def read(self) -> np.ndarray:
        with bz2.BZ2File(f"{self.fileName}", "rb") as file:
            data = pickle.load(file)
        file.close()
        return data['unwrapped']
    
    def sacale(self, ifgdata:np.ndarray, scale:dict={'min': -1, 'max': 1}) -> np.ndarray:
        ifgdata -= ifgdata.min()
        ifgdata /= ifgdata.max()
        ifgdata *= (scale['max'] - scale['min'])
        ifgdata += scale['min']
        ifgdata = ifgdata.filled(fill_value=0)
        ifgdata = ifgdata.astype(np.float32)
        return ifgdata


    def process(self, channellast:bool=True) -> np.ndarray:
        data = self.read()
        data = self.sacale(data, {'min': -1, 'max': 1})
        data = np.expand_dims(data, axis=-1 if channellast else 0)

        
        channels = self.model.input_shape[-1] if self.cfgTF else self.model.model.patch_embed.proj.in_channels
        
        if channels == 3:
            data = np.concatenate((data, data, data), axis=-1 if channellast else 0)
        return np.expand_dims(data, axis=0)
    
    def predict(self, ) -> Tuple[np.ndarray, np.ndarray]:
        data = self.process(channellast=self.cfgTF)
        label, anchor = self.model.predict(data, verbose=0) 
        label, anchor = np.asarray(label), np.asarray(anchor)

        label = label.squeeze()
        anchor = anchor.squeeze()
        anchor = anchor.astype(np.int64)
        return label, anchor

    def labelling(self, ) -> Tuple[str, float, np.ndarray]:
        label, _ = self.predict()
        indx = label.argmax()
        accurcy = label[indx]
        label = self.defo_sources[indx]
        return label, accurcy

    def anchortobbox(self, anchor:np.ndarray) -> Tuple[int, int, int, int]:
        xstart = anchor[0] - anchor[2]
        xstop = anchor[0] + anchor[2]
        ystart = anchor[1] - anchor[3]
        ystop = anchor[1] + anchor[3]
        return xstart, xstop, ystart, ystop

    def plotdata(self, axes:plt.Axes):
        data = self.read()
        ifg = axes.imshow(data, cmap='jet')
        cbar = plt.colorbar(ifg, ax=axes, shrink=0.8)
        cbar.outline.set_linewidth(0.1)
        cbar.ax.tick_params(length=0.5, width=0.1, pad=1)
    
    def plotbbox(self, axes:plt.Axes, color:str='r') -> None:
        _, anchor = self.predict()
        xstart, xstop, ystart, ystop = self.anchortobbox(anchor)
        # plot Bbox
        axes.plot((xstart, xstart), (ystart, ystop),  color=color, linewidth=0.25)           # left hand side
        axes.plot((xstart, xstop),  (ystop, ystop),   color=color, linewidth=0.25)             # bottom
        axes.plot((xstop, xstop),   (ystop, ystart),  color=color, linewidth=0.25)             # righ hand side
        axes.plot((xstop, xstart),  (ystart, ystart), color=color, linewidth=0.25)             # top
        # plot Center
        axes.scatter(anchor[0], anchor[1], color=color, s=0.15)

    def plot(self, fig:Figure,  addresult=False):
        fig.clf()
        # plt.cla()
        axes = fig.add_subplot()
        axes.axis('off')
        axes.set_xlim([0, 224])
        axes.set_ylim([0, 224])
        
        self.plotdata(axes)

        if addresult:
            self.plotbbox(axes, 'r')