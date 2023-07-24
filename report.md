|Parameter name|Brute force|Knuth-Morris-Pratt algorithm|Algorithm using z function|Boyer-Moore-Horspool algorithm|Aho-Corasick algorithm|
|-|-|-|-|-|-|
|Time complexity|O(len(haystack) * len(needle))|O(len(haystack) + len(needle))|O(len(haystack) + len(needle))|O(len(haystack) * len(needle))|O(len(needles) + len(haystack))|
|Memory complexity|O(1)|O(len(needle))|O(len(haystack) + len(needle))|O(len(needle))|O(len(needles))|
|Big data without repeating (len(substring) == 3)|6.630599964410066e-05|2.6741998735815285e-05|0.10571962400106713|1.6003998462110756e-05|8.519399911165237e-05|
|Big data without repeating (len(substring) == 8)|0.09193826199974865|0.01786244599847123|0.09881834199884906|0.004028566000051796|0.027792326000053436|
|Big data without repeating (len(substring) == 16)|0.17028204799862579|0.01765277000144124|0.10372093999991193|0.0027325520012527705|0.025527588000986725|
|Big data without repeating (len(substring) == 28)|0.32758734200149775|0.02013521600048989|0.10333897000178695|0.00215249199885875|0.030333543999586255|
|Beginning and ending of substring repeat many times|2.9834156819991766|0.20967479000100867|0.7203531339997425|0.13127437800168992|0.19767104600090535|
|Beginning of substring repeat many times|1.5642148480005562|0.1757596080005169|0.6641053540003486|0.0265743019990623|0.19553012599935754|
|Substring contains few different letters|0.8534098759992048|0.27469484000001104|0.6586529299989343|0.060392262001987544|0.15479115800000728|