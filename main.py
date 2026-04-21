from graph import build_graph
import json
if __name__ == "__main__":

    app = build_graph()

    result = app.invoke({
        "repo_url": "https://github.com/readytensor/rt-agentic-ai-cert-week6",
        "attempts": 0
    })



    print("\n" + "=" * 60)
    print("🔍 GITHUB REPOSITORY ANALYSIS REPORT")
    print("=" * 60)

    print(f"\n📦 Repository: {result['repo_url']}")
    print(f"⭐ Stars: {result['stars']}")
    print(f"🍴 Forks: {result['forks']}")
    print(f"💻 Language: {result['language']}")

    print("\n📌 Title:")
    print(result['title'])

    print("\n📝 Summary:")
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


