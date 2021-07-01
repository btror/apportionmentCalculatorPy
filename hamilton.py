import math


class Hamilton:
    def __init__(self, num_seats, states, populations):
        self.num_seats = num_seats
        self.states = states
        self.populations = populations

        self.original_divisor = sum(populations) / num_seats
        self.original_quotas = [0] * states
        self.initial_fair_shares = [0] * states

        self.decimal_list = []

    def calculate_quotas(self, final_quotas):
        for i, population in enumerate(self.populations):
            self.original_quotas[i] = population / self.original_divisor
            final_quotas[i] = population / self.original_divisor
            self.decimal_list.append(math.modf(population / self.original_divisor)[0])
        return final_quotas

    def calculate_fair_shares(self, final_fair_shares, final_quotas):
        for i, quota in enumerate(self.original_quotas):
            final_fair_shares[i] = math.floor(quota)
            self.initial_fair_shares[i] = math.floor(final_quotas[i])

        while sum(final_fair_shares) != self.num_seats:
            if sum(final_fair_shares) != self.num_seats:
                highest_decimal = max(self.decimal_list)
                index = self.decimal_list.index(highest_decimal)
                final_fair_shares[index] += 1
                self.decimal_list[index] = 0
        return final_fair_shares, final_quotas

    def calculate(self):
        final_quotas = self.calculate_quotas([0] * self.states)
        final_fair_shares, final_quotas = self.calculate_fair_shares([0] * self.states, final_quotas)
        return self.original_divisor, self.original_divisor, self.original_quotas, final_quotas, self.initial_fair_shares, final_fair_shares, sum(
            self.initial_fair_shares)