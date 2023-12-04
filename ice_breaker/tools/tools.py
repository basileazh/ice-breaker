from langchain.serpapi import SerpAPIWrapper


class CustomSerpAPIWrapper(SerpAPIWrapper):
    """
    Custom SerpAPI wrapper.
    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def _process_response(res: dict) -> str:
        """Process response from SerpAPI."""
        if "error" in res:
            raise ValueError(f"Got error from SerpAPI: {res['error']}")
        if "answer_box_list" in res:
            res["answer_box"] = res["answer_box_list"]
        if "answer_box" in res:
            answer_box = res["answer_box"]
            if isinstance(answer_box, list):
                answer_box = answer_box[0]
            if "result" in answer_box:
                return answer_box["result"]
            elif "answer" in answer_box:
                return answer_box["answer"]
            elif "snippet" in answer_box:
                return answer_box["snippet"]
            elif "snippet_highlighted_words" in answer_box:
                return answer_box["snippet_highlighted_words"]
            else:
                answer = {}
                for key, value in answer_box.items():
                    if not isinstance(value, (list, dict)) and not (isinstance(value, str) and value.startswith("http")):
                        answer[key] = value
                return str(answer)
        elif "events_results" in res:
            return res["events_results"][:10]
        elif "sports_results" in res:
            return res["sports_results"]
        elif "top_stories" in res:
            return res["top_stories"]
        elif "news_results" in res:
            return res["news_results"]
        elif "jobs_results" in res and "jobs" in res["jobs_results"]:
            return res["jobs_results"]["jobs"]
        elif "shopping_results" in res and "title" in res["shopping_results"][0]:
            return res["shopping_results"][:3]
        elif "questions_and_answers" in res:
            return res["questions_and_answers"]
        elif "popular_destinations" in res and "destinations" in res["popular_destinations"]:
            return res["popular_destinations"]["destinations"]
        elif "top_sights" in res and "sights" in res["top_sights"]:
            return res["top_sights"]["sights"]
        elif "images_results" in res and "thumbnail" in res["images_results"][0]:
            return str([item["thumbnail"] for item in res["images_results"][:10]])

        snippets = []
        if "knowledge_graph" in res:
            knowledge_graph = res["knowledge_graph"]
            title = knowledge_graph["title"] if "title" in knowledge_graph else ""
            if "description" in knowledge_graph:
                snippets.append(knowledge_graph["description"])
            for key, value in knowledge_graph.items():
                if (
                    isinstance(key, str)
                    and isinstance(value, str)
                    and key not in ["title", "description"]
                    and not key.endswith("_stick")
                    # and not key.endswith("_link")
                    and not value.startswith("http")
                ):
                    snippets.append(f"{title} {key}: {value}.")

        for organic_result in res.get("organic_results", []):
            if "link" in organic_result:
                snippets.append(organic_result["link"])
            # elif "snippet" in organic_result:
            #     snippets.append(organic_result["snippet"])
            # elif "snippet_highlighted_words" in organic_result:
            #     snippets.append(organic_result["snippet_highlighted_words"])
            # elif "rich_snippet" in organic_result:
            #     snippets.append(organic_result["rich_snippet"])
            # elif "rich_snippet_table" in organic_result:
            #     snippets.append(organic_result["rich_snippet_table"])

        if "buying_guide" in res:
            snippets.append(res["buying_guide"])
        if "local_results" in res and "places" in res["local_results"]:
            snippets.append(res["local_results"]["places"])

        if len(snippets) > 0:
            return str(snippets)
        else:
            return "No good search result found"


def get_profile_url(txt: str) -> str:
    """
    Searches for a LinkedIn profile URL for a given name.
    :param txt:
    :return:
    """

    search = CustomSerpAPIWrapper()
    res = search.run(txt)

    return res
