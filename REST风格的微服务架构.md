# REST风格的微服务架构

1. URL和参数标准化
2. 元数据和文档
3. 权限标准化
4. 部署标准化
5. 服务管理中心


## URL和参数标准化

Resource是资源的概念，描述的是一类事物，用URL表述类似于`/user`。
用于描述具体事物的信息，附加在QueryString中，类似于`/user?name=jack`。

Resource是最小的功能集合，一个完整的服务就是多个Resource的组合，
即：微服务 = N × Resource。

Action描述的是对一类资源的操作，通常是GET, POST, PUT, DELETE...这几个，
为了描述更复杂的操作，将Action限定为小写HTTP方法开头，下划线作为分隔符，
再加上任意的字符串，例如 `get_me`, `post_login`。
转换过程也很直观，首先将HTTP方法取出，剩下部分作为URL。
以 `user.get_me` 为例，转换成URL为`GET /user/me`。

把接口抽象为Resource和Action，即可形成格式统一的URL。

请求参数来源取决于HTTP方法，GET和DELETE请求，取自url参数，
POST和PUT请求，取自请求体，Content-Type为 `application/json`。


## 元数据和文档

动态语言的强大之处很大程度是因为元数据，元编程/反射/自省都是利用了元数据。
在Web接口中，元数据就是一份描述这个接口的文档。元数据本身也是一类资源，能够动态获取，并且能够随代码更新而更新。

假设一个博客系统有3个Resource：`/user`, `/article`, `/comment`，这样可以通过`GET /`获取元数据。
这些资源也可以挂载到其他路径下，例如：`/api/user`, `/api/article`, `/api/comment`, 这样则通过`GET /api`获取元数据。规定Resource路径的共同前缀为url_prefix，通过 `GET url_prefix` 获取元数据。

元数据的具体格式：

    {
        "$desc": "简介",
        "$url_prefix": "Resource路径的共同前缀",
        "$roles": {
            "Role": {
                "Resource": ["Action", ...],
                ...
            },
            ...
        },
        "$validaters": {
            "Validater":{
                "$desc":"简介",
                "Param":"参数说明",
                ...
            },
            ...
        }
        "$shared": {
            "name": "Schema",
            ...
        },
        "Resource":{
            "Action":{
                "$desc":"简介",
                "$input":"输入Schema",
                "$output":"输出Schema"
            },
            ...
        },
        ...
    }


## 权限标准化

开放授权有两种形式：

1. 对用户透明

    资源拥有者：服务提供商
    授权方式：SecertKey

    实例：
    服务提供商：七牛云
    第三方：Ncuhome
    用户：南昌大学学生


2. 需要用户点击授权

    资源拥有者：用户
    授权方式：OAuth2.0

    实例：
    服务提供商：QQ
    第三方：游戏服务器
    用户：游戏玩家


不管是哪种形式，都需要服务提供商保存第三方的权限信息。
有多少个角色，每个角色能访问哪些API这样的信息在开发程序时就确定了，这些信息属于元数据。 第三方的数量会增长，并且需要能随时修改授权信息，这些是业务数据，保存在数据库里面。

角色元数据的具体格式：

    {
        "Role": {
            "Resource": ["Action", ...],
            ...
        },
        ...
    }


## 部署标准化

Docker 和 Docker-compose

[Docker —— 从入门到实践](https://yeasy.gitbooks.io/docker_practice/content/)
[Python 开发者的 Docker 之旅](http://docs.daocloud.io/python-docker)

### 构建镜像

使用 Dockerfile 和 .dockerignore 定义镜像。Dockerfile 用 alpine 或 debian 作为基础镜像。
Docker 在构建过程中会把同目录中的所有 .dockerignore 和 Dockerfile 以外的文件打包发给镜像， 在文件过多时这会很耗时间。

### 每个容器一个程序

将应用解耦合到不同的容器中，每个进程一个容器。即应用，数据库，Nginx反向代理等等都放在不同的容器中。
处理相互依赖的容器时，使用容器的关联特性，而不是将它们直接放在同一个Docker容器里。

### 容器和数据分离

Docker容器可以随时关闭，销毁，重启，而应用程序中的数据（数据库，日志等等）需要永久保存。VOLUME 通常用作数据卷（类似于共享文件夹，实际数据储存在主机上），在容器启动的时候挂载，用于在主机和容器间共享数据。


### 部署

使用 docker-compose.yml 定义容器的依赖关系，以及开放的端口，使用的数据卷。
用 docker-compose 可以一个命令启动所有需要的容器，即一键部署。


## 服务管理中心

1. 集中管理所有的服务，启动/重启/查看日志
2. 服务状态/访问量实时监控
3. 用于管理开放API，授权/配额等等
