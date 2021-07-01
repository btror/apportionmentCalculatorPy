import math


class Adam:
    def __init__(self, num_seats, states, populations):
        self.num_seats = num_seats
        self.states = states
        self.populations = populations

        self.original_divisor = sum(populations) / num_seats
        self.original_quotas = [0] * states
        self.initial_fair_shares = [0] * states
        self.estimator_history = []

    def calculate_quotas(self, modified_divisor, final_quotas):
        for i, population in enumerate(self.populations):
            self.original_quotas[i] = population / self.original_divisor
            final_quotas[i] = population / modified_divisor
        return final_quotas

    def calculate_fair_shares(self, final_fair_shares, final_quotas, modified_divisor, estimator):
        while sum(final_fair_shares) != self.num_seats:
            for i, quota in enumerate(self.original_quotas):
                final_fair_shares[i] = math.ceil(final_quotas[i])
                self.initial_fair_shares[i] = math.ceil(quota)
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
                    final_fair_shares[i] = math.ceil(final_quotas[i])
                    self.initial_fair_shares[i] = math.ceil(quota)
        return final_fair_shares, final_quotas, modified_divisor, estimator

    def calculate(self):
        final_quotas = self.calculate_quotas(sum(self.populations) / self.num_seats, [0] * self.states)
        final_fair_shares, final_quotas, modified_divisor, estimator = self.calculate_fair_shares([0] * self.states,
                                                                                                  final_quotas, sum(
                self.populations) / self.num_seats, sum(self.populations) / self.num_seats)
        lower_boundary = self.calculate_lower_boundary(modified_divisor)
        upper_boundary = self.calculate_upper_boundary(modified_divisor)

        return self.original_divisor, modified_divisor, self.original_quotas, final_quotas, self.initial_fair_shares, final_fair_shares, sum(
            self.initial_fair_shares), lower_boundary, upper_boundary

    def calculate_lower_boundary(self, divisor):
        # see how low you can go
        quotas = [0] * self.states
        fair_shares = [0] * self.states
        counter = 0
        prev_divisor = 0
        estimator = 1000000000
        while counter < 1000:
            for i, population in enumerate(self.populations):
                quotas[i] = population / divisor
                fair_shares[i] = math.ceil(quotas[i])
            if sum(fair_shares) != self.num_seats:
                estimator = estimator / 10
                divisor = prev_divisor - estimator
            else:
                prev_divisor = divisor
                divisor = divisor - estimator
                if prev_divisor == divisor:
                    break
            counter += 1
        return prev_divisor

    def calculate_upper_boundary(self, divisor):
        # see how high you can go
        quotas = [0] * self.states
        fair_shares = [0] * self.states
        counter = 0
        prev_divisor = 0
        estimator = 1000000000
        while counter < 1000:
            for i, population in enumerate(self.populations):
                quotas[i] = population / divisor
                fair_shares[i] = math.ceil(quotas[i])
            if sum(fair_shares) != self.num_seats:
                estimator = estimator / 10
                divisor = prev_divisor + estimator
            else:
                prev_divisor = divisor
                divisor = divisor + estimator
                if prev_divisor == divisor:
                    break
            counter += 1
        return prev_divisor

    def calculate_plot_points(self, lower_divisor, upper_divisor):
        points_1 = []
        points_2 = []
        points_3 = []

        # plot the estimation coordinates
        for i, estimation in enumerate(self.estimator_history):
            points_1.append(estimation)
            points_2.append(lower_divisor)
            points_3.append(upper_divisor)

        return points_1, points_2, points_3