import autogen
from autogen import AssistantAgent, UserProxyAgent
from autogen.agentchat.contrib.math_user_proxy_agent import MathUserProxyAgent
from autogen.code_utils import extract_code

TIMEOUT = 60

config_list = autogen.config_list_from_json("configs/OAI_CONFIG_LIST.json")

def _is_termination_msg(message):
    if isinstance(message, dict):
        message = message.get("content")
        if message is None:
            return False
    cb = extract_code(message)
    contain_code = False
    for c in cb:
        if c[0] == "python":
            contain_code = True
            break
    return not contain_code

def initialize_agents():
    assistant = AssistantAgent(
        name="assistant",
        max_consecutive_auto_reply=10,
        llm_config={
            "timeout": TIMEOUT,
            "config_list": config_list,
        },
    )

    userproxy = UserProxyAgent(
        name="userproxy",
        human_input_mode="NEVER",
        is_termination_msg=_is_termination_msg,
        max_consecutive_auto_reply=10,
        code_execution_config={
            "work_dir": "coding",
            "use_docker": False,  
        },
    )

    math_proxy_agent = MathUserProxyAgent(
        name="math_proxy_agent",
        human_input_mode="NEVER",
        code_execution_config={
            "use_docker": False
        },
    )

    return assistant, userproxy, math_proxy_agent