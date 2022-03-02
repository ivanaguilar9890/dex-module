# dex-module

**IMPORTANT**: If you want to run the file I'd recommend two things. First is that you use Google Colab instead of Jupyter Notebook. Reason for that is we are working with up to 100K's rows of data. So if you attempt to make the function calls locally, you might run out of memory which is not an issue in Google Colab. The second is that due to the popularity of Bitquery in the DEX-space, Bitquery's servers run slow so I'd recommend to use the module in non-peak hours ~ usually after 9 pm PST.

**IMPORTANT**: Bitquery changed their API a bit and while the module seemed to work, I'm not sure to what extent that will remain true. Remember to include your own Bitquery and Covalent API Keys.

```python
# File with all the helper functions. Since we are using google colab, file 
# gets deleted after a while so we need to upload it every time we close the
# page. Ideally work would be done locally, or by ourselves so we can mount our
# drive to colab (if continuting to work on colab) or place on same
# directory (for jupyter notebook)
import dex
import requests
import pandas as pd
# just to view things nicer
pd.set_option('display.max_colwidth', None)
```

The following are functions to get all pools from Uniswap v2, SushiSwap, and PancakeSwap v2 using the Covalent API.

*   dex.get_uniswap_pools()
*   dex.get_sushiswap_pools()
*   dex.get_pancakse_pools()

We should use these functions if we want to know the contract address and the token decimals of a particular pool. We will need them to use BitQuery.

Technical Note: Returns a dictionary of the following form

{poolname: [contractAddress, token0-decimals, token1-decimals], ...}

poolname: concatenation of ticker symbol for token 0 and token 1

contractAddress: is the pool's smart contract address ~ we need it to
                  use bitquery

token0-decimals: how many decimals token 0 uses for precision

token1-decimals: how many decimals token 1 uses for precision


```python
# should say that covalent was able to return requests
data_from_uniswap = dex.get_uniswap_pools()
```

    Covalent was able to return requests
    


```python
# Function to get all SushiSwap pools ~ read same notes as above
data_from_sushiswap = dex.get_sushiswap_pools()
```

    Covalent was able to return requests
    


```python
# Function to get all Pancake v2 pools ~ read same notes as above
data_from_pancakeswap = dex.get_pancake_pools()
```

    Covalent was able to return request
    

dex.get_pools is a simple function to search for pools with a specific ticker symbol. It will print out the pool name and data that we will need for bitquery.

It needs pools (one of the 3 variables defined earlier) and a searchTerm (string) of ticker symbol.


```python
dex.get_pools(data_from_uniswap, "WBTC")
```



<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>pool_name</th>
      <th>pertinent_data</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>WBTC-BADGER</td>
      <td>[0xcd7989894bc033581532d2cd88da5db0a4b12859, 8, 18, WBTC, BADGER, WBTC, BADGER]</td>
    </tr>
    <tr>
      <th>1</th>
      <td>ARMOR-WBTC</td>
      <td>[0x888759cb22cedadf2cfb0049b03309d45aa380d9, 18, 8, ARMOR, WBTC, ARMOR, WBTC]</td>
    </tr>
    <tr>
      <th>2</th>
      <td>WBTC-WETH</td>
      <td>[0xbb2b8038a1640196fbe3e38816f3e67cba72d940, 8, 18, WBTC, WETH, WBTC, WETH]</td>
    </tr>
    <tr>
      <th>3</th>
      <td>WBTC-MATIC</td>
      <td>[0x4500d866bedb9d8fc280924b31c76dacf7979cae, 8, 18, WBTC, MATIC, WBTC, MATIC]</td>
    </tr>
    <tr>
      <th>4</th>
      <td>WBTC-BMI</td>
      <td>[0xfb4717730bd51736af3f19f05473bd89f7b23190, 8, 18, WBTC, BMI, WBTC, BMI]</td>
    </tr>
    <tr>
      <th>5</th>
      <td>WBTC-USDC</td>
      <td>[0x004375dff511095cc5a197a54140a24efef3a416, 8, 6, WBTC, USDC, WBTC, USDC]</td>
    </tr>
    <tr>
      <th>6</th>
      <td>WBTC-ACR</td>
      <td>[0xb301821567b2c8b7a4045000427e5c1c89bc6443, 8, 18, WBTC, ACR, WBTC, ACR]</td>
    </tr>
    <tr>
      <th>7</th>
      <td>WBTC-HEX</td>
      <td>[0x96da3b8edea72329c791d9baf5521909791df560, 8, 8, WBTC, HEX, WBTC, HEX]</td>
    </tr>
    <tr>
      <th>8</th>
      <td>WBTC-DYP</td>
      <td>[0x44b77e9ce8a20160290fcbaa44196744f354c1b7, 8, 18, WBTC, DYP, WBTC, DYP]</td>
    </tr>
    <tr>
      <th>9</th>
      <td>WBTC-SWAPP</td>
      <td>[0x5548f847fd9a1d3487d5fbb2e8d73972803c4cce, 8, 18, WBTC, SWAPP, WBTC, SWAPP]</td>
    </tr>
    <tr>
      <th>10</th>
      <td>WBTC-DAI</td>
      <td>[0x231b7589426ffe1b75405526fc32ac09d44364c4, 8, 18, WBTC, DAI, WBTC, DAI]</td>
    </tr>
    <tr>
      <th>11</th>
      <td>WBTC-XPR</td>
      <td>[0x39993cf130593b571165f4f932799d3bcb62a1d2, 8, 4, WBTC, XPR, WBTC, XPR]</td>
    </tr>
    <tr>
      <th>12</th>
      <td>WBTC-ZERO</td>
      <td>[0x87f1a9ca512a345f4c35cf5db0081ccae7015c1d, 8, 18, WBTC, ZERO, WBTC, ZERO]</td>
    </tr>
    <tr>
      <th>13</th>
      <td>WBTC-PEAK</td>
      <td>[0xc2f71bbca8fc4b8f0646bfe49c2514913f51c328, 8, 8, WBTC, PEAK, WBTC, PEAK]</td>
    </tr>
  </tbody>
</table>
</div>




```python
# different exchanges ~ different contract addresses
dex.get_pools(data_from_sushiswap, "WBTC")
```


<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>pool_name</th>
      <th>pertinent_data</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>WBTC-POLY</td>
      <td>[0x7835cb043e8d53a5b361d489956d6c30808349da, 8, 18, WBTC, POLY]</td>
    </tr>
    <tr>
      <th>1</th>
      <td>WBTC-BADGER</td>
      <td>[0x110492b31c59716ac47337e616804e3e3adc0b4a, 8, 18, WBTC, BADGER]</td>
    </tr>
    <tr>
      <th>2</th>
      <td>BTC2x-FLI-WBTC</td>
      <td>[0x164fe0239d703379bddde3c80e4d4800a1cd452b, 18, 8, BTC2x, FLI]</td>
    </tr>
    <tr>
      <th>3</th>
      <td>WBTC-WETH</td>
      <td>[0xceff51756c56ceffca006cd410b03ffc46dd3a58, 8, 18, WBTC, WETH]</td>
    </tr>
    <tr>
      <th>4</th>
      <td>WBTC-DIGG</td>
      <td>[0x9a13867048e01c663ce8ce2fe0cdae69ff9f35e3, 8, 9, WBTC, DIGG]</td>
    </tr>
  </tbody>
</table>
</div>




```python
# different exchanges ~ different contract addresses
dex.get_pools(data_from_pancakeswap, "WBTC")
```



<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>pool_name</th>
      <th>pertinent_data</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ZEFI-WBTCT</td>
      <td>[0x0c1dae111a5d4a2716c5e9b443d4a2d3c0ef9294, 18, 18, ZEFI, WBTCT]</td>
    </tr>
    <tr>
      <th>1</th>
      <td>WBNB-NEWBTC</td>
      <td>[0x15ef709244d714341828338dba5b70bbbe0cf677, 18, 18, WBNB, NEWBTC]</td>
    </tr>
    <tr>
      <th>2</th>
      <td>WBNB-NEWBTC</td>
      <td>[0x2e49edd60fd45bde3da36fa8e4943dcc6337e8fc, 18, 18, WBNB, NEWBTC]</td>
    </tr>
    <tr>
      <th>3</th>
      <td>WBNB-WBTCT</td>
      <td>[0x316f72ef0b2aaea69b20c4141374d5d91504c403, 18, 18, WBNB, WBTCT]</td>
    </tr>
    <tr>
      <th>4</th>
      <td>WBTC-WBNB</td>
      <td>[0x5f44760d62a0d84bb79f9c88a9be7d32708f35ad, 6, 18,  WBTC, WBNB]</td>
    </tr>
    <tr>
      <th>5</th>
      <td>NEWBTC-WBNB</td>
      <td>[0x99883cae45a93b37da05943d7e9cd0ba4368654c, 18, 18, NEWBTC, WBNB]</td>
    </tr>
    <tr>
      <th>6</th>
      <td>WBTCT-BUSD</td>
      <td>[0xe85b946f9858f6c6bd355cdc51affeb5e987c5ef, 18, 18, WBTCT, BUSD]</td>
    </tr>
  </tbody>
</table>
</div>



After we've done an initial query we should use dex.get_pool to get array of data used for burns and mints. Here I print them out and later copy them to show how the other functions work but ideally we save the array of data to a variable.


```python
print(dex.get_pool(data_from_uniswap, "WBTC-USDC"))
print(dex.get_pool(data_from_sushiswap, "WBTC-WETH"))
print(dex.get_pool(data_from_pancakeswap, "WBTCT-BUSD"))
```

    ['0x004375dff511095cc5a197a54140a24efef3a416', 8, 6, 'WBTC', 'USDC']
    ['0xceff51756c56ceffca006cd410b03ffc46dd3a58', 8, 18, 'WBTC', 'WETH']
    ['0xe85b946f9858f6c6bd355cdc51affeb5e987c5ef', 18, 18, 'WBTCT', 'BUSD']
    

Call dex.get_swaps() to get all swaps for a pool with specified contract address
Paramters in order:


*   exchangeName (string): name of DEX name currently only supports "Uniswap", "Pancake v2", and "SushiSwap". Do note that it is case sensitive for now.
*   contractAddress (string): Hex string for contractAddress of pool

