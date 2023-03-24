import torch
from typing import Tuple
from timm import create_model
import numpy as np

class Mean(torch.nn.Module):
    def __init__(self, dim:int=1) -> None:
        super().__init__()
        self.dim = dim
        
    def forward(self, x:torch.Tensor) -> torch.Tensor:
        return x.mean(self.dim)

class Head(torch.nn.Module):
    def __init__(self, featues:int, pool:str='avg', num_classes:int=3, num_locations:int=4) -> None:
        super().__init__()
        self.pool = torch.nn.Flatten() if pool == 'flat' else Mean() if pool == 'avg' else torch.nn.Identity()
        self.clshead = torch.nn.Linear(featues, num_classes)
        self.poshead  = torch.nn.Linear(featues, num_locations)
    
    def forward(self, x:torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        x = self.pool(x)
        return self.clshead(x), self.poshead(x)

class SepHead(torch.nn.Module):
    def __init__(self, featues:int, pool:str='sep', num_classes:int=3, num_locations:int=4) -> None:
        super().__init__()
        assert pool == 'sep'
        self.pool = Mean()
        self.clshead = torch.nn.Linear(featues, num_classes)
        self.poshead  = torch.nn.Linear(featues, num_locations)
    
    def forward(self, x:torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        
        return self.clshead(self.pool(x[:, 0:1])), self.poshead(self.pool(x[:, 1:]))

class ViT(torch.nn.Module):
    def __init__(self, statedir:str, pool:str='avg', vitname:str='vit_base_patch16_224',) -> None:
        super().__init__()
        self.model:torch.nn.Module = create_model(vitname)
        features = self.model.head.in_features * (1 if pool != 'flat' else (self.model.patch_embed.num_patches + self.model.num_prefix_tokens))
        self.model.head = Head(features, pool) if pool != 'sep' else SepHead(features,  pool)
        self.model.forward_head = lambda  x, pre_logits = False :  self.model.head(self.model.fc_norm(x)) 

        self.load_state_dict(torch.load(statedir))
    
    def forward(self, x:torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        return self.model(x)

    def predict(self, x:np.ndarray, **kwargs):
        self.eval()
        x  = torch.Tensor(x)
        with torch.no_grad():
            y, z = self.forward(x)

        return torch.nn.functional.softmax(y, dim=1).numpy(), z.numpy()

