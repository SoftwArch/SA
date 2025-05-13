from typing import Dict, List, Any
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent
from langchain.prompts import StringPromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI

class EvaluationGenerator:
    def __init__(self, llm_api_key: str):
        self.llm = OpenAI(temperature=0, openai_api_key=llm_api_key)
        self._setup_agent()

    def _setup_agent(self):
        # 定义工具
        tools = [
            Tool(
                name="evaluate_metrics",
                func=self._evaluate_metrics,
                description="评估架构风格的各项指标"
            ),
            Tool(
                name="generate_recommendations",
                func=self._generate_recommendations,
                description="生成改进建议"
            )
        ]

        # 设置提示模板
        template = """
        你是一个软件架构评估专家。请对以下架构风格进行评估：
        架构风格：{architecture_style}
        需求分析：{requirement_analysis}

        请从以下方面进行评估：
        1. 各项技术指标的得分
        2. 架构的优势和劣势
        3. 改进建议
        4. 风险评估

        使用以下工具：
        {tools}

        你的评估过程：
        {agent_scratchpad}
        """

        prompt = StringPromptTemplate(
            template=template,
            input_variables=["architecture_style", "requirement_analysis", "tools", "agent_scratchpad"]
        )

        # 创建智能体
        self.agent = LLMSingleActionAgent(
            llm_chain=LLMChain(llm=self.llm, prompt=prompt),
            allowed_tools=[tool.name for tool in tools],
            stop=["\nObservation:"],
            handle_parsing_errors=True
        )

        self.agent_executor = AgentExecutor.from_agent_and_tools(
            agent=self.agent,
            tools=tools,
            verbose=True
        )

    def _evaluate_metrics(self, architecture_style: str, requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """评估架构风格的各项指标"""
        # TODO: 实现指标评估逻辑
        return [
            {
                "name": "可扩展性",
                "score": 0.9,
                "description": "架构能够很好地支持系统扩展",
                "recommendations": ["考虑使用消息队列进行解耦", "实现服务发现机制"]
            },
            {
                "name": "性能",
                "score": 0.85,
                "description": "能够满足高并发需求",
                "recommendations": ["实现缓存机制", "优化事件处理流程"]
            }
        ]

    def _generate_recommendations(self, architecture_style: str, requirements: Dict[str, Any]) -> List[str]:
        """生成改进建议"""
        # TODO: 实现建议生成逻辑
        return [
            "引入事件溯源机制",
            "实现分布式追踪",
            "添加监控告警系统"
        ]

    async def evaluate(self, architecture_style: str, requirement_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """生成架构评估报告"""
        try:
            result = await self.agent_executor.arun(
                architecture_style=architecture_style,
                requirement_analysis=requirement_analysis
            )

            metrics = self._evaluate_metrics(architecture_style, requirement_analysis)
            recommendations = self._generate_recommendations(architecture_style, requirement_analysis)

            return {
                "overall_score": sum(metric["score"] for metric in metrics) / len(metrics),
                "metrics": metrics,
                "strengths": [
                    "高并发处理能力强",
                    "模块间耦合度低",
                    "易于扩展新功能"
                ],
                "weaknesses": [
                    "调试难度较大",
                    "需要额外的监控工具",
                    "事件一致性保证复杂"
                ],
                "improvement_suggestions": recommendations,
                "risk_assessment": {
                    "技术风险": "中等",
                    "实现风险": "较高",
                    "维护风险": "中等"
                }
            }
        except Exception as e:
            raise Exception(f"评估生成失败: {str(e)}")