** NOTE **: Getting swaps will always take longer on average than for burns and mints. As long as output is being shown, rest assured the bitquery API is working


```python
test_df = dex.get_swaps("Uniswap", ['0x004375dff511095cc5a197a54140a24efef3a416', 8, 6, 'WBTC', 'USDC'])
```

    1st API call done
    API call #2 done
    API call #3 done
    API call #4 done
    API call #5 done
    API call #6 done
    API call #7 done
    API call #8 done
    API call #9 done
    API call #10 done
    API call #11 done
    API call #12 done
    


```python
test_df
```


<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>block_height</th>
      <th>timestamp</th>
      <th>WBTCIn</th>
      <th>USDCIn</th>
      <th>WBTCOut</th>
      <th>USDCOut</th>
      <th>transaction_hash</th>
      <th>from</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>10099386</td>
      <td>2020-05-19T23:44:23Z</td>
      <td>0.000000e+00</td>
      <td>0.153417</td>
      <td>0.000016</td>
      <td>0.000000</td>
      <td>0xba9a47ed6b7d293da7e7643f434055ff76bdf609274f63f177e058d4e506ef3c</td>
      <td>0x6f1821a5fa09c0d1c833ba714f4adae3c8a8edd9</td>
    </tr>
    <tr>
      <th>1</th>
      <td>10109833</td>
      <td>2020-05-21T14:39:56Z</td>
      <td>2.501000e-04</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>2.367365</td>
      <td>0xffff2870fd0aa2f909766844c95f53b83625854c925e2950ac030233d19fe71c</td>
      <td>0x4d37f28d2db99e8d35a6c725a5f1749a085850a3</td>
    </tr>
    <tr>
      <th>2</th>
      <td>10117856</td>
      <td>2020-05-22T20:47:02Z</td>
      <td>1.047330e-03</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>9.603013</td>
      <td>0x68e9800197efaafee864d33cf6167d12e4aa29a527c9234f2288ca649d70c814</td>
      <td>0xb8bd8f4c420ada4d999f2619503d5aaa139ed7c2</td>
    </tr>
    <tr>
      <th>3</th>
      <td>10122526</td>
      <td>2020-05-23T14:00:42Z</td>
      <td>0.000000e+00</td>
      <td>0.892319</td>
      <td>0.000098</td>
      <td>0.000000</td>
      <td>0x33fbec2e6e1a3a04a1f5109f3a8809f32c7ad7e75c7da627f8ed0bea2dd1c8fe</td>
      <td>0x86e3209766b078527f77969f8013bec5dcdebaa4</td>
    </tr>
    <tr>
      <th>4</th>
      <td>10129928</td>
      <td>2020-05-24T17:37:32Z</td>
      <td>1.100000e-07</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.001000</td>
      <td>0x273375cad4d5cf584b70af639f3cf07a53ba00a0721677a37b662b2a636667dc</td>
      <td>0x211b6a1137bf539b2750e02b9e525cf5757a35ae</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>119885</th>
      <td>12775109</td>
      <td>2021-07-06T16:56:41Z</td>
      <td>0.000000e+00</td>
      <td>2000.000000</td>
      <td>0.059042</td>
      <td>0.000000</td>
      <td>0x99770e4ae6e343c68878b8f60168c37184db5d41b54083504811c83bcb0ac9ee</td>
      <td>0x4647116a410ca5e80ee2be0077335bbf0db35166</td>
    </tr>
    <tr>
      <th>119886</th>
      <td>12775480</td>
      <td>2021-07-06T18:23:18Z</td>
      <td>0.000000e+00</td>
      <td>99.379603</td>
      <td>0.002928</td>
      <td>0.000000</td>
      <td>0x8fcd26b0faada45d32a3197af84e686ddb3552869f31e878364883f246859895</td>
      <td>0xf68fcdb95782d9c403a9edf8f02f3fd9ecf0b804</td>
    </tr>
    <tr>
      <th>119887</th>
      <td>12775500</td>
      <td>2021-07-06T18:27:13Z</td>
      <td>0.000000e+00</td>
      <td>1000.000000</td>
      <td>0.029436</td>
      <td>0.000000</td>
      <td>0xd067ecea7bc2a14b6a39a27e04fe9d9332efc48008682801f13680a4b39ac9a6</td>
      <td>0x05015f9638422735a59c69720810d55a8830fb45</td>
    </tr>
    <tr>
      <th>119888</th>
      <td>12776055</td>
      <td>2021-07-06T20:26:56Z</td>
      <td>0.000000e+00</td>
      <td>677.797041</td>
      <td>0.019922</td>
      <td>0.000000</td>
      <td>0xfe722e999c33630fb49e999cb79f09c765ab669d48f494a7a02fd4e8d9e21fa1</td>
      <td>0x46eaadc8f2199463db26d1797131900575f0d264</td>
    </tr>
    <tr>
      <th>119889</th>
      <td>12776444</td>
      <td>2021-07-06T21:57:24Z</td>
      <td>8.112450e-03</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>274.457826</td>
      <td>0xbe3256a8fc3c30f26d674fec37fc091fbb0e2609b7f97d415636f48453c7f8a7</td>
      <td>0x3e696165b650bfa8e29eb1f4e9352ed0a91a489c</td>
    </tr>
  </tbody>
</table>
<p>119890 rows × 8 columns</p>
</div>




```python
# also works for sushiswap and pancakeswaps ~ tried on different file (since in shared pipeline
# colab was getting errors everytime someone ran code on their end so had to test somewhere else but still works)
```

dex.mints() is used to get the mints of a particular pool
Paramters in order:


*   exchangeName (string) name of DEX also case sensitive so "Uniswap" "Pancake v2" and "SushiSwap" only work for now
*   dataList (list): -> [contractAddress, ticker-symbol 0 decimals, ticker-symbol 1 decimals, ticker-symbol 0 name, ticker-symbol 1 name]

So again we want to use the dex.get_pool function to get this array for us. I copy/pase them here to make it clearer what I'm doing but ideally want to save output of previous function into a variable and pass it here




```python
uni_mints = dex.get_mints("Uniswap", ['0x004375dff511095cc5a197a54140a24efef3a416', 8, 6, 'WBTC', 'USDC'])
```


```python
# display data_frame
uni_mints
```

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>block_height</th>
      <th>timestamp</th>
      <th>transaction_hash</th>
      <th>from</th>
      <th>WBTC</th>
      <th>USDC</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>10092348</td>
      <td>2020-05-18T21:17:30Z</td>
      <td>0x728bb396f3d4f674d36447fae392a524244ba02db0a44f9160d132e285d9b8c6</td>
      <td>0x4d37f28d2db99e8d35a6c725a5f1749a085850a3</td>
      <td>0.000058</td>
      <td>0.565606</td>
    </tr>
    <tr>
      <th>1</th>
      <td>10096379</td>
      <td>2020-05-19T12:27:11Z</td>
      <td>0xbbfa5992d44c6b0bb0572f68ea933e648537d71b6e25dc2d3ff3e380626580ec</td>
      <td>0xe0e8c1d735698060477e79a8e4c20276fc2ec7a7</td>
      <td>0.031843</td>
      <td>308.949238</td>
    </tr>
    <tr>
      <th>2</th>
      <td>10099386</td>
      <td>2020-05-19T23:44:23Z</td>
      <td>0xba9a47ed6b7d293da7e7643f434055ff76bdf609274f63f177e058d4e506ef3c</td>
      <td>0x6f1821a5fa09c0d1c833ba714f4adae3c8a8edd9</td>
      <td>0.010943</td>
      <td>106.173412</td>
    </tr>
    <tr>
      <th>3</th>
      <td>10099386</td>
      <td>2020-05-19T23:44:23Z</td>
      <td>0xba9a47ed6b7d293da7e7643f434055ff76bdf609274f63f177e058d4e506ef3c</td>
      <td>0x6f1821a5fa09c0d1c833ba714f4adae3c8a8edd9</td>
      <td>0.000016</td>
      <td>0.152924</td>
    </tr>
    <tr>
      <th>4</th>
      <td>10100943</td>
      <td>2020-05-20T05:27:48Z</td>
      <td>0xef54b757588dd3163f28df671ec05a40685406d50e56716617fd5267f3fdfcea</td>
      <td>0xe0e8c1d735698060477e79a8e4c20276fc2ec7a7</td>
      <td>0.031445</td>
      <td>305.317587</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>629</th>
      <td>13397179</td>
      <td>2021-10-11T12:02:45Z</td>
      <td>0xd588ab9303f3b1be561bbc1f01512ff2fe6c33a4be540abdc4653bf9e5637a83</td>
      <td>0x8539d9954e76f5d25b81107b77d3194b8db6d6a3</td>
      <td>0.083782</td>
      <td>4720.518454</td>
    </tr>
    <tr>
      <th>630</th>
      <td>13444690</td>
      <td>2021-10-18T23:26:08Z</td>
      <td>0xec6e956db5a9df20ad43a3b46e28934b7506ead9657ebc1e15603d0559caefba</td>
      <td>0x45a6a57bacc5bd28b4de0e06ef8b74055eaa925a</td>
      <td>0.245886</td>
      <td>15222.753672</td>
    </tr>
    <tr>
      <th>631</th>
      <td>13568321</td>
      <td>2021-11-07T08:33:03Z</td>
      <td>0xe717ba3fc4f0c01c63def26b000f68b71b562287173231c0db72e5d69229eb1e</td>
      <td>0x24e86375c0b69ea87595f02382e5e566165dfa27</td>
      <td>0.155700</td>
      <td>9650.106680</td>
    </tr>
    <tr>
      <th>632</th>
      <td>13755954</td>
      <td>2021-12-07T02:23:07Z</td>
      <td>0x85de2156b76811617801677415f1b3bac135123292754493e37646fde4077363</td>
      <td>0x741d51f3ad128185cd4da47ea3421ce6eb6e6377</td>
      <td>0.098712</td>
      <td>5000.988000</td>
    </tr>
    <tr>
      <th>633</th>
      <td>13765545</td>
      <td>2021-12-08T15:26:02Z</td>
      <td>0x97b5c0bc1114f301c4a66b795e73ffda08da470bf21d4b88fa366ba3a0dfa1f3</td>
      <td>0x5418820a3f975bacbccce1322ece14032a8711d6</td>
      <td>0.152300</td>
      <td>7731.027611</td>
    </tr>
  </tbody>
