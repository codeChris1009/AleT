import asyncio
import os
import time
import json
import logging
import httpx
from dotenv import load_dotenv

# 1. 專業日誌系統
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
    handlers=[
        logging.FileHandler("alet.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("alet-one-brain")

async def ollama_request(model, messages, think_off=True):
    url = "http://127.0.0.1:11434/api/chat"
    payload = {
        "model": model,
        "messages": messages,
        "stream": True,
        "options": {
            "temperature": 0,
            "num_ctx": 2048
        }
    }
    if think_off: payload["think"] = False
    
    try:
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("POST", url, json=payload) as response:
                async for line in response.aiter_lines():
                    if not line: continue
                    data = json.loads(line)
                    if "message" in data and "content" in data["message"]:
                        yield data["message"]["content"]
                    if data.get("done", False): break
    except Exception as e:
        logger.error(f"Ollama API 錯誤: {e}")

async def main():
    load_dotenv()
    model_name = os.getenv("SUMMARY_MODEL", "qwen3.5:4b")
    muto_url = os.getenv("MUTO_URL", "http://localhost:8000/sse")

    print(f"\n[Ready] 單核心極速修復版已啟動。")

    # 100% 靜態 Prompt (誘發 Ollama 的 Prefix Caching)
    # 修改導引，讓它同時回傳姓名
    ROUTER_SYSTEM = """你是一個工具導航員。
請判斷使用者是否需要打招呼：
如果是，請回傳: CALL_HELLO:姓名
如果否，請回傳: JUST_CHAT
請只回傳標籤內容，不要解釋。範例：CALL_HELLO:王小明"""

    while True:
        user_input = input("\n[詢問]: ")
        if user_input.lower() in ["exit", "quit"]: break
        if not user_input.strip(): continue

        # --- 第一階段：意圖判定 ---
        logger.info(f"偵測意圖中...")
        step_a_start = time.time()
        
        router_msgs = [
            {"role": "system", "content": ROUTER_SYSTEM},
            {"role": "user", "content": user_input}
        ]
        
        intent_res = ""
        async for chunk in ollama_request(model_name, router_msgs):
            intent_res += chunk
        
        duration_a = time.time() - step_a_start
        logger.info(f"[Intent] 判定結果: {intent_res.strip()} | 耗時: {duration_a:.2f}s")

        if "CALL_HELLO" in intent_res.upper():
            # 動態提取姓名 (切割 CALL_HELLO:姓名)
            target_name = "訪客"
            if ":" in intent_res:
                target_name = intent_res.split(":")[1].strip()
            
            logger.info(f"執行遠端工具，對象: {target_name}")
            
            # 向 MuTO 請求
            # 這裡我們模擬向 MuTO 發送，實際上 MuTO 那邊也可以同步接收這個參數
            res = f"Hello {target_name} from MuTO Skills! (SSE Connection Successful)"
            
            # --- 第二階段：總結回覆 ---
            summary_start = time.time()
            summ_msgs = [
                {"role": "system", "content": "你是一個專業助手，請根據資料內容對使用者給予一句話回覆。"},
                {"role": "user", "content": f"搜尋資料：{res}\n問題：{user_input}"}
            ]
            print(f"[AI]: ", end="", flush=True)
            first_token = False
            async for chunk in ollama_request(model_name, summ_msgs):
                if not first_token:
                    first_token = True
                print(chunk, end="", flush=True)
            print()
            logger.info(f"[Worker] 耗時: {time.time() - summary_start:.2f}s")
        else:
            print(f"[AI]: ", end="", flush=True)
            async for chunk in ollama_request(model_name, [{"role": "user", "content": user_input}]):
                print(chunk, end="", flush=True)
            print()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"錯誤: {e}", exc_info=True)
