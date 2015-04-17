from ..base import HaravanResource
from ..resources import Metafield
from six.moves import urllib
import base64
import re


class Image(HaravanResource):
    _prefix_source = "/admin/products/$product_id/"

    def __getattr__(self, name):
        if name in ["pico", "icon", "thumb", "small", "compact", "medium", "large", "grande", "original"]:
            return re.sub(r"/(.*)\.(\w{2,4})", r"/\1_%s.\2" % (name), self.src)
        else:
            return super(Image, self).__getattr__(name)

    def attach_image(self, data, filename=None):
        self.attributes["attachment"] = base64.b64encode(data)
        if filename:
            self.attributes["filename"] = filename

    def metafields(self):
        if self.is_new():
            return []
        query_params = { 'metafield[owner_id]': self.id, 'metafield[owner_resource]': 'product_image' }
        return Metafield.find(from_ = '/admin/metafields.json?%s' % urllib.parse.urlencode(query_params))
