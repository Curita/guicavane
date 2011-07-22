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
                result["rating"] = r["SubRating"]
                result["downloads"] = r["SubDownloadsCnt"]
                sublinks.append(result)
        self.server.LogOut(token)
        self.sublinks = sublinks

#        for subtitle in sublinks:
#            print subtitle["downloads"]
#            destfile = subtitle["link"].split("/")[-1]
#            filename, info = urllib.urlretrieve(subtitle["link"], "/tmp/" + destfile)
#            gzfile = gzip.open(filename)
#            subfile = open("/tmp/" + name + destfile.replace(".gz", ""), "w")
#            subfile.write(gzfile.read())
#            subfile.close()
#            gzfile.close()
#            os.remove(filename)

    def download_best_sub(self, dest):
        best_sub = self.sublinks[0]
        for subtitle in self.sublinks:
            if subtitle["downloads"] > best_sub["downloads"]:
                best_sub = subtitle
        destfile = best_sub["link"].split("/")[-1]
        filename, info = urllib.urlretrieve(best_sub["link"], "/tmp/" + destfile)
        gzfile = gzip.open(filename)
        subfile = open(".".join(dest.split(".")[:-1]) + ".EN.srt", "w")
        subfile.write(gzfile.read())
        subfile.close()
        gzfile.close()
