import numpy as np
import cv2 as cv
import random


magnify = True
bake = True


class Marker:
    default = np.zeros((15, 15), np.float32)
    default_icon = cv.cvtColor(default, cv.COLOR_GRAY2RGB)


class VariantMarker(Marker):
    def __init__(self, lineage="original", size=15):
        self.lineage = lineage
        self.size = size
        self.data = np.ones((size, size), np.float32)
        self.visual = cv.cvtColor(self.data, cv.COLOR_GRAY2RGB)


    def Framed(self):
        self.data[0,:] = self.data[self.size - 1,:] = 0
        self.data[:,0] = self.data[:,self.size - 1] = 0

        return self.data

    def Generic(self, hatch_count = 1):
        # First, make a square frame
        self.data = self.Framed()

        hatch_unit = self.size - 4
        hatch_gaps = hatch_count - 1

        if (hatch_unit - hatch_gaps) % hatch_count != 0:
            return VariantMarker.Others(self)
        else:
            hatch_size = int((hatch_unit - hatch_gaps) / hatch_count)

            for i in range(0, hatch_count):
                for j in range(0, hatch_count):
                    start_x = i * (hatch_size + 1) + 2
                    end_x = start_x + hatch_size
                    start_y = j * (hatch_size + 1) + 2
                    end_y = start_y + hatch_size
                    self.data[start_x:end_x, start_y:end_y] = 0

        return self.data * 255
    
    def Striped(self, hatch_count=1, horizontal=True):
        
        self.data = self.Framed()

        hatch_unit = self.size - 4
        hatch_gaps = hatch_count - 1

        if (hatch_unit - hatch_gaps) % hatch_count != 0:
            return VariantMarker.Others(self)
        else:
            hatch_size = int((hatch_unit - hatch_gaps) / hatch_count)
            
            for i in range(0, hatch_count):
                start_x = 2
                end_x = start_x + hatch_unit
                start_y = i * (hatch_size + 1) + 2
                end_y = start_y + hatch_size
                if horizontal:
                    self.data[start_x:end_x, start_y:end_y] = 0
                else:
                    self.data[start_y:end_y, start_x:end_x] = 0 

        return self.data * 255

    def Dotted(self):
        for i in range(0, self.size):
            for j in range(0, self.size):
                if i % 2 == 0 and j % 2 == 0:
                    self.data[i,j] = 0
        return self.data * 255
    
    def Sliced(self):
        for i in range(0, self.size):
            for j in range(0, self.size):
                if (i + j) % 3 == 0:
                    self.data[i,j] = 0
        return self.data * 255
    
    def Concentric(self):
        for i in range(0, self.size):
            if i % 2 == 0:
                self.data[i,i:self.size-i] = 0
                self.data[self.size-1-i,i:self.size-i] = 0
                self.data[i:self.size-i,i] = 0
                self.data[i:self.size-i,self.size-1-i] = 0
        return self.data * 255
    
    def B1_1_7(self):
        return self.Generic(hatch_count=1)
    
    def B1_617_2(self):
        return self.Striped(hatch_count=2)
    
    def P1(self):
        return self.Striped(hatch_count=2, horizontal=False)

    def B1_1_529(self):
        return self.Generic(hatch_count=2)
    
    def BA_1_1(self):
        return self.Striped(hatch_count=3)
    
    def BA_2(self):
        return self.Striped(hatch_count=3, horizontal=False)
    
    def BA_2_12_1(self):
        return self.Generic(hatch_count=3)
    
    def BA_5(self):
        return self.Generic(hatch_count=4)
    
    def BQ_1(self):
        return self.Striped(hatch_count=4)
    
    def BQ_1_1(self):
        return self.Striped(hatch_count=4, horizontal=False)
    
    def XBB_1_5(self):
        return self.Concentric()
        
    def Alpha(self):
        return self.B1_1_7()
    
    def Beta(self):
        return self.Striped(hatch_count=2, horizontal=False)
    
    def Gamma(self):
        # to be implemented
        return self.Striped(hatch_count=2)

    def Delta(self):
        # to be implemented
        return self.Generic(hatch_count=2)
    
    def Omicron(self):
        return self.B1_1_529()

    def OmicronBA(self):
        return self.Striped(hatch_count=3)
    
    def OmicronBQ(self):
        return self.Striped(hatch_count=3, horizontal=False)
    
    def OmicronXBB(self):
        return self.XBB_1_5()
    
    def Origin(self):
        return self.default
    
    def Others(self):
        return self.Generic(6)
    
    
    def Random(self):
        self.data[0,:] = self.data[:,0] = 0
        self.data[self.size-1,:] = self.data[:,self.size-1] = 0
        for i in range(1, self.size-1):
            for j in range(1, self.size-1):
                self.data[i,j] = 0 if random.random() < 0.3 else 1
        return self.data * 255


def AllMarkers():
    markers = [
        VariantMarker(15).B1_1_7(),
        VariantMarker(15).B1_617_2(),
        VariantMarker(15).B1_1_529(),
        VariantMarker(15).BA_1_1(),
        VariantMarker(15).BA_2(),
        VariantMarker(15).BA_2_12_1(),
        VariantMarker(15).BA_5(),
        VariantMarker(15).BQ_1(),
        VariantMarker(15).BQ_1_1(),
        VariantMarker(15).Others(),
        VariantMarker(15).Origin()
    ]
    return markers

def MakeMarker(variant):
    marker = cv.resize(
        cv.cvtColor(
            getattr(VariantMarker, variant),
            cv.COLOR_GRAY2RGB
        ),
        (120, 120),
        interpolation=cv.INTER_NEAREST
    )
    return marker


def main():
    B1_1_529 = VariantMarker(15).B1_1_529() 
    icon = cv.resize(
        cv.cvtColor(B1_1_529, cv.COLOR_GRAY2RGB), 
        (120, 120), 
        interpolation=cv.INTER_NEAREST
        )
    
    if magnify:
        cv.imshow("", icon)
        cv.waitKey(0)
    
    if bake:
        cv.imwrite("B1_1_529.png", icon)


if __name__ == "__main__":
    main()