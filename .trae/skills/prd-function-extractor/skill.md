---
name: prd-function-extractor
description: "Extracts functional points from PRD documents (Feishu). Invoke when user wants to analyze requirements or extract functions from a PRD."
---
# prd-function-extractor
This skill extracts functional points from a Product Requirement Document(PRD) hosted on Feishu.
## Workflow
1.  **Get the PRD Link**: Ask the user for the Feishu document link ifnot provided.
2.  **Fetch Document Content**:
    *   **Method 1 (Preferred)**: Use the `mcp_feishu-lark-mcp_fetch-doc` tool.
        *   Argument `doc_id` should be the full URL of the Feishu document.
    *   **Method 2 (Fallback)**: If Method 1 fails or is unavailable, run the python script located at `.trae/skills/prd-function-extractor/scripts/fetch_doc.py` to fetch the content via the HTTP interface.
        *   Usage: `python ./skills/prd-function-extractor/scripts/fetch_doc.py <doc_url>`
        *   Note: You may need to install `requests` ifnot available, or use standard library `urllib` if `requests` is missing and you cannot install it.
    *   **Method 3 (Manual)**: If both Method 1 and Method 2 fail, **ask the user to paste the document content directly**. Explain that automatic fetching failed.
3.  **Analyze Content**: Use the **Function Extraction Prompt** (below) to process the markdown content.
## Function Extraction Prompt
Use the following prompt to analyze the fetched markdown content. Paste the document content at the end of this prompt or provide it as context.
---
#### **角色与任务**  
你是**顶级业务分析师（Business Analyst）**和**PRD需求提取专家**，需从**任意PRD**中**100%精准提取所有功能相关核心信息**，分批次生成需求文档。 
#### **提取规则**  
--- 
##### **1. 场景识别：覆盖所有用户操作逻辑**  
需识别PRD中**所有用户与系统交互的场景**，包括：  
- **主场景**：核心功能的常规操作（如“用户填写表单提交信息”“用户查看某模块数据列表”）；  
- **边缘场景**：异常/边界条件下的操作（如“用户输入无效值时的提示”“功能禁用时的交互限制”）；  
- **关联场景**：跨模块的联动操作（如“操作A触发模块B的状态变更”）。  
每个场景分配唯一需求ID（格式：`PRD-XXX`，按批次顺序编号）。  
##### **2. 要素提取：每个场景必须包含4项核心内容**  
需严格从PRD原文中提取以下要素，**不允许 paraphrase（改写）**，保持原文表述：  
- 场景描述：用户具体操作 + 目标（严格还原 PRD 动词、名词、流程）； 
- 业务规则：PRD 明确的逻辑规则（如计算方式、展示优先级、操作联动、数据映射关系等）； 
- 约束条件：PRD 明确的限制（输入范围、权限控制、禁用条件、提示文案、时间限制等）； 
- 优先级：PRD 标注的优先级（P0/P1/P2 / 高 / 中 / 低）。 
##### **3. 覆盖要求：确保无遗漏**  
需覆盖PRD中**所有功能相关内容**，包括但不限于：  
- **文案细节**：按钮名称、标签内容、提示语、hover说明、字段说明；  
- **边缘场景**：异常输入提示、功能禁用规则、跨模块联动限制、数据边界条件；  
- **逻辑规则**：数据计算方式、状态流转规则、权限控制逻辑、操作生效条件。  
#### **输出格式**  
严格按照如下json格式输出，确保json格式合法： 
```json 
[ 
{ 
    "requirement_id": "PRD-001", // 需求ID 
    "scenario_description": "用户在[客户管理模块]的客户列表页，查看每条客户记录的「客户名称」「注册时间」「状态」字段", // 场景描述 
    "business_rule": "客户列表页展示的字段包括：客户名称（原文名称）、注册时间（格式：YYYY-MM-DD）、状态（标签形式，内容为「激活」「冻结」「注销」）", // 业务规则 
    "constraints": "注册时间仅展示至日期，不显示时分秒；状态标签颜色随状态不同区分（激活：绿色/冻结：橙色/注销：灰色）", // 约束条件 
    "priority": "P0"// 优先级 
  }, 
  { 
    "requirement_id": "PRD-002", 
    "scenario_description": "用户在[订单管理模块]的订单详情页，查看「订单金额」字段的hover说明", 
    "business_rule": "「订单金额」字段的hover文案为：「订单金额=商品总价+运费-优惠券抵扣-满减折扣」", 
    "constraints": "hover说明仅当鼠标悬浮至「订单金额」字段时显示，文案不可修改", 
    "priority": "P0"
  } 
] 
```
