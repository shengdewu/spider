import spider

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
