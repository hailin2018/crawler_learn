# -*- coding: UTF-8 -*-
import os
import sys
# cur_dir = os.path.abspath(os.path.dirname(__file__))
# pro_dir = os.path.split(cur_dir)[0]
# sys.path.append(pro_dir)
import mylib


from mylib import division



def main():
    print(division(6, 3))


if __name__ == '__main__':
    main()
