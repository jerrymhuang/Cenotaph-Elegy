import numpy as np
import matplotlib.pyplot as mplot


def get_daily(data):
    """Add a nice docstring."""
    daily_data = np.zeros((len(data), 1), dtype=int)
    for i in range(0, len(data)):
        if i == 0:
            daily_data[i] = data[i]
        else:
            daily_data[i] = data[i] - data[i-1]
    
    return daily_data


def get_fatal_rates(cases, deads):
    """Add a nice docstring."""
    fatal_rates = np.zeros((len(cases), 1), dtype=float)
    for i in range(0, len(cases)):
        if cases[i] == 0:
            if deads[i] == 0:
                fatal_rates[i] = 0
            else:
                fatal_rates[i] = 1
        else:
            fatal_rates[i] = (float)(deads[i] / cases[i])
    
    return fatal_rates


def rolling_avg(data, n):
    """Add a nice docstring."""
    avg = np.zeros((len(data), 1), dtype=int)

    for i in range(0, len(data)):
        if i == 0:
            avg[i] = data[i]
        elif i < n:
            avg[i] = int(np.sum(data[0:i+1])/(i+1))
        else:
            avg[i] = int(np.sum(data[i-n:i])/n)
    
    return avg


def count_zero_cases(data):
    """Add a nice docstring."""
    day = 0
    for i in range(0, len(data)):
        if data[i] == 0: 
            day += 1

    print(day)


def tplot(data, fs):
    """Add a nice docstring."""
    t = np.arange(0, len(data) / fs, 1/fs, dtype=float)
    mplot.plot(t, data)


def get_activation_pattern(data, fs): # needs optimization
    """Add a nice docstring."""
    print(data)
    # First, make a seed sequence for all fatalities.
    activation_pattern = np.zeros((len(data)*fs, 1), dtype=int)
    # activation = np.zeros((len(data) * fs, source_count), dtype=int)
    for i in range(0, len(data)):
        segment = np.zeros((fs, 1), dtype=int)
        p = np.random.permutation(fs)
        for j in range(0, data[i]):
            segment[p[j]] = 1
        activation_pattern[i*fs:(i+1)*fs] = segment

    return activation_pattern


def spread_activation(pattern):
    """Add a nice docstring."""
    pass


def get_stats(input_file):
    """Add a nice docstring."""
    with open(input_file, "r") as nyt_csv:
        nyt_data = [
            [i for i in d[:-1].split(",")] 
            for d in nyt_csv.readlines()
            ][1:]
        nyt_data = np.asarray(nyt_data)

        cases = nyt_data[:,1].astype(int)
        deads = nyt_data[:,2].astype(int)
        dates = nyt_data[:,0]

        return cases, deads, dates


def main():
    """Add a nice docstring."""
    cases, deads, dates = get_stats("covid_us_nytimes.csv")
    daily_deads = get_daily(deads)
    averaged_deads = rolling_avg(daily_deads, 7)


if __name__ == "__main__":
    main()
