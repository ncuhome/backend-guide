# 项目及代码部署规范

工作室的每个项目，都应当能够不断延续和传承下去，老人离开了，项目就由新人接手。  
这份规范目的在于，通过完善的文档和手册，让新人能够轻松的接手整个项目，而不是花费大量时间去踩不必要的坑。

本规范适用于当前的技术环境，随着我们用到的技术的改进，本规范也将随之变化。


## 项目规范

### 前后端分离

采用前后端分离的目的在于前端后端分工明确，减少耦合，提高工作效率，并且能适应移动端的需求。

所有长期维护的项目都采用前后端分离的架构，后端只提供API，前端/移动端负责页面和交互。  

后端必须提供尽可能详细准确的API文档，可通过网页或Markdown的形式提供给其他成员。  

### 运维手册

每个项目都要有一份完善的README文件，里面详述代码如何上线，如何管理数据库，故障处理等内容，避免操作失误导致长时间宕机。

**关键部分:**

- 目录结构    
  描述项目各个目录的内容
 
- 如何测试    
  描述如何测试
 
- 如何部署    
  描述如何部署上线，如何管理数据库
  
- 故障处理    
  故障的处理办法


## 部署规范

所有项目使用 Docker 和 Docker compose 进行部署。

- [Docker —— 从入门到实践](https://yeasy.gitbooks.io/docker_practice/content/)
- [Python 开发者的 Docker 之旅](http://docs.daocloud.io/python-docker)
- [Docker-Compose](https://docs.docker.com/compose/overview/)

### 构建镜像

使用 Dockerfile 和 .dockerignore 定义镜像，Dockerfile 用 alpine 或 debian 作为基础镜像。

### 每个容器一个程序

将应用解耦合到不同的容器中，每个进程一个容器。即应用，数据库，Nginx反向代理等等都放在不同的容器中。

处理相互依赖的容器时，使用 docker-compose 的[Networking in Compose](https://docs.docker.com/compose/networking/)，而不是将它们直接放在同一个Docker容器里。

### 容器和数据分离

Docker容器可以随时关闭，销毁，重启，而应用程序中的数据（数据库，日志等等）需要永久保存。VOLUME 通常用作数据卷（类似于共享文件夹，实际数据储存在主机上），在容器启动的时候挂载，用于在主机和容器间共享数据。

### 部署

使用 docker-compose.yml 定义容器的依赖关系，以及开放的端口，使用的数据卷。
用 docker-compose 可以一个命令启动所有需要的容器，即一键部署。

容器中文件大致结构：

    /data
      error.log
      ...
    /code
      .git
      Dockerfile
      docker-compose.yml
      ...

data 目录中是数据，映射到主机的一个目录，code 目录中是代码。
