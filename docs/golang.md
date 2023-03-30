# Golang 代码规范 v1.0

***家园工作室研发组提醒宁 :***  
**代码千万行** **注释第一行**  
**命名不规范** **学弟两行泪**

---  


## 1.写在前面




代码是给系统运行的，但代码更是给人用的，写下一行可能只要1分钟，但未来会被一代代工程师读很多次、改很多次。代码的可读性与可维护性，是我心目中的代码第一标准。
系统恒久远，代码永流传！ —— 鲁肃-蚂蚁金服CTO

**不管团队有多少人，代码风格都应该师出同门**



本文档参考了 [Google Golang 代码规范](https://github.com/golang/go/wiki/CodeReviewComments) 并进行了一些调整
更多可参考 [Uber go 规范](https://github.com/xxjwxc/uber_go_guide_cn) 

## 2.整体风格

### 2.1 格式化
- 代码都必须使用 `gofmt` 进行格式化后推送到仓库

### 2.2 换行
- 一行代码不要超过 `120列` Goland 有参照线竖线
- 特殊情况可不考虑:
    - tag
    - 工具生成的模板代码, 比如 `protoc`
    - import 其他模块的包名

### 2.3 括号与空格
- 参照 `gofmt`

### 2.4 import 规范
- `goimports` 会自动把依赖包按首字母排序，并对包进行分组管理，通过空行隔开，默认分为本地包（标准库、内部包）、第三方包
- `main` 包之外的包不推荐引入匿名包，如需引入，需要注释包的用途
- 不推荐相对路径引入包
    ```go
    // bad
    import (
        "../package"
    )

    // good
    import (
        "github.com/hello/world"
    )
    ```

### 2.5 错误处理
- `error` 作为函数的值返回，必须对 `error` 进行处理, 或将返回值赋值给明确忽略。
- 例外
    - `defer xx.Close()` 可以不进行处理
- `error` 作为参数返回时 必须是最后一个参数

- 不行该采用选择分支处理， 应选择短路逻辑
    ```go
    // bad
    if err != nil {
        // error handling
    } else {
        // normal code
    }

    // good
    if err != nil {
        // error handling
        return // or continue, etc.
    }
    // normal code
    ```

- Golang 1.13以上， 使用 `fmt.ErrorF("xxx error: %w", err)` 生成 error

### 2.6 panic 处理
- **🈲业务逻辑禁止使用 `panic`**
- 在 `main` 包中出现无法拯救的情况允许使用 `panic`,  比如数据库无法连接导致服务完全不可用

- 建议在 `main` 包中使用 `log.Fatal` 来记录错误，这样就可以由 `log` 来结束程序，或者将 `panic` 抛出的异常记录到日志文件中，方便排查问题。

- `panic` 捕获只能到 `goroutine` 最顶层，每个自行启动的 `goroutine`，必须在入口处捕获 `panic`，并打印详细堆栈信息或进行其它处理

- 对于其它的包，可导出的接口一定不能有 `panic`；在包内传递错误时，不推荐使用 `panic` 来传递 `error`

    ```go
    // 不推荐为传递error而在包内使用panic,以下为示例

    // PError 包内定义的错误类型
    type PError string

    // Error error接口方法
    func (e PError) Error() string {
        return string(e)
    }

    func do(str string) {
        // ...
        // 此处的panic用于传递error
        panic(PError("错误信息"))
        // ...
    }

    // Do 包级访问入口
    func Do(str string) (err error) {
        defer func() {
            if e := recover(); e != nil {
                err = e.(PError)
            }
        }()
        do(str)
        return nil
    }
    ```

### 2.7 单元测试
- **提交的代码必须有单元测试并将测试代码一并提交到仓库**

- 单元测试文件名命名规范为 `example_test.go`
- 测试用例的函数名称必须以 `Test` 开头，例如 `TestExample` 
- 如果存在 `func Foo`，单测函数可以带下划线，为 `func Test_Foo`。如果存在 `func (b *Bar) Foo`，单测函数可以为 `func TestBar_Foo`。下划线不能出现在前面描述情况以外的位置。
- 单测文件行数限制是普通文件的2倍，即`1600行`。单测函数行数限制也是普通函数的2倍，即为`160行`。圈复杂度、列数限制、 import 分组等其他规范细节和普通文件保持一致
- 单元测试覆盖率要求主要逻辑代码要覆盖到，对于 `if err != nil` 可以相应减少覆盖
- Tips: 使用goland 生成测试demo准没有问题

### 2.8 断言处理

- interface 转具体类型要采用 `comma ok` 的方式
    ```go
    //bad
    t := i.(string)

    //good
    t, ok := i.(string)
    if !ok {
        //处理错误
    }
    //正常逻辑
    ```

## 3.注释

### 3.1 包注释
- 每个包都需要有包注释
- 包如果有多个 go 文件，只需要出现在一个 go 文件中（一般是和包同名的文件）即可

    ```go
    // Package ncuhome is ncuhome niubility
    package ncuhome

    // blablabla
    ```

### 3.2 结构体注释
- 每个需要导出的自定义结构体或者接口都必须有注释说明

- 结构体内的可导出成员变量名，如果是个生僻词，或者意义不明确的词，就必须要给出注释，放在成员变量的前一行或同一行的末尾

    ```go
    // User 用户结构定义了用户基础信息
    type User struct {
        Name  string
        Email string
        // Demographic 族群
        Demographic string
    }
    ```
### 3.3 方法注释
- 每个需要导出的函数或者方法（结构体或者接口下的函数称为方法）都必须有注释
- 不可导出函数 如果命名不能很好表达用途也应该有注释
- 注释描述函数或方法功能、调用方等信息

    ```go
    // NcuhomeDoSomeThing 函数是用来告诉大家家园是干什么的
    func NcuhomeDoSomeThing(ctx *common.Context) error {
        // TODO
    }
   ```

### 3.4 常量注释
- 每个需要导出的常量和变量都必须有注释说明
- 该注释对常量或变量进行简要介绍，放在常量或者变量定义的前一行
    ```go
    // NcuhomeMaxPeople 家园最大人数
    const NcuhomeMaxPeople = "50"

    // 家园各个时期的最大人数
    const (
        // 家园2018年的最大人数
        NcuhomeMaxPeople2018 = "50" 
        // 家园2019年的最大人数
        NcuhomeMaxPeople2019 = "50" 
        // 家园2020年的最大人数
        NcuhomeMaxPeople2020 = "50" 
    )

    // FullName 返回指定用户名的完整名称
    var FullName = func(username string) string {
        return fmt.Sprintf("fake-%s", username)
    }
    ```
### 3.5自定义类型注释
- 每个需要导出的类型定义（type definition）和类型别名（type aliases）都必须有注释说明

    ```go
    // StorageClass 存储类型
    type StorageClass string

    // FakeTime 标准库时间的类型别名
    type FakeTime = time.Time
    ```

## 4.命名规范

### 4.1 变量命名
- 遵循驼峰命名，首字母大小写决定访问控制
- 特有名词遵循规则
    - 如果变量为私有，且特有名词为首个单词，则使用小写，如 `apiClient`
    - 其他情况都应该使用该名词原有的写法，如 `APIClient`、`repoID`、`UserID`
    - 专有名词列表参考[这里](https://github.com/golang/lint/blob/738671d3881b9731cc63024d5d88cf28db875626/lint.go#L770)
- 若变量类型为 `bool` 类型，则名称应以 `Has`，`Is`，`Can` 或者 `Allow` 开头
- 代码生成工具自动生成的代码可排除此规则（如 xxx.pb.go 里面的 Id）

### 4.2 常量命名

- 常量均需遵循驼峰式。
    ```go
    // AppVersion 应用程序版本号定义
    const AppVersion = "1.0.0"
    ```
- 私有全局常量和局部变量规范一致，均以小写字母开头。
    ```go
    const appVersion = "1.0.0"
    ```

### 4.3 函数命名
- 函数名必须遵循驼峰式，首字母根据访问控制决定使用大写或小写。
- 代码生成工具自动生成的代码可排除此规则（如协议生成文件 xxx.pb.go , gotests 自动生成文件 xxx_test.go 里面的下划线）
- 函数名能保证基本表达了函数的用途，🈲抽象

### 4.4 结构体命名
- 采用驼峰命名方式，首字母根据访问控制采用大写或者小写
- 结构体名应该是名词或名词短语，如 `Customer`、`WikiPage`、`Account`、`AddressParser`，它不应是动词
- 结构体的声明和初始化格式采用多行，例如：
    ```go
    // User 多行声明
    type User struct {
        Name  string
        Email string
    }

    // 多行初始化
    u := User{
        UserName: "john",
        Email:    "john@example.com",
    }
    ```

### 4.5 接口命名
- 命名规则基本保持和结构体命名规则一致。

- 单个函数的接口名以 `er` 作为后缀，例如 `Reader`，`Writer`。
    ```go
    // Reader 字节数组读取接口
    type Reader interface {
        // Read 读取整个给定的字节数据并返回读取的长度
        Read(p []byte) (n int, err error)
    }
    ```

- 两个函数的接口名综合两个函数名。

- 三个以上函数的接口名，类似于结构体名。
    ```go
    // Car 小汽车结构申明
    type Car interface {
        // Start ...
        Start([]byte)
        // Stop ...
        Stop() error
        // Recover ...
        Recover()
    }
    ```

## 5.控制结构

### 5.1 if
- `if` 接受 局部变量初始化
```go
if err := file.Chmod(0664); err != nil {
    return err
}
```
- `if` 对两个值进行判断时，变量在左，常量在右：
    ```go
    // bad
    if nil != err {
        // error handling
    }

    // bad
    if 0 == errorCode {
        // do something
    }

    // good
    if err != nil {
        // error handling
    }   

    // good
    if errorCode == 0 {
        // do something
    }
    ```

- 对于 `bool` 值的判断
    ```go
    var allowUserLogin bool
    // bad
    if allowUserLogin == true {
        // do something
    }

    // bad
    if allowUserLogin == false {
        // do something
    }

    // good
    if allowUserLogin {
        // do something
    }

    // good
    if !allowUserLogin {
        // do something
    }
    ```
### 5.2 for
- 采用短变量
    ```go
    sum := 0
    for i := 0; i < 10; i++ {
        sum += 1
    }
    ```

### 5.3 range

- 如果只需要第一项（key），就丢弃第二个：
    ```go
    for key := range m {
        if key.expired() {
            delete(m, key)
        }
    }
    ```

- 如果只需要第二项，则把第一项置为下划线：
    ```go
    sum := 0
    for _, value := range array {
        sum += value
    }
    ```
### 5.4 switch
- 必须有 `default`

### 5.5 goto
- 🈲 禁止使用业务代码使用 `goto`
- 开发框架当我没说

## 6.其他

### 6.1 函数接收器
- 推荐以类名第一个英文首字母的小写作为接收器的命名
- 接收器的命名在函数超过`20行`的时候不要用单字符
- 命名不能采用 `me`，`this`，`self` 这类易混淆名称
### 6.2 代码长度
- 单文件长度不能超过`800行` 否则考虑拆分
- 单函数长度不能超过`80行` 否则考虑拆分

### 6.3 代码嵌套
- 嵌套深度不能超过`4层`：
    ```go
    // AddArea 添加成功或出错
    func (s *BookingService) AddArea(areas ...string) error {
        s.Lock()
        defer s.Unlock()
        
        for _, area := range areas {
            for _, has := range s.areas {
                if area == has {
                    return srverr.ErrAreaConflict
                }
            }
            s.areas = append(s.areas, area)
            s.areaOrders[area] = new(order.AreaOrder)
        }
        return nil
    }
    ```

    ```go
    // 建议调整为这样：

    // AddArea 添加成功或出错
    func (s *BookingService) AddArea(areas ...string) error {
        s.Lock()
        defer s.Unlock()
        
        for _, area := range areas {
            if s.HasArea(area) {
                return srverr.ErrAreaConflict
            }
            s.areas = append(s.areas, area)
            s.areaOrders[area] = new(order.AreaOrder)
        }
        return nil
    }

    // HasArea ...
    func (s *BookingService) HasArea(area string) bool {
        for _, has := range s.areas {
            if area == has {
                return true
            }
        }
        return false
    }
    ```
## 7.依赖

### 7.1 go modules
- 开发使用golang1.13以上版本
- 使用 `go modules` 作为依赖管理, `go.sum` 文件必须提交


## 8.参考
- https://github.com/golang/go/wiki/CodeReviewComment
- https://github.com/xxjwxc/uber_go_guide_cn
