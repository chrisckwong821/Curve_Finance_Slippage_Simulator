import argparse
import matplotlib.pyplot as plt
# direct copy from Curve repo
# https://github.com/curvefi/curve-contract/blob/master/tests/pools/common/integration/test_curve.py
from simulation import Curve

# 100 for oUSD
# 200 for mUSD, UST
# 500 for LUSD
# 1500 for frax
# 2000 for Mim
# 5000 for 3CRV
As = [100, 200, 500, 1500, 2000, 5000]

percentageOfEachTrade = 1
# Total poolSize
Dep = 10000000000
withdrawAmount = Dep / (percentageOfEachTrade * 100)

# set fee = 0 for stimulation purpose, set fee to 4000000 for prod
fee = 0
# two coins
n = 2
# 800 steps to push the balance with each step trade 0.1%, change for simulation accuracy
steps = [Dep/1000, 800]

# steps = [tradeSize, number of trade]
def simulate(Curve, steps, withdrawAmount):
    # tokens = Dep so it has 1LP = 1 Dep relationship
    tradeSize = steps[0]
    poolBalances = []
    slippages = []

    for i in range(steps[1]):
        old_balances = 100 * Curve.x[0] / sum(Curve.x)
        output = Curve.calc_withdraw_one_coin(withdrawAmount, 1)
        slippage = float(100 * (withdrawAmount - output) / withdrawAmount)
        #print("withdraw amount: ", Curve.calc_withdraw_one_coin(withdrawAmount, 1), " at pool balance : ", old_balances)
        #print("slippage : " , slippage, "  beginning_balances: ", old_balances)
        poolBalances.append(old_balances)
        slippages.append(slippage)
        Curve.exchange(0,1, tradeSize)
    # return the beginning pool %, the slippage(%)
    return poolBalances, slippages


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='-s slippage(%) / -p poolBalance(%)')
    parser.add_argument('-s', type=float, 
                    help='slippage(%)')
    parser.add_argument('-p', type=float,
                    help='PoolBalance(%)')
    args = parser.parse_args()
    if args.s and args.p == None:
        print(args.s)
        # slippage threshold(%) for poolBalance label on the plot
        threshold = args.s
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.set_xlabel('Pool Balance(%)')  # Add an x-label to the axes.
        ax.set_ylabel('Slippage(%)')  # Add a y-label to the axes.
        ax.set_title('Withdraw Slippage on Pool Ratio on Curve Stablepool')
        print("Withdraw -----", withdrawAmount)
        thresholds = []
        
        for i in As:
            print("A : ", i)
            curve = Curve(i, Dep,n, fee=fee, tokens=Dep)
            x, y = simulate(curve, steps, withdrawAmount)
            ax.plot(x,y, label='A={}'.format(i))

            # find the balance based on a threshold slippage (%)
            index = [ n for n,i in enumerate(y) if i>threshold ][0]

            thresholds.append(x[index])
            print( "Pool Balance: ",x[index], " Based on slippage at {} %".format(threshold))
        
        AsText = ["A={}".format(A) for A in As]
        thresholdsText = ['{}%'.format(format(t, ".1f")) for t in thresholds]
        legend1 = plt.legend(AsText)
        legend2 = plt.legend(thresholdsText, loc=1)
        ax.add_artist(legend1)
        ax.add_artist(legend2)
        ax.axhline(y=threshold, ls='--', color='r', label="{}% sliipage".format(threshold))
        ax.legend()
        plt.show()
    elif args.p and args.s == None:
        print(args.p)
        threshold = args.p
        # poolBalance(%) threshold label on the plot for slippage
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.set_xlabel('Pool Balance(%)')  # Add an x-label to the axes.
        ax.set_ylabel('Slippage(%)')  # Add a y-label to the axes.
        ax.set_title('Withdraw Slippage on Pool Ratio on Curve Stablepool')
        print("Withdrwaw -----", withdrawAmount)
        thresholds = []
        for i in As:
            print("A : ", i)
            curve = Curve(i, Dep,n, fee=fee, tokens=Dep)
            x, y = simulate(curve, steps, withdrawAmount)
            ax.plot(x,y, label='A={}'.format(i))

            # find the slippage (%) given a balance(%) threshold
            index = [ n for n,i in enumerate(x) if i>threshold ][0]

            thresholds.append(y[index])
            print( "Slippage: ", y[index], " Based on poolBlaance at {} %".format(threshold))
        
        AsText = ["A={}".format(A) for A in As]
        thresholdsText = ['{}%'.format(format(t, ".3f")) for t in thresholds]
        legend1 = plt.legend(AsText)
        legend2 = plt.legend(thresholdsText, loc=1)
        ax.add_artist(legend1)
        ax.add_artist(legend2)
        ax.axvline(x=threshold, ls='--', color='r', label="{}% poolBalance".format(threshold))
        #ax.axhline(y=threshold, ls='--', color='r', label="{}% sliipage".format(threshold))
        ax.legend()
        plt.show()
    else:
        print("Usage: python Withdraw.py [-s] slippage(%) OR [-p] poolBalance(%)")
    
    
    