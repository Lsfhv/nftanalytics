import { ERC721Validator } from '@nibbstack/erc721-validator';
import * as Web3 from 'web3';

const web3 = new Web3(new Web3.providers.HttpProvider("https://goerli.infura.io/v3/b733902d9de349448dd8a88304ae04cb"));

const contract ="0x86b50fD81eA80aB8b84A32524D8526739e6b42E5";

const valid = new ERC721Validator(web3);

validator.basic(test, contract);

