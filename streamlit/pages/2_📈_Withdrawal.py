import argparse
import matplotlib.pyplot as plt
import streamlit as st

# reference implementation from Curve repo
# https://github.com/curvefi/curve-contract/blob/master/tests/pools/common/integration/test_curve.py
from simulation import Curve

# 100 for oUSD
# 200 for mUSD, UST
# 500 for LUSD
# 1500 for frax
# 2000 for Mim
# 5000 for 3CRV
As = [100, 200, 500, 1500, 2000, 5000]

st.set_page_config(page_title="Withdrawal", page_icon="📈")
st.markdown("# Withdrawal")
st.sidebar.header("Change Parameters:")


# input as arguments
option_sorp = st.sidebar.selectbox('Slippage or Pool Balance:', ('Slippage', 'Pool Balance'))
# st.write('You selected:', option_sorp)
percent_sorp = st.sidebar.slider('Percentage of {} (%):'.format(option_sorp), 0.0, 100.0, 0.0, 0.1)
# st.write('Your percent', percent_sorp)
percent_tradesize = st.sidebar.slider('Percentage of Trade Size (%):', 0.1, 100.0, 1.0, 0.1)
# st.write('Your percent', percent_tradesize)
option_bonus = st.sidebar.checkbox('Is Bonus?')
# if option_bonus:
#      st.write('Bonus!')

# parser = argparse.ArgumentParser(description='-s slippage(%) / -p poolBalance(%)')
# parser.add_argument('-s', type=float, 
#                 help='slippage(%)')
# parser.add_argument('-p', type=float,
#                 help='PoolBalance(%)')
# parser.add_argument('--bonus', default="False",
#                 help='isBonus(%)')
# parser.add_argument('-a', type=float, required=False,
#                 help='percentageOfTradeSize')

percentageOfEachTrade = 1
# Total poolSize
Dep = 10000000000

# set fee = 0 for stimulation purpose, set fee to 4000000 for prod
fee = 0
# two coins
n = 2
# 800 steps to push the balance with each step trade 0.1%, change for simulation accuracy
steps = [Dep/1000, 800]

# steps = [tradeSize, number of trade]
def simulate(Curve, steps, withdrawAmount, is_bonus):
    # tokens = Dep so it has 1LP = 1 Dep relationship
    tradeSize = steps[0]
    poolBalances = []
    slippages = []
    for i in range(steps[1]):
        old_balances = 100 * Curve.x[0] / sum(Curve.x)
        if is_bonus == "False":
            output = Curve.calc_withdraw_one_coin(withdrawAmount, 1)
            slippage = float(100 * (withdrawAmount - output) / withdrawAmount)
        elif is_bonus == "True":
            output = Curve.calc_withdraw_one_coin(withdrawAmount, 0)
            slippage = float(100 * (output - withdrawAmount) / withdrawAmount)
        else:
            print("--bonus is either False or True")
            break
        poolBalances.append(old_balances)
        slippages.append(slippage)
        Curve.exchange(0,1, tradeSize)
        
    # return the beginning pool %, the sliipage(%)
    return poolBalances, slippages


