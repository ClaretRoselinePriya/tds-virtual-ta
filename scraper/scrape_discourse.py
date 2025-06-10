import requests
import json
import time

BASE_URL = "https://discourse.onlinedegree.iitm.ac.in"
CATEGORY_ID = 34  # TDS Knowledge Base
HEADERS = {
    'Api-Key': 'Ysk-proj-c7nLb111qny-sIYzUlyINNp6_5l7BzyLG3c7-7Sk3ehJiCyZeCNb6Lo7FYu3UMqp7xF88vLx-8T3BlbkFJ72dR6lKgu_KJ3exKR2kEosAgOiEM4fTOyco0cuSOKn6AJ_Do8oCjVFYOBCwJBQaE2G39zC8Z4A',
    'Api-Username': 'CLARET ROSELINE PRIYA V'
}

def get_topics():
    url = f"{BASE_URL}/c/courses/tds-kb/{CATEGORY_ID}.json"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get('topic_list', {}).get('topics', [])
    return []

def get_posts(topic_id):
    url = f"{BASE_URL}/t/{topic_id}.json"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get('post_stream', {}).get('posts', [])
    return []

def main():
    topics = get_topics()
    all_data = []
    for topic in topics:
        topic_id = topic.get('id')
        title = topic.get('title')
        posts = get_posts(topic_id)
        all_data.append({
            'topic_id': topic_id,
            'title': title,
            'posts': posts
        })
        time.sleep(1)

    with open('data/tds_kb_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
