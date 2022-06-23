import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",

)

st.write("# Curve Finance Slippage Simulator")

st.sidebar.success("Select Swap, Withdrawal or Deposit above.")

# st.image("https://github.com/chrisckwong821/Curve_Finance_Slippage_Simulator/blob/main/resources/80W%25.png?raw=true")

st.markdown(
    """
    Simulate slippage & bonus for pool of various Amplifier(s), based on a targeted slippage(%) or a poolBalance(%) with custom size as a percentage of pool Total Value Locked (TVL).

    **👈 Select Swap, Withdrawal or Deposit from the sidebar**
    
"""
)

st.markdown(
    """
    ### Note:

    1. Modified simulation code from [Curve Finance](https://github.com/curvefi/curve-contract/blob/master/tests/simulation.py)
    2. Use a simple 2-coins model. 
    3. Assume no admin fee in the above illustration, modify `fee` in the script to `4000000` to resemble mainnet setting of 4 bps

    ### Contributor

    Core Simulation Logic: [GeekRunner](https://twitter.com/0xGeekRunner)
    Streamlit: [VJiang](https://twitter.com/vjiang_)

"""
)