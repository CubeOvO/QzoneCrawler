from qzone import *
import qzone
import os
from functools import partial
import multiprocessing
import hashlib
import urllib

# the cookies for the curl
curl_result = ''

# contains the picture objects

pics = []



# given qqid, picture link; download it
def down_image(p,uin):
    try:
        soup = p.open().read()
    except http.client.HTTPException:
        print('Error occurred.')
        return -1
    # file name is the md5 of the file in order to prvent re download
    filename = hashlib.md5(soup).hexdigest()
    filename = os.path.join('.\\{}\\'.format(uin), str(filename) + "." + "png")



    try:
        # if the filename exists
        with open(filename, 'r') as code:
            print('file already exists {}'.format(filename))
            return 0
    # otherwise creating new file
    except FileNotFoundError:
        print('detected new file.', end=' ')

        with open(filename, 'wb') as f:
            f.write(soup)
        # if cannot open/download

        print('successfully downloaded {}'.format(filename))
        return 1


# given qqid create a new folder
def create_folder(folder_path,uin):
    qqstr = uin
    if os.path.isdir(folder_path):
        print('folder {} already exists'.format(folder_path))

        # prompt use if they want additional folder i.e. .\qq_num_new\
        newfolder = input('Creating new folder?\n')
        if newfolder:
            while True:
                qqstr = str(qqstr) + '_new'
                folder_path = '.\\{}\\'.format(qqstr)
                if not os.path.isdir(folder_path):
                    os.mkdir(folder_path)
                    print('new folder created {}'.format(folder_path))
                    break

                # if the folder qq_num_new still exist
                else:
                    print('folder {} already exists'.format(folder_path))

                    # do we want a qq_nuw_new_new?
                    newfolders = input('Creating new folder?\n')
                    if newfolders:
                        # yes we do
                        pass
                    else:
                        # no store the file in qq_num_new
                        break
            print('folder path is {}'.format(folder_path))
        return qqstr
    # else create it
    else:
        print('creating new folder {}'.format(folder_path))
        os.mkdir(folder_path)
    return qqstr


# load all of the pics objects for a given qzoneObject
def load_img(emotions):
    all = len(emotions)
    finished = 0
    for e in emotions:
        print('Processing: ',end='')
        # print('Emotion对象表示一条说说:{}，包含以下属性：\n tid: 一个能唯一标识说说的字符串:{}；\n author: 作者QQ号:{}；\n nickname: 作者昵称或备注:{}；\n ctime: 说说发布时间，Unix时间戳形式:{}；\n shortcon: 说说正文的前面一部分正文:{}；\n content: 说说完整正文:{}；\n pictures: 一个list，其中包含若干个Picture对象，后面会讲到:{}\n origin: 一个Emotion对象或None，被转发的原说说:{}；\n location: 位置信息，是一个dict:{}；\n source: 发布说说所用的设备或途径名称:{}；\n forwardn: 被转发的次数:{}；\n like: 一个dict，键为点赞的人的QQ号，值为二元组 昵称, 头像Picture对象:{}\n comments: 一个list，其中包含若干个Comment对象，后面会讲到:{}\n forwards: 一个list，其中包含若干个Emotion对象，它们都是对这条说说的转发'.format(e,e.tid,e.author,e.nickname,e.ctime,e.shortcon,e.content,e.pictures,e.origin,e.location,e.source,e.forwardn,e.like,e.comments))
        try:
            e.load()
        except urllib.error.URLError:
            print('failed')
        for j in e.pictures:
            pics.append(j)

        finished += 1
        print( "{0:.0%}".format(finished/all))

# print results
def print_out(results):
    print(results)
    success, exists, timeout = 0, 0, 0
    for i in results:
        if i == 1:
            success += 1
        elif i == 0:
            exists += 1
        else:
            timeout += 1
    print('Downloaded image , total {}, success {}, exists {}, timeout {}'.format(len(results), success, exists, timeout))



def main():
    # setting cookie to qzone object
    reset = input('Do you want to overwrite your cookie?\n')
    if reset:
        curl_result = input('Please input your curl (cmd) command here:\n')
    qzoneObject = qzone.Qzone(**qzone.get_cookie_from_curl(curl_result))

    # prompt qq from the user
    uin = input('Please input the qq number of the qzone that you wish to download:')
    # load the pictures of the qqid
    emotions = qzoneObject.emotion_list(uin, num=40, pos=0)
    load_img(emotions)
    print('Picture loaded, total amount is {}'.format(len(pics)))
    # create the folder for that qqid
    folder_path = '.\\{}\\'.format(uin)
    qqstr = create_folder(folder_path,uin)
    # download the picture of that qqid
    with multiprocessing.Pool() as pool:
        results = pool.map(partial(down_image, uin=qqstr), pics)
    # print results of the qqid
    print_out(results)



if __name__ == '__main__':
    main()
