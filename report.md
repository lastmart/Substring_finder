|Parameter name|Brute force|Knuth-Morris-Pratt algorithm|Algorithm using z function|Boyer-Moore-Horspool algorithm|Aho-Corasick algorithm|
|-|-|-|-|-|-|
|Time complexity|O(len(haystack) * len(needle))|O(len(haystack) + len(needle))|O(len(haystack) + len(needle))|O(len(haystack) * len(needle))|O(len(needles) + len(haystack))|
|Memory complexity|O(1)|O(len(needle))|O(len(haystack) + len(needle))|O(len(needle))|O(len(needles))|
|Big data without repeating (len(substring) == 4)|0.025998|0.008573|5.542295|0.001912|0.010810|
|Big data without repeating (len(substring) == 7)|2.823432|0.630748|5.545212|0.007120|0.764795|
|Big data without repeating (len(substring) == 17)|0.287820|0.030933|5.579650|0.002985|0.039387|
|Big data without repeating (len(substring) == 36)|17.291764|1.088633|5.558897|0.065365|1.348001|
|Small data without repeating (len(substring) == 3)|0.000069|0.000031|0.106455|0.000017|0.000084|
|Small data without repeating (len(substring) == 8)|0.092297|0.018990|0.099439|0.004083|0.027238|
|Small data without repeating (len(substring) == 16)|0.170137|0.018423|0.104055|0.002704|0.025124|
|Small data without repeating (len(substring) == 28)|0.318773|0.021133|0.104474|0.002166|0.029461|
|Beginning and ending of substring repeat many times|3.774920|0.232583|0.867822|0.133674|0.194140|
|Beginning of substring repeat many times|1.560437|0.201191|1.288176|0.053318|0.357373|
|Substring contains few different letters|0.905915|0.310152|0.672390|0.060735|0.156253|