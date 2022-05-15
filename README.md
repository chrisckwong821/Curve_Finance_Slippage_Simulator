# Curve_Finance_Slippage_Simulator
simulate slippage for pool of various Amplifier(s), based on a targeted slippage(%) or a poolBalance(%)

## Install 
```
pip install -r requirements.txt
```

## Usage

### Simulate withdraw on a targeted PoolBalance(%)
```
# poolBalance 80%
python3 Withdraw.py -p 80
```

![Withdraw Slippage with 80% Pool Balance](https://github.com/chrisckwong821/Curve_Finance_Slippage_Simulator/blob/main/resources/80W%25.png?raw=true)

### Simulate withdraw on a targeted Slippage(%)
```
# Slippage 2%
python3 Withdraw.py -s 2
```

![Withdraw PoolBalance with 2% Slippage](https://github.com/chrisckwong821/Curve_Finance_Slippage_Simulator/blob/main/resources/2W%25.png?raw=true)

`Swap` can be simulated in the same fashion using `Swap.py`


### Simulate swap on a targeted PoolBalance(%)
```
# poolBalance 80%
python3 Swap.py -p 80
```

![Swap Slippage with 80% Pool Balance](https://github.com/chrisckwong821/Curve_Finance_Slippage_Simulator/blob/main/resources/80S%25.png?raw=true)

### Simulate swap on a targeted Slippage(%)
```
# Slippage 2%
python3 Swap.py -s 2
```

![PoolBalance with 2% Slippage](https://github.com/chrisckwong821/Curve_Finance_Slippage_Simulator/blob/main/resources/2S%25.png?raw=true)


### Swap / Withdraw Sizes
```
# Pre-set `1%` of poolSize for both swap and withdraw. 
# Pass an optional argument -a to specify the size of the operation

# default
python3 Swap.py -s 2 -a 1
# specify swap size of 5%
python3 Swap.py -s 2 -a 5
```
![PoolBalance with 2% Slippage](https://github.com/chrisckwong821/Curve_Finance_Slippage_Simulator/blob/main/resources/2S%255S.png?raw=true)


## Note:

1. Use simulation code from [Curve Finance](https://github.com/curvefi/curve-contract/blob/master/tests/simulation.py)

2. Use a simple 2-coins model. 

3. Assume no admin fee in the above illustration, modify `fee` in the script to `4000000` to resemble mainnet setting of 4 bps

