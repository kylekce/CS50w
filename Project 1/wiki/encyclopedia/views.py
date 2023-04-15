from django.shortcuts import render

from . import util


def index(request):
    entries = util.list_entries()
    css_file = util.get_entry("CSS")
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
