# encoding: utf-8

import numpy as np
import math
import time
import argparse


def gen_col(rate, group_len):
    """
    生成一列数字形式的碱基
    :param group_len: 每一组的barcode个数
    :param rate: 组内每列每种碱基最小占比
    :return: 一列碱基
    """
    num = math.floor(group_len * rate) + 1
    col = np.concatenate((np.tile([0, 1, 2, 3], num),
                          np.random.randint(low=0, high=4, size=group_len - num * 4)),
                         axis=0)
    np.random.shuffle(col)
    return col


def gen_group_matrix(group_len, barcode_len, rate):
    """
    生成一组数字形式的barcode矩阵
    :param group_len: 每组的barcode个数
    :param barcode_len: barcode长度
    :param rate: 组内每列每种碱基最小占比
    :return: 形状为(group_len, barcode_len)的数字形式的barcode矩阵
    """
    group = []
    for i in range(barcode_len):
        group.append(gen_col(rate, group_len))
    return np.asarray(group).T


def judge_barcode_repeat_num(barcode, repeat_num):
    """
    判断barcode是否出现repeat_num个数以上的连续碱基
    :param barcode: 等待判断的barcode
    :param repeat_num: 碱基连续重复个数
    :return: 若出现,返回TRUE;否则为FALSE
    """
    return "A" * repeat_num in barcode or "C" * repeat_num in barcode \
           or "T" * repeat_num in barcode or "G" * repeat_num in barcode


def cul_dis_between_barcodes(barcode1, barcode2):
    """
    计算两个barcode之间humming距离
    :param barcode1:
    :param barcode2:
    :return: 两个barcode之间humming距离
    """
    dis = 0
    for i in range(len(barcode1)):
        if barcode1[i] != barcode2[i]:
            dis += 1
    return dis


def matrix_to_barcodes(matrix):
    """
    将一组数字形式的barcode矩阵转化为barcode列表
    :param matrix: 数字形式的barcode矩阵
    :return: barcode列表
    """
    chars = ['A', 'T', 'C', 'G']
    barcodes = []
    for row in matrix:
        barcode = []
        for index in row:
            barcode.append(chars[index])
        barcodes.append("".join(barcode))
    return barcodes


def judge_cur_barcodes(cur_barcodes, all_barcodes, repeat_num, min_dist):
    """
    判断当前的一组barcode是否符合规则
    :param min_dist: 最小humming距离
    :param repeat_num: 每个barcode中不允许出现的连续相同碱基个数
    :param cur_barcodes: 当前的一组barcode
    :param all_barcodes: 已经生成的所有barcode
    :return: 判断符合规则时返回TRUE;否则返回FALSE
    """
    for i in range(len(cur_barcodes)):

        if judge_barcode_repeat_num(cur_barcodes[i], repeat_num):
            return False
        # 组内比较humming距离
        for j in range(i + 1, len(cur_barcodes)):
            if cul_dis_between_barcodes(cur_barcodes[i], cur_barcodes[j]) < min_dist:
                return False
        # 和已经生成的所有barcode比较humming距离
        for k in range(len(all_barcodes)):
            if cul_dis_between_barcodes(cur_barcodes[i], all_barcodes[k]) < min_dist:
                return False

    return True


def gen_barcodes_groups(group_num, group_len, barcode_len, rate, repeat_num, min_dist):
    """
    生成若干组barcode
    :param group_num: 组数
    :param group_len: 每组的barcode个数
    :param barcode_len: barcode长度
    :param rate: 组内每列每种碱基最小占比
    :param repeat_num: 碱基连续重复个数
    :param min_dist: 最小humming距离
    :return: group_num组个barcode
    """
    all_barcodes = []
    for group_id in range(group_num):
        while True:
            cur_barcodes = matrix_to_barcodes(gen_group_matrix(group_len, barcode_len, rate))
            if judge_cur_barcodes(cur_barcodes, all_barcodes, repeat_num, min_dist):
                all_barcodes.extend(cur_barcodes)
                break

    return all_barcodes


def print_barcodes_groups(all_barcodes, group_num, group_len):
    """
    按组打印barcodes到barcodeFile.tsv
    :param group_num:
    :param group_num: 组数
    :param group_len: 每组的barcode个数
    :return:
    """
    with open("barcodeFile.tsv", "w") as f:
        for i in range(group_num):
            f.write("第 " + str(i + 1) + " 组\n")
            for j in range(group_len):
                f.write(str(j + 1) + ": " + all_barcodes[i * group_len + j] + "\n")


if __name__ == '__main__':
    start = time.clock()

    parser = argparse.ArgumentParser()

    parser.add_argument(dest="group_num", help="组数: 例如为" + str(5), type=int)
    parser.add_argument(dest="group_len", help="每组的barcode个数: 例如为" + str(16), type=int)
    parser.add_argument(dest="barcode_len", help="barcode长度: 例如为" + str(10), type=int)
    parser.add_argument(dest="rate", help="组内每列每种碱基最小占比: 例如为" + str(0.125), type=float)
    parser.add_argument(dest="repeat_num", help="不允许相同碱基连续重复个数: 例如为" + str(3), type=int)
    parser.add_argument(dest="min_dist", help="最小humming距离: 例如为" + str(3), type=int)

    args = parser.parse_args()

    group_num = args.group_num
    group_len = args.group_len
    barcode_len = args.barcode_len
    rate = args.rate
    repeat_num = args.repeat_num
    min_dist = args.min_dist

    print_barcodes_groups(gen_barcodes_groups(group_num, group_len, barcode_len, rate, repeat_num, min_dist), group_num,
                          group_len)

    elapsed = (time.clock() - start)
    print("barcodes已写入barcodeFile.tsv")
    print("Time used: ", elapsed)
