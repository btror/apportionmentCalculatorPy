import matplotlib.pyplot as plt
import numpy as np
from methods.hamilton import Hamilton
from methods.jefferson import Jefferson
from methods.webster import Webster
from methods.adam import Adam


class Plot:
    def __init__(self, original_divisor, modified_divisor, initial_quotas, final_quotas, initial_fair_shares,
                 final_fair_shares, total_initial_fair_shares, lower_boundary, upper_boundary, estimation_history):
        self.original_divisor = original_divisor
        self.modified_divisor = modified_divisor
        self.initial_quotas = initial_quotas
        self.final_quotas = final_quotas
        self.initial_fair_shares = initial_fair_shares
        self.final_fair_shares = final_fair_shares
        self.total_initial_fair_shares = total_initial_fair_shares
        self.lower_boundary = lower_boundary
        self.upper_boundary = upper_boundary
        self.estimation_history = estimation_history

    def create_divisor_graph(self):
        points_1, points_2, points_3 = self.calculate_plot_points()
        points = [points_1, points_2, points_3]

        fig = plt.figure()
        ax = plt.axes()

        ax.plot(points[0], '-o', color='black', label='modified divisor')
        ax.plot(points[1], '--', color='red', label='estimated lowest divisor')
        ax.plot(points[2], '--', color='blue', label='estimated highest divisor')
        ax.set_title('Estimated Divisor Boundaries')
        ax.set_xlabel('Number of estimations', fontsize=12)
        ax.set_ylabel('Estimated divisor', fontsize=12)
        ax.legend()

        plt.show()

    def create_fair_share_plot(self):
        fig = plt.figure()
        ax = plt.axes()

        width = .3
        index = 0
        ax.bar(np.arange(len(self.initial_fair_shares)) - width / 2, self.initial_fair_shares, width,
               label='initial fair shares')
        ax.bar(np.arange(len(self.final_fair_shares)) + width / 2, self.final_fair_shares, width,
               label='final fair shares')
        plt.xticks(np.arange(len(self.initial_fair_shares) + width / 2))
        ax.set_title("Fair Shares")
        ax.set_xlabel("State", fontsize=12)
        ax.set_ylabel("Fair shares", fontsize=12)
        ax.legend()

        plt.show()

    def calculate_plot_points(self):
        """
        calculate_plot_points - creates lists for estimations, lowest, and highest divisors

        :param lower_divisor: lowest estimated divisor
        :param upper_divisor: highest estimated divisor

        :return: points_1 - list of estimations, points_2 - list of lower divisors, points_3 - list of highest divisors
        """

        points_1 = []
        points_2 = []
        points_3 = []

        # plot the estimation coordinates
        for i, estimation in enumerate(self.estimation_history):
            points_1.append(estimation)
            points_2.append(self.lower_boundary)
            points_3.append(self.upper_boundary)

        return points_1, points_2, points_3


def plot_points(points, title_labels):
    """
    plot_points - plots the modified divisor, estimated lowest divisor, and estimated highest divisor

    :param points: list containing the estimator numbers, lowest estimated divisors, and highest estimated divisors
    :param title_labels: title of the x and y labels for the graph
    """

    fig, ax = plt.subplots(2, 2)
    index = 0
    for i in range(2):
        for j in range(2):
            if i == 1 and j == 1:
                break
            ax[i][j].plot(points[index][0], '-o', color="black", label="modified divisor")
            ax[i][j].plot(points[index][1], '--', color="red", label="estimated lowest divisor")
            ax[i][j].plot(points[index][2], '--', color="blue", label="estimated highest divisor")
            ax[i][j].set_title(title_labels[index])
            ax[i][j].set_xlabel('Time Step', fontsize=12)
            ax[i][j].set_ylabel('Divisor', fontsize=12)
            ax[i][j].legend()
            index += 1
    plt.tight_layout()


def plot_fair_shares(initial_fair_shares, final_fair_shares, title_labels, states):
    """
    plot_fair_shares - plots the initial and final calculated fair shares for each method

    :param initial_fair_shares: list of initial fair shares for each method
    :param final_fair_shares: list of final fair shares for each method
    :param title_labels: title of the x and y label for the graph
    :param states: number of states used in each method (same number for each method)
    """

    fig, ax = plt.subplots(2, 2)
    width = .3
    index = 0
    for i in range(2):
        for j in range(2):
            ax[i][j].bar(np.arange(states) - width / 2, initial_fair_shares[index], width, label='initial fair shares')
            ax[i][j].bar(np.arange(states) + width / 2, final_fair_shares[index], width, label='final fair shares')
            plt.xticks(np.arange(states + width / 2))
            ax[i][j].set_title(title_labels[index])
            ax[i][j].set_xlabel('State', fontsize=12)
            ax[i][j].set_ylabel('Fair Shares', fontsize=12)
            ax[i][j].legend()
            index += 1
    plt.tight_layout()