</table>
<p>634 rows × 6 columns</p>
</div>




```python
sushi_mints = dex.get_mints("SushiSwap", ['0xceff51756c56ceffca006cd410b03ffc46dd3a58', 8, 18, 'WBTC', 'WETH'])
```


```python
# display data frame
sushi_mints
```

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>block_height</th>
      <th>timestamp</th>
      <th>transaction_hash</th>
      <th>from</th>
      <th>WBTC</th>
      <th>WETH</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>10840845</td>
      <td>2020-09-11T13:29:46Z</td>
      <td>0x060e28d146967d765bacd710e53d36a55b840d9da7744c1b5f62eadb984991fd</td>
      <td>0x2c076d91b9ca5475cd168b018707eea87204baac</td>
      <td>0.177665</td>
      <td>4.970000</td>
    </tr>
    <tr>
      <th>1</th>
      <td>10925651</td>
      <td>2020-09-24T13:37:06Z</td>
      <td>0x0180442580bce896c56a6e91b6cdf4ca5c3d6d16a2913025b0a78911109c5367</td>
      <td>0x9e6e344f94305d36ea59912b0911fe2c9149ed3e</td>
      <td>0.001000</td>
      <td>0.000053</td>
    </tr>
    <tr>
      <th>2</th>
      <td>10925748</td>
      <td>2020-09-24T13:59:50Z</td>
      <td>0x5aa4f1452e87d0218780640091cf056c56fd0332392b210fda67e341bf8f2ccd</td>
      <td>0x9e6e344f94305d36ea59912b0911fe2c9149ed3e</td>
      <td>0.031364</td>
      <td>0.994633</td>
    </tr>
    <tr>
      <th>3</th>
      <td>10930581</td>
      <td>2020-09-25T07:47:42Z</td>
      <td>0x557ff5255ed925c56e196023c6424d9330490aaef776b8238130de96b1b3d3be</td>
      <td>0xc92165b4e7b7899955c73b6002a17f71bff3a28a</td>
      <td>0.001497</td>
      <td>0.052353</td>
    </tr>
    <tr>
      <th>4</th>
      <td>10952781</td>
      <td>2020-09-28T19:18:21Z</td>
      <td>0x023a71e7337fe2c321c94e76abd24ad6fae450ac2a7bd68005a3132fd179c81e</td>
      <td>0x8867ef1593f6a72dbbb941d4d96b746a4da691b2</td>
      <td>0.013900</td>
      <td>0.422353</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>8528</th>
      <td>13767886</td>
      <td>2021-12-09T00:22:12Z</td>
      <td>0x7a9a8cffc9c14622a8e82912310fe67c3921c8d33d6aac4855db70c44469ee83</td>
      <td>0xbed04c43e74150794f2ff5b62b4f73820edaf661</td>
      <td>0.005486</td>
      <td>0.062329</td>
    </tr>
    <tr>
      <th>8529</th>
      <td>13771307</td>
      <td>2021-12-09T13:31:08Z</td>
      <td>0xf624f0bd57038013561ba8979b65ba1cb676eb132c886c7b44bb90ff082799cc</td>
      <td>0x72b2342a1609f464819db63703789278bb0358af</td>
      <td>0.037526</td>
      <td>0.429924</td>
    </tr>
    <tr>
      <th>8530</th>
      <td>13784017</td>
      <td>2021-12-11T13:06:24Z</td>
      <td>0xf4d575cae9a24bd05bdae24c5c7e659d401f70335d827f6fe6dd4fe3bb45cff3</td>
      <td>0xcfbcd6928e0ab235ea2abed8f8a18775fdc8fea8</td>
      <td>0.004993</td>
      <td>0.060000</td>
    </tr>
    <tr>
      <th>8531</th>
      <td>13791243</td>
      <td>2021-12-12T15:59:35Z</td>
      <td>0x799ffe102a0865dd261ee3c404b330435cc869967ce65cafc3eed4cbe023a87c</td>
      <td>0x374730a9a23030fbc80d0c4aeb2aa0e40e04238d</td>
      <td>0.000041</td>
      <td>0.000499</td>
    </tr>
    <tr>
      <th>8532</th>
      <td>13798881</td>
      <td>2021-12-13T19:50:13Z</td>
      <td>0xf1fc9036f8e8a56abe364e2a732238b241da435e47f19dbb3a428203d21bf5ee</td>
      <td>0xb35ea231b18dc4339f9bb82f95915d65e5b30be5</td>
      <td>0.008029</td>
      <td>0.100000</td>
    </tr>
  </tbody>
</table>
<p>8533 rows × 6 columns</p>
</div>




```python
# do for pancakse swap
pancake_mints = dex.get_mints("Pancake v2", ['0xe85b946f9858f6c6bd355cdc51affeb5e987c5ef', 18, 18, 'WBTCT', 'BUSD'])
```


```python
# display dataframe
pancake_mints
```


