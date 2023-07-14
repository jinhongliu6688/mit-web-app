import pandas as pd
import json

import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse

from fastapi.templating import Jinja2Templates


app = FastAPI()
app.mount("/static", StaticFiles(directory="./static"), name="static")
templates = Jinja2Templates(directory="templates")


# Load main search-index dataframe
data_df = pd.read_csv('data/reading_database.tsv', sep='\t')
author_df = pd.read_csv('data/author_database.tsv', sep='\t')

# Populate topic drop-downs
topic_dropdown = open('data/topic_dropdown.txt', 'r').readlines()

# Load index-link mappings
with open('data/index_to_link.json', encoding='utf-8') as f:
    index_to_link = json.load(f)


# Main search function
def search_readings(TOPIC, FORMAT, INCLUDE):
    TOPIC = '-' + TOPIC
    # Topic selection (Mandatory)
    selection = data_df[data_df.Topics == TOPIC].copy()

    # Format selection (if specified)
    if FORMAT in ['Book', 'Academic Paper']:
        selection = selection[selection.Type == FORMAT]

    # Include categories (if specified)
    if INCLUDE == 'Required':
        selection = selection[selection.Category == 'Required']
    elif INCLUDE == 'Optional':
        selection = selection[selection.Category == 'Optional']

    num_courses = len(selection.Course.unique())
    num_readings = selection.shape[0]

    title_df = selection.copy()
    title_df = title_df.sort_values('Title')
    title_df['Link to Course'] = title_df.Course.apply(lambda x: index_to_link[str(x)])
    title_df = title_df.drop(columns=['Type', 'author_individual', 'Course', 'Topics'])
    title_df = pd.DataFrame(title_df.value_counts()).reset_index()
    title_df = title_df.drop(columns=['Category', 0])

    return (num_readings, num_courses), title_df


def search_authors(TOPIC, FORMAT, INCLUDE):
    TOPIC = '-' + TOPIC
    # Topic selection (Mandatory)
    selection = author_df[author_df.Topics==TOPIC].copy()

    # Format selection (if specified)
    if FORMAT in ['Book', 'Academic Paper']:
        selection = selection[selection.Type == FORMAT]

    # Include categories (if specified)
    if INCLUDE == 'Required Only':
        selection = selection[selection.Category == 'Required']
    elif INCLUDE == 'Optional Only':
        selection = selection[selection.Category == 'Optional']

    selection = selection.drop(columns=['Topics'])
    selection = pd.DataFrame(selection.author_individual.value_counts()).reset_index().rename(
        columns={'index': 'Author', 'author_individual': '# of Readings'})
    return selection


def create_table(df):
    cols = df.columns
    if '# of Readings' in cols: 
        S = ["<table width=100%>"]
    else:
        S = ["<table>"]

    for c in cols:
        S.append("<th>" + str(c) + "</th>")
    for i, row in df.iterrows():
        S.append("<tr>")
        for c in cols:
            if c == 'Link to Course':
                S.append('<td class="cell" style="text-align:center"><a href="' + str(row[c]) + '">Link</a></td>')
            elif c == 'Year':
                if row[c].isnumeric():
                    S.append('<td class="cell">' + str(row[c]) + "</td>")
                else:
                    S.append('<td class="cell">' + "" + "</td>")
            elif c == '# of Readings':
                S.append('<td class="cell" style="text-align:center">' + str(row[c]) + "</td>")
            elif c == "Author" and '# of Readings' in cols:
                S.append('<td class="cell" style="text-align:center">' + str(row[c]) + "</td>")
            else:
                S.append('<td class="cell">' + str(row[c]) + "</td>")
        S.append("</tr>")
    S.append("</table>")

    return "".join(S)


@app.get("/search-by-title")
def search_by_title(topicselection, formatselection, includeselection):
    results = search_readings(topicselection[:-1], formatselection, includeselection)
    reading_count = results[0][0]
    course_count = results[0][1]
    df = results[1]
    message = "<p>Found " + str(reading_count) + " readings for " + str(course_count) + " courses</p>"
    if reading_count == 0:
        return HTMLResponse(message)
    else:
        return HTMLResponse(message + create_table(df))

@app.get("/search-by-author")
def search_by_author(topicselection, formatselection, includeselection):
    df = search_authors(topicselection[:-1], formatselection, includeselection)
    if df.empty:
        return HTMLResponse()
    else:
        return HTMLResponse(create_table(df))

@app.get("/")
def start():
    return FileResponse("index.html")

@app.get("/index.html")
def start():
    return FileResponse("index.html")

@app.get("/statistics.html")
def start():
    return FileResponse("statistics.html")


@app.get("/search-by-title.html")
def start(request: Request):
    return templates.TemplateResponse(
        'search-by-title.html',
        context={
            'request': request,
            'topic_options': topic_dropdown, 
            })

@app.get("/search-by-author.html")
def start(request: Request):
    return templates.TemplateResponse(
        'search-by-author.html',
        context={
            'request': request,
            'topic_options': topic_dropdown, 
            })

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=9999, debug=True)
