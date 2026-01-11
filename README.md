# AI智能体开发实战

graph TD
    subgraph User_Lane [用户 (User)]
        A[提出需求: 集成图书列表] --> B[验收功能]
    end

    subgraph Agent_Core [Agent核心 (Core)]
        C[解析意图 & 任务拆解]
        H[任务完成通知]
    end

    subgraph Tools_Layer [MCP工具集 (Tools)]
        D[Shell工具: Git Clone]
        E[MySQL工具: 建表连接]
        F[File工具: 读写代码]
        G[Browser工具: 查阅文档(可选)]
    end

    subgraph Project_Env [项目/环境 (Env)]
        I[Vue3代码库]
        J[MySQL数据库]
    end

    %% Flow
    A --> C
    C -- 1. 环境初始化 --> D
    D --> I
    C -- 2. 数据层建设 --> E
    E --> J
    C -- 3. 业务层开发 --> F
    F --> I
    F -->|依赖查询| G
    I --> H
    J --> H
    H --> B