<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>block_height</th>
      <th>timestamp</th>
      <th>transaction_hash</th>
      <th>from</th>
      <th>WBTCT</th>
      <th>BUSD</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>7218813</td>
      <td>2021-05-07T16:39:05Z</td>
      <td>0xf43915422ff2c15643e6355ca100f5c7efd3d594ea090f9a81d3c3d7c0823729</td>
      <td>0xa13443db578af67aa80ea0f106377d5e9a62686f</td>
      <td>10.000000</td>
      <td>0.230000</td>
    </tr>
    <tr>
      <th>1</th>
      <td>7231920</td>
      <td>2021-05-08T03:46:41Z</td>
      <td>0x4d28dcafd6136fc8d5d34ccb490bc5e4284e555ddd645fb34eec53b8d390e37b</td>
      <td>0xc604c6eb604ce9b4e10ab55178231972be4f4cb9</td>
      <td>3776.575219</td>
      <td>86.861230</td>
    </tr>
    <tr>
      <th>2</th>
      <td>7234503</td>
      <td>2021-05-08T06:00:41Z</td>
      <td>0xa6115992df26bc6dbb4985dd400299ad786eae0f7be53df6b8b040aa7fe0e305</td>
      <td>0xe926d68bd634a1fa586e19c8e112e1f2b75a39c4</td>
      <td>752.014011</td>
      <td>11.600551</td>
    </tr>
    <tr>
      <th>3</th>
      <td>7235580</td>
      <td>2021-05-08T06:54:32Z</td>
      <td>0xf1c8ca525a6714aa34cd45283ee65d5dfc7e82da5e630e3f01046cd0cd302e34</td>
      <td>0xbf8faa9a7bca427317ac52a4fe020069bf317c08</td>
      <td>3700.000000</td>
      <td>57.076117</td>
    </tr>
    <tr>
      <th>4</th>
      <td>7238059</td>
      <td>2021-05-08T08:58:47Z</td>
      <td>0xebb754c98674c329e0665ec6ddcd82ae7ed806a743daba9b3d2027cf379e64cc</td>
      <td>0xbf8faa9a7bca427317ac52a4fe020069bf317c08</td>
      <td>1320.000000</td>
      <td>19.678841</td>
    </tr>
    <tr>
      <th>5</th>
      <td>7239380</td>
      <td>2021-05-08T10:05:19Z</td>
      <td>0xe58fad22b72dc4fe15a8939ead9c85db78647699f062c316271180b10b627adb</td>
      <td>0xbbc53779d5f1a7d016aaed9d71eaa072c2f405c6</td>
      <td>419.936813</td>
      <td>6.260507</td>
    </tr>
    <tr>
      <th>6</th>
      <td>7239500</td>
      <td>2021-05-08T10:11:19Z</td>
      <td>0x0a8446e97b848cd067d156681db9105ff0f90ec15a42a07c7bebebf82497f435</td>
      <td>0xfc11822d8b1ca7de471410bed9d0999f2fed7bd3</td>
      <td>7882.380699</td>
      <td>117.512209</td>
    </tr>
    <tr>
      <th>7</th>
      <td>7239548</td>
      <td>2021-05-08T10:13:43Z</td>
      <td>0xce275372d67933dd0e1cea87d994b6ca24aaf2ace923aa6023b9638831481863</td>
      <td>0xfc11822d8b1ca7de471410bed9d0999f2fed7bd3</td>
      <td>7870.697476</td>
      <td>145.789583</td>
    </tr>
    <tr>
      <th>8</th>
      <td>7239589</td>
      <td>2021-05-08T10:15:46Z</td>
      <td>0x6c3689a0095c57e243ed78fcb6ceb273f7d1f8a4a7a84fa5e2322023e12be474</td>
      <td>0xfc11822d8b1ca7de471410bed9d0999f2fed7bd3</td>
      <td>2869.422284</td>
      <td>53.150547</td>
    </tr>
    <tr>
      <th>9</th>
      <td>7239653</td>
      <td>2021-05-08T10:19:06Z</td>
      <td>0x0066578e4234bada6255c8f96d9ca87855280b6ac322434bb10736b45d1e2f9b</td>
      <td>0xfc11822d8b1ca7de471410bed9d0999f2fed7bd3</td>
      <td>1684.550000</td>
      <td>31.203060</td>
    </tr>
    <tr>
      <th>10</th>
      <td>7241847</td>
      <td>2021-05-08T12:09:57Z</td>
      <td>0xee973f74e0a26b3999c950ec13498a16b540754e458b0c342256d479a0e78bb7</td>
      <td>0x16f9415bc924e5b61f1d9b46a885218ca7f5f011</td>
      <td>1386.280068</td>
      <td>27.984636</td>
    </tr>
    <tr>
      <th>11</th>
      <td>7241976</td>
      <td>2021-05-08T12:16:53Z</td>
      <td>0x19fa8daa0d696adae22a9b649312eb6503ab2aa786fd95a92a69dc6f4a0e2fc8</td>
      <td>0xd4396ea8ac8e9954f33457e6d1249729db2b7960</td>
      <td>732.116349</td>
      <td>15.557488</td>
    </tr>
    <tr>
      <th>12</th>
      <td>7244128</td>
      <td>2021-05-08T14:07:12Z</td>
      <td>0xfbfb8f8a963c62c2100c17916a8b627fdbb8793907b1de96b3e1de65d20bf072</td>
      <td>0x5eca99da748778f2897d8333adcb68d4ca8d4357</td>
      <td>4017.345959</td>
      <td>90.460029</td>
    </tr>
    <tr>
      <th>13</th>
      <td>7244731</td>
      <td>2021-05-08T14:40:44Z</td>
      <td>0xe2a621357f933e5c11e81b64344473c9de18de5108b678a5ec05b83b359223b1</td>
      <td>0xc96dede7868f8c190208a22812fd3539e9e2caf6</td>
      <td>2248.741865</td>
      <td>50.635732</td>
    </tr>
    <tr>
      <th>14</th>
      <td>7245679</td>
      <td>2021-05-08T15:32:22Z</td>
      <td>0x5accef81f7d5fe2b8db8ac1746eed0a63c6f467bb71a2dc3b0961469ff6d68d1</td>
      <td>0x4f74013cdad98637b1d140517aff029ef326e441</td>
      <td>6152.561189</td>
      <td>138.860821</td>
    </tr>
    <tr>
      <th>15</th>
      <td>7252475</td>
      <td>2021-05-08T21:37:13Z</td>
      <td>0x5335d1b622e2031a7e595ca08eac4a748d220d0665d77cd2b194be2bd8af2bb5</td>
      <td>0x92e5fef90e258b742c16bee2c674e9a8dfcec01b</td>
      <td>19547.377233</td>
      <td>441.176410</td>
    </tr>
    <tr>
      <th>16</th>
      <td>7252553</td>
      <td>2021-05-08T21:41:27Z</td>
      <td>0xa3fc73d9a1ae66dfd1521eb504ffde4046dfdef4dc7277cee26629690b687361</td>
      <td>0x92e5fef90e258b742c16bee2c674e9a8dfcec01b</td>
      <td>19547.377233</td>
      <td>441.176410</td>
    </tr>
    <tr>
      <th>17</th>
      <td>7255485</td>
      <td>2021-05-09T00:10:44Z</td>
      <td>0xe283656c7a4bba619f678349736d8c951ca916b3105aa333dc282ed489eb7a38</td>
      <td>0x5952a1e9445d7f32cddc964f74f23fae80130796</td>
      <td>35445.915548</td>
      <td>800.000000</td>
    </tr>
    <tr>
      <th>18</th>
      <td>7255492</td>
      <td>2021-05-09T00:11:05Z</td>
      <td>0x54432068ba8fab01f7cbfc3af6570435d43edbb131be775be3206ec1c34292d9</td>
      <td>0x5952a1e9445d7f32cddc964f74f23fae80130796</td>
      <td>1000.000000</td>
      <td>22.569596</td>
    </tr>
    <tr>
      <th>19</th>
      <td>7318864</td>
      <td>2021-05-11T10:56:49Z</td>
      <td>0x127c6a473a4bb85836db76dd765d80c353bbee0d9e40744de50a101d9b72c1d7</td>
      <td>0x6dcb50cb08ffaa9147d6cb62d4a6ef512a8d4a76</td>
      <td>3963.593833</td>
      <td>81.680534</td>
    </tr>
    <tr>
      <th>20</th>
      <td>7332101</td>
      <td>2021-05-11T22:48:34Z</td>
      <td>0x600b5a501a27c5fb346ca5ef404d519304e62f9d1bcd18632ea3e8c613e2c0b3</td>
      <td>0x6dcb50cb08ffaa9147d6cb62d4a6ef512a8d4a76</td>
      <td>3996.338325</td>
      <td>75.000000</td>
    </tr>
    <tr>
      <th>21</th>
      <td>7339418</td>
      <td>2021-05-12T05:38:52Z</td>
      <td>0x2ecb80982dd10c21ed6316eae33763409acdf4548583bb1a36d45d99b403e54f</td>
      <td>0xec25f5068405117d75c99c6e6a27eb4727915dd0</td>
      <td>10042.000000</td>
      <td>191.173386</td>
    </tr>
    <tr>
      <th>22</th>
      <td>7408160</td>
      <td>2021-05-14T16:57:27Z</td>
      <td>0x90d63f914d67cdb4177c897ae1c0e3eec0e5d43679d5e7a2d6e58e8a9c0be3f1</td>
      <td>0x5952a1e9445d7f32cddc964f74f23fae80130796</td>
      <td>4500.000000</td>
      <td>72.564764</td>
    </tr>
    <tr>
      <th>23</th>
      <td>7408169</td>
      <td>2021-05-14T16:57:54Z</td>
      <td>0xada4a8323d4f93cb20d352b9f86d4390b545227e32fda2f44c9b04a3612ca3c8</td>
      <td>0x5952a1e9445d7f32cddc964f74f23fae80130796</td>
      <td>500.000000</td>
      <td>8.062752</td>
    </tr>
    <tr>
      <th>24</th>
      <td>7432679</td>
      <td>2021-05-15T14:01:57Z</td>
      <td>0xa63edcdaca8bc00f1ce4058c90ede2c08227f61a9cf072832d9f6e9dc29e9c1c</td>
      <td>0x53e3d894fd361a8ab76d8c8bfd32774b8a7027a8</td>
      <td>9348.006953</td>
      <td>148.348665</td>
    </tr>
    <tr>
      <th>25</th>
      <td>7444737</td>
      <td>2021-05-16T00:09:13Z</td>
      <td>0x005b4487fbcf40549ef1a7618ad122af70da6d521363a05b230f344c9e86553b</td>
      <td>0x5952a1e9445d7f32cddc964f74f23fae80130796</td>
      <td>2375.933098</td>
      <td>36.680280</td>
    </tr>
    <tr>
      <th>26</th>
      <td>7445939</td>
      <td>2021-05-16T01:10:32Z</td>
      <td>0x34d65c1966272e59d55b13abb06d096eb7c9fa63ec8d079bd2156851e664f668</td>
      <td>0x6fccec5d1f5455758cce1c1742997391dd4453bc</td>
      <td>3500.000000</td>
      <td>54.033920</td>
    </tr>
    <tr>
      <th>27</th>
      <td>7445979</td>
      <td>2021-05-16T01:12:32Z</td>
      <td>0x554cd9d4d114f316fe5b0ca75caba561365c12631c7caeff54b62230017a676c</td>
      <td>0x6fccec5d1f5455758cce1c1742997391dd4453bc</td>
      <td>500.000000</td>
      <td>7.795464</td>
    </tr>
    <tr>
      <th>28</th>
      <td>7578137</td>
      <td>2021-05-20T16:50:06Z</td>
      <td>0x1b73e9afcd4f22528a015ac9068f7bf68df8efc2984504c19f4aefecfab0e7a3</td>
      <td>0x5952a1e9445d7f32cddc964f74f23fae80130796</td>
      <td>650.000000</td>
      <td>7.779082</td>
    </tr>
    <tr>
      <th>29</th>
      <td>7635566</td>
      <td>2021-05-22T16:53:32Z</td>
      <td>0xca60264058d2e8fccd5d81d253767d93b3adde352a22ba03248bb9d3e8642a17</td>
      <td>0x5952a1e9445d7f32cddc964f74f23fae80130796</td>
      <td>2363.388451</td>
      <td>29.461673</td>
    </tr>
    <tr>
      <th>30</th>
      <td>7950797</td>
      <td>2021-06-02T16:46:41Z</td>
      <td>0x1db7f267babef72af2c9d1bf77f7c4bc85134c704dca5363516f0e004a668154</td>
      <td>0x6fccec5d1f5455758cce1c1742997391dd4453bc</td>
      <td>1000.000000</td>
      <td>15.086937</td>
    </tr>
    <tr>
      <th>31</th>
      <td>8208912</td>
      <td>2021-06-11T16:26:58Z</td>
      <td>0xf3831dab2fbe2612b6478f84042a5f04cbde8b4ab86839e2d9906c993873ff05</td>
      <td>0x5952a1e9445d7f32cddc964f74f23fae80130796</td>
      <td>540.806098</td>
      <td>6.973072</td>
    </tr>
    <tr>
      <th>32</th>
      <td>8218020</td>
      <td>2021-06-12T00:05:12Z</td>
      <td>0xc4e08b48d65937d9b49e1b3b8720b19acd6ad5086ad5a997cfd9c0155b37ea44</td>
      <td>0x094418c628d20f0eaca6e49914fcf8f741a715a1</td>
      <td>1206.432145</td>
      <td>15.414172</td>
    </tr>
    <tr>
      <th>33</th>
      <td>8575596</td>
      <td>2021-06-24T12:18:34Z</td>
      <td>0x3120c7458f6a0de57339ff0ba37f60340453449ff83ea265d72d8295d5895e39</td>
      <td>0x5952a1e9445d7f32cddc964f74f23fae80130796</td>
      <td>7600.000000</td>
      <td>82.362808</td>
    </tr>
    <tr>
      <th>34</th>
      <td>8575605</td>
      <td>2021-06-24T12:19:01Z</td>
      <td>0x7be2122bd305353955ea0ea7f5731700fa851246dc6421fb7f06f63fed80167d</td>
      <td>0x5952a1e9445d7f32cddc964f74f23fae80130796</td>
      <td>6.000000</td>
      <td>0.065023</td>
    </tr>
    <tr>
      <th>35</th>
      <td>8586637</td>
      <td>2021-06-24T21:31:48Z</td>
      <td>0x1d54bc85744907c5cf6c5684bd56b134583d2bc91d0ff2f549ac091ed4c3327a</td>
      <td>0x3c156d794d00d2f0d2f6601e61156a9fcb4964ad</td>
      <td>1763.000000</td>
      <td>19.633080</td>
    </tr>
    <tr>
      <th>36</th>
      <td>8589556</td>
      <td>2021-06-24T23:58:16Z</td>
      <td>0xacf22fca4408bb197093228b3d4bc40812aaa602cc17cf10048679819839fec2</td>
      <td>0x3c156d794d00d2f0d2f6601e61156a9fcb4964ad</td>
      <td>8068.716437</td>
      <td>98.590689</td>
    </tr>
    <tr>
      <th>37</th>
      <td>8795344</td>
      <td>2021-07-02T04:30:05Z</td>
      <td>0x2055e1f354bb99972f3a7ccc4087e226406aa34683766fcef79e527746ab437c</td>
      <td>0x423ef74065dafe5ed75fd06e68fb1f097ca7fa9f</td>
      <td>115.582476</td>
      <td>0.998518</td>
    </tr>
    <tr>
      <th>38</th>
      <td>8820819</td>
      <td>2021-07-03T01:59:36Z</td>
      <td>0xd5dbbf41c81f80fd8530ace10595706cff35c0c77b6f1a9058d19951360799c1</td>
      <td>0x5952a1e9445d7f32cddc964f74f23fae80130796</td>
      <td>1884.689326</td>
      <td>16.000000</td>
    </tr>
    <tr>
      <th>39</th>
      <td>8844792</td>
      <td>2021-07-03T22:08:19Z</td>
      <td>0xde967f31af2a6b02be559b0157c44c6dc31daac5bd0d4e5f494f38c5986d5aea</td>
      <td>0x5952a1e9445d7f32cddc964f74f23fae80130796</td>
      <td>2762.067231</td>
      <td>25.224440</td>
    </tr>
    <tr>
      <th>40</th>
      <td>8844813</td>
      <td>2021-07-03T22:09:22Z</td>
      <td>0xf99fd30d53c08171938aec8d0d977c06f8108aa2fa761403f00883dc68c5aad9</td>
      <td>0x5952a1e9445d7f32cddc964f74f23fae80130796</td>
      <td>1000.000000</td>
      <td>9.041889</td>
    </tr>
    <tr>
      <th>41</th>
      <td>8922989</td>
      <td>2021-07-06T15:50:44Z</td>
      <td>0xd0018e00632c6f18c03a5d682434581fa045369afa3703c782f149b71b5c4045</td>
      <td>0x1ccea4c8c044f5b24c71448ef498fffa22e4bd6e</td>
      <td>1434.717550</td>
      <td>13.700000</td>
    </tr>
    <tr>
      <th>42</th>
      <td>8927485</td>
      <td>2021-07-06T19:35:40Z</td>
      <td>0x7012f5588aedd50221b053fedfe71af81d4cdc42538db6186518d1a5290bd279</td>
      <td>0x1ccea4c8c044f5b24c71448ef498fffa22e4bd6e</td>
      <td>14.722390</td>
      <td>0.139311</td>
    </tr>
    <tr>
      <th>43</th>
      <td>9122341</td>
      <td>2021-07-13T14:01:06Z</td>
      <td>0xffed33a11ba77b64362a5ac78593271b26582b439b695ff1777e41277dce2aab</td>
      <td>0x8e1cbcbc2a5d2253c580320ae3b491a97594d41a</td>
      <td>741.133104</td>
      <td>6.174518</td>
    </tr>
    <tr>
      <th>44</th>
      <td>9648143</td>
      <td>2021-08-01T03:43:08Z</td>
      <td>0x0fb4154e41927bef5581d8995491018daf850a6824f0d311156da3579a8435f1</td>
      <td>0x5f0ff52df8df2c5351c47b6711c33f36c5402909</td>
      <td>1678.935030</td>
      <td>13.749800</td>
    </tr>
    <tr>
      <th>45</th>
      <td>9815294</td>
      <td>2021-08-07T04:20:46Z</td>
      <td>0x73f2a5b39a9759ba5ea9b5348e215ef01bbf69cf26d9566b4ec28cedaed302a6</td>
      <td>0x094418c628d20f0eaca6e49914fcf8f741a715a1</td>
      <td>6706.066464</td>
      <td>50.424243</td>
    </tr>
    <tr>
      <th>46</th>
      <td>11235008</td>
      <td>2021-09-25T23:13:51Z</td>
      <td>0xc6f1e34b4eeb8a2490f1a04e0b50ffa5d25496bff677ab6da776c3e67379e05b</td>
      <td>0x293ede387204a547afc28b9c6023ead78e98c375</td>
      <td>710014.971806</td>
      <td>629.838282</td>
    </tr>
  </tbody>
