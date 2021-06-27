"""Playbot provides very basic operations/keywords
by playwright/python library to the robotframework.
"""

from typing import Literal, Optional, Union

from playwright.sync_api import Browser, ElementHandle
from robot.api.deco import keyword, library

from playbot.src.browser import PlaybotBrowser
from playbot.src.context import PlaybotContext
from playbot.src.page import PlaybotPage


@library
class Playbot:
    """Represents the library for robot framework.

    This library wraps selected methods of https://playwright.dev/python/
    which can be used as Robot Framework Keywords.

    It is strongly recommended to check https://playwright.dev/python/docs/core-concepts
    to get familiar with concept of playwright.
    """

    ROBOT_LIBRARY_SCOPE = "SUITE"

    def __init__(self, browser: str = "chromium"):
        '''
        When importing the library, you have to specify, which supported browser you want to use.
        Later, when launching browser, this specified browser will be used.

        == Example ==

        |       =A=      |               =B=                   |              =C=                  |
        | ***Settings*** |                                     |                                   |
        | Library        | ${EXECDIR}${/}playbot${/}Playbot.py | browser=[chromium|firefox|webkit] |
        '''
        self._selected_browser: str = browser
        self._playbot_browser: Union[None, Browser] = None

    @keyword
    def start_browser(self, **kwargs):
        '''Starts browser. Since library has default scope set to SUITE,
        user is expected to start the browser only ONCE, ideally using
        *Suite Setup* and close the browser using *Suite Teardown*.

        Starting browser is time and resource expensive. For isolated test runs,
        user wants to use browser contexts.

        See https://playwright.dev/python/docs/api/class-browsertype#browser-type-launch for
        all available keyword arguments.

        == Example ==

        | =A=            | =B=           | =C=               |
        | ***Settings*** |               |                   |
        | Suite Setup    | Start Browser |                   |
        | Suite Setup    | Start Browser | headless=${False} |
        '''
        self._playbot_browser = PlaybotBrowser(self._selected_browser, **kwargs)

    @keyword
    def close_browser(self):
        '''Closes the browser.
        This keyword should be used together with *Suite Teardown*.

        See https://playwright.dev/python/docs/api/class-browser#browser-close
        for documentation of this method.

        == Example ==

        | =A=            | =B=           |
        | ***Settings*** |               |
        | Suite Teardown | Close Browser |
        '''
        self._playbot_browser.close_browser()

    @keyword
    def new_context(self, **kwargs):
        '''Starts a new context of the browser.
        Contexts are incognito-like isolated sessions of the browser.
        They are fast and cheap to create and should be used for running the
        tests in the suite, NOT multiple browser instances.

        See https://playwright.dev/python/docs/api/class-browser#browser-new-context for
        all available options.

        This keyword returns *PlaybotContext* class instance, which contains _context_
        property with created browser context.

        == Example ==

        | =A=         | =B=         |
        | ${context}= | New Context |

        === Create context with setting viewport ===

        | =A=          | =B=           | =C=                  |
        | &{viewport}= | width=${1920} | height=${1080}       |
        | ${context}=  | New Context   | viewport=&{viewport} |

        === Create multiple contexts in one browser ===

        You can create several contexts - as many as you like.
        These contexts are completely isolated, and you can reference them directly
        via variables. This may be useful for example testing some chat applications
        or for parallel test execution.

        | =A=           | =B=           | =C=                  |
        | &{viewport}=  | width=${1920} | height=${1080}       |
        | ${context1}=  | New Context   | viewport=&{viewport} |
        | ${context2}=  | New Context   |                      |
        '''
        return PlaybotContext(self._playbot_browser.browser, **kwargs)

    @keyword
    def close_context(self, context: PlaybotContext):
        '''Closes given browser context, which is represented by
        wrapper class *PlaybotContext*.

        See https://playwright.dev/python/docs/api/class-browsercontext#browser-context-close for
        the command documentation.

        == Example ==

        | =A=           | =B=         |
        | Close Context | ${context}  |
        '''
        context.close_context(context.context)

    @keyword
    def cookies(
        self, context: PlaybotContext, urls: Union[str, list[str], None] = None
    ):
        '''Returns list of cookies of the given browser context.

        See https://playwright.dev/python/docs/api/class-browsercontext#browser-context-cookies
        for command options.

        == Example ==

        === Return all cookies ===

        | =A=         | =B=     | =C= |
        | @{cookies}= | Cookies |     |

        === Return cookies which affect given url ===

        | =A=         | =B=     | =C=                   |
        | @{cookies}= | Cookies | https://some/url.com |

        === Return cookies which affect multiple urls ===

        | =A=         | =B=              | =C=              |
        | @{urls}=    | https://url1.com | https://url2.com |
        | @{cookies}= | Cookies          | ${urls}          |
        '''
        return context.cookies(context.context, urls)

    @keyword
    def new_page(self, context: PlaybotContext, **kwargs):
        '''Opens new page and returns its instance.
        It is represented by wrapper class *PlaybotPage*, which
        contains property _page_, which represents browser context's
        page.

        See https://playwright.dev/python/docs/api/class-browsercontext#browser-context-new-page

        You can have multiple pages opened in one context. These pages are
        then accessible directly via variables they are assigned to.

        == Example ==

        === Open one page ===

        | =A=         | =B=         | =C=        |
        | ${context}= | New Context |            |
        | ${page}=    | New Page    | ${context} |

        === Open two pages ===

        | =A=         | =B=         | =C=        |
        | ${context}= | New Context |            |
        | ${page1}=   | New Page    | ${context} |
        | ${page2}=   | New Page    | ${context} |
        '''
        return PlaybotPage(context.context, **kwargs)

    @keyword
    def click(
        self,
        handle: Union[PlaybotPage, ElementHandle],
        selector: Union[str, None] = None,
        **kwargs
    ):
        '''Click element.

        This keyword can be used either with *PlaybotPage* or with *ElementHandle*.

        See https://playwright.dev/python/docs/api/class-page#page-click for
        click with page.

        See https://playwright.dev/python/docs/api/class-elementhandle#element-handle-click for
        click with element.

        == Example ==

        === Click using page and selector ===

        | =A=         | =B=         | =C=        |
        | ${page}=    | New Page    | ${context} |
        | ${selector}= | Convert to string | xpath=//some-selector |
        | Click       | ${page}     | ${selector} |

        === Click using element ===
        | =A=          | =B=               | =C=                   | =D=         |
        | ${page}=     | New Page          | ${context}            |             |
        | ${selector}= | Convert to string | xpath=//some-selector |             |
        | ${element}=  | Query Selector    | ${page}               | ${selector} |
        | Click        | ${element}        |                       |             |
        '''
        if isinstance(handle, PlaybotPage):
            return handle.click(selector, **kwargs)
        return handle.click(**kwargs)

    @keyword
    def go_to(self, page: PlaybotPage, url: str, **kwargs):
        return page.go_to(page.page, url, **kwargs)

    @keyword
    def is_visible(
        self,
        handle: Union[PlaybotPage, ElementHandle],
        selector: Union[str, None] = None,
        timeout: Union[float, None] = None,
    ):
        if isinstance(handle, PlaybotPage):
            return handle.is_visible(selector=selector, timeout=timeout)
        return handle.is_visible()

    @keyword
    def query_selector(self, handle: Union[PlaybotPage, ElementHandle], selector: str):
        return handle.query_selector(selector)

    @keyword
    def wait_for_element_state(
        self,
        handle: ElementHandle,
        state: Literal["visible", "hidden", "enabled", "disabled", "editable"],
        **kwargs
    ):
        return handle.wait_for_element_state(state, **kwargs)

    @keyword
    def wait_for_selector(
        self, handle: Union[PlaybotPage, ElementHandle], selector: str, **kwargs
    ):
        return handle.wait_for_selector(selector, **kwargs)

    @keyword
    def wait_for_timeout(self, page: PlaybotPage, timeout: float):
        page.wait_for_timeout(page.page, timeout)
