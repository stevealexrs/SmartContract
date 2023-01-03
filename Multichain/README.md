# Multichain
Multichain is a router for web3. It is an infrastructure developed for arbitrary cross-chain interactions.

The main component of multichain is the Secure Multi Party Computation (SMPC or MPC) network. It is used to sign transaction for managing user accounts in different chains. Only whitelisted entities can join this network, you can see all the running [nodes](https://scan.multichain.org/#/network) but no one really know who they are 😶.

`anyswap-v1-core` consists of older smart contracts while `multichain-smart-contracts` stores newer smart contracts.

[Multichain Documentation](https://docs.multichain.org/)

[Source Code](https://github.com/anyswap)

# Components of Interest

## Governance Contracts
The tokens used are `MULTI` token and `veMulti` NFT. `veMULTI` is created by locking `MULTI`. `veMULTI` holders will receive part of the bridge fees. The smart contracts involved are located [here](./Contracts/veMULTI/contracts).

## Swapping
Users can move tokens from one chain to another, converting them to either native token or bridged token. Native tokens are provided via liquidity pool while bridged token are minted. There are two main functionalities for swapping which are swapin and swapout.

### Btc-like Chain
Btc-like chain only has one type of token and they can only be swapped into bridged token. To swap from btc-like chain, user needs to use P2SH script provided, sending btc to a P2SH address and gives them the hash.

### EVM-compatible chain
EVM-compatible chain usually consists of one native token and any amount of ERC20 token. To swap from EVM chain, user can simply use swapout function in smart contracts. The smart contract also consists of swapin function that can only be invoked by MPC nodes, so it is supposed that the swapin is called automatically by SMPC network after calling swapout.
