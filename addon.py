#-*- coding: utf-8 -*-
import os
import sys
import urllib
import urlparse
import xbmc
import xbmcaddon
import routing
from xbmcgui import ListItem, Dialog
from xbmcplugin import addDirectoryItem, endOfDirectory, setResolvedUrl
from resources.lib.kvartal import Kvartal

YOUTUBE_URL = "plugin://plugin.video.youtube/play/?video_id="

plugin = routing.Plugin()
kvartal = Kvartal()


@plugin.route("/")
def main_menu():
    addDirectoryItem(
        plugin.handle, 
        plugin.url_for(content_menu, "284", str(1)),
        ListItem("Den svenska modellen"), 
        True)
    addDirectoryItem(
        plugin.handle, 
        plugin.url_for(content_menu, "11", str(1)),
        ListItem("Fredagsintervjun"), 
        True)
    addDirectoryItem(
        plugin.handle, 
        plugin.url_for(content_menu, "189", str(1)),
        ListItem("Inlästa texter"), 
        True)
    addDirectoryItem(
        plugin.handle, 
        plugin.url_for(content_menu, "10", str(1)),
        ListItem("Kvartal TV"), 
        True)
    addDirectoryItem(
        plugin.handle, 
        plugin.url_for(content_menu, "13", str(1)),
        ListItem("Veckopanelen"), 
        True)
    endOfDirectory(plugin.handle)


@plugin.route("/<section>/<page>")
def content_menu(section, page):

    content = kvartal.get_content(section, int(page))

    for item in content:
        list_item = ListItem(label=item["label"],
                             thumbnailImage=item["image"])
        list_item.setInfo("video", {"plot": item["summary"]})
        list_item.setProperty("isPlayable", "true")
        if section != "10":
            addDirectoryItem(
                plugin.handle, 
                plugin.url_for(play_audio, url=item["media"]),
                list_item, 
                False)
        else:
            addDirectoryItem(
                plugin.handle, 
                plugin.url_for(play_video, url=item["media"]),
                list_item, 
                False)


    if (int(page) > 1):
        addDirectoryItem(
            plugin.handle, 
            plugin.url_for(content_menu, section, str(int(page) - 1)),
            ListItem(label="sida {}".format(str(int(page) - 1))),
            True)

    addDirectoryItem(
        plugin.handle, 
        plugin.url_for(content_menu, section, str(int(page) + 1)),
        ListItem("sida {}".format(str(int(page) + 1))),
        True)


    addDirectoryItem(
        plugin.handle, 
        plugin.url_for(content_menu, section, str(int(page) + 5)),
        ListItem(label="sida {}".format(str(int(page) + 5))),
        True)

    addDirectoryItem(
        plugin.handle, 
        plugin.url_for(content_menu, section, str(int(page) + 1)),
        ListItem(label="-----sida {:}-----".format(page), thumbnailImage=""),
        False)

    endOfDirectory(plugin.handle)

    
@plugin.route("/play_audio")
def play_audio():
    url = plugin.args["url"][0]
    url = url.replace(" ", "%20").encode("latin-1")

    item = ListItem(path=url)
    setResolvedUrl(plugin.handle, True, listitem=item)


@plugin.route("/play_video")
def play_video(): 
    video_page_url = plugin.args["url"][0]
    url = kvartal.get_youtube_link(video_page_url)

    xbmc.executebuiltin("RunPlugin(" + YOUTUBE_URL + url + ")")


if __name__ == "__main__":
    plugin.run()
