import asyncio
import copy
import time
from statistics import mean

import httpx


async def main(cnt=100):
    question = {
        "number": 1,
        "text": "question",
        "answers_options": [
            {"number": 1, "text": "Answer 1"},
            {"number": 2, "text": "Answer 2"},
            {"number": 3, "text": "Answer 3"},
            {"number": 4, "text": "Answer 4"},
            {"number": 5, "text": "Answer 5"}
        ]
    }

    questions = []

    for x in range(1, 11):
        q = copy.deepcopy(question)
        q['number'] = x
        q['text'] = f'question {x}'
        questions.append(q)

    data = {
        "name": "string",
        "questions": questions,
    }

    headers = {}

    timeout = httpx.Timeout(5.0, pool=None)
    async with httpx.AsyncClient(timeout=timeout) as client:
        res = await client.post("http://0.0.0.0:8080/api/token/", json={"username": "test", "password": "test_pwd"})
        headers['Authorization'] = 'Bearer {}'.format(res.json().get('access'))
        # Create a list of coroutines
        tasks = []

        for x in range(cnt):
            d = data.copy()
            d["name"] = f"Survey {x}"
            tasks.append(client.post("http://0.0.0.0:8080/api/surveys/", json=d, headers=headers))
        
        results = []
        # Execute concurrently and wait for all responses
        concurrently = 100
        for i in range(0, len(tasks), concurrently):
            batch = tasks[i:i+concurrently]
            results.extend(await asyncio.gather(*batch))
            print(f'batch {i}-{i+concurrently}')


        durations = []
        for response in results:
            durations.append(response.elapsed.total_seconds())
            # print(f"Status for {response.url}: [{response.status_code}] Duration: {response.elapsed.total_seconds()} seconds")

        print(f'requests count: {len(results)}')
        print(f'avg_sec: {mean(durations)}, max_sec: {max(durations)}, min_sec: {max(durations)}')


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main(cnt=1000))
    end = time.perf_counter()
    print(f"Duration: {end - start:.4f} seconds")