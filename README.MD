# MySQL Wrapper Project - New SQL (NSQL)

A lightweight, thread-safe Python wrapper for PyMySQL with enhanced features.

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![MySQL](https://img.shields.io/badge/MySQL-5.7+-orange.svg)
![PyMySQL](https://img.shields.io/badge/PyMySQL-1.0+-green.svg)

## Table of Contents
- [Advantages](#advantages)
- [Technical Principles](#technical-principles)
- [Features](#features)
- [API Reference](#api-reference)
- [Usage Examples](#usage-examples)
- [Limitations](#limitations)
- [Comparison](#comparison-with-other-projects)

## Advantages

### Compared to Other MySQL Wrappers
✔ **Thread Safety** - Built-in threading lock mechanism  
✔ **SQL Injection Protection** - Strict identifier validation  
✔ **Automatic Type Conversion** - Smart result type handling  
✔ **Flexible Parameter Binding** - Supports both tuple and dict parameters  
✔ **Connection Resilience** - Automatic reconnection handling  
✔ **Debug Mode** - Detailed SQL logging for development  

## Technical Principles

### Transaction Handling
- Uses PyMySQL's native transaction support
- Automatic `COMMIT` after each successful operation
- Manual transaction control available through raw connection

### Connection Pool
- Not a traditional connection pool
- Single persistent connection with thread locking
- Lightweight alternative for moderate workloads
- Suitable for long-running applications

## Features

### Core Features
- Parameterized query building
- Automatic FROM clause completion
- JSON data type support
- Binary data handling utilities
- Debug mode with SQL logging
- Dictionary-style result formatting

### Security Features
- SQL injection prevention
- Strict identifier validation
- Proper string escaping
- Parameter separation from queries

## API Reference

### Main Classes

#### `MySQL(host, port, charset="utf8", debug=False)`
Main wrapper class constructor.

#### `NewCursor(parent)`
Cursor class with enhanced methods.

### Core Methods

| Method | Description | Parameters |
|--------|-------------|------------|
| `use(db, Table=None)` | Switch database | `db`: database name |
| `select(_Table, FROM=None, WHERE=None, _limit=None)` | Basic SELECT | `_Table`: columns to select |
| `selectashead(_Table, FROM=None, WHERE=None, _limit=None)` | Dict-style results | Same as select |
| `insert(_Table, values=None, WHERE=None, **k)` | INSERT operation | Supports dict or kwargs |
| `update(WHERE, FROM=None, **k)` | UPDATE operation | WHERE clause required |
| `delete(FROM=None, WHERE=None)` | DELETE operation | |
| `istrue(FROM=None, WHERE=None)` | Existence check | Returns boolean |

### Helper Functions

| Function | Description | Example |
|----------|-------------|---------|
| `Func.NOW()` | Current timestamp | `Func.NOW()` |
| `Func.JSON_ARRAY()` | JSON array builder | `Func.JSON_ARRAY(1,2,3)` |
| `Func.insertbytes()` | Binary data handler | `Func.insertbytes(b'data')` |

## Usage Examples

### Basic Usage
```python
db = MySQL('localhost', 3306, debug=True)
db.__login__('user', 'password')
cursor = db.NewCursor()

# Select example
cursor.use('mydb', 'users')
results = cursor.select('*', WHERE=('age > %s', (18,)), _limit=10)

# Insert example
cursor.insert('users', {'name': 'John', 'age': 25})

# Transaction example
try:
    cursor.update(WHERE=('id=%s', (1,)), FROM='users', balance=100)
    cursor.update(WHERE=('id=%s', (2,)), FROM='users', balance=200)
except:
    cursor.conn.rollback()
```

### Advanced Features
```python
# Binary data insertion
cursor.insert('files', {
    'name': 'data.bin',
    'content': Func.insertbytes(b'\x00\x01\x02')
})

# JSON data handling
cursor.insert('config', {
    'settings': Func.JSON_ARRAY('item1', 'item2')
})

# Dictionary-style results
users = cursor.selectashead('*', FROM='users')
for user in users:
    print(user['name'], user['age'])
```

## Limitations

### Not Recommended For
❌ High-concurrency applications (consider connection pool)  
❌ Complex transaction scenarios  
❌ ORM-like object mapping  
❌ Asynchronous applications  

### Performance Considerations
- Single connection model may bottleneck under heavy load
- Not optimized for bulk operations
- Type conversion adds minor overhead

## Comparison with Other Projects

| Feature | This Wrapper | PyMySQL | SQLAlchemy | Django ORM |
|---------|-------------|---------|------------|------------|
| Thread Safety | ✔ | ✖ | ✔ | ✔ |
| Connection Pool | ✖ | ✖ | ✔ | ✔ |
| ORM Features | ✖ | ✖ | ✔ | ✔ |
| SQL Building | ✔ | ✖ | ✔ | ✔ |
| Binary Support | ✔ | ✔ | ✔ | ✔ |
| Debug Mode | ✔ | ✖ | Partial | Partial |

---

# MySQL 封装项目 - New SQL (NSQL)

一个轻量级、线程安全的 PyMySQL Python 封装器，具有增强功能。

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![MySQL](https://img.shields.io/badge/MySQL-5.7+-orange.svg)
![PyMySQL](https://img.shields.io/badge/PyMySQL-1.0+-green.svg)

## 目录
- [优势](#优势)
- [技术原理](#技术原理)
- [功能特性](#功能特性)
- [API参考](#api参考)
- [使用示例](#使用示例)
- [局限性](#局限性)
- [对比](#与其他项目的对比)

## 优势

### 与其他MySQL封装器的比较
✔ **线程安全** - 内置线程锁机制  
✔ **SQL注入防护** - 严格的标识符验证  
✔ **自动类型转换** - 智能结果类型处理  
✔ **灵活参数绑定** - 支持元组和字典参数  
✔ **连接弹性** - 自动重连处理  
✔ **调试模式** - 详细的SQL日志记录  

## 技术原理

### 事务处理
- 使用PyMySQL原生事务支持
- 每次成功操作后自动提交`COMMIT`
- 可通过原始连接手动控制事务

### 连接池
- 非传统连接池
- 带线程锁的单一持久连接
- 适用于中等工作负载的轻量级方案
- 适合长期运行的应用程序

## 功能特性

### 核心功能
- 参数化查询构建
- 自动FROM子句补全
- JSON数据类型支持
- 二进制数据处理工具
- 带SQL日志记录的调试模式
- 字典式结果格式化

### 安全特性
- SQL注入预防
- 严格标识符验证
- 正确的字符串转义
- 查询与参数分离

## API参考

### 主要类

#### `MySQL(host, port, charset="utf8", debug=False)`
主封装类构造函数

#### `NewCursor(parent)`
带增强方法的游标类

### 核心方法

| 方法 | 描述 | 参数 |
|------|------|------|
| `use(db, Table=None)` | 切换数据库 | `db`: 数据库名 |
| `select(_Table, FROM=None, WHERE=None, _limit=None)` | 基础SELECT | `_Table`: 选择列 |
| `selectashead(_Table, FROM=None, WHERE=None, _limit=None)` | 字典式结果 | 同select |
| `insert(_Table, values=None, WHERE=None, **k)` | INSERT操作 | 支持字典或关键字参数 |
| `update(WHERE, FROM=None, **k)` | UPDATE操作 | 必须包含WHERE子句 |
| `delete(FROM=None, WHERE=None)` | DELETE操作 | |
| `istrue(FROM=None, WHERE=None)` | 存在性检查 | 返回布尔值 |

### 辅助函数

| 函数 | 描述 | 示例 |
|------|------|------|
| `Func.NOW()` | 当前时间戳 | `Func.NOW()` |
| `Func.JSON_ARRAY()` | JSON数组构建器 | `Func.JSON_ARRAY(1,2,3)` |
| `Func.insertbytes()` | 二进制数据处理 | `Func.insertbytes(b'data')` |

## 使用示例

### 基础用法
```python
db = MySQL('localhost', 3306, debug=True)
db.__login__('user', 'password')
cursor = db.NewCursor()

# 查询示例
cursor.use('mydb', 'users')
results = cursor.select('*', WHERE=('age > %s', (18,)), _limit=10)

# 插入示例
cursor.insert('users', {'name': '张三', 'age': 25})

# 事务示例
try:
    cursor.update(WHERE=('id=%s', (1,)), FROM='users', balance=100)
    cursor.update(WHERE=('id=%s', (2,)), FROM='users', balance=200)
except:
    cursor.conn.rollback()
```

### 高级功能
```python
# 二进制数据插入
cursor.insert('files', {
    'name': 'data.bin',
    'content': Func.insertbytes(b'\x00\x01\x02')
})

# JSON数据处理
cursor.insert('config', {
    'settings': Func.JSON_ARRAY('item1', 'item2')
})

# 字典式结果
users = cursor.selectashead('*', FROM='users')
for user in users:
    print(user['name'], user['age'])
```

## 局限性

### 不推荐场景
❌ 高并发应用（考虑连接池方案）  
❌ 复杂事务场景  
❌ 类ORM的对象映射  
❌ 异步应用  

### 性能考量
- 单连接模型在重负载下可能成为瓶颈
- 未针对批量操作优化
- 类型转换会增加少量开销

## 与其他项目的对比

| 特性 | NSQL | PyMySQL | SQLAlchemy | Django ORM |
|------|---------|---------|------------|------------|
| 线程安全 | ✔ | ✖ | ✔ | ✔ |
| 连接池 | ✖ | ✖ | ✔ | ✔ |
| ORM功能 | ✖ | ✖ | ✔ | ✔ |
| SQL构建 | ✔ | ✖ | ✔ | ✔ |
| 二进制支持 | ✔ | ✔ | ✔ | ✔ |
| 调试模式 | ✔ | ✖ | 部分 | 部分 |