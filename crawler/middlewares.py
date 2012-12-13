from urlparse import urljoin

from scrapy.contrib.downloadermiddleware.redirect import RedirectMiddleware
from scrapy.http import HtmlResponse
from scrapy.utils.response import get_meta_refresh

class LinkRedirectMiddleware(RedirectMiddleware):

    def process_response(self, request, response, spider):

        # Remember request status
        request.meta.setdefault('redirect_status', []).append(response.status)

        if 'dont_redirect' in request.meta:
            return response
        if request.method.upper() == 'HEAD':
            if response.status in [301, 302, 303, 307] and 'Location' in response.headers:
                redirected_url = urljoin(request.url, response.headers['location'])
                redirected = request.replace(url=redirected_url)
                return self._redirect(redirected, request, spider, response.status)
            else:
                return response

        if response.status in [302, 303] and 'Location' in response.headers:
            redirected_url = urljoin(request.url, response.headers['location'])
            redirected = self._redirect_request_using_get(request, redirected_url)
            return self._redirect(redirected, request, spider, response.status)

        if response.status in [301, 307] and 'Location' in response.headers:
            redirected_url = urljoin(request.url, response.headers['location'])
            redirected = request.replace(url=redirected_url)
            return self._redirect(redirected, request, spider, response.status)

        if isinstance(response, HtmlResponse):
            interval, url = get_meta_refresh(response)
            if url and interval < self.max_metarefresh_delay:
                redirected = self._redirect_request_using_get(request, url)
                return self._redirect(redirected, request, spider, 'meta refresh')

        return response
