# 提示词润色助手 - Streamlit 版本

## 功能特性

- ✅ 6 大场景模板（通用、代码、小红书、数据分析、创意写作、总结提炼）
- ✅ 3 种输出风格（简洁版、详细版、专家版）
- ✅ 双模式优化（规则模板 + 大模型润色）
- ✅ 四维度评分系统（清晰度、结构化、约束完整性、目标明确度）
- ✅ 历史记录保存
- ✅ 一键复制结果

## 本地运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行应用

```bash
streamlit run app.py
```

浏览器会自动打开 http://localhost:8501

## 部署到 Streamlit Cloud（免费）

### 1. 推送到 GitHub

```bash
git init
git add .
git commit -m "初始版本"
git remote add origin git@github.com:semikawt/prompt-polisher-streamlit.git
git branch -M main
git push -u origin main
```

### 2. 部署到 Streamlit Cloud

1. 打开 https://share.streamlit.io
2. 用 GitHub 账号登录
3. 点击 "New app"
4. 选择仓库 `semikawt/prompt-polisher-streamlit`
5. Branch 选 `main`
6. Main file path 填 `app.py`
7. 点击 "Deploy!"

等待 1-2 分钟，部署完成后会获得一个 `https://xxxx.streamlit.app` 链接。
注意：子域名由 Streamlit 随机分配（不是"用户名-仓库名"），以控制台实际显示的为准。

> ⚠️ 新部署的应用默认是 **Private**，别人点开会要求登录。
> 请在 share.streamlit.io → 应用 → Settings（⚙️）→ Sharing 改为 **Public**，
> 然后用无痕窗口验证能直接打开。若从公开仓库部署，应用会默认继承为 Public。

### 3. 配置 API Key（可选）

在 Streamlit Cloud 中：
1. 进入应用设置 → Secrets
2. 添加：
   ```
   DOUBAO_API_KEY = "你的API Key"
   ```
3. 保存后应用会自动重启

或者直接在应用左侧边栏输入 API Key（临时使用）。

## 部署到其他平台

### Hugging Face Spaces（免费）

1. 注册 https://huggingface.co
2. 创建新 Space，选 Streamlit SDK
3. 把代码推送到 Space 仓库
4. 自动部署

### 本地服务器

```bash
# 后台运行
nohup streamlit run app.py --server.port 8501 &

# 用 Nginx 反向代理
```

## 文件结构

```
prompt-polisher-streamlit/
├── app.py              # 主应用
├── requirements.txt    # 依赖
└── README.md           # 说明文档
```

## 获取豆包 API Key

1. 打开 https://console.volcengine.com/ark
2. 注册/登录火山引擎账号
3. 进入「API Key 管理」
4. 创建新的 API Key
5. 复制保存（只显示一次）

## 注意事项

- 规则模板模式完全离线可用，不需要 API Key
- 大模型润色模式需要配置豆包 API Key
- Streamlit Cloud 免费版有休眠机制，长时间不访问会休眠，再次访问需要等待几秒启动
