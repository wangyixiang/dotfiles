import requests
import sys
import json

def get_doc_content(doc_url):
    api_url = "https://test-standardization-backend.byted.org/common/doc/markdown"
    params = {"doc": doc_url}
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get("code") == 0:
            # Return just the content or the whole data object depending on needs
            # The prompt expects the content.
            return data["data"] 
        else:
            print(f"Error: {data.get('message')}", file=sys.stderr)
            return None
    except Exception as e:
        print(f"Exception: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <doc_url>")
        sys.exit(1)
    
    doc_url = sys.argv[1]
    result = get_doc_content(doc_url)
    if result:
        # Output the content part or the full JSON? 
        # The tool output will be read by the agent. 
        # Let's output the content field primarily, or the JSON.
        # The API returns {"title":..., "content":...} in 'data'.
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        sys.exit(1)