# Public Release Boundary / 公开版边界

## 中文

`CivicMarketEngine` 是非商业、可公开查看的脱敏演示包。它不是私有研究工作区的原样复制。

公开版可以放：

- 离线演示。
- 公开说明、许可、归属和最小示例。
- 不暴露真实提示词、内部边界材料和完整私有运行时的安全源码。

公开版不能放：

- 真实提示词和提示词调试策略。
- `AGENTS.md` 以及内部 LLM/代码边界说明。
- 内部实验入口、阶段报告和长时间运行矩阵。
- LLM 运行输出、结果数据库、表格、日志、缓存和本地结果目录。
- 密钥、完整本机路径和任何只适合私有仓库保存的材料。

一句话理解：这个仓库能让外部读者看懂项目想解决什么问题、能跑一个离线小演示，但不会公开私有决策口径和正式实验证据链。

## English

`CivicMarketEngine` is the noncommercial, source-visible, sanitized public demo package. It is not a full copy of the private research workspace.

The public package may include:

- Offline demos.
- Public documentation, licensing, attribution, and minimal examples.
- Safe source files that do not expose real prompts, internal boundary material, or the full private runtime.

The public package must not include:

- Real prompts or prompt tuning strategy.
- `AGENTS.md` or internal LLM/code boundary notes.
- Internal experiment entrypoints, stage reports, or long-run matrices.
- LLM run outputs, result databases, spreadsheets, logs, caches, or local result folders.
- Secrets, full local machine paths, or anything that belongs only in the private repository.

In plain terms: this repository should help outside readers understand the idea and run a small offline demo, without exposing the private decision boundary or formal experiment evidence chain.
