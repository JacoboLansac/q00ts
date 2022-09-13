# fast-nft-template

This repository is a template for a fast NFT generation collection
When the opportunity comes, this repo should be forked and filled with the necessary information of the particular NFT collection

## Metadata

### Traits configuration
The metadata generation is automatic (and random). 
Configure a list of traits and corresponding probabilities at: `metadata-config.yaml`.

### Traits input images
Each configured trait in the `metadata-config.yaml` should have an existing `.png` file in `metadata/input/img`, example:
  - `metadata/input/img/eyes/`
  - `metadata/input/img/eyes/brown.png`
  - `metadata/input/img/eyes/blue.png`

### Generate metadata
Run the script `scripts/metadata/generate.py` to randomly generate a collection of token traits based on the configs.
Run the script `scripts/metadata/generate.py -i` also save the images overlapping traits, based on the same configuration.
(Note that the random seed is fixed, so every run will yield always same output traits).

### Metadata outputs
The generated traits of all items in the collection will be saved in:
`metadata/output/traits/collection_traits.json`

Stats for each trait class of the generated 
tokens can be found at `metadata/output/traits/stats.json`

The NFT generation will do its best to generate the NFTs respecting those probabilities, 
but as it is random, there will be small deviations.

### Metadata uploads
TODO: upload script to IPFS, programatcally, and get the hash of the collection




## Mint-page 

## Contract
Decide if we should use an ERC721 standard or a ERC721-A (Azuki). 
The benefit of ERC721-A is in gas fees when minting batches:
- ERC721: Gas price of minting 10 items is x10 of minting 1. 
- ERC721-A: Gas price of minting 10 items is == minting 1. 
We are interested in fast mints, greedy people speculating, so we want batch mints. 
