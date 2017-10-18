# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor
from ..compat import (
    compat_urllib_parse_unquote_plus
)
from ..utils import (
    int_or_none,
    remove_end,
    unified_strdate,
)


class NDTVIE(InfoExtractor):
    _VALID_URL = r'https?://(?:(?:www|gadgets|khabar|profit)\.)?ndtv\.com/videos?/(?:[^/]+/)*[^/?^&]+-(?P<id>\d+)'

    _TEST = {
        'url': 'http://www.ndtv.com/video/news/news/ndtv-exclusive-don-t-need-character-certificate-from-rahul-gandhi-says-arvind-kejriwal-300710',
        'md5': '39f992dbe5fb531c395d8bbedb1e5e88',
        'info_dict': {
            'id': '300710',
            'ext': 'mp4',
            'title': "NDTV exclusive: Don't need character certificate from Rahul Gandhi, says Arvind Kejriwal",
            'description': 'md5:ab2d4b4a6056c5cb4caa6d729deabf02',
            'upload_date': '20131208',
            'duration': 1327,
            'thumbnail': r're:https?://.*\.jpg',
        }
    }

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        title = compat_urllib_parse_unquote_plus(
            self._search_regex(r"__title\s*=\s*'([^']+)'", webpage, 'title'))

        filename = self._search_regex(
            r"__filename\s*=\s*'([^']+)'", webpage, 'video filename')
        video_url = 'https://ndtvod.bc-ssl.cdn.bitgravity.com/23372/ndtv/%s' % filename

        duration = int_or_none(self._search_regex(
            r"__duration\s*=\s*'([^']+)'", webpage, 'duration', fatal=False))

        upload_date = unified_strdate(self._html_search_meta(
            'publish-date', webpage, 'upload date', fatal=False))

        description = remove_end(self._og_search_description(webpage), ' (Read more)')

        return {
            'id': video_id,
            'url': video_url,
            'title': title,
            'description': description,
            'thumbnail': self._og_search_thumbnail(webpage),
            'duration': duration,
            'upload_date': upload_date,
        }