</table>
</div>



For burns its basically the same code for mints i.e. same paramters just changed some variables.


```python
uni_burns = dex.get_burns("Uniswap", ['0x004375dff511095cc5a197a54140a24efef3a416', 8, 6, 'WBTC', 'USDC'])
```


```python
uni_burns
```

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>block_height</th>
      <th>timestamp</th>
      <th>transaction_hash</th>
      <th>from</th>
      <th>WBTC</th>
      <th>USDC</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>10092366</td>
      <td>2020-05-18T21:20:11Z</td>
      <td>0x83dc440bfb2e445b68877f98a2f2357c3dcfb7bb02a42466adb8ae966ac990e2</td>
      <td>0x4d37f28d2db99e8d35a6c725a5f1749a085850a3</td>
      <td>0.000020</td>
      <td>0.197013</td>
    </tr>
    <tr>
      <th>1</th>
      <td>10101198</td>
      <td>2020-05-20T06:27:58Z</td>
      <td>0x7920130c2cb706299b3b2ac0bddd7effdc49cf276b1a5c3a96645da845fdcd32</td>
      <td>0xe0e8c1d735698060477e79a8e4c20276fc2ec7a7</td>
      <td>0.063276</td>
      <td>614.380910</td>
    </tr>
    <tr>
      <th>2</th>
      <td>10156957</td>
      <td>2020-05-28T22:37:40Z</td>
      <td>0x7d50703cc131458e9537380b6327ed8d6fd70676d54e3a7d4aac7a31d7593361</td>
      <td>0x0baf7b79f9174c0840aa93a93a2c2a81044a09a2</td>
      <td>0.100240</td>
      <td>926.246269</td>
    </tr>
    <tr>
      <th>3</th>
      <td>10206712</td>
      <td>2020-06-05T16:08:49Z</td>
      <td>0x42b68b99984ce2dffbacc88299e3b1bab134bd5da45a5da586c7acd1524e2995</td>
      <td>0x6f1821a5fa09c0d1c833ba714f4adae3c8a8edd9</td>
      <td>0.034953</td>
      <td>347.926154</td>
    </tr>
    <tr>
      <th>4</th>
      <td>10309087</td>
      <td>2020-06-21T12:23:07Z</td>
      <td>0x8e0d615b4be3b9924ef75338c9e4b779cb2a1111b307f75a9c4cba9110a1fc02</td>
      <td>0xede0927f363253d9e8ca98a3d24748554978ba35</td>
      <td>0.010843</td>
      <td>102.534555</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>478</th>
      <td>13656702</td>
      <td>2021-11-21T06:58:46Z</td>
      <td>0xadc84b6d2f646d7e25929d93e77f5361f668c65501fdab46be9e99c9cbdf1fe6</td>
      <td>0x0c3a50b75db3970f0220cb07c3f6e39af37762fe</td>
      <td>0.025989</td>
      <td>1529.486470</td>
    </tr>
    <tr>
      <th>479</th>
      <td>13681241</td>
      <td>2021-11-25T03:50:01Z</td>
      <td>0x3dfc8a05b6369e2fdb64543e93eb5f2c7caa5709433d4b16254fa52fbf86b3c9</td>
      <td>0xe8c6381475d1956e0dc9ef25278d087165ce9628</td>
      <td>0.006998</td>
      <td>400.167433</td>
    </tr>
    <tr>
      <th>480</th>
      <td>13687900</td>
      <td>2021-11-26T05:25:48Z</td>
      <td>0x8822037f479fa9e6f594042e040526177a8fc5d91be380770eff6992a61cf8a5</td>
      <td>0xd978f6ae3377c1a2bd74741ada0398b7fe16ba01</td>
      <td>0.083970</td>
      <td>4871.595098</td>
    </tr>
    <tr>
      <th>481</th>
      <td>13707116</td>
      <td>2021-11-29T06:46:09Z</td>
      <td>0xf7d04f0eb9a98f46449d9bab329fbbe2587aab1b26e5006712333bb35ee24956</td>
      <td>0x1d9eb67c6924c62487bf0a3982ed6281190cffce</td>
      <td>0.077707</td>
      <td>4472.614224</td>
    </tr>
    <tr>
      <th>482</th>
      <td>13752576</td>
      <td>2021-12-06T13:30:43Z</td>
      <td>0xad7f9c62ed1c9647d0950540f1dc088b95db09a23a5fa2c4f4852eb3faae8dfe</td>
      <td>0x5418820a3f975bacbccce1322ece14032a8711d6</td>
      <td>0.141347</td>
      <td>6847.504885</td>
    </tr>
  </tbody>
</table>
<p>483 rows × 6 columns</p>
</div>




```python
sushi_burns = dex.get_burns("SushiSwap", ['0xceff51756c56ceffca006cd410b03ffc46dd3a58', 8, 18, 'WBTC', 'WETH'])
```


```python
sushi_burns
```



