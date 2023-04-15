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
            "error": "Page not found"
        })
    return 