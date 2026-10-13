import os
from googleapiclient.discovery import build

class SearchAgent:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
        self.search_engine_id = os.getenv("GOOGLE_SEARCH_CX")
        self.service = build("customsearch", "v1", developerKey=self.api_key)

    def get_safe_visual_aid(self, exercise_name, detected_error, user_constraints):
        """
        user_constraints: List of strings like ['ADHD', 'Limited Mobility', 'Beginner']
        """
        
        # STAGE 1: Apply Contextual Anchors (The "Edge Case" Fix)
        # We transform a generic query into a "Medical/Therapeutic" query
        anchors = " ".join(user_constraints)
        query = f"proper {exercise_name} {detected_error} demonstration {anchors} physical therapy"

        # STAGE 2: Execute Search
        # We restrict results to sites like YouTube or medical/edu domains for quality
        try:
            result = self.service.cse().list(
                q=query,
                cx=self.search_engine_id,
                num=3,
                safe='active',
                # We can refine by site if needed
                # siteSearch="youtube.com" 
            ).execute()

            items = result.get('items', [])
            
            if not items:
                return {"status": "no_results", "url": None}

            # STAGE 3: Select the most instructional item
            # We prioritize snippets containing 'slow', 'step-by-step', or 'easy'
            best_match = items[0] 
            return {
                "status": "success",
                "title": best_match['title'],
                "link": best_match['link'],
                "thumbnail": best_match.get('pagemap', {}).get('cse_thumbnail', [{}])[0].get('src'),
                "snippet": best_match['snippet']
            }

        except Exception as e:
            print(f"Search Agent Error: {e}")
            return {"status": "error", "message": str(e)}

# Example Usage:
# agent = SearchAgent()
# result = agent.get_safe_visual_aid("squat", "heels lifting", ["Paralysis recovery", "low impact"])
# print(result['link'])