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