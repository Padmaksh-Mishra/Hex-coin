# Hexcoin - A Decentralized Blockchain-based Cryptocurrency & ICO

Hexcoin is a decentralized cryptocurrency project that includes both a Python-based blockchain and a Solidity smart contract for an Initial Coin Offering (ICO). The blockchain ensures secure transaction processing using a proof-of-work consensus mechanism, while the ICO allows users to buy and sell Hexcoins.

## Features

### Blockchain
- **Proof of Work (PoW)**: Ensures secure and decentralized validation by requiring miners to solve cryptographic puzzles.
- **Transaction Management**: Users can send Hexcoins through transactions, which are recorded in blocks.
- **Node Connectivity**: Multiple nodes can connect to the network, ensuring the longest valid blockchain is maintained.
- **REST API with Flask**: A web interface exposes endpoints to interact with the blockchain for mining blocks, adding transactions, and node synchronization.

### ICO (Initial Coin Offering)
- **Smart Contract in Solidity**: A contract that manages the buying and selling of Hexcoins during the ICO.
- **Rupee-to-Hexcoin Conversion**: Investors can buy Hexcoins by converting their investment into Hexcoins at a fixed rate.
- **Buyback Mechanism**: Investors can sell their Hexcoins back to the ICO contract.

## Project Structure

- **Blockchain (Python)**:  
  The Python-based blockchain manages mining, transactions, proof-of-work, and node synchronization using Flask.

- **ICO Smart Contract (Solidity)**:  
  The Solidity smart contract allows users to buy and sell Hexcoins and tracks their equity in both Hexcoins and USD.

## How to Run the Blockchain

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/hexcoin.git
    cd hexcoin
    ```

2. Install dependencies:
    ```bash
    pip install Flask requests
    ```

3. Run the Flask app:
    ```bash
    python hexcoin.py
    ```
    The app runs on port `5001`.

### Blockchain API Endpoints

- **Mine a Block:** `/mine_block`  
  Mines a new block and adds transactions to the blockchain.

- **Get Blockchain:** `/get_chain`  
  Returns the entire blockchain.

- **Check Validity:** `/is_valid`  
  Checks if the blockchain is valid.

- **Add Transaction:** `/add_transaction`  
  Adds a new transaction to be included in the next mined block.

- **Connect Nodes:** `/connect_nodes`  
  Connects nodes to the network.

- **Replace Chain:** `/replace_chain`  
  Syncs the blockchain across nodes to ensure consistency.

## Explanation of the ICO Smart Contract

The Hexcoin ICO smart contract is written in Solidity and is used to manage the buying and selling of Hexcoins. The contract defines key parameters such as the maximum number of Hexcoins available (1,000,000), the conversion rate from rupees to Hexcoins (1 rupee = 1000 Hexcoins), and the total number of Hexcoins bought so far.

### Key Functions

1. **Equity Tracking**:  
   Each investor's equity is tracked in both Hexcoins and USD. The contract uses mappings to store the amount of Hexcoins and USD equity an investor holds. Two functions, `equity_in_hexcoins()` and `equity_in_usd()`, allow investors to view their holdings.

2. **Buying Hexcoins**:  
   The `buy_hexcoins()` function allows an investor to purchase Hexcoins by sending an amount of investment in rupees. The function calculates how many Hexcoins can be bought with the investment, checks if the maximum supply has been reached, and updates the investor's equity and total Hexcoins bought.

3. **Selling Hexcoins (Buyback Mechanism)**:  
   Investors can sell back their Hexcoins using the `sell_hexcoins()` function. This reduces the investor's equity and decreases the total number of Hexcoins bought.

4. **Modifier to Enforce Limits**:  
   The `can_buy_hexcoin()` modifier ensures that an investor cannot purchase more Hexcoins than are available. This ensures that the total Hexcoins bought never exceeds the maximum supply of 1,000,000 Hexcoins.

### Smart Contract Flow
- **Buy Hexcoins**: When an investor buys Hexcoins, the contract checks if the total supply has room for more purchases. If so, the investor's equity is updated, and they receive Hexcoins proportional to their investment.
- **Sell Hexcoins**: Investors can sell their Hexcoins back to the contract, and their equity in both Hexcoins and USD is updated accordingly.

## How to Use the ICO Smart Contract

1. **Set up a Solidity development environment** using [Remix](https://remix.ethereum.org/) or [Truffle](https://www.trufflesuite.com/).
2. **Deploy the smart contract** on a local Ethereum network (e.g., Ganache) or a test network (e.g., Ropsten).
3. **Interact with the contract** using the exposed functions to buy and sell Hexcoins.

## Future Improvements

- **Encryption**: Add public/private key cryptography to secure transactions on the blockchain.
- **Front-end Interface**: Build a user-friendly front-end to interact with the blockchain and ICO functionalities.
- **Tokenomics**: Enhance the smart contract to support advanced tokenomics such as staking, inflation, and deflation mechanisms.
