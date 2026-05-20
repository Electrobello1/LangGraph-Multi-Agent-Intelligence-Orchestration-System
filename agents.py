from Tools import *
from state import A3State
from model import generate_llm_response

def repo_analyzer(state: A3State):
    """
      ROLE: Fetch raw repository data ONLY
      RESPONSIBILITY:
      - Read README
      - Fetch metadata (stars, forks, language)
      """
    readme = read_github_repo(state["repo_url"])
    meta = get_repo_metadata(state["repo_url"])

    return {
        "readme": readme,
        "stars": meta["stars"],
        "forks": meta["forks"],
        "language": meta["language"]
    }


def content_agent(state: A3State):
    """
       ROLE: Extract structured content from README
       RESPONSIBILITY:
       - title extraction
       - summary extraction
       - NO reasoning, NO scoring
       """
    return {
        "title": extract_title(state["readme"]),
        "summary": extract_summary(state["readme"])
    }


def metadata_agent(state: A3State):
    """
       ROLE: Extract tags ONLY
       RESPONSIBILITY:
       - keyword extraction
       - no summarization
       """
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
    """
     ROLE: Evaluate README quality ONLY
     RESPONSIBILITY:
     - scoring
     - completeness check
     """
    return {
        "quality_score": readme_quality_score(state["readme"])
    }



def llm_enrichment_agent(state):
    #
    #    ROLE: Natural language reasoning ONLY
    #    RESPONSIBILITY:
    #    - answer questions
    #    - improve summary when asked
    #
    #

    # =========================
        # EXTRACT STATE
        # =========================

        title = state.get("title", "")
        summary = state.get("summary", "")
        tags = state.get("tags", [])
        quality = state.get("quality_score", 0)
        stars = state.get("stars", 0)
        language = state.get("language", "")
        missing_sections = state.get("missing_sections", [])
        review_feedback = state.get("review_feedback", {})
        readme = state.get("readme", "")
        forks=state.get("forks", 0)
        user_question = state.get("user_question", "")



        if user_question:
            prompt = f"""
    You are an AI repository assistant.

    Answer the user's question ONLY using the repository information below.

    =========================
    REPOSITORY INFORMATION
    =========================

    TITLE:
    {title}

    SUMMARY:
    {summary}

    TAGS:
    {tags}

    QUALITY SCORE:
    {quality}

    STARS:
    {stars}
    forks:
    {forks}
    LANGUAGE:
    {language}

    MISSING SECTIONS:
    {missing_sections}

    REVIEW FEEDBACK:
    {review_feedback}

    README:
    {readme[:4000]}

    =========================
    USER QUESTION
    =========================

    {user_question}

    Provide a clear, professional, and concise response.
    """

            response = generate_llm_response(prompt)


            return {
                "llm_response": response.strip()
            }

def reviewer(state: A3State):
    """
      ROLE: Decide if output is good or needs retry
      RESPONSIBILITY:
      - validation
      - confidence scoring
      - retry decision
      """
    MAX_RETRIES = 2

    title = state.get("title") or "Untitled Project"

    reviewer_summary = (
       state.get("llm_improved_summary")
      or state.get("summary")
        or ""
    )

    tags = state.get("tags") or []
    quality_score = state.get("quality_score") or 0
    stars = state.get("stars") or 0
    missing_sections = state.get("missing_sections") or []

    feedback = {}

    # STRICT RULES
    if title == "Untitled Project":
        feedback["title"] = "weak"

    if len(reviewer_summary) < 40:
        feedback["summary"] = "too short"

    if not isinstance(tags, list) or len(tags) < 3:
        feedback["tags"] = "insufficient"

    if quality_score < 3:
        feedback["quality"] = "low"

    if stars < 5:
        feedback["popularity"] = "low stars"

    if missing_sections:
        feedback["structure"] = "incomplete"

    issues = len(feedback)

    penalties = {
        "title": 0.25,
        "summary": 0.25,
        "tags": 0.20,
        "quality": 0.15,
        "popularity": 0.10,
        "structure": 0.30
    }

    confidence = 1.0
    for k in feedback:
        confidence -= penalties.get(k, 0.1)

    confidence = max(0.0, confidence)
    confidence = round(confidence, 2)

    attempts = state.get("attempts", 0) + 1
    prev = state.get("prev_issue_count", issues + 1)

    critical_failure = (
        "title" in feedback or
        "summary" in feedback or
        "tags" in feedback
    )

    should_retry = (
        attempts < MAX_RETRIES and
        (critical_failure or issues > prev)
    )

    if should_retry:
        status = "retry"

    else:
        status = "pass"

    return {
        "review_feedback": feedback,
        "status": status,
        "attempts": attempts,
        "confidence": confidence,
        "prev_issue_count": issues
    }