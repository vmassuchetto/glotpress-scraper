import os, re
from cgi import parse_header
from urllib import urlopen

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

class LinkPipeline(object):

    def process_item(self, item, spider):
        u = urlopen(item['url'])

        d = spider.settings.get('DOWNLOAD_DIR') + '/' + item['project']
        d = re.sub(r'export-translations', '', d)
        if not os.path.isdir(d):
            mkdir_p(d)

        _, params = parse_header(u.headers.get('Content-Disposition', ''))
        filename = params['filename']
        filepath = d + '/' + filename
        f = open(filepath, 'w')
        f.write(u.read())
        f.close()
