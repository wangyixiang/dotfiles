---
name: function-level-defect-tracer
description: 基于 MR 的 source commit id 与 target commit id，对本次 MR 变更内容进行差异分析与定位（文件/函数级），输出变更摘要、关键 diff 片段索引与风险点，供缺陷校验使用。
---

# function-level-defect-tracer

## Goal
对指定 commit 范围（source..target）进行变更分析，产出“本次 MR 变更包”，包括：变更文件清单、关键 diff、涉及函数/接口、潜在影响面与风险标注。

## When to use
- 对缺陷检测系统报告的缺陷进行校验前，需要先明确本次 MR 改了什么。
- 需要验证缺陷是否由本次 MR 引入（或是否已在 MR 中修复/回归）。

## Inputs
- repo_path: 本地仓库路径。
- source_commit_id: MR source commit id。
- target_commit_id: MR target commit id。
- optional:
  - focus_files: 缺陷报告涉及的文件列表（优先分析）。
  - focus_symbols: 缺陷报告涉及的函数/方法名列表（优先分析）。
  - diff_granularity: file | function（默认 function）。

### Input example
```json
{
  "repo_path": "/path/to/repo",
  "source_commit_id": "abc123",
  "target_commit_id": "def456",
  "focus_files": ["dash_board_action.go"],
  "focus_symbols": ["QueryConversationDispatch"],
  "diff_granularity": "function"
}
```

## Outputs
- commit_range: {source, target}
- changed_files: [{path, change_type, stats(add/del), hunks_count}]
- function_level_changes: [{symbol, file_path, change_summary, diff_hunks_refs}]
- risk_notes: [{entity, reason}]
- trace_hints: 给 business-defect-assessor 的线索（哪些变更最可能关联缺陷）

### Output example(shape)
```json
{
  "commit_range": {"source": "abc123", "target": "def456"},
  "changed_files": [
    {"path": "dash_board_action.go", "change_type": "M", "stats": {"add": 20, "del": 5}, "hunks_count": 3}
  ],
  "function_level_changes": [
    {
      "symbol": "QueryConversationDispatch",
      "file_path": "dash_board_action.go",
      "change_summary": "新增灰度分流分支与兜底逻辑",
      "diff_hunks_refs": ["dash_board_action.go#HUNK2"]
    }
  ],
  "risk_notes": [
    {"entity": "QueryConversationDispatch", "reason": "核心分发逻辑被改动，且包含条件分支"}
  ],
  "trace_hints": ["优先核对灰度开关含义与分支是否对齐业务规则"]
}
```

## Procedure
1. 验证 commit 存在且可比较。
2. 生成 file-level diff：变更文件、增删行统计、hunk 数。
3. 生成 function-level 索引（能做到就做到）：
   - 对 Go/Java 等可通过简单符号匹配或 AST/ctags 生成函数级差异索引。
   - 若难以精确到函数，至少输出“可能涉及的函数/方法名 + diff hunk 位置”。
4. 对 focus_files / focus_symbols 做优先级排序输出。
5. 标注风险点：核心链路、条件分支、状态机、并发/缓存/一致性相关变更。

## Guardrails
- 只描述“变更事实 + 风险线索”，不判断缺陷对错（留给 assessor）。
- 对于无法稳定提取函数级差异的语言/仓库结构，明确降级策略与不确定性。
