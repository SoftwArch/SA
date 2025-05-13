from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="软件架构风格智能助手",
    description="基于大语言模型的软件架构风格推荐系统",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "欢迎使用软件架构风格智能助手"}

# 导入路由
from app.api import requirements, architecture, evaluation

# 注册路由
app.include_router(requirements.router, prefix="/api/requirements", tags=["需求分析"])
app.include_router(architecture.router, prefix="/api/architecture", tags=["架构推荐"])
app.include_router(evaluation.router, prefix="/api/evaluation", tags=["决策支持"])