<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>block_height</th>
      <th>timestamp</th>
      <th>transaction_hash</th>
      <th>from</th>
      <th>WBTC</th>
      <th>WETH</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>10841880</td>
      <td>2020-09-11T17:19:31Z</td>
      <td>0xcd8868e0ba00a0ab7cc57503e0812a071b62da7e0866233ad349aac0cad19262</td>
      <td>0x2c076d91b9ca5475cd168b018707eea87204baac</td>
      <td>0.177665</td>
      <td>4.970000</td>
    </tr>
    <tr>
      <th>1</th>
      <td>10944565</td>
      <td>2020-09-27T12:14:18Z</td>
      <td>0xf1504c719f69061ce473276255d7811fa128ba99f7d0f3faf5b8ece3080737fd</td>
      <td>0xc92165b4e7b7899955c73b6002a17f71bff3a28a</td>
      <td>0.001756</td>
      <td>0.044639</td>
    </tr>
    <tr>
      <th>2</th>
      <td>10956555</td>
      <td>2020-09-29T09:19:09Z</td>
      <td>0x494f0ce9dd930206894d56c2e3d8bcaef3c9c377813f249034fc88374444f561</td>
      <td>0x12429f1842c56e2116f93cbd6cf09418e49abcd7</td>
      <td>9.513224</td>
      <td>288.260201</td>
    </tr>
    <tr>
      <th>3</th>
      <td>10959190</td>
      <td>2020-09-29T19:21:49Z</td>
      <td>0x93afd9bdf4b6051ec82ded7067f3eba4fed6c93c246d39927463e8de6bb97cca</td>
      <td>0xfcb0a9851cf9b2623933a4cf0e19ffb2fa4d4f7a</td>
      <td>24.358952</td>
      <td>737.947121</td>
    </tr>
    <tr>
      <th>4</th>
      <td>10959224</td>
      <td>2020-09-29T19:28:52Z</td>
      <td>0xa02aa5a39049685ed48615f0671fcdc2fab2071df626d4b3abad911bc8f92556</td>
      <td>0xf4d0eb7258cf300c17226ac0f390602946cefd2d</td>
      <td>8.956882</td>
      <td>271.346028</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>5289</th>
      <td>13787616</td>
      <td>2021-12-12T02:20:41Z</td>
      <td>0x60846ca3be76a7bc7b64d00c67dda6fe4042dc267fd80b6f2bfe6383cfcd9e6a</td>
      <td>0xc3fe67c9595a3fb9fae726a680ee200d38ccb5f5</td>
      <td>0.000098</td>
      <td>0.001194</td>
    </tr>
    <tr>
      <th>5290</th>
      <td>13788646</td>
      <td>2021-12-12T06:15:00Z</td>
      <td>0x818fc7a1c779d80f5acb84bc24020732d8cb33d14dec6fef52f9ec93b63e1202</td>
      <td>0xa4b423909c829b1a040e7e1a012fccefa90116a7</td>
      <td>0.003985</td>
      <td>0.048414</td>
    </tr>
    <tr>
      <th>5291</th>
      <td>13794353</td>
      <td>2021-12-13T03:12:24Z</td>
      <td>0xa24a469c852ff4946670b2b24d6f93f060f2889d6b25f3ea88b558dde1205189</td>
      <td>0x1f14be60172b40dac0ad9cd72f6f0f2c245992e8</td>
      <td>0.004601</td>
      <td>0.056434</td>
    </tr>
    <tr>
      <th>5292</th>
      <td>13794995</td>
      <td>2021-12-13T05:39:53Z</td>
      <td>0xfe80b9be06db51bdc3e7a92f69fcf418887f7e7066dce425b2574f22a27c7e55</td>
      <td>0xb9e4a0756ebe28db8fee68a5d06cadc6561bbd2e</td>
      <td>22.400385</td>
      <td>274.197033</td>
    </tr>
    <tr>
      <th>5293</th>
      <td>13795289</td>
      <td>2021-12-13T06:50:13Z</td>
      <td>0x4cfea0454df7fd9cf53a57538e78ad4df4c4c82d6907bee5e26cd57d57578aa3</td>
      <td>0xf6b5d813bf6e00a29110d03005f6719b52d50829</td>
      <td>0.253165</td>
      <td>3.096641</td>
    </tr>
  </tbody>
</table>
<p>5294 rows × 6 columns</p>
</div>




```python
pancake_burns = dex.get_burns("Pancake v2", ['0xe85b946f9858f6c6bd355cdc51affeb5e987c5ef', 18, 18, 'WBTCT', 'BUSD'])
```


```python
pancake_burns
```



