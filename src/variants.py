from datetime import datetime as dt
import numpy as np
import matplotlib.pyplot as pplot
import csv


def get_variant_stats(input_file, output_file):
    """Add a nice docstring."""
    with open(input_file, "r") as variant_csv:
        variant_raw = [d for d in variant_csv.readlines()]
        variant_usa = []

        for i in range(0, len(variant_raw)):
            items = [d for d in variant_raw[i].split(",")]
            if (items[0] == "USA" and 
                items[7] == "weighted" and
                items[8] == "weekly"):
                variant_usa.append(items[0:len(items) - 1])
        
        us_variant_sorted = sorted(variant_usa, 
                                   key=lambda t: dt.strptime(t[1], '%m/%d/%Y %I:%M:%S %p')
                                   )

        with open(output_file, "w", newline="\n") as usa_csv:
            writer = csv.writer(usa_csv, delimiter=",")
            for i in range(0, len(us_variant_sorted)):
                writer.writerow(us_variant_sorted[i])
    
    return us_variant_sorted


def get_pango_lineage(variant_name):
    """Add a nice docstring."""
    lineage = ""
    if variant_name == "alpha" or variant_name == "Beta":
        lineage = "B.1.1.7"
    elif variant_name == "beta" or variant_name == "Beta":
        lineage = "B.1.351"
    elif variant_name == "gamma" or variant_name == "Gamma":
        lineage = "P.1"
    elif variant_name == "delta" or variant_name == "Delta":
        lineage = "B.1.617.2"
    elif variant_name == "omicron" or variant_name == "Omicron":
        lineage = "B.1.1.529"
    return lineage


def get_lineages(data):
    """Add a nice docstring."""
    lineages = []
    for i in range(0, len(data)):
        if data[i][2] not in lineages:
            lineages.append(data[i][2])
    # print(len(lineages))
    return lineages


def get_variant_data(variant_name):
    """Add a nice docstring."""
    lineage = get_pango_lineage(variant_name)
    variant_data = []
    with open("sars_cov_2_usa.csv", "r") as usa_file:
        usa_data = csv.reader(usa_file, delimiter=",")
        for i in usa_data:
            if i[2] == lineage:
                variant_data.append(i)
        # print(len(variant_data))
        return variant_data


def get_variant_count(data):
    """Add a nice docstring."""
    variant_counts = []
    pango_lineages = []
    variant_count = 0
    variant_time_stamp = data[0][1]

    for i in range(0, len(data)):
        if data[i][1] != variant_time_stamp:
            variant_counts.append(variant_count)
            variant_count = 0
            variant_time_stamp = data[i][1]
            pango_lineages = []
        else:
            if data[i][2] not in pango_lineages:
                pango_lineages.append(data[i][2])
                variant_count += 1

    # print(pango_lineages)
    return variant_counts


def get_variant_proportions(data, lineage):
    """Add a nice docstring."""
    variant_proportions = []
    variant_proportion = []
    variant_time_stamp = data[0][1]

    for i in range(0, len(data)):
        if data[i][1] != variant_time_stamp:
            if variant_proportion == []:
                variant_proportions.append(0.0)
            else:
                variant_proportions.append(min(variant_proportion))                                  
            variant_proportion = []
            variant_time_stamp = data[i][1]
        else:
            if data[i][2] == lineage and data[i][3] != "NULL":
                variant_proportion.append(float(data[i][3]))  

    return variant_proportions


def get_variant_proportions_by_name(data, variant_name):
    """Add a nice docstring."""
    pango_lineage = get_pango_lineage(variant_name)
    return get_variant_proportions(data, pango_lineage)


def get_all_proportions(data, lineages):
    """Add a nice docstring."""
    proportions = []

    for i in range(0, len(lineages)):
        proportion = get_variant_proportions(data, lineages[i])
        # print(len(proportion))
        proportions.append(proportion)

    return proportions


