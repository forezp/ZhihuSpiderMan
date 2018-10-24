<div>
    <p align="center">
        <img src="https://www.fangzhipeng.com/img/avatar.jpg" width="258" height="258"/>
        <br>
        扫码关注公众号有惊喜
    </p>
    <p align="center" style="margin-top: 15px; font-size: 11px;color: #cc0000;">
        <strong>（转载本站文章请注明作者和出处 <a href="https://www.fangzhipeng.com">方志朋的博客</a>）</strong>
    </p>
</div>

# ZhihuSpiderMan


### 一、使用的技术栈：

* 爬虫：python27 +requests+json+bs4+time
* 分析工具： ELK套件
* 开发工具：pycharm

### 二、数据成果
爬取了573347条数据，在python代码中我并没有采取线程池，而是采用了开起10个__main（）__方法去抓取，即10个进程，历时4个小时，爬取了57w+数据。
![在kibana上显示的数据量](http://upload-images.jianshu.io/upload_images/2279594-c61576f1217b31aa.jpeg?imageMogr2/auto-orient/strip%7CimageView2/2/w/600)

### 三、简单的可视化分析

1.性别分布

* 0 绿色代表的是男性 ^ . ^
* 1 代表的是女性
* -1 性别不确定

可见知乎的用户男性颇多。


![WechatIMG2.jpeg](http://upload-images.jianshu.io/upload_images/2279594-22b13dd888296ab7.jpeg?imageMogr2/auto-orient/strip%7CimageView2/2/w/600)

2.粉丝最多的top30

粉丝最多的前三十名：依次是张佳玮、李开复、黄继新等等，去知乎上查这些人，也差不多这个排名，说明爬取的数据具有一定的说服力。

![粉丝最多的top30](http://upload-images.jianshu.io/upload_images/2279594-8a57509513af7829.jpeg?imageMogr2/auto-orient/strip%7CimageView2/2/w/600)


3.写文章最多的top30
![写文章最多的top30](http://upload-images.jianshu.io/upload_images/2279594-c29b348c4eb380f9.jpeg?imageMogr2/auto-orient/strip%7CimageView2/2/w/600)


4.知乎用户写文章篇数人数分布
不在知乎上写文章的占到了45w，差不多90%吧，说明知乎用户大多数都是看文章，看回答，内容生产者只有10%。

![知乎用户写文章篇数人数分布情况](http://upload-images.jianshu.io/upload_images/2279594-872f0a771e6ea438.jpeg?imageMogr2/auto-orient/strip%7CimageView2/2/w/600)

### 四、爬虫架构

爬虫架构图如下：
![爬虫架构图](http://upload-images.jianshu.io/upload_images/2279594-26c9bd69af563fd5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/600)

说明：

* 选择一个活跃的用户（比如李开复）的url作为入口url.并将已爬取的url存在set中。
* 抓取内容，并解析该用户的关注的用户的列表url，添加这些url到另一个set中，并用已爬取的url作为过滤。
* 解析该用户的个人信息，并存取到本地磁盘。
* logstash取实时的获取本地磁盘的用户数据，并给elsticsearch
* kibana和elasticsearch配合，将数据转换成用户友好的可视化图形。

#### 五.编码

爬取一个url:

```
def download(url):
    if url is None:
        return None
    try:
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
            'authorization': 'your authorization '
        })
        print (response.content)
        if (response.status_code == 200):
            return response.content
        return None
    except:
        return None

```

解析内容：

```
def parse(response):
    try:
        print (response)
        json_body = json.loads(response);
        json_data = json_body['data']
        for item in json_data:
            if (not old_url_tokens.__contains__(item['url_token'])):
                if(new_url_tokens.__len__()<2000):
                   new_url_tokens.add(item['url_token'])
            if (not saved_users_set.__contains__(item['url_token'])):
                jj=json.dumps(item)
                save(item['url_token'],jj )
                saved_users_set.add(item['url_token'])

        if (not json_body['paging']['is_end']):
            next_url = json_body['paging']['next']
            response2 = download(next_url)
            parse(response2)

    except:
        print ('parse fail')

```

存本地文件：

```
def save(url_token, strs):
    f = file("\\Users\\forezp\\Downloads\\zhihu\\user_" + url_token + ".txt", "w+")
    f.writelines(strs)
    f.close()

```

代码说明：
* 需要修改获取requests请求头的authorization。
* 需要修改你的文件存储路径。


### 六.如何获取authorization

* 打开chorme，打开https://www.zhihu.com/，  
* 登陆，首页随便找个用户，进入他的个人主页，F12(或鼠标右键，点检查)
* 点击关注，刷新页面，见图：


![如何获取authorization](http://upload-images.jianshu.io/upload_images/2279594-0fa965cff3cddc64.jpeg?imageMogr2/auto-orient/strip%7CimageView2/2/w/600)


### 七、可改进的地方

* 可增加线程池，提高爬虫效率
* 存储url的时候我才用的set(),并且采用缓存策略，最多只存2000个url，防止内存不够，其实可以存在redis中。
* 存储爬取后的用户我说采取的是本地文件的方式，更好的方式应该是存在mongodb中。
* 对爬取的用户应该有一个信息的过滤，比如用户的粉丝数需要大与100或者参与话题数大于10等才存储。防止抓取了过多的僵尸用户。

### 八.关于ELK套件

关于elk的套件安装就不讨论了，具体见官网就行了。网站：https://www.elastic.co/


另外logstash的配置文件如下：

```

input {
  # For detail config for log4j as input,
  # See: https://www.elastic.co/guide/en/logstash/current/plugins-inputs-log4j.html

    file {
        path => "/Users/forezp/Downloads/zhihu/*"
    }


}
filter {
  #Only matched data are send to output.
}
output {
  # For detail config for elasticsearch as output,
  # See: https://www.elastic.co/guide/en/logstash/current/plugins-outputs-elasticsearch.html
 elasticsearch {
    action => "index"          #The operation on ES
    hosts  => "localhost:9200"   #ElasticSearch host, can be array.
    index  => "zhihu"         #The index to write data to.
  }
}

```
### 九、结语

从爬取的57万用户数据可分析的地方很多，比如地域、学历、年龄等等，我就不一一列举了。另外，我觉得爬虫是一件非常有意思的事情，在这个内容消费升级的年代，如何在广阔的互联网的数据海洋中挖掘有价值的数据，是一件值得思考和需不断践行的事情。
