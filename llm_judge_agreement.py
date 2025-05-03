from fasthtml.common import *
import pandas as pd
from pathlib import Path

df = pd.read_csv('llm_judge_score_agreement.csv')

app, rt = fast_app(hdrs=[
    Style("""
        .selected {
            background-color: #28a745;
            color: black;
          }
        """
)])

@dataclass
class Row:
    id: int
    category: str
    prompt: str
    completion: str
    text: str
    score: float
    explanation: str

@patch
def __ft__(self: Row):
    return Div(
        H2(f"Category: {self.category}"),
        Div(
            H3("Prompt:"),
            P(self.prompt),
            H3("Completion:"),
            P(self.completion),
            H3("Criterion:"),
            P(self.text),
            H3("Score:"),
            P(f"{self.score}"),
            H3("Explanation:"),
            P(self.explanation),
        )
    )

@rt("/item")
def item(id:int=1):
    _row = df.iloc[id - 1]
    row = Row(
        id = _row.id,
        category = _row.category,
        prompt = _row.res_prompt,
        completion = _row.res_completion,
        text = _row.text,
        score = _row.score,
        explanation = _row.explanation
    )

    prev = Button("Previous", hx_get=item.to(id=max(1, id-1)), hx_target="#content-area")
    forward = Button("Forward", hx_get=item.to(id=min(id+1, len(df))), hx_target="#content-area")
    nav_buttons = Div(prev, forward, cls="navigation-buttons")

    agree_btn = Button("Agree", hx_get=agree.to(id=id, agree=True), hx_target="#content-area", cls="selected" if _row.agree else "", hx_trigger="click delay:100ms"),
    disagree_btn = Button("Disagree", hx_get=agree.to(id=id, agree=False), hx_target="#content-area", cls="selected" if not _row.agree else "")
    agree_buttons = Div(agree_btn, disagree_btn, cls="agree-buttons")
    print(_row.comments)
    comments = Div(
        H3("Comments:"),
        Textarea(
            _row.comments if len(_row.comments)> 0 else "",
            id="comments", 
            name="comments", 
            rows=5, 
            cols=50,
            hx_post=f"/{id}/save_comments",
            hx_trigger="keyup changed delay:500ms",
        )
    )

    return P(id), nav_buttons, Hr(), agree_buttons, Hr(), comments, Hr(), row

@rt("/agree")
def agree(id:int=1, agree:bool = False): 
    df.at[id-1, "agree"] = agree
    df.to_csv("llm_judge_score_agreement.csv", index=False)
    return item(id+1)

@rt("/{id}/save_comments")
def save_comments(id:int, comments:str=""): 
   df.at[id-1, "comments"] = comments
   df.to_csv("llm_judge_score_agreement.csv", index=False)
   print(f"Saving comments for ID {id}: {comments}")

@rt
def index(id:int = 1): 
    return Titled(
        "LLM Judge Agreement", 
        Div(id="content-area", hx_get=item.to(id=id), hx_trigger="load"),
    )

serve()
