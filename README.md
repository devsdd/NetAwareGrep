# NetAwareGrep

NetAwareGrep is a program designed to make it easy to search for IP's and subnets in logfiles. While the UNIX command grep offers a million different and powerful ways to search for text in a file, this is a more specialized use-case. NetAwareGrep is able to intelligently identify strings passed as command-line arguments as IPv4 addresses with or without CIDR formatting. The typical use case is to find all requests coming to your server from a particular **network** instead of a particular IP. You can use traditional grep to do it, but that will only allow you to search for IP's from the same /24 or /16 or /8 networks by omitting certain octets from your search string. If you want to search for IP's from a /23, for example, you would be hard-pressed to get grep to do that for you out of the box. Hence, this program.

The path to the log file is defined in a separate config file called **settings.yaml**.

### Invocation

```
$ python weblogHelper.py
usage: weblogHelper.py [-h] --ip IP
weblogHelper.py: error: argument --ip is required
```

```
$ python weblogHelper.py --ip 180.76.15.137 
180.76.15.137 - - [02/Jun/2015:17:05:28 -0700] "GET /logs/access_140730.log HTTP/1.1" 200 7849856 "-" "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)" "www.redlug.com"
180.76.15.137 - - [02/Jun/2015:20:05:23 -0700] "GET /Publications/ HTTP/1.1" 200 645 "-" "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)" "www.redlug.com"
180.76.15.137 - - [02/Jun/2015:21:46:59 -0700] "GET /paper2004/?C=S;O=A HTTP/1.1" 200 1847 "-" "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)" "www.redlug.com"
```

As you can imagine, a web-scale crawler won't just hit your site from one IP, so you can specify various subnets as follows:
```
$ python weblogHelper.py --ip 180.76.15.137/24
180.76.15.135 - - [02/Jun/2015:17:05:23 -0700] "GET /logs/access_140730.log HTTP/1.1" 200 979626 "-" "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)" "www.redlug.com"
180.76.15.137 - - [02/Jun/2015:17:05:28 -0700] "GET /logs/access_140730.log HTTP/1.1" 200 7849856 "-" "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)" "www.redlug.com"
180.76.15.17 - - [02/Jun/2015:17:20:23 -0700] "GET /logs/access_141026.log HTTP/1.1" 200 45768 "-" "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)" "www.redlug.com"
...
```

```
$ python weblogHelper.py --ip 180.76.15.137/23
180.76.15.135 - - [02/Jun/2015:17:05:23 -0700] "GET /logs/access_140730.log HTTP/1.1" 200 979626 "-" "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)" "www.redlug.com"
180.76.15.137 - - [02/Jun/2015:17:05:28 -0700] "GET /logs/access_140730.log HTTP/1.1" 200 7849856 "-" "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)" "www.redlug.com"
180.76.15.17 - - [02/Jun/2015:17:20:23 -0700] "GET /logs/access_141026.log HTTP/1.1" 200 45768 "-" "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)" "www.redlug.com"
180.76.15.20 - - [02/Jun/2015:17:23:05 -0700] "GET /logs/access_140817.log HTTP/1.1" 200 54711 "-" "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)" "redlug.com"
```

## Testing The Code

This repository includes a full test-suite written using **pytest**. The code is defined in [test_weblog_helper.py](https://github.com/devsdd/NetAwareGrep/blob/master/test_weblog_helper.py) and [conftest.py](https://github.com/devsdd/NetAwareGrep/blob/master/conftest.py).

### Testsuite Invocation

On the terminal, run
```
$ py.test --ip 180.76.15.137/24
========================================================= test session starts =========================================================
platform linux2 -- Python 2.7.12, pytest-2.8.7, py-1.4.31, pluggy-0.3.1
rootdir: </path/to/code/dir/testdir>, inifile: 
collected 10 items 

====================================================== 10 passed in 0.06 seconds ======================================================```

