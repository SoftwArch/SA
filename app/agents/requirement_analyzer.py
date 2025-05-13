from typing import Dict, List, Any
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent
from langchain.prompts import StringPromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI

class RequirementAnalyzer:
    def __init__(self, llm_api_key: str):
        self.llm = OpenAI(temperature=0, openai_api_key=llm_api_key)
        self._setup_agent()

    def _setup_agent(self):
        # 定义工具
        tools = [
            Tool(
                name="extract_features",
                func=self._extract_features,
                description="从需求描述中提取关键特征"
            ),
            Tool(
                name="identify_constraints",
                func=self._identify_constraints,
                description="识别需求中的约束条件"
            )
        ]

        # 设置提示模板
        template = """
        你是一个软件需求分析专家。请分析以下软件需求描述：
        {requirement_description}

        请提取以下信息：
        1. 关键功能特征
        2. 非功能性需求
        3. 约束条件
        4. 总体分析总结

        使用以下工具：
        {tools}

        你的分析过程：
        {agent_scratchpad}
        """

        prompt = StringPromptTemplate(
            template=template,
            input_variables=["requirement_description", "tools", "agent_scratchpad"]
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

    def _extract_features(self, text: str) -> List[str]:
        """提取需求中的关键特征"""
        # TODO: 实现特征提取逻辑
        return ["高并发", "实时性", "可扩展性"]

    def _identify_constraints(self, text: str) -> List[str]:
        """识别需求中的约束条件"""
        # TODO: 实现约束识别逻辑
        return ["跨平台", "实时通信"]

    async def analyze(self, requirement_description: str) -> Dict[str, Any]:
        """分析需求描述"""
        try:
            result = await self.agent_executor.arun(
                requirement_description=requirement_description
            )
            return {
                "key_features": self._extract_features(requirement_description),
                "non_functional_requirements": {
                    "性能": "支持万人同时在线",
                    "可靠性": "消息传递可靠性保证",
                    "可扩展性": "支持快速扩展新功能"
                },
                "constraints": self._identify_constraints(requirement_description),
                "analysis_summary": result
            }
        except Exception as e:
            raise Exception(f"需求分析失败: {str(e)}")