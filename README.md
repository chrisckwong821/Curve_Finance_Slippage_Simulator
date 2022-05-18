# Curve_Finance_Slippage_Simulator
simulate slippage & bonus for pool of various Amplifier(s), based on a targeted slippage(%) or a poolBalance(%) with custom size as a percentage of pool Total Value Locked (TVL).

Scripts for **Swap**, **Withdrawal** and **Deposit**

## Install 
```
pip install -r requirements.txt
```

## Usage

### Simulate withdrawal slippage on a targeted PoolBalance(%)
```
# poolBalance 80%
python3 Withdraw.py -p 80
```

![Withdraw Slippage with 80% Pool Balance](https://github.com/chrisckwong821/Curve_Finance_Slippage_Simulator/blob/main/resources/80W%25.png?raw=true)

### Simulate withdrawal on a targeted Slippage(%)
```
# Slippage 2%
python3 Withdraw.py -s 2
```

![Withdraw PoolBalance with 2% Slippage](https://github.com/chrisckwong821/Curve_Finance_Slippage_Simulator/blob/main/resources/2W%25.png?raw=true)

### Simulate withdrawal bonus on a targeted PoolBalance(%)
```
# the excess assets are withdrawed
python3 Withdraw.py -p 80 --bonus True
```

![Withdraw Bonus with 80% Pool Balance](https://github.com/chrisckwong821/Curve_Finance_Slippage_Simulator/blob/main/resources/WB80.png?raw=true)

### Simulate withdrawal bonus on a targeted bonus(%)

```
# bonus 2%
python3 Withdraw.py -s 2 --bonus True
```

![Targeted Withdrawal Bonus 2%](https://github.com/chrisckwong821/Curve_Finance_Slippage_Simulator/blob/main/resources/WB2.png?raw=true)



### Simulate Swap slippage on a targeted PoolBalance(%)
```
# swap excess asset with needed asset, further tilt the pool
python3 Swap.py -p 80
```

![Swap Slippage with 80% Pool Balance](https://github.com/chrisckwong821/Curve_Finance_Slippage_Simulator/blob/main/resources/80S%25.png?raw=true)

### Simulate swap on a targeted Slippage(%)

```
# Slippage 2%
python3 Swap.py -s 2
```

![PoolBalance with 2% Slippage](https://github.com/chrisckwong821/Curve_Finance_Slippage_Simulator/blob/main/resources/2S%25.png?raw=true)


### Simulate Swap bonus on a targeted PoolBalance(%)

```
# swap needed asset with access asset, return the pool to balance
python3 Swap.py -p 80 --bonus True
```

![Swap Bonus with 80% Pool Balance](https://github.com/chrisckwong821/Curve_Finance_Slippage_Simulator/blob/main/resources/80SB.png?raw=true)


### Simulate Swap on a targeted Bonus(%)

```
# Bonus 2%
python3 Swap.py -s 2 --bonus True
```

![PoolBalance with 2% Bonus](https://github.com/chrisckwong821/Curve_Finance_Slippage_Simulator/blob/main/resources/2SB.png?raw=true)


### Simulate Deposit slippage on a targeted PoolBalance(%)
```
# deposit excess asset
python3 Deposit.py -p 80
```

![Swap Slippage with 80% Pool Balance](https://github.com/chrisckwong821/Curve_Finance_Slippage_Simulator/blob/main/resources/80SD.png?raw=true)

### Simulate Deposit on a targeted Slippage(%)

```
# Slippage 2%
python3 Deposit.py -s 2
```

![PoolBalance with 2% Slippage](https://github.com/chrisckwong821/Curve_Finance_Slippage_Simulator/blob/main/resources/2SD.png?raw=true)


### Simulate Deposit bonus on a targeted PoolBalance(%)

```
# deposit needed asset, return the pool to balance
python3 Deposit.py -p 80 --bonus True
```

![Deposit Bonus with 80% Pool Balance](https://github.com/chrisckwong821/Curve_Finance_Slippage_Simulator/blob/main/resources/80DB.png?raw=true)


### Simulate Deposit on a targeted Bonus(%)

```
# Bonus 2%
python3 Deposit.py -s 2 --bonus True
```

![Deposit with 2% Bonus](https://github.com/chrisckwong821/Curve_Finance_Slippage_Simulator/blob/main/resources/2DB.png?raw=true)


### Deposit / Swap / Withdraw Sizes
```
# Pre-set `1%` of poolSize for the operations
# Pass an optional argument -a to specify the size as a percentage of TVL

# default
python3 Swap.py -s 2 -a 1
# specify swap size of 5%
python3 Swap.py -s 2 -a 5
```
![PoolBalance with 2% Slippage](https://github.com/chrisckwong821/Curve_Finance_Slippage_Simulator/blob/main/resources/2S%255S.png?raw=true)


## Note:

1. Modified simulation code from [Curve Finance](https://github.com/curvefi/curve-contract/blob/master/tests/simulation.py)

2. Use a simple 2-coins model. 

3. Assume no admin fee in the above illustration, modify `fee` in the script to `4000000` to resemble mainnet setting of 4 bps

