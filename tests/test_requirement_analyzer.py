import pytest
from app.agents.requirement_analyzer import RequirementAnalyzer

@pytest.fixture
def analyzer():
    return RequirementAnalyzer(llm_api_key="test_key")

@pytest.mark.asyncio
async def test_analyze_requirement(analyzer):
    # 测试用例
    requirement = """
    开发一个跨平台的即时通讯系统，要求支持万人同时在线，
    需要保证消息的实时性和可靠性，后期可能需要快速扩展视频通话功能
    """
    
    result = await analyzer.analyze(requirement)
    
    # 验证结果
    assert "key_features" in result
    assert "non_functional_requirements" in result
    assert "constraints" in result
    assert "analysis_summary" in result
    
    # 验证关键特征
    assert "高并发" in result["key_features"]
    assert "实时性" in result["key_features"]
    assert "可扩展性" in result["key_features"]
    
    # 验证非功能性需求
    assert "性能" in result["non_functional_requirements"]
    assert "可靠性" in result["non_functional_requirements"]
    
    # 验证约束条件
    assert "跨平台" in result["constraints"]
    assert "实时通信" in result["constraints"]