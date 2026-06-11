# CivicMarketEngine

## 中文

`CivicMarketEngine` 是一个非商业、脱敏的房地产市场模拟演示包。

它想回答的不是“明天房价涨不涨”，也不是“你该买哪套房”。它更像一个复盘工具，帮我们把一句很笼统的话拆开：市场到底冷不冷，为什么你看中的那套房还是不便宜，为什么有些房子能成交，有些房子谈着谈着就停住了。

现实里买房、卖房，很容易被一句“市场冷”或“市场热”带走。但真正落到一套房上，还是要回到几个笨问题：

- 谁会来买？
- 这些人的预算够不够？
- 同地段、同价位、同户型的替代房多不多？
- 卖家愿不愿意让价？
- 谈判最后有没有真的走到交割？

这个公开仓库保留的是可以公开看的外壳、说明、离线演示和少量安全源码。完整私有研究工作区、真实提示词、内部报告、长时间运行结果和关键边界材料没有放进来。

## English

`CivicMarketEngine` is a source-visible, noncommercial, sanitized demo package for a real-estate market simulation project.

It is not here to tell you whether prices will rise tomorrow, and it does not tell anyone which home to buy. Think of it more as a review tool: it breaks a vague market sentence into concrete questions. Is the market really cold? Why is one home still hard to bargain down? Why do some deals close while others stop halfway?

In real housing decisions, it is easy to get pulled around by big labels like "hot market" or "cold market". For one specific home, the better questions are simpler:

- Who might actually buy it?
- Can those buyers afford it?
- How many similar homes can replace it?
- Is the seller willing to move on price?
- Does the negotiation reach a real closing step?

This public repository keeps the parts that are safe to share: public-facing notes, an offline demo, packaging checks, and a small set of non-sensitive helper files. The private research workspace, real prompts, internal reports, long-run outputs, and key boundary materials are intentionally left out.

## 快速运行 / Quick Check

```bash
python scripts/check_public_snapshot.py .
python scripts/public_smoke_test.py --rounds 1 --seed 42
```

中文：这个 smoke 是离线的，只检查公开包能不能跑通，以及能不能生成临时的 `simulation.db` 和 `01_result_bundle.xlsx` 形态文件。它不是正式实验结果，也不是投资建议。

English: This smoke test is offline. It only checks that the public package can run and create temporary `simulation.db` and `01_result_bundle.xlsx` shaped artifacts. It is not a formal experiment result and it is not investment advice.

## 这个公开版包含什么 / What Is Included

- 中文：离线演示、公开说明、非商业许可、归属说明、脱敏检查器，以及少量安全源码。
- English: An offline demo, public documentation, noncommercial licensing, attribution notes, a redaction checker, and a small set of safe source files.

## 这个公开版不包含什么 / What Is Not Included

- 中文：真实提示词、内部边界文档、完整私有运行时、长时间运行结果、数据库、表格、日志、密钥和本地结果目录。
- English: Real prompts, internal boundary documents, the full private runtime, long-run outputs, databases, spreadsheets, logs, secrets, and local result folders.

## 许可 / License

中文：本公开包使用 PolyForm Noncommercial License 1.0.0。商业使用需要单独授权。

English: This public package is distributed under the PolyForm Noncommercial License 1.0.0. Commercial use requires separate permission.
