from mcp.server.fastmcp import FastMCP
import requests

mcp = FastMCP()


@mcp.tool(name="get_weather", description="查询指定城市的天气信息")
def get_weather(city: str) -> str:
    """查询指定城市的天气信息，使用wttr.in API"""
    try:
        # 使用wttr.in API查询天气
        url = f"http://wttr.in/{city}?format=3"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        weather_info = response.text.strip()
        
        # 如果返回的是原始文本，进行简单处理
        if "wttr.in" in weather_info:
            return f"查询天气失败：无法获取{city}的天气信息"
        
        return f"{city}天气：{weather_info}"
        
    except requests.RequestException as e:
        return f"查询天气失败：{str(e)}"
    except Exception as e:
        return f"查询天气时发生未知错误：{str(e)}"


if __name__ == '__main__':
    mcp.run(transport="stdio")
