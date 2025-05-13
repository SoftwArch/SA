# 软件架构风格智能助手

基于大语言模型的软件架构风格推荐系统，支持需求分析、架构推荐和决策支持。

## 项目结构

```
.
├── app/                    # 主应用目录
│   ├── api/               # API 接口
│   ├── core/              # 核心配置
│   ├── agents/            # 智能体实现
│   ├── models/            # 数据模型
│   └── services/          # 业务服务
├── tests/                 # 测试用例
├── docs/                  # 文档
└── scripts/               # 工具脚本
```

## 主要功能

1. 需求分析：接收用户自然语言描述的软件功能需求，进行语义理解与关键特征提取
2. 架构推荐：根据需求分析结果，推荐至少3种候选体系结构风格
3. 决策支持：通过多维度对比分析，给出最终推荐架构风格及其优缺点评估报告
4. 知识进化：支持架构知识库的持续扩展与案例学习能力

## 技术栈

- FastAPI：Web框架
- LangChain：智能体框架
- Neo4j：知识图谱存储
- Transformers：大语言模型集成
- NetworkX：图分析
- Matplotlib：可视化

## 快速开始

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 配置环境变量：
```bash
cp .env.example .env
# 编辑 .env 文件，填入必要的配置信息
```

3. 启动服务：
```bash
uvicorn app.main:app --reload
```

## API文档

启动服务后访问：http://localhost:8000/docs

## 测试

运行测试用例：
```bash
pytest
```