# Scrapy框架

- Scrapy是用纯Python实现一个为了爬取网站数据、提取结构性数据而编写的应用框架，用途非常广泛。

- 框架的力量，用户只需要定制开发几个模块就可以轻松的实现一个爬虫，用来抓取网页内容以及各种图片，非常之方便。
- Scrapy 使用了 Twisted`['twɪstɪd]`(其主要对手是Tornado)异步网络框架来处理网络通讯，可以加快我们的下载速度，不用自己去实现异步框架，并且包含了各种中间件接口，可以灵活的完成各种需求。

## Scrapy架构图



![img](file:///D:/%E9%BB%91%E9%A9%AC%E4%B8%8A%E6%B5%B737%E6%9C%9FPython%E8%A7%86%E9%A2%91/%E8%AF%BE%E4%BB%B6%E8%B5%84%E6%96%99/%E5%9F%BA%E7%A1%80%E7%8F%AD-%E5%B0%B1%E4%B8%9A%E7%8F%AD%E8%AF%BE%E4%BB%B6%E8%B5%84%E6%96%99%20-1-4%E4%BD%8D%E5%9F%BA%E7%A1%80%E7%8F%AD%20%205-14%E5%B0%B1%E4%B8%9A%E7%8F%AD/11-%E7%88%AC%E8%99%AB%E5%BC%80%E5%8F%91%E9%98%B6%E6%AE%B5-%E7%88%AC%E8%99%AB%E5%9F%BA%E7%A1%80-MongoDB%E6%95%B0%E6%8D%AE%E5%BA%93-%E7%88%AC%E8%99%ABScrapy%E6%A1%86%E6%9E%B6%E5%92%8C%E6%A1%88%E4%BE%8B/%E7%88%AC%E8%99%AB%E8%AF%BE%E4%BB%B6V3.1/%E7%88%AC%E8%99%AB%E8%AF%BE%E4%BB%B6/file/images/scrapy_all.png)

- Scrapy Engine(引擎)`: 负责`Spider`、`ItemPipeline`、`Downloader`、`Scheduler`中间的通讯，信号、数据传递等。
- `Scheduler(调度器)`: 它负责接受`引擎`发送过来的Request请求，并按照一定的方式进行整理排列，入队，当`引擎`需要时，交还给`引擎`。
- `Downloader（下载器）`：负责下载`Scrapy Engine(引擎)`发送的所有Requests请求，并将其获取到的Responses交还给`Scrapy Engine(引擎)`，由`引擎`交给`Spider`来处理。
- `Spider（爬虫）`：它负责处理所有Responses,从中分析提取数据，获取Item字段需要的数据，并将需要跟进的URL提交给引擎，再次进入Scheduler(调度器)。
- `Item Pipeline(管道)`：它负责处理`Spider`中获取到的Item，并进行进行后期处理（详细分析、过滤、存储等）的地方。
- `Downloader Middlewares（下载中间件）`：你可以当作是一个可以自定义扩展下载功能的组件。
- `Spider Middlewares（Spider中间件）`：你可以理解为是一个可以自定扩展和操作`引擎`和`Spider`中间`通信`的功能组件（比如进入`Spider`的Responses;和从`Spider`出去的Requests）。

# Scrapy 和 scrapy-redis的区别

​	Scrapy 是一个通用的爬虫框架，但是不支持分布式，Scrapy-redis是为了更方便地实现Scrapy分布式爬取，而提供了一些以redis为基础的组件(仅有组件)。

`pip install scrapy-redis`

​	Scrapy-redis提供了下面四种组件（components）：(四种组件意味着这四个模块都要做相应的修改)

- Scheduler
- Duplication Filter
- Item Pipeline
- Base Spider

# scrapy-redis架构



![img](file:///D:/%E9%BB%91%E9%A9%AC%E4%B8%8A%E6%B5%B737%E6%9C%9FPython%E8%A7%86%E9%A2%91/%E8%AF%BE%E4%BB%B6%E8%B5%84%E6%96%99/%E5%9F%BA%E7%A1%80%E7%8F%AD-%E5%B0%B1%E4%B8%9A%E7%8F%AD%E8%AF%BE%E4%BB%B6%E8%B5%84%E6%96%99%20-1-4%E4%BD%8D%E5%9F%BA%E7%A1%80%E7%8F%AD%20%205-14%E5%B0%B1%E4%B8%9A%E7%8F%AD/11-%E7%88%AC%E8%99%AB%E5%BC%80%E5%8F%91%E9%98%B6%E6%AE%B5-%E7%88%AC%E8%99%AB%E5%9F%BA%E7%A1%80-MongoDB%E6%95%B0%E6%8D%AE%E5%BA%93-%E7%88%AC%E8%99%ABScrapy%E6%A1%86%E6%9E%B6%E5%92%8C%E6%A1%88%E4%BE%8B/%E7%88%AC%E8%99%AB%E8%AF%BE%E4%BB%B6V3.1/%E7%88%AC%E8%99%AB%E8%AF%BE%E4%BB%B6/file/images/scrapy-redis.png)

如上图所⽰示，scrapy-redis在scrapy的架构上增加了redis，基于redis的特性拓展了如下组件：

``Scheduler`：`

​	Scrapy改造了python本来的collection.deque(双向队列)形成了自己的Scrapy queue([https://github.com/scrapy/queuelib/blob/master/queuelib/queue.py)](https://github.com/scrapy/queuelib/blob/master/queuelib/queue.py))，但是Scrapy多个spider不能共享待爬取队列Scrapy queue， 即Scrapy本身不支持爬虫分布式，scrapy-redis 的解决是把这个Scrapy queue换成redis数据库（也是指redis队列），从同一个redis-server存放要爬取的request，便能让多个spider去同一个数据库里读取。

 	Scrapy中跟“待爬队列”直接相关的就是调度器`Scheduler`，它负责对新的request进行入列操作（加入Scrapy queue），取出下一个要爬取的request（从Scrapy queue中取出）等操作。它把待爬队列按照优先级建立了一个字典结构，比如：

```json
{
    优先级0 : 队列0
    优先级1 : 队列1
    优先级2 : 队列2
}
```

然后根据request中的优先级，来决定该入哪个队列，出列时则按优先级较小的优先出列。为了管理这个比较高级的队列字典，Scheduler需要提供一系列的方法。但是原来的Scheduler已经无法使用，所以使用Scrapy-redis的scheduler组件。

`Duplication Filter`

​	Scrapy中用集合实现这个request去重功能，Scrapy中把已经发送的request指纹放入到一个集合中，把下一个request的指纹拿到集合中比对，如果该指纹存在于集合中，说明这个request发送过了，如果没有则继续操作。这个核心的判重功能是这样实现的：

```python
   def request_seen(self, request):
        # 把请求转化为指纹  
        fp = self.request_fingerprint(request)

        # 这就是判重的核心操作  ，self.fingerprints就是指纹集合
        if fp in self.fingerprints:
            return True  #直接返回
        self.fingerprints.add(fp) #如果不在，就添加进去指纹集合
        if self.file:
            self.file.write(fp + os.linesep)
```

​	在scrapy-redis中去重是由`Duplication Filter`组件来实现的，它通过redis的set 不重复的特性，巧妙的实现了Duplication Filter去重。scrapy-redis调度器从引擎接受request，将request的指纹存⼊redis的set检查是否重复，并将不重复的request push写⼊redis的 request queue。

​	引擎请求request(Spider发出的）时，调度器从redis的request queue队列⾥里根据优先级pop 出⼀个request 返回给引擎，引擎将此request发给spider处理。

`Item Pipeline`

​	引擎将(Spider返回的)爬取到的Item给Item Pipeline，scrapy-redis 的Item Pipeline将爬取到的 Item 存⼊redis的 items queue。

​	修改过`Item Pipeline`可以很方便的根据 key 从 items queue 提取item，从⽽实现 `items processes`集群。

`Base Spider`

​	不在使用scrapy原有的Spider类，重写的`RedisSpider`继承了Spider和RedisMixin这两个类，RedisMixin是用来从redis读取url的类。

​	当我们生成一个Spider继承RedisSpider时，调用setup_redis函数，这个函数会去连接redis数据库，然后会设置signals(信号)：

- 一个是当spider空闲时候的signal，会调用spider_idle函数，这个函数调用`schedule_next_request`函数，保证spider是一直活着的状态，并且抛出DontCloseSpider异常。
- 一个是当抓到一个item时的signal，会调用item_scraped函数，这个函数会调用`schedule_next_request`函数，获取下一个request。

## Scrapy-Redis实例

使用scrapy-redis的example来修改

先从github上拿到scrapy-redis的示例，然后将里面的example-project目录移到指定的地址：

`git clone https://github.com/rolando/scrapy-redis.git`

### 一、dmoz (class DmozSpider(CrawlSpider))

这个爬虫继承的是CrawlSpider，它是用来说明Redis的持续性，当我们第一次运行dmoz爬虫，然后Ctrl + C停掉之后，再运行dmoz爬虫，之前的爬取记录是保留在Redis里的。

分析起来，其实这就是一个 scrapy-redis 版 CrawlSpider 类，需要设置Rule规则，以及callback不能写parse()方法。

执行方式:`scrapy crawl dmoz`

### 二、myspider_redis (class MySpider(RedisSpider))

这个爬虫继承了RedisSpider， 它能够支持分布式的抓取，采用的是basic spider，需要写parse函数。

其次就是不再有start_urls了，取而代之的是redis_key，scrapy-redis将key从Redis里pop出来，成为请求的url地址。

**注意：**
RedisSpider类 不需要写allowd_domains和start_urls：

scrapy-redis将从在构造方法__init__()里动态定义爬虫爬取域范围，也可以选择直接写allowd_domains。

必须指定redis_key，即启动爬虫的命令，参考格式：redis_key = 'myspider:start_urls'

根据指定的格式，start_urls将在 Master端的 redis-cli 里 lpush 到 Redis数据库里，RedisSpider 将在数据库里获取start_urls。

**执行方式：**
通过runspider方法执行爬虫的py文件（也可以分次执行多条），爬虫（们）将处于等待准备状态：

`scrapy crawl dangdang`
在Master端的redis-cli输入push指令，参考格式：

`$redis > lpush dangdang http://book.dangdang.com/`
Slaver端爬虫获取到请求，开始爬取。

### 三、mycrawler_redis (class MyCrawler(RedisCrawlSpider))

这个RedisCrawlSpider类爬虫继承了RedisCrawlSpider，能够支持分布式的抓取。因为采用的是crawlSpider，所以需要遵守Rule规则，以及callback不能写parse()方法。

同样也不再有start_urls了，取而代之的是redis_key，scrapy-redis将key从Redis里pop出来，成为请求的url地址。

**注意：**
同样的，RedisCrawlSpider类不需要写allowd_domains和start_urls：

scrapy-redis将从在构造方法__init__()里动态定义爬虫爬取域范围，也可以选择直接写allowd_domains。

必须指定redis_key，即启动爬虫的命令，参考格式：redis_key = 'myspider:start_urls'

根据指定的格式，start_urls将在 Master端的 redis-cli 里 lpush 到 Redis数据库里，RedisSpider 将在数据库里获取start_urls。

**执行方式：**
通过runspider方法执行爬虫的py文件（也可以分次执行多条），爬虫（们）将处于等待准备状态：

`scrapy crawl amazon`
在Master端的redis-cli输入push指令，参考格式：

`$redis > lpush amazon https://www.amazon.cn/%E5%9B%BE%E4%B9%A6/b?ie=UTF8&node=658390051`
爬虫获取url，开始执行。

# Crontab爬虫定时执行

- 安装:`apt-get install cron`(服务器环境默认有安装)
- 使用:
  - 使用`crontab -e `进入编辑界面
  - 使用`crontab -l`查看当前的定时crontab任务
- 编辑:
  - 分		小时		日		月		星期		命令
  - 0-59    0-23      1-31    1-12      0-7       command
  - 30         7            8          *            *            ls             每月8号的7:30执行一次命令(ls)
  - */15      *          *           *            *             ls             每15分钟执行一次命令(ls)
  - 0          */2          *          *           *             ls             每隔2个小时执行一次命令(ls)
- 注意点
  - 星期中的 0 表示周日
  - 每隔两个小时的时候 分 的位置不能为*，如果\*表示分钟都会执行

## Crontab + Scrapy_Redis使用

- 1.先把python的执行命令写入.sh脚本
- 2.把.sh脚本添加可执行权限
- 3.把.sh程序写入crontab配置文件中

### 编写shell脚本

spider.sh

```shell
#!/bin/sh
cd `dirname $0` || exit 1
/usr/bin/scrapy crawl amazon >> run.log 2>&1
```

### 赋予权限

`chmod +x spider.sh`

### crontab配置文件

```* * * * * /home/laisent/desktop/spider/spider.sh >> /home/laisent/desktop/spider/run_cro.log 2>&1```

**注意：**

​	2>&1: linux中 0:标准输入  1:标准输出  2:标准错误输出

​	重定向只有把标准输出重定向，这里把屏幕输出的内容重定向到文件，同时吧标准错误一起输出到文件

