"""AutoGen multi-agent fashion stylist."""
import autogen

config_list = [{"model": "gpt-4o", "api_key": "OPENAI_API_KEY"}]

assistant = autogen.AssistantAgent(
    name="StyleAssistant",
    system_message="You are a fashion expert. Recommend outfits.",
    llm_config={"config_list": config_list},
)

user_proxy = autogen.UserProxyAgent(
    name="UserProxy",
    human_input_mode="NEVER",
    code_execution_config={"work_dir": "/tmp"},
)

user_proxy.initiate_chat(assistant, message="Create a festive outfit for Diwali.")
