from qzone import *
from image import *
import os
from functools import partial
import time
from datetime import datetime

curl_result = '' 
emotime = []
# load all of the emotions for a given qzoneObject
def load_emo(emotions):
    all = len(emotions)
    finished = 0
    for e in emotions:
        print('Processing: ', end='')
        # print('Emotion对象表示一条说说:{}，包含以下属性：\n tid: 一个能唯一标识说说的字符串:{}；\n author: 作者QQ号:{}；\n nickname: 作者昵称或备注:{}；\n ctime: 说说发布时间，Unix时间戳形式:{}；\n shortcon: 说说正文的前面一部分正文:{}；\n content: 说说完整正文:{}；\n pictures: 一个list，其中包含若干个Picture对象，后面会讲到:{}\n origin: 一个Emotion对象或None，被转发的原说说:{}；\n location: 位置信息，是一个dict:{}；\n source: 发布说说所用的设备或途径名称:{}；\n forwardn: 被转发的次数:{}；\n like: 一个dict，键为点赞的人的QQ号，值为二元组 昵称, 头像Picture对象:{}\n comments: 一个list，其中包含若干个Comment对象，后面会讲到:{}\n forwards: 一个list，其中包含若干个Emotion对象，它们都是对这条说说的转发'.format(e,e.tid,e.author,e.nickname,e.ctime,e.shortcon,e.content,e.pictures,e.origin,e.location,e.source,e.forwardn,e.like,e.comments))
        if type(e.content) == NotLoadedType:
            e.load()
        emolist.append(str(e.content))
        emotime.append(datetime.fromtimestamp(e.ctime))

        finished += 1
        print("{0:.0%}".format(finished / all))

# write all of the emotions into the file
def down_emo(qq,emolist,emotime):
    filename = os.path.join('.\\{}\\'.format(qq), str(qq) + "." + "txt")
    with open(filename,'w', encoding="utf-8") as f:
        for e,c in zip(emolist,emotime):
            try:
                print(c,e+'\n'*2,file=f,sep=':\n')
            except UnicodeEncodeError:
                print('error occured when decoding, skipping')
                pass
        print('saved')
    return 0



def main():
    # setting cookie to qzone object
    reset = input('Do you want to overwrite your cookie?\n')
    if reset:
        curl_result = input('Please input your curl (cmd) command here:\n')
    qzoneObject = qzone.Qzone(**qzone.get_cookie_from_curl(curl_result))
    # prompt qq from the user
    qq = input('Please input the qq number of the qzone that you wish to download:')
    # load the emotions of the qqid
    emotions = qzoneObject.emotion_list(qq, num=40, pos=0)
    load_emo(emotions)
    print('Emotion loaded, total amount is {}'.format(len(emolist)))
    print(emolist,emotime)
    # create the folder for that qqid
    folder_path = '.\\{}\\'.format(qq)
    qqstr = create_folder(folder_path, qq)
    # download the picture of that qqid
    down_emo(qqstr,emolist,emotime)



if __name__ == '__main__':
    main()
