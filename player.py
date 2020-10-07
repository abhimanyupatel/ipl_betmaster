class Player:
    def __init__(self, first_name, last_name, alias):
        self.first_name = first_name
        self.last_name = last_name
        self.alias = alias
        self.bets = set()
        self.current_bet = set()

    def get_current_bet(self):
        return self.current_bet

    def set_current_bet(self, bet):
        self.current_bet.update(bet)

    def clear_current_bet(self):
        self.current_bet = set()

    def get_all_bets(self):
        return self.bets

    def get_name(self):
        return self.first_name + ' ' + self.last_name

    def print(self):
        print("name={}, alias={}, current_bet={}, all_bets={}".format(self.get_name(), self.alias,
                                                                         self.current_bet, self.bets))
