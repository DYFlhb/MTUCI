import aiohttp
import asyncio
import csv
from datetime import datetime
from aiohttp import ClientConnectionError
from tabulate import tabulate

urls = [
    "https://example.com",
    "https://httpbin.org/get",
    "https://www.python.org",
    "https://badurl.test"
]

attempts = 5
sem = asyncio.Semaphore(2)
results = []


async def fetch(session, url):
    result = {
        "url": url,
        "status": None,
        "length": None,
        "error": None,
        "attempts_used": 0,
        "success": False
    }

    async with sem:
        for attempt in range(1, attempts + 1):
            result["attempts_used"] = attempt
            try:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    text = await response.text()
                    result["status"] = response.status
                    result["length"] = len(text)
                    result["success"] = True
                    result["error"] = None
                    print(f"{url} — статус: {response.status}, длина: {len(text)} символов")
                    break
            except ClientConnectionError:
                result["error"] = "Connection error"
                print(f'{url} - недоступен, {attempt} попытка запроса')
            except asyncio.TimeoutError:
                result["error"] = "Timeout error"
                print(f'{url} - превышено время ожидания, {attempt} попытка запроса')
            except aiohttp.ClientError as e:
                result["error"] = f"Client error: {str(e)}"
                print(f'{url} - клиентская ошибка, {attempt} попытка запроса')
            except Exception as e:
                result["error"] = str(e)
                print(f'{url} - {e}, {attempt} попытка запроса')

        results.append(result)


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        await asyncio.gather(*tasks)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"results_{timestamp}.csv"

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["URL", "Status", "Length", "Attempts", "Success", "Error"])
        for r in results:
            writer.writerow([
                r["url"],
                r["status"] if r["success"] else "",
                r["length"] if r["success"] else "",
                r["attempts_used"],
                "Yes" if r["success"] else "No",
                r["error"][:100] if r["error"] else ""
            ])

    print(f"\nРезультаты сохранены в файл: {filename}")

    successful = sum(1 for r in results if r["success"])
    failed = len(results) - successful
    print(f"\nСтатистика: Успешно: {successful}, Неудачно: {failed}")


if __name__ == "__main__":
    asyncio.run(main())