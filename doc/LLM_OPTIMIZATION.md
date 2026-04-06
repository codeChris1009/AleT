# AleT LLM 效能優化與架構說明文件

本文件詳細紀錄了為了達成「無延遲對話體驗」所進行的 LLM 選型與緩存對齊優化歷程。

## 🔍 現況與挑戰
*   **硬體限制**: 8GB VRAM (NVIDIA GPU)。
*   **初步問題**: 使用 9B/7B 模型時，因顯存溢出 (VRAM Overflow) 導致 Ollama 切換至 CPU 慢速模式，首字延遲長達 121 秒。
*   **架構痛點**: 頻繁在多模型 (2B-Router + 4B-Worker) 間切換，導致 Ollama 的 KV Cache 被頻繁清空，判定時間維持在 15 秒以上。

## 🚀 最終解決方案：單核心「前綴緩存 (Prefix Caching)」架構

### 1. 模型選型 (Model Selection)
*   **核心大腦**: `qwen3.5:4b`。
*   **優勢**: 體積極小 (約 3.4GB)，能完美常駐於顯存，並保留足夠空間給作業系統與未來的 Embedding 模型。

### 2. 緩存對齊技術 (Context Alignment)
*   **靜態引導 (Static Prompt)**: 將工具判定的 System Prompt 固定，誘發 Ollama 0.18.3 的「前綴緩存」功能。
*   **效能結果**: 
    *   初次請求 (Cold Start): ~8.0s (計算緩存)。
    *   後續請求 (Cache Hit): **0.7s ~ 1.5s** (秒回判定)。

### 3. API 直接驅動 (Direct API Driver)
*   **去框架化**: 繞過 LangChain 的 `bind_tools` 沉重封裝，改用手動 API 請求，節省了 1.4 秒的物件處理延遲。
*   **參數固定**: 強制 `think: false` (關閉思考模式) 置於 Top-level，防止 0.18.3 版本誤入長生成循環。

## 🏗️ 三位一體預告 (RAG 階段)
*   **領航員/專家**: `qwen3.5:4b` (已實作)。
*   **圖書管理員**: `qwen3-embedding:0.6b` (預計進駐 EIDo)。

---
**維護者備註**: 
未來擴充工具時，請務必保持 `ROUTER_SYSTEM` 引導詞的前綴不變，以維持「秒回」的緩存體感。
