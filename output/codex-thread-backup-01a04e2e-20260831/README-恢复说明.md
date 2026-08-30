# Codex 对话迁移包

本包用于恢复以下 Codex Desktop task：

- 标题：`这是最新的LASS要投稿的工作；熟悉我们在干什么`
- 主 thread ID：`01a04e2e-68b9-7043-b462-15f9a38273ab`
- 原工作区：`/Users/tanghaohan/Desktop/ALL/thh/research/LASS-2026`
- Git 仓库：`git@github.com:slkdyXP/LASS-2026.git`
- 原 Codex CLI schema 版本：`0.146.0-alpha.9.2`

包内包含主对话 rollout、3 个内部审计子任务、相关 shell snapshot、该线程生成的图像，以及用于合并到 `state_5.sqlite` 的元数据。包内不包含 `auth.json`、API key、账号凭据、浏览器数据、Codex 配置或其他聊天。

## 在另一台 Mac 上恢复

1. 安装 Codex Desktop，登录账号，并至少启动一次，让它创建 `~/.codex/state_5.sqlite`。
2. 将项目仓库 clone 或复制到目标电脑，例如：

   ```bash
   git clone git@github.com:slkdyXP/LASS-2026.git /path/to/LASS-2026
   ```

3. 完全退出 Codex Desktop。不要只关闭窗口。
4. 解压本迁移包，在解压目录执行：

   ```bash
   python3 restore_thread.py --workspace "/path/to/LASS-2026"
   ```

5. 重新启动 Codex Desktop，在任务列表中查找：

   ```text
   这是最新的LASS要投稿的工作；熟悉我们在干什么
   ```

如果界面没有立即显示，可尝试在终端运行：

```bash
codex resume 01a04e2e-68b9-7043-b462-15f9a38273ab
```

恢复脚本不会覆盖整套 Codex 数据库。它会先备份目标电脑的 `state_5.sqlite`，然后只插入或更新本包的 4 条 thread 记录，并复制对应 rollout 文件。已有其他聊天不会被删除。

## 重要说明

- 迁移包恢复的是对话和 Codex task 元数据，不包含项目工作区本身，也不会恢复未提交的代码修改。请另行迁移或同步 LASS-2026 仓库。
- rollout 会保留历史工具输出和本地路径；`--workspace` 会修正 thread 的工作目录以及每个 rollout 首行的 session cwd，但历史消息里出现的旧绝对路径仍会作为文本保留。
- Codex 内部存储格式可能随版本变化。建议目标电脑使用不低于源电脑的 Codex Desktop 版本。脚本会只写入目标 schema 中实际存在的列。
- 本包未加密，其中包含完整对话、提示词、工具输出及可能出现的本地文件内容。请按敏感研究资料保管，不要公开上传。
- 如果恢复失败，脚本创建的 `~/.codex/state_5.sqlite.pre-thread-restore-时间戳` 是恢复前的数据库备份。
