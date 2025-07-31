# Examples



## Example 2
The urban bloom potential index is a custom score that we created to rank different metro areas based on their economic potential and attractiveness for commerical growth.
It's not just a single number from a dataset, instead its a blend of three factors we believe that are important for identifying the potential of an area.

Three main ingredients to our recipe are:
1. Median Income: This tells us the income of the typical house hold in an area. It's a strong indicator of the general economic health.
2. High-Earner Percentage: We calculated this metric by adding together the percent of househoulds that earn over $150k a year. This factor measures the
concentration of wealth in an area, which is a good proxy for the potential market for the high-end stuff
3. Population Size (Log-transformation): This represents the total size of the market. We apply a logrithmic transformationo to it so that massive cities like New York or Los angeles don't completely dominate the rankings based on their size. In our opinion, we believe this balances the score making the comparison between small, medium and large cities more meaningful.

Example2 takes these three factors and puts them into a 0 to 1 scale, and then combines them using our opinated weights we defined [x,x,x]. The final result is a single, powerful urban potential index score that ranks every metro area from the highest potential to the lowest.

Sample:
```
steve@rayquaza:~/sources/data-science/UrbanBloom$ poetry run python example/example2.py
Loading and cleaning data...
Data loaded successfully. Shape after cleaning: (935, 5)
Performing feature engineering...
New features 'high_earner_percent' and 'log_population' created.
Calculating the UrbanBloom Potential Index...
Index calculation complete.
Top 20 Metro Areas by UrbanBloom Potential Index
                                                 metro_area  urbanbloom_index  median_income  high_earner_percent  population
0             San Jose-Sunnyvale-Santa Clara, CA Metro Area          0.937246         157444                 52.0     1969353
1              San Francisco-Oakland-Fremont, CA Metro Area          0.841788         133780                 45.4     4653593
2   Washington-Arlington-Alexandria, DC-VA-MD-WV Metro Area          0.787491         123896                 41.0     6263796
3                                 Los Alamos, NM Micro Area          0.731149         143188                 46.9       19374
4                 Boston-Cambridge-Newton, MA-NH Metro Area          0.718801         112484                 37.2     4917661
5                    Seattle-Tacoma-Bellevue, WA Metro Area          0.705113         112594                 36.1     4021467
6                Bridgeport-Stamford-Danbury, CT Metro Area          0.680142         111656                 38.3      947528
7                             Lexington Park, MD Metro Area          0.679200         123577                 39.1      208163
8             New York-Newark-Jersey City, NY-NJ Metro Area          0.676098          97334                 32.4    19756722
9                                      Heber, UT Micro Area          0.671582         125583                 40.8       78517
10            San Diego-Chula Vista-Carlsbad, CA Metro Area          0.637539         102285                 31.9     3282782
11                  Denver-Aurora-Centennial, CO Metro Area          0.631157         102339                 31.4     2977085
12              Oxnard-Thousand Oaks-Ventura, CA Metro Area          0.631089         107327                 34.0      838259
13            Los Angeles-Long Beach-Anaheim, CA Metro Area          0.629805          93525                 29.3    13012469
14                    Santa Cruz-Watsonville, CA Metro Area          0.623228         109266                 36.3      266021
15                            Urban Honolulu, HI Metro Area          0.608623         104264                 31.6     1003666
16       Minneapolis-St. Paul-Bloomington, MN-WI Metro Area          0.605746          98180                 28.9     3693351
17                 Baltimore-Columbia-Towson, MD Metro Area          0.605375          97300                 30.1     2839409
18                                 Nantucket, MA Micro Area          0.603118         119750                 40.1       14299
19              Austin-Round Rock-San Marcos, TX Metro Area          0.599730          97638                 29.9     2357497
------------------------------------------------------------
```
