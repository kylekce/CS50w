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


def search(request):
    if request.method == "POST":
        query = request.POST["q"]
        content = convertMd(query)
        if content is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": query,
                "content": content
            })
        else:
            entries = util.list_entries()
            recomendations = []
            for entry in entries:
                if query.lower() in entry.lower():
                    recomendations.append(entry)
            return render(request, "encyclopedia/result.html", {
                "recomendations": recomendations
            })


def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        if title in util.list_entries():
            return render(request, "encyclopedia/error.html", {
                "message": "Sorry, but the page you requested already exists."
            })
        else:
            util.save_entry(title, content)
            content = convertMd(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": content
            })

    return render(request, "encyclopedia/create.html")
