# Project Configuration 專案配置說明：alet

本專案採用現代化 Python 開發標準，使用 pyproject.toml 進行依賴管理與工具設定

## 1. Project Metadata 專案基本資訊

定義專案的身分證，讓開發工具知道如何處理這個專案

- **Name 專案名稱**：alet
- **Version 專案版本**：0.1.0（初始開發版本）
- **Requires-python Python 版本要求**：<br/>
  設定為 >=3.13這代表專案可以使用 Python 3.13 引入的最新效能優化與語法（如改良後的 JIT 編譯 與更強大的 TaskGroup）

## 2. Dependencies 生產環境依賴

## 核心運行套件清單

這些套件是程式「運行」時必須安裝的核心組件：

| Package 套件名稱  | Purpose 用途說明                                                                    |
| ----------------- | ----------------------------------------------------------------------------------- |
| FastAPI           | Core Framework 核心框架負責路由管理、自動產生 Swagger API 文件與非同步請求處理      |
| Uvicorn           | ASGI Server 伺服器引擎在底層驅動 FastAPI 運作，負責與網路協定溝通                   |
| SQLAlchemy        | Database ORM 資料庫工具將資料庫資料表對應成 Python 物件，避免手動撰寫原始 SQL       |
| Asyncpg           | PostgreSQL Async Driver 異步驅動專門為 PostgreSQL 設計的高效能異步驅動程式          |
| Alembic           | Migration Tool 資料庫遷移管理資料庫結構版本（如新增欄位），確保團隊資料庫結構一致   |
| Greenlet          | Worker Helper 協程輔助SQLAlchemy 在執行異步操作時，必須依賴它來切換 Python 執行狀態 |
| Pydantic-settings | Settings Management 設定管理自動讀取環境變數（如資料庫連線字串）並確保其格式正確    |
| Pydantic[email]   | Data Validation 資料驗證延伸 Pydantic 功能，增加嚴格的 Email 格式驗證               |
| Python-dotenv     | Env Loader 環境變數載入將 .env 檔案中的變數載入到系統環境中                         |
| PyJWT             | Auth Token 認證令牌用於處理使用者登入後的 JWT 簽發與驗證                            |
| Passlib[bcrypt]   | Security 加密安全提供安全的雜湊演算法（Bcrypt），確保資料庫不儲存明文密碼           |
| Httpx             | HTTP Client 請求工具讓後端可以發送請求給其他第三方 API，支援異步模式                |
| Pytest            | Test Framework 測試框架撰寫單元測試與整合測試，確保程式邏輯正確                     |

## 3. Dependency Groups 開發環境工具

這類套件只在開發程式碼時需要，部署到伺服器運行時不會安裝

Ruff：Linter & Formatter 檢查與排版目前 Python 社群公認最快的工具，能同時檢查語法錯誤並自動調整程式碼格式

## 4. Ruff Tool Configuration 工具細節設定

為了統一程式碼風格，專案啟用了以下規則：

[Tool.ruff] 基礎設定
Line-length = 88：設定每行程式碼最大長度為 88 個字元（符合 PEP 8 規範且最通用的標準）

Target-version = "py313"：指定 Python 3.13 語法標準，避免誤判新語法為錯誤

[Tool.ruff.lint] 代碼檢查規則
Select = ["E", "F", "I"]：

E (Error)：偵測違反 PEP 8 的一般錯誤

F (Pyflakes)：偵測嚴重的邏輯錯誤（如未定義的變數）

I (Isort)：自動排序 import 語句，確保檔案上方匯入順序整齊

Ignore = []：保持最嚴謹檢查，不忽略任何警告

[Tool.ruff.format] 排版格式設定
Quote-style = "double"：強制使用 雙引號 "，減少單雙引號混用的混亂

## COMMAND 套件指令操作

### Manual Execution 手動執行

安裝與同步所有套件：

```Bash
uv sync
```

Check 檢查錯誤：

```Bash
uv run ruff check .
```

Fix 自動修正：這會幫你修正一些簡單的語法錯誤（例如未使用的變數）

```Bash
uv run ruff check --fix .
```

Format 自動排版：這會調整程式碼的間距、括號等外觀，使其符合標準

```Bash
uv run ruff format .
```
