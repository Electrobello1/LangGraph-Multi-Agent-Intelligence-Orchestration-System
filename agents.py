from Tools import *
from state import A3State


def repo_analyzer(state: A3State):
    readme = read_github_repo(state["repo_url"])
    meta = get_repo_metadata(state["repo_url"])

    return {
        "readme": readme,
        "stars": meta["stars"],
        "forks": meta["forks"],
        "language": meta["language"]
    }


def content_agent(state: A3State):
    return {
        "title": extract_title(state["readme"]),
        "summary": extract_summary(state["readme"])
    }


def metadata_agent(state: A3State):
    return {
        "tags": extract_tags(state["readme"])
    }


def structure_critic(state: A3State):
    readme = state["readme"].lower()

    required = ["installation", "usage", "example", "license"]
    missing = [r for r in required if r not in readme]

    return {
        "missing_sections": missing,
        "improvements": [f"Add section: {r}" for r in missing]
    }


def quality_agent(state: A3State):
    return {
        "quality_score": readme_quality_score(state["readme"])
    }


def reviewer(state: A3State):

    feedback = {}

    if state["title"] == "Untitled Project":
        feedback["title"] = "weak"

    if len(state["summary"]) < 20:
        feedback["summary"] = "too short"

    if len(state["tags"]) < 3:
        feedback["tags"] = "poor"

    if state["quality_score"] < 2:
        feedback["quality"] = "low"

    if state["stars"] < 5:
        feedback["popularity"] = "low stars"

    if state["missing_sections"]:
        feedback["structure"] = "incomplete"

    issues = len(feedback)

    confidence = 1.0
    confidence -= 0.2 if "title" in feedback else 0
    confidence -= 0.2 if "summary" in feedback else 0
    confidence -= 0.2 if "tags" in feedback else 0
    confidence -= 0.4 if "structure" in feedback else 0
    confidence = max(0.0, confidence)

    prev = state.get("prev_issue_count", 999)

    attempts = state.get("attempts", 0) + 1

    status = (
        "pass"
        if issues == 0 or issues < prev or confidence >= 0.75 or attempts >= 2
        else "retry"
    )

    return {
        "review_feedback": feedback,
        "status": status,
        "attempts": attempts,
        "confidence": confidence,
        "prev_issue_count": issues
    }