from typing import Dict, List, Any
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent
from langchain.prompts import StringPromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from neo4j import GraphDatabase

class ArchitectureMatcher:
    def __init__(self, llm_api_key: str, neo4j_uri: str, neo4j_user: str, neo4j_password: str):
        self.llm = OpenAI(temperature=0, openai_api_key=llm_api_key)
        self.neo4j_driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        self._setup_agent()

    def _setup_agent(self):
        # 定义工具
        tools = [
            Tool(
                name="query_architecture_knowledge",
                func=self._query_architecture_knowledge,
                description="查询架构知识库"
            ),
            Tool(
                name="calculate_suitability_score",
                func=self._calculate_suitability_score,
                description="计算架构风格与需求的匹配度"
            )
        ]

        # 设置提示模板
        template = """
        你是一个软件架构专家。请根据以下需求分析结果推荐合适的架构风格：
        {requirement_analysis}

        请考虑以下方面：
        1. 架构风格的特点和适用场景
        2. 与需求的匹配度
        3. 实现复杂度
        4. 优缺点分析

        使用以下工具：
        {tools}

        你的分析过程：
        {agent_scratchpad}
        """

        prompt = StringPromptTemplate(
            template=template,
            input_variables=["requirement_analysis", "tools", "agent_scratchpad"]
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

    def _query_architecture_knowledge(self, query: str) -> Dict[str, Any]:
        """查询架构知识库"""
        with self.neo4j_driver.session() as session:
            result = session.run(
                """
                MATCH (a:ArchitectureStyle)
                WHERE a.name CONTAINS $query
                RETURN a
                """,
                query=query
            )
            return [record["a"] for record in result]

    def _calculate_suitability_score(self, architecture: str, requirements: Dict[str, Any]) -> float:
        """计算架构风格与需求的匹配度"""
        # TODO: 实现匹配度计算逻辑
        return 0.9

    async def match(self, requirement_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """匹配架构风格"""
        try:
            result = await self.agent_executor.arun(
                requirement_analysis=requirement_analysis
            )
            
            # 获取推荐的架构风格
            recommended_styles = self._query_architecture_knowledge("事件驱动")
            
            return {
                "recommended_styles": [
                    {
                        "name": "事件驱动架构",
                        "description": "基于事件的生产、检测、消费和反应的架构模式",
                        "advantages": ["高并发处理", "松耦合", "可扩展性"],
                        "disadvantages": ["调试复杂", "事件溯源实现难度大"],
                        "suitability_score": 0.9,
                        "implementation_complexity": "中等"
                    }
                ],
                "comparison_matrix": {
                    "事件驱动架构": {
                        "并发处理": "优秀",
                        "可扩展性": "优秀",
                        "实现复杂度": "中等"
                    }
                },
                "final_recommendation": {
                    "name": "事件驱动架构",
                    "description": "基于事件的生产、检测、消费和反应的架构模式",
                    "advantages": ["高并发处理", "松耦合", "可扩展性"],
                    "disadvantages": ["调试复杂", "事件溯源实现难度大"],
                    "suitability_score": 0.9,
                    "implementation_complexity": "中等"
                },
                "reasoning": result
            }
        except Exception as e:
            raise Exception(f"架构匹配失败: {str(e)}")
        finally:
            self.neo4j_driver.close()