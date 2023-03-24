import queue
import threading
import urllib3
import urllib.parse as U

def ft_fp(filepath, extensions):
    words = queue.Queue()
    with open(filepath,"r") as dosya:
        raw = dosya.readline()
        while raw:
            for word in raw.split():
                word += extensions
                words.put(word)
            raw = dosya.readline()
    return words

def ft_dirb(target, words, extensions):
    while not words.empty():
        brute = words.get()
        try_list = []
        if "." not in brute:
            try_list.append("/{}/".format(brute))
        else:
            try_list.append("/{}".format(brute))

        if extensions:
            for extension in extensions:
                try_list.append("{}{}".format(brute, extension))

        for brutes in try_list:
            url = "{}{}".format(target, U.quote(brutes))
            try:
                http = urllib3.PoolManager()
                response = http.request("GET",url=url)

                if len(response.data):
                    if response.status != 404:
                        print("[{}] ==> {}".format(response.status, url))

            except (urllib3.exceptions.URLError, urllib3.exceptions.HTTPError) as e:
                if hasattr(e, 'code') and e.code != 404:
                    print("!!!!! [{}] ==> {}".format(e.code, url))
                pass

def main():
    target = input("Target URL:")
    filepath = input("FilePath:")
    extensions = input("Extensions:")
    words = ft_fp(filepath, extensions)
    ft_dirb(target, words, [])

if __name__ == "__main__":
    main()
