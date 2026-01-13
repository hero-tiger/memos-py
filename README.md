# 🚀 Memos Python Implementation

Memos 的 Python 实现版本 - 一个开源、自托管的隐私优先笔记服务 📝

## 📖 项目简介

这是 Memos 项目的 Python 实现，基于 FastAPI 框架构建，提供了完整的笔记管理功能，包括用户认证、Markdown 支持、附件管理、标签系统等核心特性。

## ✨ 核心功能

### 👤 用户管理
- ✅ 用户注册与登录
- 🔐 JWT Token 认证
- 🔑 Personal Access Token (PAT) 管理
- 👑 用户角色系统（HOST/ADMIN/USER）
- 📝 用户个人资料管理

### 📝 Memo 管理
- ✏️ 创建、编辑、删除 Memo
- 📄 Markdown 内容支持（使用 markdown-it-py）
- 👁️ 三种可见性级别：PUBLIC（公开）、PROTECTED（保护）、PRIVATE（私有）
- 🏷️ 标签系统
- 📌 置顶功能
- 🔗 Memo 关联与引用
- 😊 反应系统（Reaction）

### 📎 附件管理
- 📤 文件上传与管理
- 💾 支持本地存储和 S3 存储
- 🔗 附件与 Memo 关联

### 🔍 搜索功能
- 🔎 全文搜索
- 🎯 按标签、创建者、可见性过滤

### 🔌 插件系统
- ⏰ **任务调度插件**：基于 APScheduler 的定时任务
- 📧 **邮件插件**：SMTP 邮件发送，支持欢迎邮件、密码重置等

### 📚 API 文档
- 📖 自动生成 OpenAPI 文档
- 🎨 Swagger UI 界面
- 📄 ReDoc 文档

## 🛠️ 技术栈

- ⚡ **Web 框架**：FastAPI 0.109.0
- 🗄️ **数据库 ORM**：SQLAlchemy 2.0.25 (async)
- 🐘 **数据库支持**：SQLite (默认)、PostgreSQL、MySQL
- 🔒 **认证**：JWT (python-jose)、bcrypt 密码加密
- 📝 **Markdown**：markdown-it-py 3.0.0
- ⏰ **任务调度**：APScheduler 3.10.4
- 📧 **邮件**：smtplib
- 🚀 **ASGI 服务器**：Uvicorn

## 📁 项目结构

```
memos-py/
├── app/
│   ├── api/v1/              # API 路由
│   │   ├── __init__.py      # 路由聚合
│   │   ├── users.py         # 用户相关 API
│   │   ├── memos.py         # Memo 相关 API
│   │   ├── tokens.py        # Token 管理 API
│   │   ├── attachments.py   # 附件管理 API
│   │   └── search.py        # 搜索 API
│   ├── core/                # 核心功能
│   │   ├── deps.py          # 依赖注入（认证等）
│   │   ├── security.py      # 安全相关（JWT、密码）
│   │   └── markdown.py      # Markdown 处理
│   ├── db/                  # 数据库
│   │   ├── base.py          # 数据库基类
│   │   ├── models.py        # SQLAlchemy 模型
│   │   └── session.py       # 数据库会话
│   ├── plugins/             # 插件系统
│   │   ├── scheduler.py     # 任务调度插件
│   │   └── email.py         # 邮件插件
│   ├── schemas/             # Pydantic 模式
│   │   └── schemas.py       # 请求/响应模型
│   ├── services/            # 业务逻辑层
│   │   └── services.py      # 服务类
│   ├── config.py            # 配置管理
│   └── main.py              # FastAPI 应用入口
├── scripts/                 # 工具脚本
│   └── init_db.py           # 数据库初始化
├── data/                    # 数据目录（自动创建）
│   ├── memos.db            # SQLite 数据库
│   └── attachments/        # 附件存储
├── requirements.txt         # Python 依赖
├── Dockerfile              # Docker 镜像
├── docker-compose.yml      # Docker Compose 配置
├── .env.example            # 环境变量示例
├── .gitignore              # Git 忽略文件
└── run.py                  # 应用启动脚本
```

