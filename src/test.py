import numpy as np
import cv2 as cv 
import random

from marker import VariantMarker as Variant

cell_size = 15

day_count = 10
daily_cell_count = 8
channel_count = 128
cell_count = day_count * daily_cell_count

colored = False


def generate():
    r_block = np.random.random((cell_count, channel_count * daily_cell_count))
    d_block = np.ndarray((cell_count, channel_count * daily_cell_count), np.float32)
    for i in range(0, cell_count):
        for j in range(0, channel_count * daily_cell_count):
            if r_block[i,j] < 0.35:
                d_block[i,j] = 0.0
            else:
                d_block[i,j] = 255.0

    print(d_block)
    vis = cv.cvtColor(d_block, cv.COLOR_GRAY2RGB)
    print(vis)
    cv.imwrite("vis0.jpg", vis)
    return d_block


def visualize(data):
    x, y = data.shape
    pixel_size_x = cell_size * x
    pixel_size_y = cell_size * y

    vis = cv.resize(
        cv.cvtColor(data, cv.COLOR_GRAY2RGB), 
        (pixel_size_y, pixel_size_x), 
        interpolation=cv.INTER_NEAREST
    )
    
    cell = np.ones((cell_size, cell_size), np.float32)
    print(cell.shape)
    
    # Separate days
    for k in range(0, day_count):
        vis[cell_size * daily_cell_count * k,:,:] = (140, 0, 236)
        vis[cell_size * daily_cell_count * (k+1) - 1,:,:] = (140, 0, 236)
    #Give everyday a base color
    # for i in range(0, day_count):
    #     current_day = cell_size * daily_cell_count * i
    #     next_day = cell_size * daily_cell_count * (i+1)
    #     r = (255 - (255 - 78) / day_count * (i + 1)) / 255
    #     g = (255 - (255 - 42) / day_count * (i + 1)) / 255
    #     b = (255 - (255 - 132) / day_count * (i + 1)) / 255
    #     vis[current_day:next_day,:,:] = (r, g, b)
    
    # Mark cells with variants
    for i in range(0, y):
        for j in range(0, x):
            if data[j,i] == 0:
                start_x = cell_size * i
                end_x = cell_size * (i+1)
                start_y = cell_size * j
                end_y = cell_size * (j+1)

                cell = cv.cvtColor(
                    Variant().Generic(1) if random.random() < 0.4 else
                    Variant().Generic(2) if random.random() < 0.4 else
                    Variant().Generic(3) if random.random() < 0.4 else
                    Variant().Generic(4) if random.random() < 0.4 else
                    Variant().Generic(6), cv.COLOR_GRAY2RGB)
                
                vis[start_y:end_y, start_x:end_x,:] = cell

    if colored:
        for i in range(0, vis.shape[0]):
            for j in range(0, vis.shape[1]):
                if vis[i,j,0] == vis[i,j,1] == vis[i,j,2] == 0:
                    vis[i,j,:] =(71, 185, 88)
                else:
                    vis[i,j,:] = (53, 2, 29)

    return vis


def animate(img):
    width, height, c = img.shape
    i = 0
    while True:
        if i == 1200:
            i = 0
        else:
            i += 1
        t = img[i:,:]
        b = img[:i,:]
        new = np.vstack((t, b))

        cv.imshow("", new)

        if (cv.waitKey(1) == ord("q")):
            cv.destroyAllWindows()
            break


def main():
    d_block = generate()
    vis = visualize(d_block)
    cv.imwrite("test.png", vis) 
    animate(vis)


if __name__ == "__main__":
    main()