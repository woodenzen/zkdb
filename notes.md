This is how /Users/will/Dropbox/zettelkasten/20211130084613 Will checkmarks broken.md
gets presented in zkdashboard.py -m

14 digit uid and no UUID. 

11/30/2021 :: [](thearchive://match/20211130084613 Will checkmarks broken)

** Need to test formatting of output. 

Tested and should work no matter where in the filename the 12 or more digit UID is.
---

link_pattern = re.compile(r"(?<!{UUID_sign})\[\[.*?\d{8}]]")
Unused?  

---






Lambda, map() and filter() instead of for loops.


filter(<f>, <iterable>)
filter(<f>, <iterable>) applies function <f> to each element of <iterable> and returns an iterator that yields all items for which <f> is truthy. Conversely, it filters out all items for which <f> is falsy.

map(<f>, <iterable>)
map(<f>, <iterable>) returns in iterator that yields the results of applying function <f> to each element of <iterable>.

The syntax of a lambda expression is as follows:

lambda <parameter_list>: <expression>
The following table summarizes the parts of a lambda expression:

Component	Meaning
lambda	The keyword that introduces a lambda expression
<parameter_list>	An optional comma-separated list of parameter names
:	Punctuation that separates <parameter_list> from <expression>
<expression>	An expression usually involving the names in <parameter_list>
The value of a lambda expression is a callable function, just like a function defined with the def keyword. It takes arguments, as specified by <parameter_list>, and returns a value, as indicated by <expression>.