# 同构JSON-Schema

> “程序写出来是给人看的，附带能在机器上运行。”
> <div style="text-align:right">《计算机程序的结构与解释》的卷首语</div>

## 同构JSON-Schema与JSON-Schema比较

### JSON-Schema

[JSON-Schema](http://json-schema.org)是一个互联网标准草案，用于描述JSON数据。
JSON Schema was an Internet Draft, most recently version 4, which expired on August 4, 2013.

但是它有一个很大的缺点：复杂。

先来看官网上的例子：http://json-schema.org/example1.html

这个是实际数据：

    {
        "id": 1,
        "name": "A green door",
        "price": 12.50,
        "tags": ["home", "green"]
    }

这个是对应的Schema:

    {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "title": "Product",
        "description": "A product from Acme's catalog",
        "type": "object",
        "properties": {
            "id": {
                "description": "The unique identifier for a product",
                "type": "integer"
            },
            "name": {
                "description": "Name of the product",
                "type": "string"
            },
            "price": {
                "type": "number",
                "minimum": 0,
                "exclusiveMinimum": true
            },
            "tags": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "minItems": 1,
                "uniqueItems": true
            }
        },
        "required": ["id", "name", "price"]
    }

可以看到Schema比实际数据复杂的多，而且Schema的结构和实际数据的结构并不完全相同。
在描述嵌套的JSON数据时，JSON-Schema会更复杂，编写和阅读很困难。

**所以，用JSON-Schema来描述API接口并不合适。**

### 同构JSON-Schema的语法

在去年大概10月份，我开始做一个功能和JSON-Schema类似的，用来描述JSON数据的语法和校验JSON数据的工具，这种语法最大的特点就是Schema与实际JSON数据的结构完全相同，并且语法尽可能简洁。


下面推导出这种语法：

[JSON](http://json.org/json-zh.html)有3种结构：对象，数组，值。

需要用一种通用的方式同时描述3种结构，这种方式只有**函数**，但大多数情况下不需要完整定义
一个函数，因为这些函数都是类似的，只要用一个更高阶的函数生成校验函数。

	# 高阶函数
	def generate_validater(*args, **kwargs):
		def validater(value):
			# raise Exception if value not valid
			return value
		return validater
	
	# 整数校验函数伪代码
	def int_validater(min, max, optional=False):
		def validater(value):
			if value is None:
				if optional:
					return value
				else:
					raise Invalid
			else:
				if value<min:
					raise Invalid
				elif value>max:
					raise Invalid
				else:
					return value
		return validater

那么如何在JSON里面调用高阶函数？用一个字符串表示：

	"validater(arg1,arg2)&key1&key2=value"

这种格式类似于URL里面的QueryString，可以取名为ValidaterString，其中：

- arg1, arg2...value都是有效JSON值，即true/false是小写的，空值为null，字符串要加双引号。
- 如果validater是dict或list，可以省略，因为可以从JSON结构看出是dict还是list。
- 如果arg1, arg2...都是默认值，则括号可以省略。
- 如果key对应的value为true，只需写&key，不需要写&key=true。

因为Schema和JSON数据是同构的，所以这3种结构都需要是自己描述自身，即：

对象用特殊的key描述自身，其余key描述对象里的内容：

	{
		"$self": "ValidaterString",
		"key": "value"
	}

数组用第一个元素描述自身，第二个元素描述数组里的内容：

	["ValidaterString", Item]

值用字符串描述自身：

	"ValidaterString"


下面来用一下新语法

还是刚才那个实际数据：

    {
        "id": 1,
        "name": "A green door",
        "price": 12.50,
        "tags": ["home", "green"]
    }

同构的JSON-Schema：

    {
    	"$self":"&desc=\"A product from Acme's catalog\""
        "id": "int&desc=\"The unique identifier for a product\"",
        "name": "str&desc=\"Name of the product\"",
        "price": "float&min=0&emin&desc=\"价格\"",
        "tags": ["&minlen=1&unique", "str&desc=\"标签\""]
    }

可以看到比原来的简洁了不少，主要不足是&desc的值是字符串且比较长，再次改进一下。

在JSON对象结构中，可以在上层描述下一层，即前置描述：

	{
		"$self": "A product from Acme's catalog",
        "id？int": "The unique identifier for a product",
        "name?str": "Name of the product",
        "price?float&min=0&emin": "价格",
        "tags?&minlen=1&unique": ["str&desc=\"标签\""]
    }

这里用？分隔key和ValidaterString，另外tags里面只需要一个元素了。
可以看到简洁多了，并且因为是同构的，从Scheme可以直接看出实际数据的结构。


**引用**

不同的Schema可能含有相同的部分，假设有一个公共的Schema，其他Schema需要包含或继承它，
并添加或覆盖公共Schema中的部分结构，可以使用引用语法。

    # override: 覆盖，addition：添加
    # 自描述
    {
        "key": "@shared(override_arg1, arg2)&override_k=v",
        "addition_key": ...
    }
    # 前置描述
    {
        "key@shared(override_arg1, arg2)&override_k=v": "override_desc",
        "addition_key?...": ...
    }


## 内置的校验函数
    
    # 所有布尔型默认值都是false
    list(minlen=0, maxlen=1024*1024, unique=false, default=null, optional=false)

    dict(optional=false)

    bool(default=null, optional=false)

    int(min=-math.inf, max=math.inf, default=null, optional=false)

    # emin:是否不包括最小值, emax:是否不包括最大值
    float(min=-math.inf, max=math.inf, emin=false, emax=false, default=null, optional=false)

    # 时间格式为ISO8601，与JSON标准一致
    date(format="%Y-%m-%d", default=null, optional=false)
    datetime(format="%Y-%m-%dT%H:%M:%S.%fZ", default=null, optional=false)

    str(minlen=0, maxlen=1024*1024, escape=false, default=null, optional=false)

    email(default=null, optional=false)
    phone(default=null, optional=false)
    ipv4(default=null, optional=false)
    idcard(default=null, optional=false)
    url(default=null, optional=false)
    password(minlen=6, maxlen=16, default=null, optional=false)


## 例子

	新US的API: us-api.json

## 其他

[Validater](https://github.com/guyskk/validater)经过几次较大的改变，语法基本达到目标。
以上语法是今年暑假打算实现的。

validater是拼写错误，英文词典里没这个单词，正确的拼写是validator。
然而validator这个名字已经被用掉了，所以还是继续用这个拼写错误的单词吧。

在实现validater的过程中，我发现这种Schema可以用来将任意对象转换成JSON格式，
标准库里的json只能处理Python内置的几个类型，要序列化自定义的类型需要自己写转换函数。

这种Schema可以简化API的编写：

- 先写接口，后写实现。Schema即文档
- 可以用来自动处理请求参数，提高安全性
- 可以用来序列化任意类型的对象


