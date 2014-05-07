ganji-num-ocr
=============

赶集网用户联系方式的识别

##识别思路：
其实没有使用OCR技术，因为在做图片分割的时候个人不是很熟练，尝试使用了tesseract-ocr，但是识别准确率只有50%。 

受到了@yangming 的指导和启发，采用template-matching的方式来解决了这个问题。

##程序环境依赖：
* python2.6+

##程序包依赖：
* numpy  
* PIL

##使用

* 将numtemplate文件夹以及nummatch.py文件加入项目中。
* 调用convert_to_string方法。