def main():
    """
    main - function that initializes data to test with each method
    """

    # initialize variables
    num_seats = 12
    state_populations = [20, 30, 44, 12]
    states = len(state_populations)

    # hamilton
    model_1 = Hamilton(num_seats, states, state_populations)
    original_divisor_1, modified_divisor_1, initial_quotas_1, final_quotas_1, initial_fair_shares_1, final_fair_shares_1, total_initial_fair_shares_1, lower_boundary_2, upper_boundary_2 = model_1.calculate()

    # adam
    model_2 = Adam(num_seats, states, state_populations)
    original_divisor_2, modified_divisor_2, initial_quotas_2, final_quotas_2, initial_fair_shares_2, final_fair_shares_2, total_initial_fair_shares_2, lower_boundary_2, upper_boundary_2 = model_2.calculate()

    # jefferson
    model_3 = Jefferson(num_seats, states, state_populations)
    original_divisor_3, modified_divisor_3, initial_quotas_3, final_quotas_3, initial_fair_shares_3, final_fair_shares_3, total_initial_fair_shares_3, lower_boundary_3, upper_boundary_3 = model_3.calculate()

    # webster
    model_4 = Webster(num_seats, states, state_populations)
    original_divisor_4, modified_divisor_4, initial_quotas_4, final_quotas_4, initial_fair_shares_4, final_fair_shares_4, total_initial_fair_shares_4, lower_boundary_4, upper_boundary_4 = model_4.calculate()

    print("Hamilton Results")
    print("original divisor", original_divisor_1, "\nmodified divisor", modified_divisor_1, "\ninitial quotas",
          initial_quotas_1, "\nfinal quotas", final_quotas_1, "\ninitial fair shares", initial_fair_shares_1,
          "\nfinal fair shares", final_fair_shares_1, "\ntotal initial fair shares", total_initial_fair_shares_1)

    print("\nAdam Results")
    print("original divisor", original_divisor_2, "\nmodified divisor", modified_divisor_2, "\ninitial quotas",
          initial_quotas_2, "\nfinal quotas", final_quotas_2, "\ninitial fair shares", initial_fair_shares_2,
          "\nfinal fair shares", final_fair_shares_2, "\ntotal initial fair shares", total_initial_fair_shares_2,
          "\nestimated lower boundary", lower_boundary_2, "\nestimated upper boundary", upper_boundary_2)

    print("\nJefferson Results")
    print("original divisor", original_divisor_3, "\nmodified divisor", modified_divisor_3, "\ninitial quotas",
          initial_quotas_3, "\nfinal quotas", final_quotas_3, "\ninitial fair shares", initial_fair_shares_3,
          "\nfinal fair shares", final_fair_shares_3, "\ntotal initial fair shares", total_initial_fair_shares_3,
          "\nestimated lower boundary", lower_boundary_3, "\nestimated upper boundary", upper_boundary_3)

    print("\nWebster Results")
    print("original divisor", original_divisor_4, "\nmodified divisor", modified_divisor_4, "\ninitial quotas",
          initial_quotas_4, "\nfinal quotas", final_quotas_4, "\ninitial fair shares", initial_fair_shares_4,
          "\nfinal fair shares", final_fair_shares_4, "\ntotal initial fair shares", total_initial_fair_shares_4,
          "\nestimated lower boundary", lower_boundary_4, "\nestimated upper boundary", upper_boundary_4)

    points_2_1, points_2_2, points_2_3 = model_2.calculate_plot_points(lower_boundary_2, upper_boundary_2)
    points_3_1, points_3_2, points_3_3 = model_3.calculate_plot_points(lower_boundary_3, upper_boundary_3)
    points_4_1, points_4_2, points_4_3 = model_4.calculate_plot_points(lower_boundary_4, upper_boundary_4)

    points_2 = [points_2_1, points_2_2, points_2_3]
    points_3 = [points_3_1, points_3_2, points_3_3]
    points_4 = [points_4_1, points_4_2, points_4_3]

    points_list = [points_2, points_3, points_4]
    title_labels = ["Adam", "Jefferson", "Webster", "Hamilton"]
    initial_fair_shares_list = [initial_fair_shares_2, initial_fair_shares_3,
                                initial_fair_shares_4, initial_fair_shares_1]
    final_fair_shares_list = [final_fair_shares_2, final_fair_shares_3, final_fair_shares_4, final_fair_shares_1]

    plot_points(points_list, title_labels)
    plot_fair_shares(initial_fair_shares_list, final_fair_shares_list, title_labels, states)
    plt.show()

# main()
