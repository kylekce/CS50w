from django.shortcuts import render
import markdown

from . import util


def convertMd(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content is None:
        return None
    else:
        return markdowner.convert(content)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    content = convertMd(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "Sorry, but the page you requested could not be found."
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content
        })
    return


def search(request):
    if request.method == "POST":
        query = request.POST["q"]
        entries = util.list_entries()
        
