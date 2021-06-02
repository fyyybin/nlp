from os.path import join
from codecs import open


def build_corpus(split, make_vocab=True, data_dir="./train"):
    """读取数据"""
    assert split in ['train', 'val']

    tag_lists = []
    words_lists = []
    with open(join(data_dir, split+"_data.txt"), 'r', encoding='utf-8') as f:
        text = f.readlines()
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

    # 如果make_vocab为True，还需要返回word2id和tag2id
    if make_vocab:
        word2id = build_map(words_lists)
        tag2id = build_map(tag_lists)
        return words_lists, tag_lists, word2id, tag2id
    else:
        return words_lists, tag_lists


def build_map(lists):
    maps = {}
    for list_ in lists:
        for e in list_:
            if e not in maps:
                maps[e] = len(maps)

    return maps
