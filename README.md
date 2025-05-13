# 软件架构风格智能助手

基于大语言模型的软件架构风格推荐系统，支持需求分析、架构推荐和决策支持。

[llm_client](app/llm_client.py): 调用deepseek实现需求解析，架构匹配， 评估生成。
[test_architecture_recommendation](tests/test_architecture_recommendation.py): 测试用例。