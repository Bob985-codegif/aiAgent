from mcp.server.fastmcp import FastMCP

# 这里创建了一个 FastMCP 实例，用于注册工具
mcp = FastMCP()


@mcp.tool(name="query_rag", description="从百炼平台查询知识库信息")
def query_rag_from_bailian(
    query: Annotated[str,
                     Field(description="访问知识库查询的内容", examples="终端的操作规范")]
) -> str:
    bailian_client = create_client()
    workspace_id = "llm-46p7ujuq0wrobzyq"
    index_id = "w1f629cent"
    rag = retrieve_index(bailian_client, workspace_id, index_id, query)

    result = ""

    for data in rag.body.data.nodes:
        result += f"""{data.text}
---"""
    return result