<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>block_height</th>
      <th>timestamp</th>
      <th>transaction_hash</th>
      <th>from</th>
      <th>WBTCT</th>
      <th>BUSD</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>7252530</td>
      <td>2021-05-08T21:40:13Z</td>
      <td>0x284170df61077ea153ea6be2a0eddd380cabf06ff04b76839fee92836046431b</td>
      <td>0x92e5fef90e258b742c16bee2c674e9a8dfcec01b</td>
      <td>19547.377233</td>
      <td>441.176410</td>
    </tr>
    <tr>
      <th>1</th>
      <td>7255593</td>
      <td>2021-05-09T00:16:08Z</td>
      <td>0x266358c34582c40d566a2682005187ed606695e45f6949c6069face513d39dc6</td>
      <td>0xd4396ea8ac8e9954f33457e6d1249729db2b7960</td>
      <td>682.153759</td>
      <td>15.395935</td>
    </tr>
    <tr>
      <th>2</th>
      <td>7271545</td>
      <td>2021-05-09T14:10:30Z</td>
      <td>0x0347f793781ab1eb6348a070d68951b32c54448fdead499d40d7caad50a04788</td>
      <td>0xc604c6eb604ce9b4e10ab55178231972be4f4cb9</td>
      <td>3677.675154</td>
      <td>82.412111</td>
    </tr>
    <tr>
      <th>3</th>
      <td>7272410</td>
      <td>2021-05-09T14:56:42Z</td>
      <td>0x6ce44b87ea30a5bf6e7923d4f48b4f00e8ecac3d49ee1b6d598cbbcb0d63fc37</td>
      <td>0x86c9db8dc40e77da03b56dbb0c75a614a0380f67</td>
      <td>3895.289161</td>
      <td>87.288569</td>
    </tr>
    <tr>
      <th>4</th>
      <td>7296348</td>
      <td>2021-05-10T12:01:40Z</td>
      <td>0xad2b2f553b5185da60e236b025ab1b7d06cb93aaadbb59dc8d5100463e2dbcaf</td>
      <td>0x92e5fef90e258b742c16bee2c674e9a8dfcec01b</td>
      <td>18862.355498</td>
      <td>421.610307</td>
    </tr>
    <tr>
      <th>5</th>
      <td>7323369</td>
      <td>2021-05-11T14:56:37Z</td>
      <td>0xe7af81b749499b5c5a5117f726eb9ff3525eb4cb30d15c766a6a79c1ebc8f8a6</td>
      <td>0xbbc53779d5f1a7d016aaed9d71eaa072c2f405c6</td>
      <td>342.662897</td>
      <td>7.082896</td>
    </tr>
    <tr>
      <th>6</th>
      <td>7328430</td>
      <td>2021-05-11T19:23:27Z</td>
      <td>0xe2a12757e426744dfe7a720920d9bcd9dc4cbe58fbf4550700952fc2e13eb74f</td>
      <td>0x4f74013cdad98637b1d140517aff029ef326e441</td>
      <td>6329.534545</td>
      <td>124.550858</td>
    </tr>
    <tr>
      <th>7</th>
      <td>7331459</td>
      <td>2021-05-11T22:14:39Z</td>
      <td>0x4992d167f975cc22e27260ecc6cc2b6d23cc0e02cd10c20d833c3955099a9d58</td>
      <td>0x6dcb50cb08ffaa9147d6cb62d4a6ef512a8d4a76</td>
      <td>3961.613320</td>
      <td>75.365741</td>
    </tr>
    <tr>
      <th>8</th>
      <td>7346908</td>
      <td>2021-05-12T12:38:03Z</td>
      <td>0x9f0aadf95066b45114bcc8c3ab362f3f50a55c33943e026a75294afd7119e039</td>
      <td>0x5eca99da748778f2897d8333adcb68d4ca8d4357</td>
      <td>4227.244458</td>
      <td>79.358263</td>
    </tr>
    <tr>
      <th>9</th>
      <td>7370495</td>
      <td>2021-05-13T09:07:23Z</td>
      <td>0x3e83435fa1f5467fc408eade8a34042fd94f02ddcf23ca6993659b8efcd67764</td>
      <td>0x6dcb50cb08ffaa9147d6cb62d4a6ef512a8d4a76</td>
      <td>4033.902812</td>
      <td>68.492075</td>
    </tr>
    <tr>
      <th>10</th>
      <td>7397154</td>
      <td>2021-05-14T07:38:23Z</td>
      <td>0x26f2d7f0937091e5d0fdc08c564f465cc0687e53dc1308d88593ea5c744ad544</td>
      <td>0xc96dede7868f8c190208a22812fd3539e9e2caf6</td>
      <td>2612.423497</td>
      <td>40.272420</td>
    </tr>
    <tr>
      <th>11</th>
      <td>7449748</td>
      <td>2021-05-16T04:22:03Z</td>
      <td>0xc51321d8eeb22031f2f1e2288644659a0c6743a55ceadc185990556c4866de14</td>
      <td>0x86c9db8dc40e77da03b56dbb0c75a614a0380f67</td>
      <td>1632.703179</td>
      <td>25.455359</td>
    </tr>
    <tr>
      <th>12</th>
      <td>7502307</td>
      <td>2021-05-18T00:41:42Z</td>
      <td>0xd34e8d8c616f439160c62af0efba242fdc9361ff71440ae964e0620cad880c76</td>
      <td>0xa13443db578af67aa80ea0f106377d5e9a62686f</td>
      <td>12.654447</td>
      <td>0.182679</td>
    </tr>
    <tr>
      <th>13</th>
      <td>7553162</td>
      <td>2021-05-19T19:52:59Z</td>
      <td>0xd655f10ee330f4996eb466aea71a07b72ce9f2acc09d51a588588f2db66718df</td>
      <td>0xfc11822d8b1ca7de471410bed9d0999f2fed7bd3</td>
      <td>22369.915071</td>
      <td>291.268164</td>
    </tr>
    <tr>
      <th>14</th>
      <td>7593446</td>
      <td>2021-05-21T05:38:40Z</td>
      <td>0xc0083584ac2e505f513092326dae5c1d47955927a0dd01caba6f794854108dbf</td>
      <td>0x86c9db8dc40e77da03b56dbb0c75a614a0380f67</td>
      <td>27.580522</td>
      <td>0.343020</td>
    </tr>
    <tr>
      <th>15</th>
      <td>7646730</td>
      <td>2021-05-23T02:11:45Z</td>
      <td>0xd9ac08d58565fd75b41a8fc48e10ea93196cc1bf02d59cfbce599b422661ae1d</td>
      <td>0x86c9db8dc40e77da03b56dbb0c75a614a0380f67</td>
      <td>95.247899</td>
      <td>1.187347</td>
    </tr>
    <tr>
      <th>16</th>
      <td>7705372</td>
      <td>2021-05-25T03:17:01Z</td>
      <td>0xea97bd1dc2460d3e40f8f0858a9c27c2ed9d8d3eecf5a0dc100d15063097049e</td>
      <td>0xec25f5068405117d75c99c6e6a27eb4727915dd0</td>
      <td>5583.414957</td>
      <td>76.250393</td>
    </tr>
    <tr>
      <th>17</th>
      <td>7737656</td>
      <td>2021-05-26T06:16:11Z</td>
      <td>0xa034e58320880721d4a46b5b2c134fb595b742944e895511c3782814da9307fa</td>
      <td>0xbf8faa9a7bca427317ac52a4fe020069bf317c08</td>
      <td>5448.943799</td>
      <td>65.634498</td>
    </tr>
    <tr>
      <th>18</th>
      <td>7744319</td>
      <td>2021-05-26T11:51:45Z</td>
      <td>0x5afda661ab50fd33a9d5a827ab2117b2c4cb4f3eec1c73c1fe9bbc21e24ed6ff</td>
      <td>0xec25f5068405117d75c99c6e6a27eb4727915dd0</td>
      <td>6869.646404</td>
      <td>67.477290</td>
    </tr>
    <tr>
      <th>19</th>
      <td>7875634</td>
      <td>2021-05-31T01:53:54Z</td>
      <td>0x19afcf4fe492831beb33e46c8c51ddc4da0f4979044775a4a2cd3116822f345e</td>
      <td>0x86c9db8dc40e77da03b56dbb0c75a614a0380f67</td>
      <td>0.717364</td>
      <td>0.009026</td>
    </tr>
    <tr>
      <th>20</th>
      <td>7957991</td>
      <td>2021-06-02T22:47:15Z</td>
      <td>0x7bc8ee2c0ee097f8a207c68fc3a72bf4d821d6a7cf566dd2e17d88a2e77c8bb5</td>
      <td>0xe926d68bd634a1fa586e19c8e112e1f2b75a39c4</td>
      <td>753.425250</td>
      <td>10.799707</td>
    </tr>
    <tr>
      <th>21</th>
      <td>8106968</td>
      <td>2021-06-08T03:14:02Z</td>
      <td>0xd1d4edd8b28574fbf375b93768133ce6d5c1e18d70c4fa4893df65608d6d834a</td>
      <td>0x86c9db8dc40e77da03b56dbb0c75a614a0380f67</td>
      <td>43.525907</td>
      <td>0.555438</td>
    </tr>
    <tr>
      <th>22</th>
      <td>8340250</td>
      <td>2021-06-16T07:02:39Z</td>
      <td>0x35d9c0e6431cc0cf7775149264f8819f5c5c14ae408c171fa134d1368eec79ff</td>
      <td>0x86c9db8dc40e77da03b56dbb0c75a614a0380f67</td>
      <td>69.768362</td>
      <td>0.926952</td>
    </tr>
    <tr>
      <th>23</th>
      <td>9007310</td>
      <td>2021-07-09T14:09:03Z</td>
      <td>0x031ccf6b50fc7ab1cb01e5a0a5629642526ce72b222e09400df91540eb89c269</td>
      <td>0x1ccea4c8c044f5b24c71448ef498fffa22e4bd6e</td>
      <td>1408.491469</td>
      <td>13.128361</td>
    </tr>
    <tr>
      <th>24</th>
      <td>9314765</td>
      <td>2021-07-20T06:28:13Z</td>
      <td>0x6bee1af8858f23a6aa4fdec60ff1529c20b72027270c924d911c60f1661d3b22</td>
      <td>0x5952a1e9445d7f32cddc964f74f23fae80130796</td>
      <td>11469.639781</td>
      <td>89.828313</td>
    </tr>
    <tr>
      <th>25</th>
      <td>9382898</td>
      <td>2021-07-22T15:15:57Z</td>
      <td>0x8015c9d98dcab84fdb70b6c60400019b3bcc5f745b1445cac599dc3e61b9f458</td>
      <td>0x86c9db8dc40e77da03b56dbb0c75a614a0380f67</td>
      <td>1244.553883</td>
      <td>8.820676</td>
    </tr>
    <tr>
      <th>26</th>
      <td>9390886</td>
      <td>2021-07-22T21:55:23Z</td>
      <td>0x590fb682d4adf485d4b299affb2d72c3daa9ee7801f8f5594ffb98f61836f550</td>
      <td>0x07d80ae6f36a5e08dca74ce884a24d39db9934ed</td>
      <td>480.351761</td>
      <td>3.334675</td>
    </tr>
    <tr>
      <th>27</th>
      <td>9970069</td>
      <td>2021-08-12T16:45:46Z</td>
      <td>0xb452c4b0d6d9d16a7f1b17c170a50067086b3ee7aaf574542102ddb1c4351762</td>
      <td>0x86c9db8dc40e77da03b56dbb0c75a614a0380f67</td>
      <td>355.710610</td>
      <td>2.420170</td>
    </tr>
    <tr>
      <th>28</th>
      <td>10281900</td>
      <td>2021-08-23T14:20:41Z</td>
      <td>0xeae22a321ed04c9ab7464534551868db3c8fe052e9156293d051c5b1f97ded36</td>
      <td>0x5952a1e9445d7f32cddc964f74f23fae80130796</td>
      <td>8422.204626</td>
      <td>77.720163</td>
    </tr>
    <tr>
      <th>29</th>
      <td>10363290</td>
      <td>2021-08-26T10:31:04Z</td>
      <td>0x18b1cf7afa67644764d9d7f130739095ef74725a991d42e244b0a49cae5e15ff</td>
      <td>0x8e1cbcbc2a5d2253c580320ae3b491a97594d41a</td>
      <td>720.097469</td>
      <td>5.877560</td>
    </tr>
    <tr>
      <th>30</th>
      <td>11146657</td>
      <td>2021-09-22T21:12:33Z</td>
      <td>0x432227cc224e238e6c3a069cf2cda2c7eaf785f6fa63b4ba2ff4d294b3d01693</td>
      <td>0x5952a1e9445d7f32cddc964f74f23fae80130796</td>
      <td>1895.106870</td>
      <td>1.358835</td>
    </tr>
    <tr>
      <th>31</th>
      <td>11172045</td>
      <td>2021-09-23T18:32:53Z</td>
      <td>0x0f54c00354efb994e8c3c13788c612abb246267f166f59df0654408d3cc51255</td>
      <td>0x094418c628d20f0eaca6e49914fcf8f741a715a1</td>
      <td>23763.136387</td>
      <td>20.200175</td>
    </tr>
    <tr>
      <th>32</th>
      <td>11381491</td>
      <td>2021-10-01T02:32:12Z</td>
      <td>0xd2575353bc43bcb25b11165a13e0da16fb850fe91800c318f408f586623b8d36</td>
      <td>0x86c9db8dc40e77da03b56dbb0c75a614a0380f67</td>
      <td>25868.023828</td>
      <td>27.691138</td>
    </tr>
    <tr>
      <th>33</th>
      <td>11656883</td>
      <td>2021-10-10T17:01:09Z</td>
      <td>0x044f1998e64933560d79453d0c860b4bb618d22ba9fbb3614ebd6784a29d14cb</td>
      <td>0x5952a1e9445d7f32cddc964f74f23fae80130796</td>
      <td>50798.970860</td>
      <td>189.437569</td>
    </tr>
    <tr>
      <th>34</th>
      <td>11659962</td>
      <td>2021-10-10T19:35:11Z</td>
      <td>0xd99ac86fd3b338c93bbb83c13319f587924bee57cc458aefdd4aaeebe935a91e</td>
      <td>0x3c156d794d00d2f0d2f6601e61156a9fcb4964ad</td>
      <td>17282.760707</td>
      <td>62.989382</td>
    </tr>
    <tr>
      <th>35</th>
      <td>11709956</td>
      <td>2021-10-12T14:02:33Z</td>
      <td>0x3d2431f77dad57deeb6eb0f436ea858685b5222f2981c1be89645dfd9e504035</td>
      <td>0x5f0ff52df8df2c5351c47b6711c33f36c5402909</td>
      <td>2204.766080</td>
      <td>9.790314</td>
    </tr>
    <tr>
      <th>36</th>
      <td>11741475</td>
      <td>2021-10-13T16:45:37Z</td>
      <td>0x4b0906b581669ee5aa81234746c51ecdd7e7f58515627ffd14b8be15fc067b79</td>
      <td>0x16f9415bc924e5b61f1d9b46a885218ca7f5f011</td>
      <td>2958.792554</td>
      <td>12.486387</td>
    </tr>
    <tr>
      <th>37</th>
      <td>11754045</td>
      <td>2021-10-14T03:17:53Z</td>
      <td>0x046c13b5764c2862c805b09fd8b8e33d53d0b439c318bda219dc2d642ebd865f</td>
      <td>0x293ede387204a547afc28b9c6023ead78e98c375</td>
      <td>310632.482521</td>
      <td>1331.540295</td>
    </tr>
    <tr>
      <th>38</th>
      <td>11777982</td>
      <td>2021-10-14T23:19:24Z</td>
      <td>0x5ee664b540f853675545bece39c16db091376ba41f17ff6243d1f88d5912bdd6</td>
      <td>0x5952a1e9445d7f32cddc964f74f23fae80130796</td>
      <td>4468.496882</td>
      <td>19.154416</td>
    </tr>
    <tr>
      <th>39</th>
      <td>11865906</td>
      <td>2021-10-18T00:57:37Z</td>
      <td>0x3867068744d038fd8d299b9404e28ce5be9f1b9ffb16725df6d4f1ca15a8ad9d</td>
      <td>0x6fccec5d1f5455758cce1c1742997391dd4453bc</td>
      <td>5388.046035</td>
      <td>21.238499</td>
    </tr>
  </tbody>
</table>
</div>



Can now pull up swaps/burns/mints for any pool in uniswap v2 and sushiswap and pancake saw (also works for uniswap v3 but from what i understood they implement some new minting system so might not be good to work with uniswap v3 data)


```python
dex.get_pool(data_from_uniswap, "PAX")
```




    ['0x77253e7e781a74fc6fccb316969300695b7eae8e', 18, 18, 'UNI', 'PAX']




```python
# much smaller pool 
df = dex.get_swaps("Uniswap",'0x709f7b10f22eb62b05913b59b92ddd372d4e2152')
```


```python
df
```


