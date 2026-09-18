---
name: arlo-verify-finish
description: Arlo 项目的验证与收尾流程：按改动风险运行 ruff、pytest 和必要的手动验收，区分失败与环境阻塞；只有用户明确授权时才提交或推送。当用户说“验证并提交”“跑测试”“收尾”，或 arlo-stage 进入验证阶段时使用。
---

# Arlo 验证与收尾（Verify & Finish）

Arlo 项目编码改动的验证与收尾 SOP，供编码类任务收尾，也可单独触发。

## 流程（按顺序执行）

1. **建立范围基线**：检查 `git status`、`git diff --name-only` 和当前任务边界，保留用户已有改动，不清理无关文件。
2. **同步版本信息**：读取 `CHANGELOG.md` 最新版本、`README.md` 展示版本和 `pyproject.toml` 的 `[project].version`；按 `AGENTS.md` 的规则决定 PATCH 或 MINOR 递增，更新三处并确认完全一致。版本同步发生在暂存和提交之前。
3. **验证**：按 [references/verify.md](references/verify.md) 和 `AGENTS.md` 的要求运行 `ruff check`、`ruff format --check`、`pytest`；文档任务检查 Markdown、链接、UTF-8 和敏感信息。
4. **失败分类**：区分本轮回归、既有基线和环境无法验证，不把未执行写成通过。
5. **失败处理**：本轮范围内的失败先修复并重跑；超出范围的问题记录，不顺手扩大任务。
6. **验收门**：按 [references/acceptance.md](references/acceptance.md) 的模板给出改动摘要与测试结果，等待用户手动验收。
   - 验收不通过：回到修改，循环直至通过。
   - 验收通过：继续。
7. **提交**：只有用户明确要求提交时，才按 [references/commit.md](references/commit.md) 检查改动范围、拆分 commit、填写信息并提交；提交前再次确认三处版本一致。
8. **推送确认**：推送必须获得用户单独明确确认；不因“收尾”或“完成”自动推送。
9. **收尾说明**：报告修改范围、版本号、验证结果、未验证项、已知限制和下一步建议。

## 硬性规则

- 未获用户明确验收通过，不得提交；推送还需要单独明确确认。
- 推送必须获得用户单独明确确认。
- 不提交与当前任务无关的改动，不夹带无关重构。
- 推送前确认当前分支与改动范围。
