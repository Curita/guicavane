import xmlrpclib
import urllib
import socket
import gzip
import os

class SubCrawler(object):

    def __init__(self):
        self.server_url = "http://api.opensubtitles.org/xml-rpc"

    def search_subs(self, name):
        self.server = xmlrpclib.Server(self.server_url)
        search = {}
        search["sublanguageid"] = "eng"
        search["query"] = name
        socket.setdefaulttimeout(10)
        try:
            log_result = self.server.LogIn("", "", "eng", "periscope")
            token = log_result["token"]
        except Exception as exc:
            print exc

        results = self.server.SearchSubtitles(token, [search])
        sublinks = []
        if results["data"]:
            for r in results["data"]:
                result = {}
                result["release"] = r["SubFileName"]
                result["link"] = r["SubDownloadLink"]
                #result["lang"] = r["SubLanguageID"]
                sublinks.append(result)
        self.server.LogOut(token)

        for subtitle in sublinks:
            print subtitle
            destfile = subtitle["link"].split("/")[-1]
            filename, info = urllib.urlretrieve(subtitle["link"], "/tmp/" + destfile)
            gzfile = gzip.open(filename)
            subfile = open("/tmp/" + name + destfile.replace(".gz", ""), "w")
            subfile.write(gzfile.read())
            subfile.close()
            gzfile.close()
            os.remove(filename)
