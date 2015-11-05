# my_scrapy
https://github.com/uileyar/my_scrapy.git

scrapy crawl domz
scrapy shell "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/"
scrapy crawl domz -o items.json

有用的xpath路径表达式：
表达式	    描述
nodename	选取此节点的所有子节点。
/	        从根节点选取。
//	        从匹配选择的当前节点选择文档中的节点，而不考虑它们的位置。
.	        选取当前节点。
..	        选取当前节点的父节点。
@	        选取属性。
