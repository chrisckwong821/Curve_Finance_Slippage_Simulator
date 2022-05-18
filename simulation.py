class Curve:

    """
    Python model of Curve pool math.
    """

    def __init__(self, A, D, n, fee=None, p=None, tokens=None):
        """
        A: Amplification coefficient
        D: Total deposit size
        n: number of currencies
        p: target prices
        """
        self.A = A  # actually A * n ** (n - 1) because it's an invariant
        self.n = n
        # 4000000  = 0.04% implemented in prod
        if fee == None:
            self.fee = 4000000
        else:
            self.fee = fee
        if p:
            self.p = p
        else:
            self.p = [10 ** 18] * n
        if isinstance(D, list):
            self.x = D
        else:
            self.x = [D // n * 10 ** 18 // _p for _p in self.p]
        self.tokens = tokens

    def xp(self):
        return [x * p // 10 ** 18 for x, p in zip(self.x, self.p)]

    def D(self):
        """
        D invariant calculation in non-overflowing integer operations
        iteratively
        A * sum(x_i) * n**n + D = A * D * n**n + D**(n+1) / (n**n * prod(x_i))
        Converging solution:
        D[j+1] = (A * n**n * sum(x_i) - D[j]**(n+1) / (n**n prod(x_i))) / (A * n**n - 1)
        """
        Dprev = 0
        xp = self.xp()
        S = sum(xp)
        D = S
        Ann = self.A * self.n
        while abs(D - Dprev) > 1:
            D_P = D
            for x in xp:
                D_P = D_P * D // (self.n * x)
            Dprev = D
            D = (Ann * S + D_P * self.n) * D // ((Ann - 1) * D + (self.n + 1) * D_P)

        return D

    def y(self, i, j, x):
        """
        Calculate x[j] if one makes x[i] = x
        Done by solving quadratic equation iteratively.
        x_1**2 + x1 * (sum' - (A*n**n - 1) * D / (A * n**n)) = D ** (n+1)/(n ** (2 * n) * prod' * A)
        x_1**2 + b*x_1 = c
        x_1 = (x_1**2 + c) / (2*x_1 + b)
        """
        D = self.D()
        xx = self.xp()
        xx[i] = x  # x is quantity of underlying asset brought to 1e18 precision
        xx = [xx[k] for k in range(self.n) if k != j]
        Ann = self.A * self.n
        c = D
        for y in xx:
            c = c * D // (y * self.n)
        c = c * D // (self.n * Ann)
        b = sum(xx) + D // Ann - D
        y_prev = 0
        y = D
        while abs(y - y_prev) > 1:
            y_prev = y
            y = (y ** 2 + c) // (2 * y + b)
        return y  # the result is in underlying units too

    def y_D(self, i, _D):
        """
        Calculate x[j] if one makes x[i] = x
        Done by solving quadratic equation iteratively.
        x_1**2 + x1 * (sum' - (A*n**n - 1) * D / (A * n**n)) = D ** (n+1)/(n ** (2 * n) * prod' * A)
        x_1**2 + b*x_1 = c
        x_1 = (x_1**2 + c) / (2*x_1 + b)
        """
        xx = self.xp()
        xx = [xx[k] for k in range(self.n) if k != i]
        S = sum(xx)
        Ann = self.A * self.n
        c = _D
        for y in xx:
            c = c * _D // (y * self.n)
        c = c * _D // (self.n * Ann)
        b = S + _D // Ann
        y_prev = 0
        y = _D
        while abs(y - y_prev) > 1:
            y_prev = y
            y = (y ** 2 + c) // (2 * y + b - _D)
        return y  # the result is in underlying units too

    # find swapped amount without acconting fee
    def dy(self, i, j, dx):
        # dx and dy are in underlying units
        xp = self.xp()
        return xp[j] - self.y(i, j, xp[i] + dx)
    # find swapped amount with acconting fee
    def dyWfee(self, i, j, dx):
        xp = self.xp()
        dy = xp[j] - self.y(i, j, xp[i] + dx)
        return dy - dy * self.fee // 10 ** 10
    
    def exchange(self, i, j, dx):
        xp = self.xp()
        x = xp[i] + dx
        y = self.y(i, j, x)
        dy = xp[j] - y
        fee = dy * self.fee // 10 ** 10
        assert dy > 0
        self.x[i] = x * 10 ** 18 // self.p[i]
        self.x[j] = (y + fee) * 10 ** 18 // self.p[j]
        return dy - fee

    # return the lp tokens needed to withdraw 
    def remove_liquidity_imbalance(self, amounts):
        _fee = self.fee * self.n // (4 * (self.n - 1))

        old_balances = self.x
        new_balances = self.x[:]
        D0 = self.D()
        for i in range(self.n):
            new_balances[i] -= amounts[i]
        self.x = new_balances
        D1 = self.D()
        self.x = old_balances
        fees = [0] * self.n
        for i in range(self.n):
            ideal_balance = D1 * old_balances[i] // D0
            difference = abs(ideal_balance - new_balances[i])
            fees[i] = _fee * difference // 10 ** 10
            new_balances[i] -= fees[i]
        self.x = new_balances
        D2 = self.D()
        self.x = old_balances

        token_amount = (D0 - D2) * self.tokens // D0

        return token_amount

    def calc_withdraw_one_coin(self, token_amount, i):
        xp = self.xp()
        if self.fee:
            fee = self.fee - self.fee * xp[i] // sum(xp)
        else:
            fee = 0

        D0 = self.D()
        D1 = D0 - token_amount * D0 // self.tokens
        dy = xp[i] - self.y_D(i, D1)

        return dy - dy * fee // 10 ** 10

    def get_virtual_price(self):
        return D / self.tokens
    
    def D_withBalance(self, new_balance):
        """
        D invariant calculation in non-overflowing integer operations
        iteratively
        A * sum(x_i) * n**n + D = A * D * n**n + D**(n+1) / (n**n * prod(x_i))
        Converging solution:
        D[j+1] = (A * n**n * sum(x_i) - D[j]**(n+1) / (n**n prod(x_i))) / (A * n**n - 1)
        """
        Dprev = 0
        xp = new_balance
        S = sum(xp)
        D = S
        Ann = self.A * self.n
        while abs(D - Dprev) > 1:
            D_P = D
            for x in xp:
                D_P = D_P * D // (self.n * x)
            Dprev = D
            D = (Ann * S + D_P * self.n) * D // ((Ann - 1) * D + (self.n + 1) * D_P)

        return D

    # add coin i with amount, return lp_amount
    def calc_add_liquidity(self, token_amount, i):
        old_balance = self.xp()
        D0 = self.D()
        
        new_balance = old_balance
        new_balance[i] += token_amount
        D1 = self.D_withBalance(new_balance)

        assert D1 > D0
        total_supply = self.tokens
        if self.fee:
            fee = self.fee - self.fee * old_balance[i] // sum(old_balance)
        else:
            fee = 0

        new_balance[i] -= fee // 10 ** 10
        D2 = self.D_withBalance(new_balance)
        mint_amount = total_supply * (D2 - D0) / D0
        return mint_amount