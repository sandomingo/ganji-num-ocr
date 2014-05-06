#encoding=utf-8
import os
import numpy as np
from PIL import Image


num_templates = {} # 数字模板
hight = 20 # 模板数字的高
width = 12 # 模板数字的宽


def gen_array(file_path):
    """从指定的图片文件生成一个numpy array
    :param file_path 输入图片文件的路径
    :return None
    """
    img = Image.open(file_path)
    img = img.convert('L')
    return np.array(img)



def load_num_template(template_dir):
    """加载制作好的数字模板文件,加载的数字模板为一组值为0-255的点的坐标
    :param template_dir: /path/to/num/template/
    :return None
    """
    files = os.listdir(template_dir)
    loaded_num = []
    for filename in files:
        if filename.endswith('.png'):
            num = filename[0]
            file_path = template_dir + filename
            num_arr = gen_array(file_path)
            m, n = num_arr.shape
            # generate number template
            num_temp = []
            for mi in range(m):
                for ni in range(n):
                    if num_arr[mi][ni] != 255:
                        num_temp.append((mi, ni))
            num_templates[num] = num_temp
            loaded_num.append(num)
    print "Template loaded for numbers: ", loaded_num


def match_cur_window(cur_window, num_template):
    """
    判断给定window的切块是否与数字模板匹配
    :param cur_window:
    :param num_template:
    :return: True 匹配， False 不匹配
    """
    is_match = True
    for x, y in num_template:  # (x, y) point need to be 255
        if cur_window[x, y] == 255:
            is_match = False
            break
    return is_match


def match(img_arr):
    """输入一个图片的二值化矩阵，以数字模板的尺寸为窗口，在图片矩阵中从上到下，从左到右移动
    匹配数字模板，并记录匹配结果
    :param  img_array = numpy.array(Image.open(image_file).convert('L'))
    :return a string represent the numbers in the img_arr
    """
    out = []  # 线性扫描输出队列
    m, n = img_arr.shape  # m行, n列
    m_max = m - hight + 1
    n_max = n - width + 1
    for ni in range(n_max):
        for mi in range(m_max):
            cur_window = img_arr[mi:mi+hight, ni:ni+width]
            match_one = False
            for num, num_template in num_templates.items():
                # match one num template
                if match_cur_window(cur_window, num_template):
                    out.append(num)
                    match_one = True
                    break
            if match_one:  # 如果在当前列范围内找到一个匹配，则窗口右移
                break
    # 将返回的结果拼接成字符串输出
    return ''.join([str(num) for num in out])

def convert_to_string(image_file):
    """
    将一个图片文件中的数字转换成字符串
    :param image_file: 输入图片
    :return: 识别出的数字字符串
    """
    img_arr = gen_array(image_file)
    m, n = img_arr.shape
    # append
    padding = np.zeros((m, 5)) + 255
    img_arr = np.concatenate((padding, img_arr), 1)
    # print_arr(img_arr, "Image")
    result = match(img_arr)
    return result


def print_arr(np_arr, arr_name):
    """输出图片的矩阵，used for debugging"""
    print 'Filename: ', arr_name
    m, n = np_arr.shape
    print 'Shape: ', m, n
    for mi in range(m):
        for ni in range(n):
            bit = ' '
            if np_arr[mi, ni] != 255:
                bit = '*'
            print bit,
        print ''
    print ''


if __name__ == '__main__':
    # init
    template_dir = 'numtemplate/'
    load_num_template(template_dir)

    # run
    files = os.listdir('data/')
    for filename in files:
        if filename.endswith('.png'):
            test_file = 'data/' + filename
            result = convert_to_string(test_file)
            print filename, " ===>", result