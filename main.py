import os
import re
def get_data_lists(filepath):

    fp = open(filepath, 'r', encoding='utf-8')
    text = fp.readlines()

    tag_lists = []
    words_lists = []

    for i in text:

        lables = i.split('|||')[1:][:-1]
        content = i.split('|||')[0]
        words_list = [word for word in content]
        words_lists.append(words_list)

        tag_list = []
        begin = []
        end = []
        tags = []

        # begin是实体的起始位置，end是结束为止，tags是标签
        for j in lables:
            p = j.split('    ')
            begin.append(int(p[0]))
            end.append(int(p[1]))
            tags.append(p[2])

        # print('-------------------')
        # print(words_list)
        # print(begin)
        # print(end)
        # print(tags)

        id_tag = 0
        for j in range(len(words_list)):
            if j in begin:
                id_tag = begin.index(j)
                tag = 'B' + '-' + tags[id_tag]
            elif j > begin[id_tag] and j < end[id_tag]:
                tag = 'I' + '-' + tags[id_tag]
            elif j == end[id_tag]:
                tag = 'E' + '-' + tags[id_tag]
            else:
                tag = 'O'
            tag_list.append(tag)
        tag_lists.append(tag_list)
    return tag_lists, words_lists

def build_dict(lists):
    maps = {}
    for list_ in lists:
        for e in list_:
            if e not in maps:
                maps[e] = len(maps)
    return maps

# 处理起始数据文件
train_tags_lists, train_words_lists = get_data_lists('E:/train_data.txt')
# 讲tags和words变为字典便于成矩阵
word2id = build_dict(train_words_lists)
tag2id = build_dict(train_tags_lists)

import torch
class HMM(object):
    def __init__(self, tag2id, word2id):
        N = len(tag2id)
        M = len(word2id)
        self.N = N
        self.M = M
        # A是状态概率转移矩阵，B是观测概率矩阵，Pi初始概率矩阵
        self.A = torch.zeros(N, N)
        self.B = torch.zeros(N, M)
        self.Pi = torch.zeros(N)




