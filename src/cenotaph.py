import cv2 as cv
import numpy as np
import random

from stats import get_stats, get_daily, rolling_avg
import variants as V
from variants import get_variant_stats, get_lineages
from marker import AllMarkers


# USER INPUTS =================================================================
dispX, dispY        = 15360, 1200        #Display size
cell_size           = 15                 #Pixel size per cell
gridX, gridY        = int(dispX / cell_size), int(dispY / cell_size)
cell_count          = 8
pixel_per_day = cell_size * cell_count
# print(pixel_per_day)
source_count        = int(gridX / cell_count)
day_count           = int(gridY / cell_count)
audio_buffer_count  = int(gridX / source_count)
let_animate         = True
bake                = False
day_marker_color    = (236, 0, 140)

# COVID STAT INPUT ============================================================
cases, deads, dates = get_stats("covid_us_nytimes.csv")
averaged_deads = np.squeeze(rolling_avg(get_daily(deads), 7))
# print(averaged_deads)

# COVID VARIANT INPUT =========================================================
variants = get_variant_stats("sars_cov_2_proportions.csv", "sars_cov_2_us.csv")
lineages = get_lineages(variants)
# print(lineages)
proportions = V.get_all_proportions(variants, lineages)
key_variants, key_proportions = V.get_key_proportions(
    lineages, proportions, key_threshold=0.05
)
cumulated_proportions = V.get_proportion_cumulations(key_proportions)
np.set_printoptions(suppress=True)
print(cumulated_proportions[:,65:70])
odd_proportions = V.get_odd_proportion(key_proportions)
# print(key_proportions.shape, odd_proportions.shape)


def make_canvas(day_count=day_count):
    """Add a nice docstring."""
    h, w = pixel_per_day * day_count, dispX
    canvas = cv.cvtColor(cv.Mat(
        np.ones((h, w), dtype=np.float32)),
        cv.COLOR_GRAY2RGB
    )
    return canvas


def generate(deads_count=3000):
    """Add a nice docstring."""
    d_grid = np.ndarray((cell_count, gridX), dtype=np.float32)
    total_cell_count = d_grid.shape[0] * d_grid.shape[1]
    # print(total_cell_count)
    deads_cells = np.random.permutation(total_cell_count)[0:deads_count]
    
    for i in range(0, total_cell_count):
        d_grid[int(i / gridX), i % gridX] = 0 if i in deads_cells else 1

    return d_grid


def aggregate(start_day=100, day_count=10):
    """Add a nice docstring."""
    d_grid = np.ndarray((cell_count * day_count, gridX), dtype=np.float32)
    for i in range(0, day_count):
        d_grid[cell_count*i:cell_count*(i+1),:] = generate(
            averaged_deads[start_day+day_count]
        )
    return d_grid


def partition(d_grid):
    """Add a nice docstring."""
    x, y = d_grid.shape
    p_size = int(y / source_count)
    print(d_grid[0:2, 0:p_size])
    partitions = np.ndarray((x * p_size, source_count), 
        dtype=np.float32
        )
    
    for i in range(0, source_count):
        p = np.reshape(d_grid[:,p_size*i:p_size*(i+1)], (x*p_size, ))
        partitions[:,i] = p
    print(partitions[0:16,0])
    return partitions


def visualize(d_grid):
    """Add a nice docstring."""
    markers = AllMarkers()
    # print(len(markers))

    x, y = d_grid.shape
    px, py = x * cell_size, y * cell_size
    # print(x, y, px, py)

    cell = np.ones((cell_size, cell_size), np.float32)
    g = cv.resize(cv.cvtColor(d_grid, cv.COLOR_GRAY2RGB), 
                  (py, px), 
                  interpolation=cv.INTER_NEAREST)
    
    g[0,:,:] = g[px-1,:,:] = day_marker_color

    for i in range(0, y):
        for j in range(0, x):
            if d_grid[j,i] == 0:
                start_x = cell_size * i
                end_x   = cell_size + start_x
                start_y = cell_size * j
                end_y   = cell_size + start_y

                cell = cv.cvtColor(
                    markers[random.randint(0, len(markers)-1)], # entry point
                    cv.COLOR_GRAY2RGB)        
                
                g[start_y:end_y, start_x:end_x,:] = cell
    return g * 255


def get_snippet(start_day, day_count=day_count):
    """Add a nice docstring."""
    snippet = make_canvas(day_count)

    for d in range(0, day_count):
        snippet[d*pixel_per_day:(d+1)*pixel_per_day,:] = visualize(
            generate(averaged_deads[start_day+d])
            )
    
    cv.imwrite(
        "./Assets/Visual/snippet_{}_{}.png".format(source_count, start_day), 
        snippet
    )
    print(snippet.shape)


def animate(img):
    """Add a nice docstring."""
    height, width, c = img.shape
    # print(width, height)
    i = 0
    while True:
        if i == height:
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


def animate_timeline(start_day, end_day, day_count):
    """Add a nice docstring."""
    timeline = make_canvas(day_count)
    h = timeline.shape[0]
    # print(timeline.shape)
    d = start_day
    d_current   = visualize(generate(averaged_deads[d - 1]))
    d_next      = visualize(generate(averaged_deads[d]))
    # print(d_next.shape)

    i = 0
    while d < end_day:
        timeline[0:h-1,:] = timeline[1:,:]
        timeline[h-1,:] = d_current[i,:]

        if i == d_current.shape[0] - 1:
            d_current = d_next
            d += 1
            # print(d)
            d_next = visualize(generate(averaged_deads[d]))
            i = 0
        else:
            i += 1
        
        cv.imshow("", timeline)

        if (cv.waitKey(1) == ord("q")):
            cv.destroyAllWindows()
            break


def main():
    """Add a nice docstring."""
    g = visualize(generate(averaged_deads[349]))

    if let_animate:
        animate(g)
    else:
        cv.imshow("", g)
        cv.waitKey(0)
        cv.imwrite("short.png", g)


def test():
    """Add a nice docstring."""
    d_grid = aggregate()

    partition(d_grid)
    # get_snippet(900, 100)
    # animate_timeline(100, 1000, 4)


if __name__ == "__main__":
    test()