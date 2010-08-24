#!/usr/bin/env python
"""
_JSONParser_

API for parsing JSON URLs and returning as python objects.

"""

__revision__ = "$Id: JSONParser.py,v 1.2 2008/08/18 20:28:17 ewv Exp $"
__version__ = "$Revision: 1.2 $"

import urllib
import cStringIO
import tokenize

class JSONParser:
    """
    API for dealing with retrieving information from SiteDB
    """


    def __init__(self, url):
        self.url = url


    def getJSON(self, service, **args):
        """
        _getJSON_

        retrieve JSON formatted information given the service name and the
        argument dictionaries

        """
        query = self.url
        query += "%s" % service

        params = urllib.urlencode(args)
        try:
            f = urllib.urlopen(query, params)
            result = f.read()
            f.close()
        except IOError:
            raise RuntimeError("URL not available: %s" % query)

        output = self.dictParser(result)
        return output


    def parse(self, token, src):
        """
        Dictionary string parser from
        Fredrik Lundh (fredrik at pythonware.com)
        on python-list
        """
        if token[1] == "{":
            out = {}
            token = src.next()
            while token[1] != "}":
                key = self.parse(token, src)
                token = src.next()
                if token[1] != ":":
                    raise SyntaxError("Malformed dictionary")
                value = self.parse(src.next(), src)
                out[key] = value
                token = src.next()
                if token[1] == ",":
                    token = src.next()
            return out
        elif token[1] == "[":
            out = []
            token = src.next()
            while token[1] != "]":
                out.append(self.parse(token, src))
                token = src.next()
                if token[1] == ",":
                    token = src.next()
            return out
        elif token[0] == tokenize.STRING:
            return token[1][1:-1].decode("string-escape")
        elif token[0] == tokenize.NUMBER:
            try:
                return int(token[1], 0)
            except ValueError:
                return float(token[1])
        else:
            print "Bad token", token
            raise SyntaxError("Malformed expression")


    def dictParser(self, source):
        """
        Dictionary string parser from
        Fredrik Lundh (fredrik at pythonware.com)
        on python-list
        """
        src = cStringIO.StringIO(source).readline
        src = tokenize.generate_tokens(src)
        return self.parse(src.next(), src)