def get_key_proportions(lineages, proportions, key_threshold=0.25):
    """Add a nice docstring."""
    key_variants = []
    key_variants_proportions = []
    for i in range(0, len(lineages)):
        # if at one point a variant accounts for 25% of all cases
        # before 10/15/2022, then it is considered a key variant.
        if (max(proportions[i]) > key_threshold and
            lineages[i] != "Other" and
            np.argmax(proportions[i]) < 91):
            key_variants.append(lineages[i])
            key_variants_proportions.append(proportions[i])
            # print(lineages[i], max(proportions[i]), np.argmax(proportions[i]))

    return key_variants, np.asarray(key_variants_proportions, dtype=np.float16)


def plot_key_proportions(lineages, proportions, show=False):
    """Add a nice docstring."""
    for i in range(0, proportions.shape[0]):
        pplot.plot(proportions[i,0:91])
    
    if show:
        pplot.xlabel("week")
        pplot.ylabel("proportions")
        pplot.xticks([0, 30, 60, 90])
        pplot.legend(lineages)
        pplot.show()


def get_odd_proportion(key_variant_proportions):
    """Add a nice docstring."""
    key_variant_proportion = np.sum(key_variant_proportions, 0)
    odd_variant_proportion = 1 - key_variant_proportion
    # print(other_variant_proportion)
    return odd_variant_proportion


def get_odd_cutoff(odd_variant_proportions):
    """Add a nice docstring."""
    return np.argmin(odd_variant_proportions)


def plot_odd_proportion(other_variant_proportions, show=False):
    """Add a nice docstring."""
    pplot.plot(other_variant_proportions[0:91])

    if show:
        pplot.xlabel("week")
        pplot.ylabel("proportions")
        pplot.legend(["Others"])
        pplot.show()


def get_proportion_cumulations(proportions):
    """Add a nice docstring."""
    lineage_count, week_count = proportions.shape
    cumulations = np.zeros((lineage_count + 1, week_count), dtype=np.float16)

    for i in range(1, lineage_count):
        cumulations[i] = cumulations[i-1] + proportions[i-1]
    
    cumulations[lineage_count] = 1

    return cumulations


def plot_variant_proportions(lineages, proportions):
    """Add a nice docstring."""
    key_variants, key_proportions = get_key_proportions(lineages, proportions)
    other_proportion = get_odd_proportion(key_proportions)
    key_variants.append("Others")

    plot_key_proportions(key_variants, key_proportions)
    plot_odd_proportion(other_proportion)

    pplot.xlabel("week")
    pplot.ylabel("proportions")
    pplot.xticks([0, 30, 60, 90])
    pplot.legend(lineages)
    pplot.show()


def main():
    """Add a nice docstring."""
    variant = get_variant_stats("sars_cov_2_proportions.csv", "sars_cov_2_us.csv")
    # print(variant[0][1])
    lineages = get_lineages(variant)
    proportions = get_all_proportions(variant, lineages)
    key_variants, key_proportions = get_key_proportions(lineages, proportions, 0.25)
    cumulated_proportions = get_proportion_cumulations(key_proportions)
    np.set_printoptions(precision=4, suppress=True)
    print(cumulated_proportions[:,60:63])

    odd_proportions = get_odd_proportion(key_proportions)
    odd_cutoff = get_odd_cutoff(odd_proportions)
    print(odd_cutoff)

    
    # key_variants_2, key_proportions_2 = get_key_proportions(lineages, proportions, 0.04)
    # odd_proportion_1, odd_proportion_2 = get_odd_proportion(key_proportions_1), get_odd_proportion(key_proportions_2)
    # plot_odd_proportion(odd_proportion_1, show=False)
    # plot_odd_proportion(odd_proportion_2, show=False)

    # pplot.xlabel("week")
    # pplot.ylabel("proportion")
    # pplot.xticks([0, 30, 60, 90])
    # pplot.legend([
    #     "Threshold=0.25, #variants={}".format(len(key_variants_1)), 
    #     "Threshold=0.04, #variants={}".format(len(key_variants_2))
    #     ])
    # pplot.show()


if __name__ == "__main__":
    main()