## 🗄️ 数据库模型

### 👤 User（用户）
- `id` - 用户 ID
- `username` - 用户名（唯一）
- `email` - 邮箱（唯一）
- `nickname` - 昵称
- `password_hash` - 密码哈希
- `avatar_url` - 头像 URL
- `role` - 角色（HOST/ADMIN/USER）
- `description` - 个人简介
- `created_ts` - 创建时间
- `updated_ts` - 更新时间

### 📝 Memo（笔记）
- `id` - Memo ID
- `uid` - 唯一标识符（UUID）
- `creator_id` - 创建者 ID
- `content` - 内容（Markdown 格式）
- `visibility` - 可见性（PUBLIC/PROTECTED/PRIVATE）
- `tags` - 标签列表（JSON）
- `payload` - 额外数据（JSON）
- `pinned` - 是否置顶
- `created_ts` - 创建时间
- `updated_ts` - 更新时间

### 📎 Attachment（附件）
- `id` - 附件 ID
- `uid` - 唯一标识符（UUID）
- `creator_id` - 创建者 ID
- `memo_id` - 关联的 Memo ID
- `filename` - 文件名
- `file_type` - 文件类型
- `file_size` - 文件大小
- `storage_type` - 存储类型（local/s3）
- `reference` - 存储引用
- `payload` - 额外数据（JSON）
- `created_ts` - 创建时间
- `updated_ts` - 更新时间

### 😊 Reaction（反应）
- `id` - 反应 ID
- `creator_id` - 创建者 ID
- `memo_id` - Memo ID
- `reaction` - 反应内容（emoji）
- `created_ts` - 创建时间

### 🔗 MemoRelation（笔记关联）
- `id` - 关联 ID
- `memo_id` - Memo ID
- `related_memo_id` - 关联的 Memo ID
- `type` - 关联类型
- `created_ts` - 创建时间

### 🔑 PersonalAccessToken（个人访问令牌）
- `id` - Token ID
- `user_id` - 用户 ID
- `token` - Token 字符串
- `description` - 描述
- `issued_at` - 签发时间
- `expires_at` - 过期时间

### ⚙️ UserSetting（用户设置）
- `id` - 设置 ID
- `user_id` - 用户 ID
- `key` - 设置键
- `value` - 设置值
- `created_ts` - 创建时间
- `updated_ts` - 更新时间

### 🏢 InstanceSetting（实例设置）
- `id` - 设置 ID
- `key` - 设置键（唯一）
- `value` - 设置值
- `description` - 描述
- `created_ts` - 创建时间
- `updated_ts` - 更新时间

## 🚀 快速开始

### 📋 环境要求

- 🐍 Python 3.11+
- 📦 pip
- 🗄️ SQLite（默认）或 PostgreSQL/MySQL

### 📦 安装步骤

1. **克隆仓库** 📥
```bash
git clone https://github.com/hero-tiger/memos-py.git
cd memos-py
```

2. **创建虚拟环境** 🐍
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **安装依赖** 📦
```bash
pip install -r requirements.txt
```

4. **配置环境变量** ⚙️
```bash
cp .env.example .env
# 编辑 .env 文件，修改必要的配置
```

5. **初始化数据库** 🗄️
```bash
python scripts/init_db.py
```

6. **启动应用** 🚀
```bash
python run.py
```

应用将在 `http://localhost:8081` 启动 ✨

## ⚙️ 配置说明

在项目根目录创建 `.env` 文件：