if __name__ == "__main__":
    # args = parser.parse_args()
    # if args.a != None:
    #     percentageOfEachTrade = args.a
    # else:
    #     percentageOfEachTrade = 1
    percentageOfEachTrade = percent_tradesize
    withdrawAmount = Dep * percentageOfEachTrade / 100
    
    logs = []
    if option_bonus == False:
        if option_sorp == "Slippage":
            
            # slippage threshold(%) for poolBalance label on the plot
            threshold = percent_sorp
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
            ax.set_xlabel('Pool Balance(%)')  # Add an x-label to the axes.
            ax.set_ylabel('Slippage(%)')  # Add a y-label to the axes.
            ax.set_title('Withdraw Slippage of Size({}% TVL) on Pool Ratio on Curve Stablepool'.format(percentageOfEachTrade))
            print("Withdraw -----", withdrawAmount)
            logs.append("Withdraw ----- {}".format(withdrawAmount))
            thresholds = []
            
            for i in As:
                print("A : ", i)
                curve = Curve(i, Dep,n, fee=fee, tokens=Dep)
                x, y = simulate(curve, steps, withdrawAmount, "False")
                ax.plot(x,y, label='A={}'.format(i))

                # find the balance based on a threshold slippage (%)
                index = [ n for n,i in enumerate(y) if i>threshold ][0]

                thresholds.append(x[index])
                print( "Pool Balance: ",x[index], " Based on slippage at {} %".format(threshold))
                logs.append( "Pool Balance: {} Based on slippage at {} %".format(x[index], threshold))
            
            AsText = ["A={}".format(A) for A in As]
            thresholdsText = ['{}%'.format(format(t, ".1f")) for t in thresholds]
            # legend1 = plt.legend(AsText)
            legend2 = plt.legend(thresholdsText, loc=1)
            # ax.add_artist(legend1)
            ax.add_artist(legend2)
            ax.axhline(y=threshold, ls='--', color='r', label="{}% sliipage".format(threshold))
            ax.legend()
            st.pyplot(fig) # streamlit magic
            st.code("\n".join(logs))
            # plt.show()
        elif option_sorp == "Pool Balance":
            
            threshold = percent_sorp
            # poolBalance(%) threshold label on the plot for slippage
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
            ax.set_xlabel('Pool Balance(%)')  # Add an x-label to the axes.
            ax.set_ylabel('Slippage(%)')  # Add a y-label to the axes.
            ax.set_title('Withdraw Slippage of Size({}% TVL) on Pool Ratio on Curve Stablepool'.format(percentageOfEachTrade))
            print("Withdraw -----", withdrawAmount)
            logs.append("Withdraw ----- {}".format(withdrawAmount))
            thresholds = []
            for i in As:
                print("A : ", i)
                curve = Curve(i, Dep,n, fee=fee, tokens=Dep)
                x, y = simulate(curve, steps, withdrawAmount, "False")
                ax.plot(x,y, label='A={}'.format(i))

                # find the slippage (%) given a balance(%) threshold
                index = [ n for n,i in enumerate(x) if i>threshold ][0]

                thresholds.append(y[index])
                print( "Slippage: ", y[index], " Based on poolBlaance at {} %".format(threshold))
                logs.append("Slippage: {} Based on poolBlaance at {} %".format(y[index], threshold))
                
            AsText = ["A={}".format(A) for A in As]
            thresholdsText = ['{}%'.format(format(t, ".3f")) for t in thresholds]
            # legend1 = plt.legend(AsText)
            legend2 = plt.legend(thresholdsText, loc=1)
            # ax.add_artist(legend1)
            ax.add_artist(legend2)
            ax.axvline(x=threshold, ls='--', color='r', label="{}% poolBalance".format(threshold))
            #ax.axhline(y=threshold, ls='--', color='r', label="{}% sliipage".format(threshold))
            ax.legend()
            st.pyplot(fig) # streamlit magic
            st.code("\n".join(logs))
            # plt.show()
        else:
            print("Usage: python Withdraw.py [-s] slippage(%) OR [-p] poolBalance(%) | (optional) --bonus [-a] TVL(%)")
    elif option_bonus == True:
        if option_sorp == "Slippage":
            
            # slippage threshold(%) for poolBalance label on the plot
            threshold = percent_sorp
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
            ax.set_xlabel('Pool Balance(%)')  # Add an x-label to the axes.
            ax.set_ylabel('Bonus(%)')  # Add a y-label to the axes.
            ax.set_title('Withdraw Bonus of Size({}% TVL) on Pool Ratio on Curve Stablepool'.format(percentageOfEachTrade))
            print("Withdraw -----", withdrawAmount)
            logs.append("Withdraw ----- {}".format(withdrawAmount))
            thresholds = []
            
            for i in As:
                print("A : ", i)
                curve = Curve(i, Dep,n, fee=fee, tokens=Dep)
                x, y = simulate(curve, steps, withdrawAmount, "True")
                ax.plot(x,y, label='A={}'.format(i))

                # find the balance based on a threshold slippage (%)
                index = [ n for n,i in enumerate(y) if i>threshold ][0]

                thresholds.append(x[index])
                print( "Pool Balance: ",x[index], " Based on Bonus at {} %".format(threshold))
                logs.append("Pool Balance: {} Based on Bonus at {} %".format(x[index], threshold))
            
            AsText = ["A={}".format(A) for A in As]
            thresholdsText = ['{}%'.format(format(t, ".1f")) for t in thresholds]
            # legend1 = plt.legend(AsText)
            legend2 = plt.legend(thresholdsText, loc=1)
            # ax.add_artist(legend1)
            ax.add_artist(legend2)
            ax.axhline(y=threshold, ls='--', color='r', label="{}% bonus".format(threshold))
            ax.legend()
            st.pyplot(fig) # streamlit magic
            st.code("\n".join(logs))
            # plt.show()
        elif option_sorp == "Pool Balance":
            
            threshold = percent_sorp
            # poolBalance(%) threshold label on the plot for slippage
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
            ax.set_xlabel('Pool Balance(%)')  # Add an x-label to the axes.
            ax.set_ylabel('Bonus(%)')  # Add a y-label to the axes.
            ax.set_title('Withdraw Bonus of Size({}% TVL) on Pool Ratio on Curve Stablepool'.format(percentageOfEachTrade))
            print("Withdraw -----", withdrawAmount)
            logs.append("Withdraw ----- {}".format(withdrawAmount))
            thresholds = []
            for i in As:
                print("A : ", i)
                curve = Curve(i, Dep,n, fee=fee, tokens=Dep)
                x, y = simulate(curve, steps, withdrawAmount, "True")
                ax.plot(x,y, label='A={}'.format(i))

                # find the slippage (%) given a balance(%) threshold
                index = [ n for n,i in enumerate(x) if i>threshold ][0]

                thresholds.append(y[index])
                print( "Bonus: ", y[index], " Based on poolBlaance at {} %".format(threshold))
                logs.append( "Bonus: {} Based on poolBlaance at {} %".format(y[index], threshold))
            
            AsText = ["A={}".format(A) for A in As]
            thresholdsText = ['{}%'.format(format(t, ".3f")) for t in thresholds]
            # legend1 = plt.legend(AsText)
            legend2 = plt.legend(thresholdsText, loc=1)
            # ax.add_artist(legend1)
            ax.add_artist(legend2)
            ax.axvline(x=threshold, ls='--', color='r', label="{}% poolBalance".format(threshold))
            #ax.axhline(y=threshold, ls='--', color='r', label="{}% sliipage".format(threshold))
            ax.legend()
            st.pyplot(fig) # streamlit magic
            st.code("\n".join(logs))
            # plt.show()
        else:
            print("Usage: python Withdraw.py [-s] slippage(%) OR [-p] poolBalance(%) | (optional) --bonus [-a] TVL(%)")
    else:
        print("--bonus is either False or True")
    
    
    
