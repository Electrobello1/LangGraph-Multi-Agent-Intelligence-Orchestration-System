import requests
import re
import base64


def read_github_repo(repo_url: str):
    try:
        parts = repo_url.replace("https://github.com/", "").split("/")
        owner, repo = parts[0], parts[1]

        url = f"https://api.github.com/repos/{owner}/{repo}/readme"
        res = requests.get(url)

        if res.status_code == 200:
            return base64.b64decode(res.json()["content"]).decode("utf-8")
    except:
        pass

    return "No README found"


def get_repo_metadata(repo_url: str):
    try:
        parts = repo_url.replace("https://github.com/", "").split("/")
        owner, repo = parts[0], parts[1]

        url = f"https://api.github.com/repos/{owner}/{repo}"
        res = requests.get(url)

        if res.status_code == 200:
            data = res.json()
            return {
                "stars": data.get("stargazers_count", 0),
                "forks": data.get("forks_count", 0),
                "language": data.get("language", "unknown")
            }
    except:
        pass

    return {"stars": 0, "forks": 0, "language": "unknown"}


def readme_quality_score(readme: str):
    score = 0
    if len(readme) > 500:
        score += 1
    if "##" in readme:
        score += 1
    if "```" in readme:
        score += 1
    return score


def extract_title(readme):
    for line in readme.split("\n"):
        if line.startswith("#"):
            return line.replace("#", "").strip()
    return "Untitled Project"

def extract_summary(readme):
    if not readme:
        return "No summary available"

    # remove markdown headers
    text = re.sub(r"^#+\s*", "", readme, flags=re.MULTILINE)

    # remove bullet points
    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip() and not line.strip().startswith(("-", "*"))
    ]

    text = " ".join(lines)

    # split into sentences (simple but effective)
    sentences = re.split(r"(?<=[.!?])\s+", text)

    summary = []
    length = 0
    MAX_LEN = 400


    for s in sentences:
        if length + len(s) > MAX_LEN:
            break
        summary.append(s)
        length += len(s)

    return " ".join(summary).strip()
def extract_tags(readme):
    words = re.findall(r'\b[a-zA-Z]{4,}\b', readme.lower())

    stopwords = {
        "this","that","with","from","have","will",
        "your","about","using","project","https","http","www","com","lesson"
    }

    keywords = [w for w in words if w not in stopwords]

    freq = {}
    for w in keywords:
        freq[w] = freq.get(w, 0) + 1

    return sorted(freq, key=freq.get, reverse=True)[:5]