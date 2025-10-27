# mcp-gdscript 開発ガイド

このファイルはプロジェクト開発時の動作確認と トラブルシューティング手順を記載しています。

## 動作確認手順

### 1. ローカル開発環境での確認

**推奨:** uv を使用（グローバル環境を汚さない）

```bash
# uv 環境でサーバー起動テスト
uv run mcp-gdscript
```

予想される出力:
- MCP サーバーが起動し、標準入力からのメッセージを待機する状態になります


### 2. uvx での直接実行確認

GitHub からのインストール版を直接テストできます:

```bash
# 最新版を uvx で実行
uvx mcp-gdscript@git+https://github.com/minami110/mcp-gdscript

# または PyPI リリース版を実行（リリース後）
uvx mcp-gdscript
```

#### 依存関係エラーの対処

**エラー例:**
```
× No solution found when resolving tool dependencies:
╰─▶ Because there is no version of mcp==1.3.1 ...
```

**原因:** `pyproject.toml` で指定されている mcp のバージョンが存在しない

**解決方法:**
1. `pyproject.toml` の `dependencies` セクションを確認
2. mcp バージョンを最新の安定版に更新

```toml
# 修正前
dependencies = [
    "mcp==1.3.1",  # ❌ このバージョンは存在しない
    "tree-sitter-language-pack==0.3.9",
]

# 修正後
dependencies = [
    "mcp>=1.19.0",  # ✅ 最新の安定版を指定
    "tree-sitter-language-pack==0.3.9",
]
```

利用可能なバージョンは [PyPI mcp](https://pypi.org/project/mcp/#history) で確認できます。

### 3. 他プロジェクトでの利用確認

別のプロジェクトで MCP サーバーとして利用する場合:

**設定ファイル**: `.claude/mcp.json` または `~/.claude/mcp.json`

```json
{
  "mcpServers": {
    "gdscript": {
      "command": "uvx",
      "args": ["mcp-gdscript@git+https://github.com/minami110/mcp-gdscript"]
    }
  }
}
```

#### 利用確認方法

1. Claude コード内で確認
2. 以下のコマンドで CLI から確認:

```bash
# mcp.json が有効か確認
cd /path/to/another-project
uvx mcp-gdscript@git+https://github.com/minami110/mcp-gdscript
```

## トラブルシューティング

### エラー: "Module not found: mcp"

**原因:** 依存パッケージがインストールされていない

**解決方法:**
```bash
# uv で依存関係を再解決
uv sync

# または uv で実行
uv run mcp-gdscript
```

### エラー: "Python version 3.10 or higher required"

**原因:** Python バージョンが 3.10 未満

**確認方法:**
```bash
python --version  # 3.10 以上である必要があります
```

**解決方法:**

uv は Python バージョンの管理も含まれているため、以下で自動的に解決されます:
```bash
uv run mcp-gdscript  # 必要な Python バージョンがあれば自動検出
```

手動で Python 3.10+ に切り替える場合:
```bash
# Python 3.10 が利用可能か確認
python3.10 --version

# Python 3.10 を指定して実行
uv run --python 3.10 mcp-gdscript
```

### エラー: "tree-sitter-language-pack version mismatch"

**原因:** tree-sitter-language-pack のバージョン不一致

**解決方法:**
```bash
# uv で依存関係をリセット
uv sync --refresh

# またはキャッシュをクリアして再実行
rm -rf .venv
uv run mcp-gdscript
```

## デバッグ方法

### ログ出力を有効化

```bash
# 詳細ログを表示
RUST_LOG=debug mcp-gdscript

# または
RUST_LOG=debug uvx mcp-gdscript@git+https://github.com/minami110/mcp-gdscript
```

### テスト実行

```bash
# uv で全テスト実行
uv run pytest

# 特定のテストのみ実行
uv run pytest tests/test_analyzer.py -v

# 詳細出力でテスト実行
uv run pytest -vv
```

## 開発時の確認チェックリスト

- [ ] `uv run mcp-gdscript` でローカル実行できる
- [ ] `uvx mcp-gdscript@git+...` で uvx 実行できる
- [ ] `uv run pytest` で全テストがパスする
- [ ] `uv run black .` でコード整形が通る
- [ ] `uv run ruff check .` で linter が通る
- [ ] 他プロジェクトの mcp.json で認識される
- [ ] MCP サーバーとして起動できる

## 参考リンク

- [MCP 公式ドキュメント](https://modelcontextprotocol.io/)
- [PyPI mcp パッケージ](https://pypi.org/project/mcp/)
- [tree-sitter](https://tree-sitter.github.io/tree-sitter/)
- [GDScript ドキュメント](https://docs.godotengine.org/en/stable/getting_started/scripting/gdscript/index.html)
