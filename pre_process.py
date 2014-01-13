
def is_chinese(uchar):  
    """判断一个unicode是否是汉字"""  
    if uchar >= u'\u4e00' and uchar<=u'\u9fa5':  
        return True  
    else:  
        return False  
  
def is_number(uchar):  
    """判断一个unicode是否是数字"""  
    if uchar >= u'\u0030' and uchar<=u'\u0039':  
        return True  
    else:  
        return False  
  
def is_alphabet(uchar):  
    """判断一个unicode是否是英文字母"""  
    if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):  
        return True  
    else:  
        return False  
  
def is_other(uchar):  
    """判断是否非汉字，数字和英文字符"""  
    if not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar)):  
        return True  
    else:  
        return False  
  
def b2q(uchar):  
    """半角转全角"""  
    inside_code=ord(uchar)  
    if inside_code<0x0020 or inside_code>0x7e: #不是半角字符就返回原来的字符  
        return uchar  
    if inside_code==0x0020: #除了空格其他的全角半角的公式为:半角=全角-0xfee0  
        inside_code=0x3000  
    else:  
        inside_code+=0xfee0  
    return unichr(inside_code)  
    
def b2q_string(ustring):
    """utf-8编码下，把字符串半角转为全角"""
    return "".join([b2q(uchar) for uchar in ustring])

def q2b(uchar):
    """utf-8编码下，全角转半角"""
    inside_code = ord(uchar)
    if inside_code == 0x3000:
        inside_code = 0x0020
    else: inside_code -= 0xfee0
    if inside_code < 0x0020 or inside_code > 0x7e:
        return uchar
    return chr(inside_code)

def q2b_string(ustring):
    """utf-8编码下，把字符串全角转为半角"""
    return "".join([q2b(uchar) for uchar in ustring])
