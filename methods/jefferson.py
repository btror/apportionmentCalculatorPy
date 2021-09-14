import math


class Jefferson:
    def __init__(self, num_seats, states, populations):
        """
        init - initialize variables

        :param num_seats: number of seats to apportion
        :param states: number of states to apportion to
        :param populations: list of populations for each state
        """

        self.num_seats = num_seats
        self.states = states
        self.populations = populations

        self.original_divisor = sum(populations) / num_seats
        self.original_quotas = [0] * states
        self.initial_fair_shares = [0] * states
        self.estimator_history = []

    def calculate_quotas(self, modified_divisor, final_quotas):
        """
        calculate_quotas - calculates the quotas for each state

        :param modified_divisor: updated divisor
        :param final_quotas: list of final quotas
        :return: final_quotas - updated list of final quotas
        """

        for i, population in enumerate(self.populations):
            self.original_quotas[i] = population / self.original_divisor
            final_quotas[i] = population / modified_divisor
        return final_quotas

    def calculate_fair_shares(self, final_fair_shares, final_quotas, modified_divisor, estimator):
        """
        calculate_fair_shares - calculates final fair shares

        :param final_fair_shares: list of final fair shares :param final_quotas: list of final quotas
        :param final_quotas: list of updated quotas
        :param modified_divisor: updated divisor
        :param estimator: heuristic value used to calculate a modified divisor :param modified_divisor: updated
        divisor

        :return: final_fair_shares - list of final fair shares, final_quotas - list of final quotas, modified_divisor
        - updated divisor, estimator - updated heuristic
        """

        time_keeper = 0
        while sum(final_fair_shares) != self.num_seats:
            if time_keeper == 5000:
                break
            for i, quota in enumerate(self.original_quotas):
                final_fair_shares[i] = math.floor(final_quotas[i])
                self.initial_fair_shares[i] = math.floor(quota)
            # recalculate divisor
            if sum(final_fair_shares) != self.num_seats:
                if sum(final_fair_shares) > self.num_seats:
                    modified_divisor += estimator
                else:
                    modified_divisor -= estimator
                self.estimator_history.append(modified_divisor)
                estimator = estimator / 2
                if modified_divisor == 0:
                    modified_divisor = 1
                final_quotas = self.calculate_quotas(modified_divisor, final_quotas)
                for i, quota in enumerate(self.original_quotas):
                    final_fair_shares[i] = math.floor(final_quotas[i])
                    self.initial_fair_shares[i] = math.floor(quota)
            time_keeper += 1

        if time_keeper == 5000:
            return None, None, None, None
        else:
            return final_fair_shares, final_quotas, modified_divisor, estimator

    def calculate(self):
        """
        calculate - apportions seats to states based on their populations using Hamilton's method

        :return: original_divisor - original calculated divisor, modified_divisor - updated calculated divisor,
        original_quotas - original calculated quotas, final_quotas - final list of quotas, initial_fair_shares - list
        of initial fair shares, final_fair_shares - final list of quotas, sum(initial_fair_shares) - total initial
        fair shares, lower_boundary - lowest possible divisor, upper_boundary - highest possible divisor
        """

        final_quotas = self.calculate_quotas(sum(self.populations) / self.num_seats, [0] * self.states)
        final_fair_shares, final_quotas, modified_divisor, estimator = self.calculate_fair_shares([0] * self.states,
                                                                                                  final_quotas, sum(
                self.populations) / self.num_seats, sum(self.populations) / self.num_seats)

        lower_boundary = self.calculate_lower_boundary(modified_divisor)
        upper_boundary = self.calculate_upper_boundary(modified_divisor)

        if estimator is None:
            return None, None, None, None, None, None, None, None, None, None
        else:
            return self.original_divisor, modified_divisor, self.original_quotas, final_quotas, self.initial_fair_shares, final_fair_shares, sum(
                self.initial_fair_shares), lower_boundary, upper_boundary, self.estimator_history

    def calculate_with_divisor(self, divisor):
        # calculate final quotas
        final_quotas = []

        for i, population in enumerate(self.populations):
            final_quotas.append(population / divisor)

        # calculate final fair shares
        final_fair_shares = []

        for i, quota in enumerate(final_quotas):
            final_fair_shares.append(math.floor(quota))

        return final_quotas, final_fair_shares

    def calculate_lower_boundary(self, divisor):
        """
        calculate_lower_boundary - calculates the estimated lowest possible divisor

        :param divisor: updated divisor used in calculations

        :return: lowest_divisor - estimated lowest divisor
        """

        # see how low you can go
        quotas = [0] * self.states
        fair_shares = [0] * self.states
        counter = 0
        lowest_divisor = 0
        prev_divisor = 0
        estimator = 1000000000
        while counter < 1000:
            for i, population in enumerate(self.populations):
                if divisor is None or population is None:
                    return None
                quotas[i] = population / divisor
                fair_shares[i] = math.floor(quotas[i])
            if sum(fair_shares) != self.num_seats:
                estimator = estimator / 10
                prev_divisor = divisor
                divisor = lowest_divisor - estimator
            else:
                lowest_divisor = divisor
                divisor = prev_divisor - estimator
                if lowest_divisor == divisor:
                    break
            counter += 1
        return math.ceil(lowest_divisor * 1000) / 1000

    def calculate_upper_boundary(self, divisor):
        """
        calculate_upper_boundary - calculates the estimated highest possible divisor

        :param divisor: updated divisor used in calculations

        :return: highest_divisor - estimated highest divisor
        """

        # see how high you can go
        quotas = [0] * self.states
        fair_shares = [0] * self.states
        counter = 0
        highest_divisor = 0
        prev_divisor = 0
        estimator = 1000000000
        while counter < 1000:
            for i, population in enumerate(self.populations):
                if divisor is None:
                    return None
                quotas[i] = population / divisor
                fair_shares[i] = math.floor(quotas[i])
            if sum(fair_shares) != self.num_seats:
                estimator = estimator / 10
                prev_divisor = divisor
                divisor = highest_divisor + estimator
            else:
                highest_divisor = divisor
                divisor = prev_divisor + estimator
                if highest_divisor == divisor:
                    break
            counter += 1
        return math.floor(highest_divisor * 1000) / 1000

    def calculate_plot_points(self, lower_divisor, upper_divisor):
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
        for i, estimation in enumerate(self.estimator_history):
            points_1.append(estimation)
            points_2.append(lower_divisor)
            points_3.append(upper_divisor)

        return points_1, points_2, points_3
