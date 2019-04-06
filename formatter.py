#encoding=utf-8

import re 

# [u4e00-u9fa5]只能匹配非中文和部分符号(,?';][@) 数据中有"-"所以加了“-”
regex = "[u4e00-u9fa5]|\-"

re = re.compile(regex)

class Formatter(object):

    # num为数据的总数, args为显示列名的str
    def __init__(self, num, args=[]):
       self.num = num
       self.args = args
       self.lens = None
       self.format_str1 = None 
       self.format_str2 = None
    
    # 返回长度（含中文汉字）
    def get_str_len(self, string):
        num_str = len(string)
        num_byte = len(string.encode("utf-8"))
        if num_str == num_byte:
            return num_str
        else:
            num_re = len(re.findall(string))
            num_words = (num_byte - num_re) // 3
            num_lens = num_words*2 + num_re
            return num_lens

    # 每一列的宽度
    def get_col_lens(self, datas=[]):
        lens = {}
        for arg in self.args:
            lens[arg] = len(arg)
        
        for data in datas:
            for arg in lens:
                if data[arg] == None:
                    continue
                if lens[arg] < self.get_str_len(data[arg]):
                    lens[arg] = self.get_str_len(data[arg])
        
        self.lens = lens 

    # 示例: str="+-----+-----+-----+----+-----+----+" 
    def get_format_string1(self):
        str_show = "+"
        for arg in self.args:
            str_add = "-"*(self.lens[arg] + 2)
            str_show = str_show + str_add + "+"
      
        
        self.format_str1 = str_show

    # 示例: str="|{0:^len}|{1:^len}|{2:^len}|{3:^len}|"
    def get_format_string2(self):
        order = 0
        str_show ="|"
        for arg in self.args:
            str_add = "{%d:^%d}"%(order, self.lens[arg] + 2)
            str_show = str_show + str_add + "|"
            order = order + 1 

        self.format_str2 = str_show 
        
    def show_head(self):
        print(self.format_str1)
        print(self.format_str2.format(*self.args))
        print(self.format_str1)
        
    def show_bottom(self):
        print(self.format_str1)
        print("row %d in set"%self.num)

    def show_content(self, datas={}):
        print_list = []
        print_dict = {}

        # 中文显示需要的数据 
        flag = False    # 中文是否被显示
        change = {} # key记录显示中文的所在列名,value记录中文被替换的字符数

        for arg in self.args:
            print_dict[arg]=""
          
        for k, v in datas.items():
            if v != None:
                v = str(v)

                num_bytes = len(v.encode("utf-8"))
                num_str = len(v)
    
                if num_bytes > num_str:
                    # 显示中文
                    for arg in self.args:
                        if k == arg:
                            
                            num_re = len(re.findall(v))
                            num_words = (num_bytes - num_re)//3
                            
                            change[arg] = num_words

                            # 改变该行数据
                            self.lens[arg] = self.lens[arg] - num_words
                            
                            flag = True

                            # 重绘string2
                            self.get_format_string2()
                
                v = v.replace("\n"," ").replace("\t", " ")
                print_dict[k] = v

        for arg in self.args:
            print_list.append(print_dict[arg])
        
        print(self.format_str2.format(*print_list))
        
        if flag == True:
            # 恢复原来的显示
            for k, v in change.items():
                self.lens[k] = self.lens[k] + v
            # 恢复原来的string2
            self.get_format_string2()

# mysql /g模式显示
class FormatterG(object):
    def __init__(self, num, args=[]):
       self.num = num
       self.args = args
       self.lens = 0

    # 左侧的宽度
    def get_left_lens(self):
        for arg in self.args:
            if self.lens >= len(arg):
                continue
            else:
                self.lens = len(arg)

    def show(self, datas):
        count = 1
        for row in datas:
            print("*"*20 + " %d.row "%count + "*"*20)
            for arg in self.args:
                print(arg.rjust(self.lens) + ":{}".format(row[arg]))
            count = count + 1

        print("{} rows in set".format(self.num))

    
    

'''
参数
total:int 数据总数 
args:[] 要显示的列名 
datas:[{},{},{}] 数据
'''

def show_datas(total, args=[], datas=[]):
    fmt = Formatter(total, args)
    fmt.get_col_lens(datas)
    fmt.get_format_string1()
    fmt.get_format_string2()
    fmt.show_head()
    for data in datas:
        fmt.show_content(data)
    fmt.show_bottom()

def show_datas_g(total, args=[], datas=[]):
    fmt = FormatterG(total, args)
    fmt.get_left_lens()
    fmt.show(datas)

if __name__ == "__main__":
    datas = [{"a":":哈哈","b":"123"}]
    fm = Formatter(2,["a","b"])
    fm.get_col_lens(datas)
    fm.get_format_string1()
    fm.get_format_string2()
    fm.show_head()
    for i in datas:
        fm.show_content(i)
    fm.show_bottom()
    
    # \G模式   
    datas = [{"a":"b", "c":"d", "bc":"ab"},{"a":"ba", "c":"da", "bc":"aab"}]
    fmt = FormatterG(len(datas), ["a", "c", "bc"])
    fmt.get_left_lens()
    fmt.show(datas)
