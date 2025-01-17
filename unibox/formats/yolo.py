import cv2
import numpy as np
from unibox import Dataset,Bbox


class Yolo:
    @staticmethod
    def import_set(dset:Dataset, in_stream,norm2pixel=False,**kwargs):
        # Read the YOLO format dataset from the text file
        dset.clear()
        for line in in_stream:
            line = line.strip().split()
            if len(line) < 5:
                continue
            line = list(map(float, line))
            label = int(line[0])
            x, y, w, h = line[1:5]
            info = {'label':str(label)}
            if len(line)>5:
                info["extra"] = line[5:]
                
            img_shape = None
            if norm2pixel:
                img_shape = dset["img_shape"]  # w,h
                if img_shape is None:
                    img_path = dset["img_path"]
                    img = cv2.imdecode(np.fromfile(img_path, np.uint8), 1)
                    img_shape = [img.shape[1], img.shape[0]]

            bbox = Bbox([x, y, w, h], "ltwh", False,img_shape,info)
            dset.append(bbox)


    

        
        
    @staticmethod
    def export_set(dset:Dataset,mapping:dict=None):
        
        shape = []
        
        if dset["img_shape"] is None:
            img_wh = dset.label[0].img_wh()
            if img_wh is None:
                if dset.img_path is None:
                    raise ValueError("Image shape is not defined.")
                img = cv2.imdecode(np.fromfile(dset.img_path, np.uint8), 1)
                dset["img_shape"] = [img.shape[1], img.shape[0]]
                img_wh = dset["img_shape"]
            else:
                dset["img_shape"] = img_wh

        img_wh = dset["img_shape"]
      
        

        for bbox in dset.label:
            x,y,w,h = bbox.xywh(is_pixel_distance=False).tolist()
            l = bbox.info.get("label",None)
            if l is None:
                l = "0"
            elif mapping is not None:
                l = mapping[l]

            shape.append(f"{l} {x} {y} {w} {h}")
        

        return '\n'.join(shape)