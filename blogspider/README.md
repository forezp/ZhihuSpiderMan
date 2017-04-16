# Python爬虫，看看我最近博客都写了啥，带你制作高逼格的数据聚合云图

今天看了简书的作者[向右奔跑]的文章，一时兴趣来了，想用python爬爬自己的博客，通过数据聚合，制作高逼格的云图(对词汇出现频率视觉上的展示)，看看最近我到底写了啥文章。

## 一、直接上几张我的博客数据的云图

#### 1.1 爬取文章的标题的聚合

![爬取的文章标题的数据聚合](http://upload-images.jianshu.io/upload_images/2279594-661382846e212a86.jpeg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


![爬取的文章标题的数据聚合](http://upload-images.jianshu.io/upload_images/2279594-03d5c12e7a0309d7.jpeg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![爬取的文章标题的数据聚合](http://upload-images.jianshu.io/upload_images/2279594-c7a31451ae8f9e2c.jpeg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


#### 1.2 爬取文章的摘要的聚合

![33.jpeg](http://upload-images.jianshu.io/upload_images/2279594-9e1ad67661db5d2c.jpeg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![34.jpeg](http://upload-images.jianshu.io/upload_images/2279594-19e435f576714e3e.jpeg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#### 1.3 爬取文章的标题+摘要的聚合


![21.jpeg](http://upload-images.jianshu.io/upload_images/2279594-09f48b5098ee2f02.jpeg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![22.jpeg](http://upload-images.jianshu.io/upload_images/2279594-7d75005594f939b4.jpeg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**我最近写了SpringCloud系列教程，还有一些微服务架构方面，从云图上看，基本吻合。你若不信，可以进我的博客看看，数据还是非常准确的**

## 二、技术栈

* 开发工具: pycharm
* 爬虫技术：bs64、requsts、jieba
* 分析工具：wordArt

## 三、爬虫构架设计



![Azure.png](http://upload-images.jianshu.io/upload_images/2279594-c1c0cbb4a6c38d51.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

整个爬虫架构非常简单：

* 爬取我的博客：http://blog.csdn.net/forezp
* 获取数据
* 将数据用“结巴”库，分词。
* 将得到的数据在在artword上制作云图。
* 将制作出来的云图展示给用户。

## 四、具体实现

先根据博客地址爬去数据：

```
url = 'http://blog.csdn.net/forezp'

titles=set()

def download(url):
    if url is None:
        return None
    try:
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
        })
        if (response.status_code == 200):
            return response.content
        return None
    except:
        return None

```

解析标题

```
def parse_title(html):
    if html is None:
        return None
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all('a', href=re.compile(r'/forezp/article/details'))
    for link in links:

        titles.add(link.get_text())

```

解析摘要：

```

def parse_descrtion(html):
    if html is None:
        return None
    soup=BeautifulSoup(html, "html.parser")
    disciptions=soup.find_all('div',attrs={'class': 'article_description'})
    for link in disciptions:

        titles.add(link.get_text())

```
 用“结巴”分词，"激8"分词怎么用，看这里：[https://github.com/fxsjy/jieba/](https://github.com/fxsjy/jieba/) .
 
 
 ```
 def jiebaSet():
    strs=''
    if titles.__len__()==0:
        return
    for item in titles:
        strs=strs+item;


    tags = jieba.analyse.extract_tags(strs, topK=100, withWeight=True)
    for item in tags:
        print(item[0] + '\t' + str(int(item[1] * 1000)))
 ```
 因为数据比较少，所以我直接打印在控制台，并把它复制下来，更好的方法是存在mongodb中。
 
 制作云图：
 用 artword在线工具，地址：[https://wordart.com](https://wordart.com)
 
 首先：
 导入从控制台复制过来的数据：
 
 ![Paste_Image.png](http://upload-images.jianshu.io/upload_images/2279594-de72be046ecac0d1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

令人尴尬的是，这个网站在绘制图的时候不支持中文，需要你从c:/windows/fonts下选择一个支持中文的字体，mac 用户从windows拷下文件夹也可以，或者在网上下。

![Paste_Image.png](http://upload-images.jianshu.io/upload_images/2279594-fc5c023b1cf9f2c7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

然后点击Visulize就可以生成高逼格的云图了。讲解完毕，有什么需要改进的请大家留言。

源码下载：

#### 五、文章参考

[超简单：快速制作一款高逼格词云图](http://www.jianshu.com/p/4fb27471295f)

 