<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>tradeIndex</th>
      <th>buyAmount</th>
      <th>buyAmountInUsd</th>
      <th>sellAmount</th>
      <th>sellAmountInUsd</th>
      <th>tradeAmount</th>
      <th>transaction.hash</th>
      <th>transaction.gasValue</th>
      <th>date.date</th>
      <th>block.height</th>
      <th>buyCurrency.symbol</th>
      <th>sellCurrency.symbol</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>10</td>
      <td>2292.959467</td>
      <td>2291.592484</td>
      <td>2297.029038</td>
      <td>2297.029038</td>
      <td>2291.592484</td>
      <td>0x9c29aa4a22397044f154595c5aaa88880ddec044fbb06421307a596b1452ac5d</td>
      <td>0.000000</td>
      <td>2021-06-11</td>
      <td>12610495</td>
      <td>PAX</td>
      <td>PAXG</td>
    </tr>
    <tr>
      <th>1</th>
      <td>18</td>
      <td>13986.707918</td>
      <td>13987.531586</td>
      <td>13966.083026</td>
      <td>13966.083026</td>
      <td>13966.083026</td>
      <td>0x813c73df0e44bed4906282836f20f0e6388ae72324e02d96fb33ab3f9ae96eda</td>
      <td>0.027896</td>
      <td>2021-06-11</td>
      <td>12610732</td>
      <td>PAX</td>
      <td>PAXG</td>
    </tr>
    <tr>
      <th>2</th>
      <td>11</td>
      <td>5004.713033</td>
      <td>5010.460757</td>
      <td>4976.796615</td>
      <td>4976.796615</td>
      <td>4976.796615</td>
      <td>0x98a60a19040177e0aeb833662d66548c9b6c660c977b9554b5daa3aaa13dc258</td>
      <td>0.006146</td>
      <td>2021-06-11</td>
      <td>12611785</td>
      <td>PAX</td>
      <td>PAXG</td>
    </tr>
    <tr>
      <th>3</th>
      <td>18</td>
      <td>21006.620915</td>
      <td>21011.504075</td>
      <td>20820.369194</td>
      <td>20820.369194</td>
      <td>20820.369194</td>
      <td>0x57ba09de20ff6a2be540f5472fd28fcfcc6005f0ab419daecf32cd2ca4595395</td>
      <td>0.020571</td>
      <td>2021-06-11</td>
      <td>12612164</td>
      <td>PAX</td>
      <td>PAXG</td>
    </tr>
    <tr>
      <th>4</th>
      <td>6</td>
      <td>13.242065</td>
      <td>25304.786831</td>
      <td>25362.108304</td>
      <td>25362.108304</td>
      <td>25304.786831</td>
      <td>0xe43b16193e0998cb3c1b2867f80fcbda6188186703edf1a8beb805ffeba60545</td>
      <td>0.017931</td>
      <td>2021-06-11</td>
      <td>12612254</td>
      <td>PAXG</td>
      <td>PAX</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>403</th>
      <td>13</td>
      <td>20284.324803</td>
      <td>20488.572762</td>
      <td>20395.686397</td>
      <td>20395.686397</td>
      <td>20395.686397</td>
      <td>0x21cecdc0e2583753c8bb5e95905528bd93c1f6214801a11b65e866ba8ddf52e7</td>
      <td>0.029691</td>
      <td>2021-11-27</td>
      <td>13697995</td>
      <td>PAX</td>
      <td>PAXG</td>
    </tr>
    <tr>
      <th>404</th>
      <td>11</td>
      <td>10.539045</td>
      <td>18658.858189</td>
      <td>18769.560896</td>
      <td>18769.560896</td>
      <td>18658.858189</td>
      <td>0x87c9fd53124257c0a29d603d02f3bcd7bd4a9c56b45eb76d1ee1a0aafe8e4880</td>
      <td>0.037919</td>
      <td>2021-12-02</td>
      <td>13728902</td>
      <td>PAXG</td>
      <td>PAX</td>
    </tr>
    <tr>
      <th>405</th>
      <td>6</td>
      <td>20637.668193</td>
      <td>20698.034164</td>
      <td>20654.628563</td>
      <td>20654.628563</td>
      <td>20654.628563</td>
      <td>0x7ae94b7618aed8a5cca350c1b528c14d8a352f4da6f7b165022f177637369a5c</td>
      <td>0.047057</td>
      <td>2021-12-04</td>
      <td>13738414</td>
      <td>PAX</td>
      <td>PAXG</td>
    </tr>
    <tr>
      <th>406</th>
      <td>11</td>
      <td>8.538190</td>
      <td>15166.963190</td>
      <td>15248.321108</td>
      <td>15248.321108</td>
      <td>15166.963190</td>
      <td>0x928ab6e9300be6818a1a18d6d2dfbaf69ecb30444d65966521cc03ba12c58f67</td>
      <td>0.027757</td>
      <td>2021-12-10</td>
      <td>13775928</td>
      <td>PAXG</td>
      <td>PAX</td>
    </tr>
    <tr>
      <th>407</th>
      <td>6</td>
      <td>11987.524028</td>
      <td>11996.881279</td>
      <td>11986.852492</td>
      <td>11986.852492</td>
      <td>11986.852492</td>
      <td>0xe44d1dc38fcc8ca740a2ffa4fa7c340e2982ccd5df3d9d46114e5cef73a498f4</td>
      <td>0.018363</td>
      <td>2021-12-10</td>
      <td>13779664</td>
      <td>PAX</td>
      <td>PAXG</td>
    </tr>
  </tbody>
</table>
<p>408 rows × 12 columns</p>
</div>




```python
df2 = dex.get_swaps("Uniswap", ['0x709f7b10f22eb62b05913b59b92ddd372d4e2152', 18, 18, 'PAXG', 'PAX'])
```


```python
df2
```


<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>block_height</th>
      <th>timestamp</th>
      <th>PAXGIn</th>
      <th>PAXIn</th>
      <th>PAXGOut</th>
      <th>PAXOut</th>
      <th>transaction_hash</th>
      <th>from</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>12610495</td>
      <td>2021-06-11T02:12:24Z</td>
      <td>0.000000</td>
      <td>2292.959467</td>
      <td>1.203857</td>
      <td>0.000000</td>
      <td>0x9c29aa4a22397044f154595c5aaa88880ddec044fbb06421307a596b1452ac5d</td>
      <td>0x788c5de9d101870f2689b819785fb37c9d5e7050</td>
    </tr>
    <tr>
      <th>1</th>
      <td>12610732</td>
      <td>2021-06-11T03:00:35Z</td>
      <td>0.000000</td>
      <td>13986.707918</td>
      <td>7.319575</td>
      <td>0.000000</td>
      <td>0x813c73df0e44bed4906282836f20f0e6388ae72324e02d96fb33ab3f9ae96eda</td>
      <td>0x35f0c1c4717c2367fb06e3e2ea16fe23cd616997</td>
    </tr>
    <tr>
      <th>2</th>
      <td>12611785</td>
      <td>2021-06-11T06:58:56Z</td>
      <td>0.000000</td>
      <td>5004.713033</td>
      <td>2.609187</td>
      <td>0.000000</td>
      <td>0x98a60a19040177e0aeb833662d66548c9b6c660c977b9554b5daa3aaa13dc258</td>
      <td>0xdee8f81017ebca8aaa096c3e78db2c417b7fcd45</td>
    </tr>
    <tr>
      <th>3</th>
      <td>12612164</td>
      <td>2021-06-11T08:23:18Z</td>
      <td>0.000000</td>
      <td>21006.620915</td>
      <td>10.895356</td>
      <td>0.000000</td>
      <td>0x57ba09de20ff6a2be540f5472fd28fcfcc6005f0ab419daecf32cd2ca4595395</td>
      <td>0xdf6878895f35016fd3e214937c9d105606ca9d16</td>
    </tr>
    <tr>
      <th>4</th>
      <td>12612254</td>
      <td>2021-06-11T08:44:50Z</td>
      <td>13.242065</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>25356.214046</td>
      <td>0xe43b16193e0998cb3c1b2867f80fcbda6188186703edf1a8beb805ffeba60545</td>
      <td>0xc5df9f7f975b0325b2e38b10de86685f2fa66666</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>403</th>
      <td>13697995</td>
      <td>2021-11-27T19:44:40Z</td>
      <td>0.000000</td>
      <td>20284.324803</td>
      <td>11.367987</td>
      <td>0.000000</td>
      <td>0x21cecdc0e2583753c8bb5e95905528bd93c1f6214801a11b65e866ba8ddf52e7</td>
      <td>0x09c7a6707d28931c5021b71cdbe613aebe167e63</td>
    </tr>
    <tr>
      <th>404</th>
      <td>13728902</td>
      <td>2021-12-02T18:27:43Z</td>
      <td>10.539045</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>18704.565680</td>
      <td>0x87c9fd53124257c0a29d603d02f3bcd7bd4a9c56b45eb76d1ee1a0aafe8e4880</td>
      <td>0xa61c2bad4ceba1ab041e84e5f36c55cc94c641c6</td>
    </tr>
    <tr>
      <th>405</th>
      <td>13738414</td>
      <td>2021-12-04T07:02:17Z</td>
      <td>0.000000</td>
      <td>20637.668193</td>
      <td>11.550109</td>
      <td>0.000000</td>
      <td>0x7ae94b7618aed8a5cca350c1b528c14d8a352f4da6f7b165022f177637369a5c</td>
      <td>0x53d8a6a3368ffe7b844782d8a037012497110d81</td>
    </tr>
    <tr>
      <th>406</th>
      <td>13775928</td>
      <td>2021-12-10T07:06:09Z</td>
      <td>8.538190</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>15198.153443</td>
      <td>0x928ab6e9300be6818a1a18d6d2dfbaf69ecb30444d65966521cc03ba12c58f67</td>
      <td>0xa61c2bad4ceba1ab041e84e5f36c55cc94c641c6</td>
    </tr>
    <tr>
      <th>407</th>
      <td>13779664</td>
      <td>2021-12-10T20:44:58Z</td>
      <td>0.000000</td>
      <td>11987.524028</td>
      <td>6.703043</td>
      <td>0.000000</td>
      <td>0xe44d1dc38fcc8ca740a2ffa4fa7c340e2982ccd5df3d9d46114e5cef73a498f4</td>
      <td>0xe85b85bf0cccdab2f5a07a1c9b676d42c664f7c6</td>
    </tr>
  </tbody>
</table>
<p>408 rows × 8 columns</p>
</div>
