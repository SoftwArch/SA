from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

class ArchitectureKnowledgeBase:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            os.getenv("NEO4J_URI", "bolt://localhost:7687"),
            auth=(os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "your_password"))
        )

    def close(self):
        self.driver.close()

    def create_architecture_styles(self):
        with self.driver.session() as session:
            # 创建架构风格节点
            session.run("""
                CREATE (a:ArchitectureStyle {
                    name: '事件驱动架构',
                    description: '基于事件的生产、检测、消费和反应的架构模式',
                    advantages: ['高并发处理', '松耦合', '可扩展性'],
                    disadvantages: ['调试复杂', '事件溯源实现难度大'],
                    use_cases: ['实时通信系统', '物联网应用', '金融交易系统'],
                    implementation_complexity: '中等'
                })
            """)

            session.run("""
                CREATE (a:ArchitectureStyle {
                    name: '微服务架构',
                    description: '将应用程序构建为一组小型服务的架构风格',
                    advantages: ['服务独立部署', '技术栈灵活', '团队自治'],
                    disadvantages: ['分布式系统复杂性', '服务间通信开销'],
                    use_cases: ['大型企业应用', '云原生应用', '电子商务平台'],
                    implementation_complexity: '较高'
                })
            """)

            session.run("""
                CREATE (a:ArchitectureStyle {
                    name: '分层架构',
                    description: '将系统划分为多个层次，每层都有特定的职责',
                    advantages: ['结构清晰', '易于维护', '职责分离'],
                    disadvantages: ['层次间耦合', '性能开销'],
                    use_cases: ['传统企业应用', 'Web应用', '桌面应用'],
                    implementation_complexity: '低'
                })
            """)

            # 创建架构风格之间的关系
            session.run("""
                MATCH (a:ArchitectureStyle {name: '事件驱动架构'})
                MATCH (b:ArchitectureStyle {name: '微服务架构'})
                CREATE (a)-[:CAN_COMBINE_WITH]->(b)
            """)

    def create_quality_attributes(self):
        with self.driver.session() as session:
            # 创建质量属性节点
            session.run("""
                CREATE (q:QualityAttribute {
                    name: '可扩展性',
                    description: '系统处理负载增长的能力',
                    metrics: ['水平扩展能力', '垂直扩展能力', '扩展成本']
                })
            """)

            session.run("""
                CREATE (q:QualityAttribute {
                    name: '性能',
                    description: '系统响应时间和吞吐量',
                    metrics: ['响应时间', '并发用户数', '资源利用率']
                })
            """)

            # 创建架构风格与质量属性的关系
            session.run("""
                MATCH (a:ArchitectureStyle {name: '事件驱动架构'})
                MATCH (q:QualityAttribute {name: '可扩展性'})
                CREATE (a)-[:SUPPORTS {score: 0.9}]->(q)
            """)

def main():
    kb = ArchitectureKnowledgeBase()
    try:
        kb.create_architecture_styles()
        kb.create_quality_attributes()
        print("架构知识库初始化完成")
    finally:
        kb.close()

if __name__ == "__main__":
    main()