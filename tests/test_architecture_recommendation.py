import pytest
from unittest.mock import AsyncMock, patch
from app.llm_client import LLMFactory

@pytest.mark.asyncio
async def test_architecture_recommendation():
    # 1. 准备测试数据
    requirement = """
    开发一个跨平台的即时通讯系统，要求支持万人同时在线，
    需要保证消息的实时性和可靠性，后期可能需要快速扩展视频通话功能
    """
    
    # 2. 创建模拟的需求分析结果
    mock_requirement_analysis = {
        "key_features": ["高并发", "实时通信", "跨平台", "可扩展性"],
        "non_functional_requirements": {
            "性能": "支持万人同时在线",
            "可靠性": "消息传递可靠性保证",
            "可扩展性": "支持快速扩展新功能"
        },
        "constraints": ["跨平台", "实时通信"],
        "analysis_summary": "高并发即时通信系统，需要强大的可扩展性和消息可靠性"
    }
    
    # 3. 创建模拟的架构推荐结果
    mock_architecture_recommendation = {
        "recommended_styles": ["事件驱动架构", "微服务架构"],
        "comparison_matrix": {
            "事件驱动架构": {"并发处理": "优", "可扩展性": "优", "实现复杂度": "中"},
            "微服务架构": {"并发处理": "中", "可扩展性": "优", "实现复杂度": "高"}
        },
        "final_recommendation": "事件驱动架构",
        "reasoning": "高并发场景下的事件异步处理能力，松耦合特性便于扩展视频通话模块",
        "pros_cons": {
            "pros": ["高吞吐量", "模块解耦", "扩展性强"],
            "cons": ["事件溯源实现复杂度高", "调试困难"]
        }
    }
    
    # 4. 创建DeepSeekClient的模拟对象
    with patch('app.llm_client.DeepSeekClient') as MockClient:
        mock_client = MockClient.return_value
        mock_client.analyze_requirements = AsyncMock(return_value=mock_requirement_analysis)
        mock_client.recommend_architecture = AsyncMock(return_value=mock_architecture_recommendation)
        
        # 5. 使用LLMFactory创建模拟客户端
        with patch('app.llm_client.LLMFactory.create_llm_client', return_value=mock_client):
            client = LLMFactory.create_llm_client()
            
            # 6. 执行需求分析
            req_analysis = await client.analyze_requirements(requirement)
            
            # 7. 执行架构推荐
            arch_recommendation = await client.recommend_architecture(req_analysis)
            
            # 8. 验证结果
            assert arch_recommendation["final_recommendation"] == "事件驱动架构"
            assert "微服务架构" in arch_recommendation["recommended_styles"]
            assert "高并发场景" in arch_recommendation["reasoning"]
            assert "高吞吐量" in arch_recommendation["pros_cons"]["pros"]
            assert "调试困难" in arch_recommendation["pros_cons"]["cons"]