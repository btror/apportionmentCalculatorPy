import math


class Hamilton:
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

        self.decimal_list = []

    def calculate_quotas(self, final_quotas):
        """
        calculate_quotas - calculates the quotas for each state

        :param final_quotas: list of final quotas
        :return: final_quotas - updated list of final quotas
        """

        for i, population in enumerate(self.populations):
            self.original_quotas[i] = population / self.original_divisor
            final_quotas[i] = population / self.original_divisor
            self.decimal_list.append(math.modf(population / self.original_divisor)[0])
        return final_quotas

    def calculate_fair_shares(self, final_fair_shares, final_quotas):
        """
        calculate_fair_shares - calculates final fair shares

        :param final_fair_shares: list of final fair shares
        :param final_quotas: list of final quotas
        :return: final_fair_shares - list of final fair shares, final_quotas - list of final quotas
        """

        for i, quota in enumerate(self.original_quotas):
            final_fair_shares[i] = math.floor(quota)
            self.initial_fair_shares[i] = math.floor(final_quotas[i])

        time_keeper = 0
        while sum(final_fair_shares) != self.num_seats:
            if time_keeper == 5000:
                break
            if sum(final_fair_shares) != self.num_seats:
                highest_decimal = max(self.decimal_list)
                index = self.decimal_list.index(highest_decimal)
                final_fair_shares[index] += 1
                self.decimal_list[index] = 0
            time_keeper += 1
        if time_keeper == 5000:
            return None, None
        else:
            return final_fair_shares, final_quotas

    def calculate(self):
        """
        calculate - apportions seats to states based on their populations using Hamilton's method

        :return: original_divisor - original calculated divisor, original_divisor - original calculated divisor,
        original_quotas - original calculated quotas, final_quotas - final list of quotas, initial_fair_shares - list
        of initial fair shares, final_fair_shares - final list of quotas, sum(initial_fair_shares) - total initial
        fair shares
        """

        final_quotas = self.calculate_quotas([0] * self.states)
        final_fair_shares, final_quotas = self.calculate_fair_shares([0] * self.states, final_quotas)

        if final_fair_shares is None:
            return None, None, None, None, None, None, None
        else:
            return self.original_divisor, self.original_divisor, self.original_quotas, final_quotas, \
                   self.initial_fair_shares, final_fair_shares, sum(self.initial_fair_shares), 0, 0, 0
