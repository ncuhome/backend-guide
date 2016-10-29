# Python编码风格规范

## 编码风格

编码风格统一遵守PEP8规范，可参考[<译> PEP8-Python 编码风格指南](http://drafts.damnever.com/2015/EPE8-style-guide-for-python-code.html)。

**提示:**

- 使用 [flake8](https://pypi.python.org/pypi/flake8) 进行编码风格检查
- 使用 [autopep8](https://github.com/hhatto/autopep8) 自动格式化代码
- 未遵守PEP8会出现的错误码: [PEP8 Error codes](http://pep8.readthedocs.io/en/release-1.7.x/intro.html#error-codes)
- 大部分编辑器都有以上两个工具的插件，请自行配置

## 注释规范

PEP8未规定文档字符串中内容，业界有三种规范:

- [Google](https://google.github.io/styleguide/pyguide.html#Comments)
- [Sphinx](http://www.sphinx-doc.org/en/stable/ext/autodoc.html)
- [NumPy](https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt)

Google规范可读性较好，注释清晰易懂，也方便编写，工作室统一遵守Google规范。   

示例:

```python
def my_func(arg1, arg2):
    """
    一句话功能介绍

    较详细介绍

    Args:
        arg1 (int): 参数1的说明，可以用括号注明类型
        arg2: 参数2的说明

    Returns:
        返回值说明，字典类型可提供示例。
        
        Example:
            
            {
                "key": "字段说明",
            }

    Raises:
        IOError: 异常说明
    """
    pass
    
class SampleClass(object):
    """
    一句话介绍

    较详细介绍

    Attributes:
        attr1: 属性介绍
        attr2 (str): 属性介绍，可以用括号注明类型
    """

    def __init__(self, likes_spam=False):
        self.likes_spam = likes_spam
        self.eggs = 0

    def public_method(self):
        """一句话介绍，如果有参数和返回值，注释格式和函数一样"""
```

**注意:**

- 公共的函数和类必须要有完整的注释。  
- 注释使用中文，不要使用蹩脚的英文。
