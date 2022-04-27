from matplotlib import pyplot as plt
from numpy import array

from linear_regression import perform_linear_regression


def rainfall_vs_forest_cover():
    """ Performing a linear fit between rainfall and forest cover, based on real-world data """
    # Result:
    # m: 0.0008587709484891738
    # c: -0.17015471066607157      
    # r_squared: 0.9399832140229544

    # This data was obtained from IKONOS satellite imaging of the Kalahari transect
    x = array([879, 811, 698, 409, 365, 216])
    y = array([0.65, 0.54, 0.32, 0.19, 0.14, 0.04])
    m, c, r_squared = perform_linear_regression(x, y)

    print(f"m: {m}")
    print(f"c: {c}")
    print(f"r_squared: {r_squared}")

    plt.title("Linear fit of Forest cover vs Rainfall")
    plt.xlabel("Rainfall (mm/year)")
    plt.ylabel("Forest cover (fraction)")
    plt.plot(x, y, 'ko')
    x_line = array(x)
    y_line = m * x_line + c
    plt.plot(x_line, y_line)
    plt.show()


def cluster_statistics_vs_rainfall():
    """ Plots number of clusters, cluster size and SD vs rainfall """
    # This data was obtained from cluster_statistics.py
    rainfall = array([300, 400, 500, 600, 700, 800])
    num_clusters = array([10442.2, 16121.8, 18491.2, 17965.4, 15267, 11517])
    average_cluster_size = array([8.17, 6.67, 6.72, 7.76, 10.07, 14.51])
    sd = array([7.77, 7.26, 10.34, 20.8, 48.77, 148.14])

    plt.title("Number of clusters vs Rainfall")
    plt.xlabel("Rainfall (mm/year)")
    plt.ylabel("Number of clusters")
    plt.plot(rainfall, num_clusters)
    plt.show()

    plt.title("Average cluster size vs Rainfall")
    plt.xlabel("Rainfall (mm/year)")
    plt.ylabel("Average cluster size")
    plt.plot(rainfall, average_cluster_size)
    plt.show()

    plt.title("SD of cluster size vs Rainfall")
    plt.xlabel("Rainfall (mm/year)")
    plt.ylabel("SD of cluster size")
    plt.plot(rainfall, sd)
    plt.show()


def rainfall_variation():
    """ Variation of power-law exponent with rainfall (results from automaton simulations) """
    # Result:
    # m: -0.002734285714285714
    # c: 3.165523809523809
    # r_squared: 0.9663725685022448

    # this data was obtained from the fitting parameters of the graphs under observations/rainfall_variation
    # fit was performed by fit_power_law function of power_law_graph.py
    x = array([300, 400, 500, 600, 700, 800])
    y = array([2.3, 2.22, 1.74, 1.47, 1.17, 1.07])
    m, c, r_squared = perform_linear_regression(x, y)

    print(f"m: {m}")
    print(f"c: {c}")
    print(f"r_squared: {r_squared}")

    plt.title("Variation of power-law exponent with rainfall")
    plt.xlabel("Rainfall (mm/year)")
    plt.ylabel("Power-law exponent")
    plt.plot(x, y, marker="o", linestyle="None")
    y_line = m * x + c
    plt.plot(x, y_line)
    plt.show()


def cluster_statistics_vs_radius():
    """ Plots number of clusters, cluster size and SD vs radius of influence """
    # This data was obtained from cluster_statistics.py
    radius = array([2, 4, 6, 8, 10])
    num_clusters = array([5663.4, 14280.4, 17571.4, 18804, 19820.2])
    average_cluster_size = array([18.59, 7.56, 6.18, 5.79, 5.42])
    sd = array([22.94, 9.09, 6.03, 5.34, 4.93])

    plt.title("Number of clusters vs Radius")
    plt.xlabel("Radius")
    plt.ylabel("Number of clusters")
    plt.plot(radius, num_clusters)
    plt.show()

    plt.title("Average cluster size vs Radius")
    plt.xlabel("Radius")
    plt.ylabel("Average cluster size")
    plt.plot(radius, average_cluster_size)
    plt.show()

    plt.title("SD of cluster size vs Radius")
    plt.xlabel("Radius")
    plt.ylabel("SD of cluster size")
    plt.plot(radius, sd)
    plt.show()


def radius_variation():
    """ Variation of power-law exponent with radius (results from automaton simulations) """
    # Result:
    # m: 0.16899999999999998
    # c: 1.222
    # r_squared: 0.7995129188478012

    # this data was obtained from the fitting parameters of the graphs under observations/radius_variation
    # fit was performed by fit_power_law function of power_law_graph.py
    x = array([2, 4, 6, 8, 10])
    y = array([1.83, 1.62, 1.98, 2.84, 2.91])
    m, c, r_squared = perform_linear_regression(x, y)

    print(f"m: {m}")
    print(f"c: {c}")
    print(f"r_squared: {r_squared}")

    plt.title("Variation of power-law exponent with radius")
    plt.xlabel("Radius")
    plt.ylabel("Power-law exponent")
    plt.plot(x, y, marker="o", linestyle="None")
    y_line = m * x + c
    plt.plot(x, y_line)
    plt.show()


def cluster_statistics_vs_immediacy():
    """ Plots number of clusters, cluster size and SD vs immediacy """
    # This data was obtained from cluster_statistics.py
    immediacy = array([12, 18, 24, 30, 36])
    num_clusters = array([16115, 16288.8, 15976.8, 16227.2, 16055.6])
    average_cluster_size = array([6.65, 6.58, 6.79, 6.61, 6.73])
    sd = array([6.95, 6.94, 7.18, 7.19, 7.15])

    plt.title("Number of clusters vs Immediacy")
    plt.xlabel("Immediacy")
    plt.ylabel("Number of clusters")
    plt.plot(immediacy, num_clusters)
    plt.show()

    plt.title("Average cluster size vs Immediacy")
    plt.xlabel("Immediacy")
    plt.ylabel("Average cluster size")
    plt.plot(immediacy, average_cluster_size)
    plt.show()

    plt.title("SD of cluster size vs Immediacy")
    plt.xlabel("Immediacy")
    plt.ylabel("SD of cluster size")
    plt.plot(immediacy, sd)
    plt.show()


def immediacy_variation():
    """ Variation of power-law exponent with immediacy (results from automaton simulations) """
    # Result:
    # m: -0.008666666666666663
    # c: 2.146
    # r_squared: 0.4019024970273477

    # this data was obtained from the fitting parameters of the graphs under observations/immediacy_variation
    # fit was performed by fit_power_law function of power_law_graph.py
    x = array([12, 18, 24, 30, 36])
    y = array([2.13, 1.88, 1.98, 1.78, 1.92])
    m, c, r_squared = perform_linear_regression(x, y)

    print(f"m: {m}")
    print(f"c: {c}")
    print(f"r_squared: {r_squared}")

    plt.title("Variation of power-law exponent with immediacy")
    plt.xlabel("Immediacy")
    plt.ylabel("Power-law exponent")
    plt.plot(x, y, marker="o", linestyle="None")
    y_line = m * x + c
    plt.plot(x, y_line)
    plt.show()


if __name__ == '__main__':
    rainfall_vs_forest_cover()
    cluster_statistics_vs_rainfall()
    rainfall_variation()
    cluster_statistics_vs_radius()
    radius_variation()
    cluster_statistics_vs_immediacy()
    immediacy_variation()