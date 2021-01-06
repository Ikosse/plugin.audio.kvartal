# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup
import requests


def get_page_soup(url):
    page = requests.get(url)
    return BeautifulSoup(page.text, "html.parser")


class Kvartal(object):

    def __init__(self):
        self.content_url = "https://kvartal.se/wp-content/themes/kvartal-v2/"


    def _get_audio_label(self, section):
        links = section.find_all("a")
        for link in links:
            try:
                label = link.get("href").encode("utf-8")
                if "subject=" in label:
                    return label.split("=")[1][:-5]
            except:
                continue
        return ""


    def _get_video_label(self, section):
        try:
            label = section.find("h2").string.encode("utf-8")
            try:
                date = section.find("div", {"class": "post-date"}).string.encode("utf-8")
                label = label + " (" + date + ")"
            except:
                pass
            return label
        except:
            return ""


    def _get_audio_url(self, section):
        links = section.find_all("a")
        for link in links:
            try:
                audio_url = link.get("href").encode("utf-8")
                if ".mp3" in audio_url:
                    return audio_url
            except:
                continue
        return ""
    

 
    def _get_video_url(self, section):
        links = section.find_all("a")
        for link in links:
            try:
                video_url = link.get("href").encode("utf-8")
                if "autoplay=" in video_url:
                    return video_url 
            except:
                continue
        return ""


    def _get_image_url(self, section):
        try:
            image = section.find(
                "div", 
                {"class": "kmp-image"}
            ).encode("utf-8")
            image_url = image.split("url(")[1][:-2].split(");")[0]
            return image_url
        except:
            return ""
    
    
    def _get_summary(self, section):
        try:
            summary = section.find("div", {"class": "pc-byline"}).next_sibling
            summary = summary.encode("utf-8").strip("\n").strip(" ")
            return summary
        except:
            return ""


    def _scrape_content(self, section_code, content_number):
        content_code = (content_number-1)*5
        section_url = "ajax-get-podcasts.php?o={:d}&c={}&e=999999".format(content_code, section_code)
        page = get_page_soup(self.content_url + section_url)

        content_sections = page.find_all("div", {"class": "kvartal-media-post"})

        items = []
        for content in content_sections:
            if section_code != "10":
                media_url = self._get_audio_url(content)
                label = self._get_audio_label(content)
                summary = self._get_summary(content)
                image_url = self._get_image_url(content)
            else:
                media_url = self._get_video_url(content)
                label = self._get_video_label(content)
                summary = self._get_summary(content)
                image_url = self._get_image_url(content)

            items.append({"label": label, 
                          "summary": summary,
                          "media": media_url, 
                          "image": image_url})
    
        return items


    def get_youtube_link(self, video_url):
        video_page = get_page_soup(video_url)
        for div in video_page.find_all("div"):
            try:
                youtube_link = div.attrs["onclick"]
                start = youtube_link.find("('")
                return youtube_link[start+2:-3].encode("utf-8")
            except:
                continue
        return ""


    def get_content(self, section_code, page_number):
        content_number = 2*page_number - 1
        page_1 = self._scrape_content(section_code, content_number)
        page_2 = self._scrape_content(section_code, content_number+1)

        return page_1 + page_2
