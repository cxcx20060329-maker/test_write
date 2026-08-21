
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request


API_URL = "https://match.yuanrenxue.cn/api/question/19"
REFERER = "https://match.yuanrenxue.cn/match/19"
NORMAL_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/126.0.0.0 Safari/537.36"
)


def fetch_page(
    page: int,
    sessionid: str,
    *,
    timeout: float = 20.0,
    retries: int = 3,
) -> list[int]:
    """请求指定页；第 5 页按题目要求切换 User-Agent。"""
    query = urllib.parse.urlencode(
        {
            "page": page,
            "pageSize": 10,
            "kw": "",
            "m": "",
        }
    )
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Referer": REFERER,
        "User-Agent": "yuanrenxue" if page == 5 else NORMAL_USER_AGENT,
        "X-Requested-With": "XMLHttpRequest",
    }
    if sessionid:
        headers["Cookie"] = f"sessionid={sessionid}"

    request = urllib.request.Request(f"{API_URL}?{query}", headers=headers)
    last_error: Exception | None = None

    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
            values = payload.get("data")
            if not isinstance(values, list) or not values:
                raise ValueError(f"第 {page} 页没有返回有效 data 数组：{payload!r}")
            if not all(isinstance(value, int) for value in values):
                raise ValueError(f"第 {page} 页包含非整数数据：{values!r}")
            return values
        except (OSError, ValueError, json.JSONDecodeError) as error:
            last_error = error
            if attempt < retries:
                time.sleep(0.8 * attempt)

    raise RuntimeError(f"第 {page} 页请求失败（已重试 {retries} 次）：{last_error}")


def solve(sessionid: str) -> int:
    print("=" * 72)
    print("猿人学第 19 题：请求全部 5 页并计算加和")
    print("会话状态：" + ("已携带 sessionid（值不会输出）" if sessionid else "匿名会话验证"))
    print("第 5 页 User-Agent：yuanrenxue")
    print("=" * 72)

    grand_total = 0
    item_count = 0
    for page in range(1, 6):
        values = fetch_page(page, sessionid)
        subtotal = sum(values)
        grand_total += subtotal
        item_count += len(values)
        marker = "  [UA=yuanrenxue]" if page == 5 else ""
        print(f"第 {page} 页{marker}")
        print(f"  数据：{values}")
        print(f"  小计：{subtotal}")

    print("-" * 72)
    print(f"请求成功：5/5 页，共 {item_count} 个数值")
    print(f"最终加和：{grand_total}")
    print("程序运行成功。")
    return grand_total


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sessionid",
        default=os.environ.get("MATCH_SESSIONID", "").strip(),
        help="登录后的 sessionid；也可通过 MATCH_SESSIONID 环境变量传入",
    )
    return parser.parse_args()


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    args = parse_args()
    try:
        solve(args.sessionid)
    except Exception as error:
        print(f"运行失败：{error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
