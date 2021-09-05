import matplotlib.pyplot as plt
import numpy as np


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

    def create_combined_graph(self):
        fig, ax = plt.subplots(1, 2, figsize=(10, 4))

        # line graph
        width = .3
        points_1, points_2, points_3 = self.calculate_plot_points()
        points = [points_1, points_2, points_3]

        ax[0].plot(points[0], '-o', color="black", label="modified divisor")
        ax[0].plot(points[1], '--', color="red", label="estimated lowest divisor")
        ax[0].plot(points[2], '--', color="blue", label="estimated highest divisor")
        ax[0].set_title('Estimated Divisor Boundaries')
        ax[0].set_xlabel('Time Step', fontsize=12)
        ax[0].set_ylabel('Divisor', fontsize=12)
        ax[0].legend()

        # bar graph
        initial_fair_shares = [0]
        final_fair_shares = [0]

        for i in range(len(self.initial_fair_shares)):
            initial_fair_shares.append(self.initial_fair_shares[i])
            final_fair_shares.append(self.final_fair_shares[i])

        ax[1].bar(np.arange(len(initial_fair_shares)) - width / 2, initial_fair_shares, width,
                  label='initial fair shares')
        ax[1].bar(np.arange(len(final_fair_shares)) + width / 2, final_fair_shares, width,
                  label='final fair shares')
        plt.xticks(np.arange(len(initial_fair_shares) + width / 2))
        ax[1].set_title("Fair Shares")
        ax[1].set_xlabel("State", fontsize=12)
        ax[1].set_ylabel("Fair shares", fontsize=12)
        ax[1].legend()

        fig.tight_layout()
        plt.show()

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

        initial_fair_shares = [0]
        final_fair_shares = [0]

        for i in range(len(self.initial_fair_shares)):
            initial_fair_shares.append(self.initial_fair_shares[i])
            final_fair_shares.append(self.final_fair_shares[i])

        width = .3
        ax.bar(np.arange(len(initial_fair_shares)) - width / 2, initial_fair_shares, width,
               label='initial fair shares')
        ax.bar(np.arange(len(final_fair_shares)) + width / 2, final_fair_shares, width,
               label='final fair shares')
        plt.xticks(np.arange(len(initial_fair_shares) + width / 2))

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


