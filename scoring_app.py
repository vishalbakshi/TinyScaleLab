from fasthtml.common import *
import pandas as pd


app, rt = fast_app(hdrs=[
    Style("""
        .selected {
            background-color: #28a745;
            color: black;
        }
        .score-buttons {
            display: flex;
            gap: 5px;
        }
        .category-buttons {
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
        }
        .category-buttons button.selected {
            background-color: #28a745;
        }
          
        .index-indicator {
            text-align: center;
            font-weight: bold;
            margin-bottom: 10px;
        }
    """)
])

criteria_df = pd.read_csv('criteria.csv')
lm_data_df = pd.read_csv('lm_data.csv')
output_df = pd.read_csv('output.csv')

def get_row(idx): return lm_data_df.iloc[idx]

@dataclass
class Row:
    id: int
    category: str
    prompt: str
    completion: str
    model_name: str

@patch
def __ft__(self:Row):
    _category = P("CATEGORY: ", self.category)
    _prompt = P(self.prompt)
    _completion = P(self.completion)
    return Div(
        _category,
        Hr(),
        P("PROMPT:"),
        _prompt, 
        Hr(),
        P("COMPLETION:"),
        _completion)

@rt("/item")
def item(idx: int = 0):
    row_data = get_row(idx)
    row = Row(
        id=row_data.ID,
        category=row_data.category,
        prompt=row_data.prompt,
        completion=row_data.completion,
        model_name=row_data.model_name
    )
    
    index_indicator = P(f"Item {idx+1} of {len(lm_data_df)}", cls="index-indicator")
    
    prev_btn = Button("Previous", hx_get=item.to(idx=max(0, idx-1)), hx_target="#content-area")
    next_btn = Button("Next", hx_get=item.to(idx=min(len(lm_data_df)-1, idx+1)), hx_target="#content-area")
    nav_buttons = Div(prev_btn, next_btn, cls="navigation-buttons")
    
    update_criteria = Script(f"htmx.ajax('GET', '/criteria?idx={idx}', '#criteria-area');")
    
    return index_indicator, row, nav_buttons, update_criteria

@rt("/save_score")
def save_score(category: str, label: str, score: float, idx: int):
    global output_df
    
    row_data = get_row(idx)
    score_col = f'{category}_{label}_score'

    if (output_df['ID'] == row_data.ID).any():
        idx_to_update = output_df.index[output_df['ID'] == row_data.ID][0]
        output_df.at[idx_to_update, score_col] = score
    else:
        new_row = {
            'ID': row_data.ID,
            'category': row_data.category,
            'prompt': row_data.prompt,
            'completion': row_data.completion,
            'model_name': row_data.model_name,
        }
        
        new_row[score_col] = score
        new_df = pd.DataFrame([new_row])
        output_df = pd.concat([output_df, new_df], ignore_index=True)
    
    output_df.to_csv('output.csv', index=False)
    
    return criteria(category, idx)

@rt("/criteria")
def criteria(category: str = None, idx: int = 0):
    if category is None: category = criteria_df['category'].unique()[0]
    row_data = get_row(idx)
    categories = criteria_df['category'].unique()
    
    category_buttons = []
    for cat in categories:
        btn = Button(cat, 
                    hx_get=f"/criteria?category={cat}&idx={idx}",
                    hx_target="#criteria-area",
                    cls="selected" if cat == category else "")
        category_buttons.append(btn)
    
    category_nav = Div(*category_buttons, cls="category-buttons")

    category_criteria = criteria_df[criteria_df['category'] == category]
    
    scores = {}
    if (output_df['ID'] == row_data.ID).any():
        row = output_df[output_df['ID'] == row_data.ID].iloc[0]
        for col in row.index:
            if col.startswith(f'{category}_') and col.endswith('_score') and not pd.isna(row[col]):
                label = col.split('_')[1]
                scores[label] = float(row[col])
    
    criteria_elements = []
    for _, row in category_criteria.iterrows():
        label = row['label']
        text = row['text']
        
        current_score = scores.get(label, None)
        
        btn_0 = Button("0.0", 
                      hx_post=f"/save_score?category={category}&label={label}&score=0.0&idx={idx}",
                      hx_target="#criteria-area",
                      cls="selected" if current_score == 0.0 else "")
        
        btn_5 = Button("0.5", 
                      hx_post=f"/save_score?category={category}&label={label}&score=0.5&idx={idx}",
                      hx_target="#criteria-area",
                      cls="selected" if current_score == 0.5 else "")
        
        btn_1 = Button("1.0", 
                      hx_post=f"/save_score?category={category}&label={label}&score=1.0&idx={idx}",
                      hx_target="#criteria-area",
                      cls="selected" if current_score == 1.0 else "")
        
        criteria_elements.append(Div(
            P(f"{label}: {text}"),
            Div(btn_0, btn_5, btn_1, cls="score-buttons"),
            id=f"criterion-{label}"
        ))

    return Div(
        category_nav,
        H3(category),
        *criteria_elements,
        id="criteria-container"
    )

@rt
def index(idx: int = 0):
    return Titled(
        "LM Scoring App", 
        Div(id="content-area", hx_get=item.to(idx=idx), hx_trigger="load"),
        Hr(),
        Div(id="criteria-area", hx_get=criteria.to(idx=idx), hx_trigger="load"))


serve()
