#encoding: utf-8
s = "你好" # 整个文件是UTF-8编码，所以这里的字符串也是UTF-8
u = s.decode("utf-8") # 将utf-8的str转换为unicode
g = u.encode('GBK') # 将unicode转换为str，编码为GBK
print type(s), "len=", len(s)
# 输出： len= 6，utf-8每个汉字占3字节
print type(u), "len=", len(u)
# 输出： len= 6，unicode统计的是字数
print type(g), "len=", len(g)
# 输出：g = u.encode('GBK')，GBK每个汉字占2字节
print s
# 在GBK/ANSI环境下（如Windows），输出乱码，
#因为此时屏幕输出会被强制理解为GBK；Linux下显示正常
print g
# 在Windows下输出“你好”，
#Linux(UTF-8环境)下报错，原因同上。
