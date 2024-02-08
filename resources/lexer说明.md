利用python的re库，处理token的匹配

```python
tk_regex = '|'.join('(?P<%s>%s)' % pair for pair in TOKEN_SPECIFICATION)
get_token = re.compile(tk_regex).match
```

生成一个大的正则表达式，将  `Token_SPECIFICATION`中的所有模式合并成一个单独的正则表达式

编译这个大的正则表达式，并创建匹配函数`get_token`


