---
name: trd-spec-extractor
description: "Extracts technical specifications from TRD documents (Feishu), mapping business rules to technical implementations. Invoke after PRD analysis when a TRD is available."
---
# trd-spec-extractor
This skill extracts technical specifications from a Technical Requirement Document(TRD) hosted on Feishu, mapping them to PRD business rules.
## Prerequisites
*   **PRD Analysis**: This skill is designed to run **after** `prd-function-extractor`. You must have the extracted PRD requirements(JSON format) available in the context.
## Workflow
1.  **Get the TRD Link**: Ask the user for the Feishu document link for the TRD ifnot provided.
2.  **Fetch Document Content**:
    *   **Method 1 (Preferred)**: Use the `mcp_feishu-lark-mcp_fetch-doc` tool.
        *   Argument `doc_id` should be the full URL of the Feishu document.
    *   **Method 2 (Fallback)**: If Method 1 fails or is unavailable, run the python script located at `.trae/skills/trd-spec-extractor/scripts/fetch_doc.py` to fetch the content via the HTTP interface.
        *   Usage: `python .trae/skills/trd-spec-extractor/scripts/fetch_doc.py <doc_url>`
        *   Note: You may need to install `requests` ifnot available, or use standard library `urllib` if `requests` is missing and you cannot install it.
    *   **Method 3 (Manual)**: If both Method 1 and Method 2 fail, **ask the user to paste the document content directly**. Explain that automatic fetching failed.
3.  **Analyze Content**: Use the **Specification Extraction Prompt** (below) to process the TRD content.
    *   **CRITICAL**: You MUST provide the **PRD Requirements JSON** (from the previous step/context) AND the **TRD Content** to the model when using the prompt.
## Specification Extraction Prompt
Use the following prompt to analyze the fetched TRD content.
**Input Context Required**:
1.  **PRD Requirements**: [Insert the JSON output from prd-function-extractor here]
2.  **TRD Content**: [Insert the fetched TRD markdown content here]
---
# 【核心目标】  
作为TRD技术规范提取专家，需**严格关联PRD中的「业务角色」「核心业务规则」与TRD中的「技术实现细节」**，从技术文档中提取**业务逻辑与技术方案一一对应**的可执行规范，确保规范既覆盖业务意图，又明确技术落地要求。 
# 【处理规则】  
1. **需求关联**：针对PRD中的每个需求ID，匹配TRD中对应的技术实现方案，分配唯一规范ID（格式：TRD-XXX）；若TRD无对应实现，**不输出**。  
2. **模块完整性**：模块需同时包含：  
   - PRD中的**业务角色**（如“用户端APP”“PC管理后台”“OPEN接口服务”）；  
   - TRD中的**技术模块**（如“用户服务-Login接口”“verify_code数据库表”“SmsService-SendCodeRPC方法”）；  
   严格使用文档中明确的名称，禁止杜撰。  
3. **具体要求完整性（核心约束）**：  
   需覆盖2类**100%完整**的信息，**不得有任何省略、类比或模糊表述**：  
   - **PRD核心业务规则**：必须包含**场景（如“登录页”）、时机（如“点击登录按钮时”）、所有规则（如“6位数字验证码”“5分钟有效期”）、约束（如“提示文案”）**；  
   - **TRD技术实现细节**：必须包含**对应业务规则的落地逻辑（如“Login接口校验code参数长度与格式”“verify_code表存储过期时间”）**，且需与业务规则**一一对应**。 
# 【禁止性约束（强制红线）】  
- ❌ **禁止遗漏业务上下文**：必须保留PRD中的“业务角色”“场景”“时机”“所有规则”“约束”（如PRD要求“6位数字验证码”，则规范中必须完整写“6位数字验证码”，不得简化为“验证码”）；  
- ❌ **禁止技术细节孤立**：技术实现需与业务规则强关联（如“PRD要求验证码5分钟有效，所以TRD中verify_code表存储创建时间，接口校验当前时间≤创建时间+5分钟”）；  
- ❌ **禁止模糊表述**：模块、字段、接口名需与PRD/TRD完全一致（如“用户端APP”“Login接口”“verify_code表”）；  
- ❌ **禁止类比/省略描述**：即使规则与其他需求重复，也需**完整复述所有内容**（如PRD-002要求“注册验证码规则同登录”，则规范中必须完整写出“6位数字、5分钟有效”，不得使用“同登录规则”）；**若违反此条，该规范直接无效**。  
# 【Few-Shot示例】  
## 场景背景：  
PRD需求是“用户端APP提交订单时，需填写包含省、市、区的收货地址，且地址需非空；订单服务需存储完整地址。PC端提交订单逻辑同APP端。”；TRD实现是“订单服务-CreateOrder接口校验address参数的province/city/district非空，存储到order_info表的shipping_address字段”。  
## ❌ Bad Case1（问题：丢失业务角色与业务规则，仅描述技术实现）  
```json 
{ 
  "specification_id": "TRD-001", 
  "related_requirement_id": "PRD-001", 
  "module": "订单服务-CreateOrder接口、order_info表", 
  "specific_requirements": "CreateOrder接口校验address参数的province/city/district非空；order_info表新增shipping_address字段存储地址"
} 
```  
**问题分析**：  
- 未提及PRD中的「业务角色」（用户端APP）；  
- 未关联「业务规则」（用户端需填写三级地址）与技术实现的逻辑关系（因为用户端要填，所以接口要校验）； 
## ✅ Good Case（正确：覆盖业务+技术，逻辑闭环）  
```json 
{ 
  "specification_id": "TRD-001", 
  "related_requirement_id": "PRD-001", 
  "module": "用户端APP、订单服务-CreateOrder接口、order_info表", 
  "specific_requirements": "1. PRD业务规则：用户端APP提交订单时，需填写包含省、市、区的收货地址，地址字段非空；2. TRD技术实现：订单服务-CreateOrder接口校验address参数的province/city/district字段非空"
} 
```  
## ❌ Bad Case2（类比/省略） 
```json 
{ 
  "specification_id": "TRD-002", 
  "related_requirement_id": "PRD-002", 
  "module": "PC端、订单服务-CreateOrder接口、order_info表", 
  "specific_requirements": "1. PRD业务规则：PC端提交订单逻辑同APP端。2. TRD技术实现：订单服务-CreateOrder接口校验address参数的province/city/district字段非空"
} 
``` 
## ✅ Good Case（完整/无省略）  
```json 
{ 
  "specification_id": "TRD-002", 
  "related_requirement_id": "PRD-002", 
  "module": "PC端、订单服务-CreateOrder接口、order_info表", 
  "specific_requirements": "1. PRD业务规则：PC端提交订单时，需填写包含省、市、区的收货地址，地址字段非空；2. TRD技术实现：订单服务-CreateOrder接口校验address参数的province/city/district字段非空"
} 
```  
# 【输出格式要求】  
严格遵循以下JSON数组格式，确保json合法（注意必要的双引号转义不能丢失）：  
```json 
[ 
  { 
    "specification_id": "TRD-XXX", // 技术规范ID（唯一） 
    "related_requirement_id": "PRD-XXX", // 关联PRD需求ID 
    "module": "业务角色1、技术模块1、技术模块2", // 如“用户端APP、订单服务-CreateOrder接口、order_info表” 
    "specific_requirements": "1. PRD核心业务规则；2. TRD技术实现细节"// 分点覆盖业务+技术，无任何省略 
  } 
] 
```