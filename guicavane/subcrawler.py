import xmlrpclib
import socket

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
        print sublinks
        print token
        print search
        self.server.LogOut(token)
