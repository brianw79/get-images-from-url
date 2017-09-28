import mimetypes
import re
import urllib2
import urllib
import urlparse


def get_all_urls_from_http_string(data):
    http_strings = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', data)
    return http_strings


def is_image_url(url):
    if url.endswith("script>"):
        return False
    try:
        if mimetypes.guess_type(url)[0].startswith("image"):
            return True
    except AttributeError:
        return False

    return False


def get_all_image_urls(data):
    http_strings = get_all_urls_from_http_string(data)
    image_http_strings = []
    for http_string in http_strings:
        if is_image_url(http_string):
            print("found " + http_string)
            image_http_strings.append(http_string)

    print("Found " + str(len(image_http_strings)) + " URL(s)")
    return image_http_strings


def read_url_as_string(url):
    print("Reading " + url + " as string")
    req = urllib2.Request(url, headers={'User-Agent': "Magic Browser"})
    con = urllib2.urlopen(req)
    url_string = con.read()
    print("Got string of length " + str(len(url_string)))
    return url_string


def save_images_from_url(url, save_path):
    url_data = read_url_as_string(url)
    image_urls = get_all_image_urls(url_data)

    for image_url in image_urls:
        image_filename = urlparse.urlsplit(image_url).path.split('/')[-1]
        urllib.urlretrieve(image_url, save_path + "\\" + ''.join(image_filename))


# urlData = read_url_as_string("https://www.blah.com")
# all_image_urls = get_all_image_urls(urlData)
#
# for img_url in all_image_urls:
#     print(urlparse.urlsplit(img_url).path.split('/')[-1])

# print(urlparse.urlsplit(image_urls))

url_to_save_images_from = "https://stackshare.io/trending/tools"
save_path = r"C:\temp\images"
save_images_from_url(url_to_save_images_from, save_path)