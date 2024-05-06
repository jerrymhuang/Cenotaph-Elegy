import cv2 as cv
import numpy as np

from marker import VariantMarker as Marker

cell_size = 15

def main():
    alpha   = Marker().Alpha()
    beta    = Marker().Beta()
    gamma   = Marker().Gamma()
    delta   = Marker().Delta()
    omicron = Marker().Omicron()
    ba      = Marker().OmicronBA()
    bq      = Marker().OmicronBQ()
    xbb     = Marker().OmicronXBB()
    others  = Marker().Others()


    markers = [alpha, beta, gamma, delta, omicron, ba, bq, xbb, others]

    grid = np.zeros((8, 8), dtype=np.float32)
    g = cv.resize(
        cv.cvtColor(grid, cv.COLOR_GRAY2RGB), 
        (120, 120), 
        interpolation=cv.INTER_NEAREST
        )
    print(g)
    
    for i in range(0, 8):
        grid[i,:] = np.random.permutation(8)
        for j in range(0, 8):
            cell = cv.cvtColor(markers[int(grid[i,j])], cv.COLOR_GRAY2RGB)
            g[i*cell_size:(i+1)*cell_size, j*cell_size:(j+1)*cell_size,:] = cell

    cv.imwrite("mosaic.png", cv.resize(g, (1440, 1440), interpolation=cv.INTER_NEAREST))

    print(grid)



if __name__ == "__main__":
    main()