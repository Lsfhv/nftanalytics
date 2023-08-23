import { ERC721Validator } from '@nibbstack/erc721-validator';
import * as Web3 from 'web3';

const web3 = new Web3(new Web3.providers.HttpProvider("https://goerli.infura.io/v3/b733902d9de349448dd8a88304ae04cb"));

web3.eth.subscribe()


