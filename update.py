#!/usr/bin/env python3
import os
import re
import shutil
import subprocess
from urllib.parse import urljoin
from urllib.request import urlopen


def get_url_content(url):
    return urlopen(url).read().decode("utf-8")


def parse_version(version_str):
    try:
        return tuple(map(int, version_str.split(".")))
    except ValueError:
        return None


def get_archive_url():
    buildbot_base_url = "https://buildbot.libretro.com/"

    versions_html = get_url_content(urljoin(buildbot_base_url, "stable"))
    pattern = r'<a\s+[^>]*href=[\'"]([^"\']*)[\'"][^>]*>(.*?)<\/a>'
    versions_link_texts = re.findall(pattern, versions_html, re.DOTALL)
    versions_links = [
        (url, text) for url, text in versions_link_texts if parse_version(text)
    ]
    version_link = max(
        versions_links, key=lambda x: parse_version(x[1]), default=(None, None)
    )
    version_dir_url = version_link[0]
    version_archive_url = urljoin(
        buildbot_base_url, urljoin(version_dir_url, "emscripten/RetroArch.7z")
    )
    return version_archive_url


def main():
    if os.path.exists("retroarch"):
        os.rename("retroarch", "retroarch~")
    if not os.path.exists("retroarch.7z"):
        archive_url = get_archive_url()
        subprocess.check_output(["curl", archive_url, "-o", "retroarch.7z"])
    if not os.path.exists("retroarch"):
        subprocess.check_output(["7z", "x", "retroarch.7z"])

    for name in os.listdir("retroarch"):
        path = os.path.join("retroarch", name)
        if os.path.isdir(path):
            shutil.rmtree(path, ignore_errors=True)
        elif os.path.isfile(path):
            base, ext = os.path.splitext(name)
            if ext == ".js":
                wasm = os.path.join("retroarch", base + ".wasm")
                if os.path.isfile(wasm):
                    subprocess.check_output(["zip", "-j", os.path.join("retroarch", base + ".zip"), path, wasm])
                    os.remove(path)
                    os.remove(wasm)
                else:
                    os.remove(path)
            elif not ext == ".wasm":
                os.remove(path)

    shutil.rmtree("retroarch~", ignore_errors=True)

if __name__ == "__main__":
    main()
