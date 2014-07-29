#coding:utf-8
import urllib2, urllib, cookielib
import re
import getpass
import random
import time
import Spider

class AutoEpisodeUpload:
    def __init__(self, user, pwd, args):
      self.username = user
      self.password = pwd
      self.args = args
      self.isLogin = False
      self.cj = cookielib.CookieJar()
      self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
      self.signin()

    def signin(self):
        try:
            #user_agent = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 2.0.507"
            #opener.addheaders = [('User-agent', user_agent)]
            urllib2.install_opener(self.opener)
            signin_data = {
                "session" : {
                    "email": self.username,
                    "password": self.password
                }
            }
            signin_data = urllib.urlencode(signin_data)
            #request = urllib2.Request(self.args['signin_submit_url'], signin_data)
            #response = urllib2.urlopen(request)
            response = self.opener.open(self.args['signin_submit_url'], signin_data)
            if response == None:
              print "Yes"
            else:
              print response.info()
            self.isLogin = True
            print 'login success...'
        except Exception, e:
            print 'login error: %s' % e

    def postEpisode(self, episode, image_url):
        response = None
        try:
            upload_data = {
              "script": episode
            }
            if image_url != "#":
                upload_data["imgurl"] = image_url

            upload_data = urllib.urlencode(upload_data)
            response = self.opener.open(self.args['upload_episode_url'], upload_data)
            print 'upload success...'
        except Exception, e:
            print 'upload error: %s' % e
        finally:
            print response

if __name__ == '__main__':
    username = "Lily@gmail.com"#raw_input('username').strip()
    password = "123456"#getpass.getpass('password').strip()
    args = {
        "signin_submit_url" : "http://localhost:3000/sessions",
        "upload_episode_url" : "http://localhost:3000/episodes",
        "spider_content_object_page": "http://www.qiushibaike.com/"
    }
    aep = AutoEpisodeUpload(username, password, args)
    sr = Spider.SpiderRobost(args)
    sr.extractContent()
    upload_content = sr.getDataFromDB()
    for i in range(len(upload_content)):
        tmp = upload_content[i][0]
        url = upload_content[i][1]
        if tmp != None:
            tmp = tmp.encode('utf8')
            url = url.encode('utf8')
            aep.postEpisode(tmp, url)
            time.sleep(50.0 / 1000.0)
    print "Finished"
    sr.closeDB();
    #replyList = [
    #    "屌丝租房，返迁房的隔音效果真不是盖的，隔壁一对奇葩每晚十一点后叫声不断，猛烈的撞击墙，有天实在受不了，敲门：能不能别每天晚上这么叫？男的开门了，我看了一眼：哦，之前的那对搬走了啊，转身关门。隔壁就听到吵架了，男的怒吼：我出差几天谁来这了？深藏功与名",
    #    "高中时候的事了，一次教导主任把我们班几个上课迟到的学生连我们班的班主任一块训斥一顿，关键是当着全班同学的面，教导主任走后，班主任觉得很没面子，生气的说自己的屁股擦不干净还好意思管我们，叨叨一堆，终于一个逗比站起来非常气氛说了句：不如我们反了吧！！！！",
    #    "这家伙骗了多少人的蝌蚪。懂吧。",
    #    "大荒南经属于山海经中第十五卷，讲述大荒山中的各山各海等地方，这些地方的各种人物、事物、神怪志异的传说故事。在南海的岛屿上，有一个神，是人的面孔，耳朵上穿挂着两条青色蛇，脚底下踩踏着两条红色蛇，这个神叫不廷胡余。有个神人名叫因乎，南方人单称他为因，从南方吹来的风称作民，他处在大地的南极主管风起风停。有座襄山。又有座重阴山。有人在吞食野兽肉，名叫季厘。帝俊生了季厘，所以称作季厘国。有一个缗渊。少昊生了倍伐，倍伐被贬住在缗渊。有一个水池是四方形的，名叫俊坛。有个国家叫臷民国。帝舜生了无淫，无淫被贬在臷这个地方居住，他的子孙后代就是所谓的巫臷民。巫臷民姓朌，吃五谷粮食，不从事纺织，自然有衣服穿；不从事耕种，自然有粮食吃。这里有能歌善舞的鸟，鸾鸟自由自在地歌唱，凤鸟自由自在地舞蹈。这里又有各种各样的野兽，群居相处。还是各种农作物汇聚的地方。",
    #    "窗前明月光疑是地上霜举头望明月低头思故乡"
    #]
    #for i in range(100):
    #    episode = random.choice(replyList);
    #    aep.postEpisode(episode);
    #    time.sleep(50.0 / 1000.0);