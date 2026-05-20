from graph import build_graph
import json
from agents import llm_enrichment_agent


if __name__ == "__main__":



    app = build_graph()

    result = app.invoke({
        "repo_url": "https://github.com/Electrobello1/Flask-Chatbot-Using-DialoGPT-and-WhatsAuto-Integration",
        "attempts": 0
    })
    print("\n==============================")
    print("LLM AGENT OUTPUT")
    print("==============================")
    print(result.get("llm_improved_summary"))

    print("\n" + "=" * 60)
    print("🔍 GITHUB REPOSITORY ANALYSIS REPORT")
    print("=" * 60)

    print(f"\n📦 Repository: {result['repo_url']}")
    print(f"⭐ Stars: {result['stars']}")
    print(f"🍴 Forks: {result['forks']}")
    print(f"💻 Language: {result['language']}")

    print("\n📌 Title:")
    print(result['title'])

    print("\n📝Summary:")
    print(result['summary'])

    print("\n🏷️ Tags:")
    print(", ".join(result['tags']))

    print("\n⚠️ Missing Sections:")
    print(", ".join(result['missing_sections']) if result['missing_sections'] else "None")

    print("\n📊 Quality Score:", result['quality_score'])

    print("\n🧠 Review Feedback")
    print("-" * 18)

    if not result["review_feedback"]:
        print("No issues found ✅")
    else:
        print(json.dumps(result["review_feedback"], indent=2))

    print("\n" + "═" * 70)

    # =========================
    # 🧠 HUMAN-IN-THE-LOOP (ADD THIS)


print("\n" + "=" * 60)
print("🧠 HUMAN-IN-THE-LOOP REPOSITORY ASSISTANT")
print("=" * 60)

while True:

    user_question = input(
        "\nAsk anything about the repository (or type 'exit'):\n> "
    )

    if user_question.lower() == "exit":
        print("\n✅ Conversation ended.")
        break

    llm_result = llm_enrichment_agent({

         "title": result.get("title", ""),
         "summary": result.get("llm_improved_summary", result.get("summary", "")),
          "tags": result.get("tags", []),
          "quality_score": result.get("quality_score", 0),
          "stars": result.get("stars", 0),
          "language": result.get("language", ""),
          "readme": result.get("readme", ""),
          "missing_sections": result.get("missing_sections", []),
          "forks": result.get("forks", 0),
          "review_feedback": result.get("review_feedback", {}),

          # 🔥 unified input
         "user_question": user_question
     })

    print("\n==============================")
    print("🤖 AI RESPONSE")
    print("==============================")

    print(llm_result["llm_response"])