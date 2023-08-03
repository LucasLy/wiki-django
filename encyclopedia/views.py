from django.shortcuts import render
from markdown2 import Markdown
from . import util
import random

mdx = Markdown()

def htmlConverter(title: str):
    content = util.get_entry(title)
    "return convertted markdown to html or null if not found"
    return mdx.convert(content) if content is not None else None

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    res = htmlConverter(title)

    "render content if found, else render error page"
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": htmlConverter(title)
    }) if res is not None else render(request, "encyclopedia/error.html", {
        "title": "404 - Page not found",
        "error": f"There are no results for \"{title}\"",
    })


def search(request):
    if(request.method == "POST"):
        "get query from search bar"
        query = request.POST['q']
        converted = htmlConverter(query)
        "check if query is in entries"
        if converted is not None:
            return entry(request, query)
        else:
            entries = util.list_entries()
            "fetch all entries that contain query"
            results = [entry for entry in entries if query.lower() in entry.lower()]
            print(results)
            return render(request, "encyclopedia/search.html", {
                "entries": results,
                "query": query
            })
    else:
        return render(request, "encyclopedia/error.html", {
            "title": "Error!",
            "error": "You must use the search bar to search for something.",
        })

    
        
        
def new(request):
    if(request.method == "POST"):
        title = request.POST['title']
        content = request.POST['content']
        "check if page already exists"
        existing = util.get_entry(title)
        if existing is not None:
            return render(request, "encyclopedia/error.html", {
                "title": "Page already exists",
                "error": "A page with this title already exists."
            })
        else:
            util.save_entry(title, content)
            return entry(request, title) # redirect to new page
    else:
        return render(request, "encyclopedia/new.html")


def edit(request):
    if(request.method == "POST"):
         title = request.POST['edit_title']
         content = util.get_entry(title)
         return render(request, "encyclopedia/edit.html", {
             "title": title,
             "current_content": content
         })
    else:
        # throw error if user tries to edit page without context
        return render(request, "encyclopedia/error.html", {
            "title": "Error!",
            "error": "You cannot edit a page without context.",
        })
         
         
def edit_save(request):
    if(request.method == "POST"):
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        return entry(request, title) # redirect to updated page
    else:
        # throw error if user tries to save edit without context
        return render(request, "encyclopedia/error.html", {
            "title": "Error!",
            "error": "You cannot save a non existing edit.",
        })
        
def rand(request):
    entries = util.list_entries()
    title = random.choice(entries)
    return entry(request, title)