```env
# 应用配置
APP_NAME=Memos
APP_VERSION=0.1.0
DEBUG=false
HOST=0.0.0.0
PORT=8081

# 数据目录
DATA_DIR=./data

# 数据库配置
# SQLite（默认）
DATABASE_URL=sqlite+aiosqlite:///./data/memos.db

# PostgreSQL
# DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/memos

# MySQL
# DATABASE_URL=mysql+aiomysql://user:password@localhost:3306/memos

# 安全配置
SECRET_KEY=your-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=15

# CORS 配置
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]

# 邮件配置（可选）
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=your-email@gmail.com
SMTP_FROM_NAME=Memos
SMTP_USE_TLS=true

# S3 配置（可选）
S3_BUCKET=
S3_REGION=
S3_ACCESS_KEY=
S3_SECRET_KEY=
S3_ENDPOINT=
```

## 📚 API 文档

启动应用后，访问以下地址查看 API 文档：

- 📖 **Swagger UI**: http://localhost:8081/api/docs
- 📄 **ReDoc**: http://localhost:8081/api/redoc
- 🔧 **OpenAPI JSON**: http://localhost:8081/api/openapi.json

## 🔌 API 端点

### 🔐 认证
- `POST /api/v1/auth/signup` - 用户注册
- `POST /api/v1/auth/signin` - 用户登录

### 👤 用户
- `GET /api/v1/users/me` - 获取当前用户信息
- `PATCH /api/v1/users/me` - 更新当前用户信息
- `GET /api/v1/users` - 获取用户列表
- `GET /api/v1/users/{user_id}` - 获取指定用户信息

### 📝 Memo
- `POST /api/v1/memos` - 创建 Memo
- `GET /api/v1/memos` - 获取 Memo 列表（支持过滤）
- `GET /api/v1/memos/{memo_id}` - 根据 ID 获取 Memo
- `GET /api/v1/memos/uid/{uid}` - 根据 UID 获取 Memo
- `PATCH /api/v1/memos/{memo_id}` - 更新 Memo
- `DELETE /api/v1/memos/{memo_id}` - 删除 Memo

### 🔑 Personal Access Token
- `POST /api/v1/tokens` - 创建 PAT
- `GET /api/v1/tokens` - 获取用户的 PAT 列表
- `DELETE /api/v1/tokens/{token_id}` - 删除 PAT

### 📎 附件
- `POST /api/v1/attachments` - 上传附件
- `GET /api/v1/attachments/{attachment_id}` - 获取附件信息
- `DELETE /api/v1/attachments/{attachment_id}` - 删除附件

### 🔍 搜索
- `GET /api/v1/search` - 搜索 Memo

## 💡 使用示例

### ✅ 注册用户

```bash
curl -X POST http://localhost:8081/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'
```

### 🔐 登录

```bash
curl -X POST "http://localhost:8081/api/v1/auth/signin?email=test@example.com&password=password123"
```

返回示例：
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### ✏️ 创建 Memo

```bash
curl -X POST http://localhost:8081/api/v1/memos \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "# Hello World\n\nThis is my first memo with **Markdown** support!",
    "visibility": "PRIVATE",
    "tags": ["test", "first"],
    "pinned": false
  }'
```

### 📋 获取 Memo 列表

```bash
curl -X GET "http://localhost:8081/api/v1/memos?tag=test&limit=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 🔄 更新 Memo

```bash
curl -X PATCH http://localhost:8081/api/v1/memos/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "# Updated Memo\n\nThis content has been updated.",
    "pinned": true
  }'
```

### 🔑 创建 Personal Access Token

```bash
curl -X POST http://localhost:8081/api/v1/tokens \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "My API Token"
  }'
```

## 🔌 插件使用

### ⏰ 任务调度插件

```python
from app.plugins.scheduler import scheduler

# 添加定时任务
scheduler.add_job(
    my_task,
    job_id="daily_task",
    cron_expression="0 9 * * *",  # 每天 9:00 执行
    timezone="UTC"
)

# 启动调度器
await scheduler.start()

# 移除任务
scheduler.remove_job("daily_task")

# 列出所有任务
jobs = scheduler.list_jobs()
```

### 📧 邮件插件

```python
from app.plugins.email import email_plugin

