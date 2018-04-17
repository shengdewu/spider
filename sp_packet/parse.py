import spider
import jieba
import pandas as pd

class parse(object):

    def get_comment(self, content):
        s = spider.spider()
        comments = {}
        for iter in content:
            subject = iter.get('data-subject', -1)
            if -1 == subject:
                continue
            comment = s.get_comment(subject, 30)
            comments[subject] = comment
        return comments

    def parse_word(self, key, value):
        segment = jieba.lcut(value)
        word = pd.DataFrame({'segment':segment})
        stopwords = pd.read_csv("./stopwords.txt", index_col=False, quoting=3, sep="\t", names=['stopword'],
                                encoding='utf-8')
        word = word[word.segment.isin(stopwords.stopword)]
        print word.head()
        return
