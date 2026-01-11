# AI智能体开发实战

```mermaid
graph TD;
    A[提出需求: 集成图书列表] --> C[解析意图 & 任务拆解];
    C -->|环境初始化| D[Shell工具: Git Clone];
    D --> I[Vue3代码库];
    C -->|数据层建设| E[MySQL工具: 建表连接];
    E --> J[MySQL数据库];
    C -->|业务层开发| F[File工具: 读写代码];
    F --> I;
    F -->|依赖查询| G[Browser工具: 查阅文档(可选)];
    I --> H[任务完成通知];
    J --> H;
    H --> B[验收功能];
    H --> B