# 发送邮件
await email_plugin.send_email(
    to_email="user@example.com",
    subject="Welcome!",
    html_content="<h1>Welcome!</h1>"
)

# 发送欢迎邮件
await email_plugin.send_welcome_email(
    to_email="user@example.com",
    username="John"
)

# 发送密码重置邮件
await email_plugin.send_password_reset_email(
    to_email="user@example.com",
    reset_link="https://example.com/reset?token=xxx"
)
```

## 🐳 Docker 部署

### 📦 使用 Dockerfile

```bash
# 构建镜像
docker build -t memos-py .

# 运行容器
docker run -d \
  -p 8081:8081 \
  -v $(pwd)/data:/app/data \
  --name memos-py \
  memos-py
```

### 🐙 使用 Docker Compose

```bash
# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## 🏭 生产环境部署

### 🔒 安全建议

1. 🔑 **设置强密钥**：使用随机生成的强密钥作为 `SECRET_KEY`
2. 🚫 **禁用调试模式**：设置 `DEBUG=false`
3. 🔐 **使用 HTTPS**：配置反向代理（nginx、traefik）启用 SSL/TLS
4. 🗄️ **数据库安全**：使用 PostgreSQL 或 MySQL 替代 SQLite
5. 🌐 **CORS 配置**：限制允许的源地址
6. 💾 **定期备份**：定期备份数据库和附件

### ⚡ 性能优化

1. 🐘 **使用生产级数据库**：PostgreSQL 或 MySQL
2. 🚀 **配置缓存**：使用 Redis 缓存热点数据
3. ⚖️ **负载均衡**：使用多个应用实例
4. 🌍 **CDN**：使用 CDN 加速静态资源
5. 🔧 **数据库连接池**：优化数据库连接池配置

### 🌐 反向代理配置（Nginx）

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8081;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 💻 开发

### 🧪 运行测试

```bash
pytest
```

### 🎨 代码格式化

```bash
# 使用 black 格式化代码
black app/

# 使用 isort 排序导入
isort app/
```

### 🔍 代码检查

```bash
# 使用 pylint 检查代码
pylint app/

# 使用 mypy 进行类型检查
mypy app/
```

## 🔄 数据库迁移

项目使用 SQLAlchemy 的 Alembic 进行数据库迁移。

### 📝 创建迁移

```bash
alembic revision --autogenerate -m "description"
```

### ⬆️ 应用迁移

```bash
alembic upgrade head
```

### ⬇️ 回滚迁移

```bash
alembic downgrade -1
```

## ❓ 常见问题

### 🔄 如何重置数据库？

删除数据库文件并重新初始化：

```bash
rm data/memos.db
python scripts/init_db.py
```

### 🐘 如何更改数据库为 PostgreSQL？

修改 `.env` 文件中的 `DATABASE_URL`：

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/memos
```

### 📧 如何启用邮件功能？

在 `.env` 文件中配置 SMTP 相关参数：

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=your-email@gmail.com
SMTP_FROM_NAME=Memos
SMTP_USE_TLS=true
```

## 🤝 贡献指南

欢迎贡献！请遵循以下步骤：

1. 🍴 Fork 本仓库
2. 🌿 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. ✅ 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 📤 推送到分支 (`git push origin feature/AmazingFeature`)
5. 🔀 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [Memos](https://github.com/usememos/memos) - 原始项目
- [FastAPI](https://fastapi.tiangolo.com/) - 现代 Web 框架
- [SQLAlchemy](https://www.sqlalchemy.org/) - Python SQL 工具包和 ORM

## 📞 联系方式

- 🐙 GitHub: [hero-tiger/memos-py](https://github.com/hero-tiger/memos-py)
- 🐛 Issues: [GitHub Issues](https://github.com/hero-tiger/memos-py/issues)

---

**注意**：本项目是 Memos 的 Python 实现，旨在提供相同的功能体验，但使用 Python 技术栈构建。🎉
