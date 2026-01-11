import asyncio

from langchain_core.messages import convert_to_messages
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor

from app.bailian.common import file_tools
from app.code_agent.model.qwen import llm_qwen
from app.code_agent.tools.shell_tools import get_stdio_shell_tools
from app.code_agent.tools.terminal_tools import get_stdio_terminal_tools


def pretty_print_messages(update, last_message=False):
    # for node_name, node_update in update.items():
    #     update_label = f"Update from node {node_name}:"
    #     print(update_label)

    # messages = convert_to_messages(node_update['messages'])
    messages = convert_to_messages(update['messages'])
    if last_message:
        messages = messages[-1:]

    for message in messages:
        pretty_message = message.pretty_repr(html=True)
        print(pretty_message)

    print("\n\n")


async def run_agent():
    memory = MemorySaver()

    shell_tools = await get_stdio_shell_tools()

    research_agent = create_react_agent(
        model=llm_qwen,
        tools=shell_tools + file_tools,
        name="research_expert",
        prompt="你是一个技术主管，负责设计技术方案。请注意：运行环境是 Windows 11。请不要直接写代码，请指导 code_agent 进行工作",
    )

    code_agent = create_react_agent(
        model=llm_qwen,
        tools=shell_tools + file_tools,
        name="code_expert",
        prompt=("你是一个编程专家，请根据 research_expert 设计的技术方案来实现代码或进行代码文件相关的操作。"
                "重要提示：\n"
                "1. 当前环境是 Windows 11，请务必使用 Windows 风格的路径（例如 D:\\path\\to\\file），绝对不要使用 Linux 路径（如 /d/path）。\n"
                "2. 【严禁使用】 'mkdir -p'，Windows 不支持。如果目录可能不存在，请直接用 shell 命令 'mkdir \"path\"' (如果父目录不存在它可能会报错，可以分级创建或者忽略错误) 或者用 python 代码创建。\n"
                "3. 【严禁使用】 'rm' 或 'rm -rf'。删除目录请用 'rmdir /s /q \"path\"'。\n"
                "4. 执行 git clone 时，**必须**加上 '--progress --verbose' 参数，否则后台运行看不到进度会以为卡死。\n"
                "   - 建议格式：'git clone --depth 1 --progress --verbose <url> <target_full_path>'\n"
                "   - 如果目标目录已存在且不为空，git clone 会失败。请先用 'rmdir /s /q' 删除旧目录，再 clone。\n"
                "5. clone 完成后，必须使用 'dir' 命令验证文件是否存在。"),
    )

    supervisor_agent = create_supervisor(
        agents=[research_agent, code_agent],
        model=llm_qwen,
        prompt=
        ("You are a team supervisor managing a research expert and a code expert."
         "For task planning and task researching, use research_agent."
         "For code problems, use code_agent."))

    app = supervisor_agent.compile(checkpointer=memory)

    while True:
        user_input = input("用户：")

        if user_input.lower() == "exit":
            break

        config = RunnableConfig(configurable={"thread_id": 1},
                                recursion_limit=100)

        # async for chunk in app.astream(input={"messages": user_input}, config=config):
        #     pretty_print_messages(chunk, last_message=True)

        result = await app.ainvoke(input={"messages": user_input},
                                   config=config)
        pretty_print_messages(result)


asyncio.run(run_agent())
