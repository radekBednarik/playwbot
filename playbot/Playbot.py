# pylint: disable=invalid-name, line-too-long, no-self-use

"""Playbot provides very basic operations/keywords
by playwright/python library to the robotframework.
"""

from typing import Callable, Literal, Pattern, Union

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
        | Library        | ${EXECDIR}${/}playbot${/}Playbot.py | browser=<chromium|firefox|webkit> |
        '''
        self._selected_browser: str = browser
        self._playbot_browser: Union[None, Browser] = None

    @keyword
    def start_browser(self, **kwargs):
        '''Starts browser. Since library has default scope set to SUITE,
        user is expected to start the browser only ONCE, ideally using
        *Suite Setup* and close the browser using *Suite Teardown*.

        Starting browser is time and memory expensive. For isolated test runs,
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
    def close_page(
        self, page: PlaybotPage, run_before_unload: Union[bool, None] = None
    ):
        '''Closes the given page.

        See https://playwright.dev/python/docs/api/class-page#page-close for
        documentation.

        == Example ==

        | =A=        | =B=      | =C=                  |
        | ${page}=   | New Page | ${context}           |
        | Go To      | ${page}  | https://some/url.com |
        | Close Page | ${page}  |                      |
        '''
        return page.close_page(page.page, run_before_unload=run_before_unload)

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
    def frame(
        self,
        page: PlaybotPage,
        name: Union[str, None] = None,
        url: Union[str, Pattern, Callable, None] = None,
    ):
        '''Returns frame matching the given arguments.

        You have to provide either _name_ or _url_.

        See https://playwright.dev/python/docs/api/class-page#page-frame for
        documentation.

        Returns *<Frame>* object.

        == Example ==

        | =A=       | =B=      | =C=        | =D =                       |
        | ${page}=  | New Page | ${context} |                            |
        | ${frame}= | Frame    | ${page}    | https://some/url/of/iframe |
        | ${frame}= | Frame    | ${page}    | url=**/some/pattern        |
        | ${frame}= | Frame    | ${page}    | name=frame_name            |
        '''
        return page.frame(page.page, name=name, url=url)

    @keyword
    def go_to(self, page: PlaybotPage, url: str, **kwargs):
        '''Navigates to given url. Returns the response of the last redirect.

        See https://playwright.dev/python/docs/api/class-page#page-goto for
        the documentation.

        == Example ==

        | =A=          | =B=      | =C=                  | =D=                    | =E=                    |
        | ${page}=     | New Page | ${context}           |                        |                        |
        | Go To        | ${page}  | https://some/url.com |                        |                        |
        | ${response}= | Go To    | ${page}              | https://some/url.com   | wait_until=networkidle |
        '''
        return page.go_to(page.page, url, **kwargs)

    @keyword
    def is_visible(
        self,
        handle: Union[PlaybotPage, ElementHandle],
        selector: Union[str, None] = None,
        timeout: Union[float, None] = None,
    ):
        '''Predicate. Verifies, whether element is visible.

        Can be used with *PlaybotPage* or *ElementHandle*.

        See https://playwright.dev/python/docs/api/class-page#page-is-visible for
        page variant documentation.

        See https://playwright.dev/python/docs/api/class-elementhandle#element-handle-is-visible for
        element variant documentation.

        == Example ==

        === Is Visible with page and selector ===

        | =A=            | =B=               | =C=                  | =D=         | =E=          |
        | ${page}=       | New Page          | ${context}           |             |              |
        | ${selector}=   | Convert To String | xpath=/some-selector |             |              |
        | ${status}=     | Is Visible        | ${page}              | ${selector} | timeout=5000 |
        | Should Be True | ${status}==True   |                      |             |              |

        === Is Visible with element ===

        | =A=            | =B=               | =C=                  | =D=         |
        | ${page}=       | New Page          | ${context}           |             |
        | ${selector}=   | Convert To String | xpath=/some-selector |             |
        | ${element}=    | Query Selector    | ${page}              | ${selector} |
        | ${status}=     | Is Visible        | ${element}           |             |
        | Should Be True | ${status}==True   |                      |             |
        '''
        if isinstance(handle, PlaybotPage):
            return handle.is_visible(selector=selector, timeout=timeout)
        return handle.is_visible()

    @keyword
    def query_selector(self, handle: Union[PlaybotPage, ElementHandle], selector: str):
        '''Finds and returns element that matches the given selector. If no element is found, returns _None_.

        Can be used with *PlaybotPage* or *ElementHandle*.

        See https://playwright.dev/python/docs/api/class-page/#page-query-selector for
        page variant documentation.

        See https://playwright.dev/python/docs/api/class-elementhandle#element-handle-query-selector for
        element variant documentation.

        == Example ==

        === Query Selector with page and selector ===

        | =A=              | =B=               | =C=                    | =D=             |
        | ${page}=         | New Page          | ${context}             |                 |
        | ${selector_one}= | Convert To String | xpath=//some-selector1 |                 |
        | ${element_one}=  | Query Selector    | ${page}                | ${selector_one} |

        === Query Selector from the element ===

        | =A=              | =B=               | =C=                    | =D=             |
        | ${page}=         | New Page          | ${context}             |                 |
        | ${selector_one}= | Convert To String | xpath=//some-selector1 |                 |
        | ${selector_two}= | Convert To String | xpath=//some-selector2 |                 |
        | ${element_one}=  | Query Selector    | ${page}                | ${selector_one} |
        | ${element_two}=  | Query Selector    | ${element_one}         | ${selector_two} |
        '''
        return handle.query_selector(selector)

    @keyword
    def query_selector_all(
        self, handle: Union[PlaybotPage, ElementHandle], selector: str
    ):
        '''Finds all elements matching given selector and returns them in _list_. If no
        elements are found, returns an empty _list_.

        This keyword can be used with *PlaybotPage* or *ElementHandle*.

        See https://playwright.dev/python/docs/api/class-page#page-query-selector-all for
        page variant documentation.

        See https://playwright.dev/python/docs/api/class-elementhandle/#element-handle-query-selector-all for
        element variant documentation.

        == Example ==

        === With Page ===

        | =A=          | =B=                | =C=                   | =D=         |
        | ${page}=     | New Page           | ${context}            |             |
        | ${selector}= | Convert To String  | xpath=//some-selector |             |
        | @{elements}= | Query Selector All | ${page}               | ${selector} |

        === With Element ===

        | =A=            | =B=                | =C=                    | =D=           |
        | ${page}=       | New Page           | ${context}             |               |
        | ${selector_1}= | Convert To String  | xpath=//some-selector1 |               |
        | ${selector_2}= | Convert To String  | xpath=//some-selector2 |               |
        | ${element}=    | Query Selector     | ${page}                | ${selector_1} |
        | @{elements}=   | Query Selector All | ${element}             | ${selector_2} |
        '''
        return handle.query_selector_all(selector)

    @keyword
    def wait_for_element_state(
        self,
        handle: ElementHandle,
        state: Literal["visible", "hidden", "enabled", "disabled", "editable"],
        **kwargs
    ):
        '''Waits, until given state is satisfied. If state is not satisfied until given timeout, the
        keyword will throw an error.

        Returns None.

        See https://playwright.dev/python/docs/api/class-elementhandle#element-handle-wait-for-element-state for
        documentation.

        == Example ==

        | =A=                    | =B=               | =C=                   | =D=         | =E=            |
        | ${page}=               | New Page          | ${context}            |             |                |
        | ${selector}=           | Convert To String | xpath=//some-selector |             |                |
        | ${element}=            | Wait For Selector | ${page}               | ${selector} | state=attached |
        | Wait For Element State | ${element}        | visible               |             |                |
        '''
        return handle.wait_for_element_state(state, **kwargs)

    @keyword
    def wait_for_load_state(
        self,
        page: PlaybotPage,
        state: Union[Literal["load", "domcontentloaded", "networkidle"], None] = "load",
        timeout: Union[float, None] = None,
    ):
        '''Returns, when the given load state of the page was reached.

        Default state is set to _load_.

        See https://playwright.dev/python/docs/api/class-page#page-wait-for-load-state for
        documentation.

        == Example ==

        | =A=                 | =B=      | =C=                  | =D=           |
        | ${page}=            | New Page | ${context}           |               |
        | Go To               | ${page}  | https://some/url.com |               |
        | Wait For Load State | ${page}  | state=networkidle    | timeout=10000 |
        '''
        return page.wait_for_load_state(page.page, state=state, timeout=timeout)

    @keyword
    def wait_for_selector(
        self, handle: Union[PlaybotPage, ElementHandle], selector: str, **kwargs
    ):
        '''Returns element, if matches the given selector and if satisfies the state option (in **kwargs).
        Default options for state is _visible_.

        If the element is not returned withing given timeout, the keyword will throw.

        This keyword can be used with *PlaybotPage* or *ElementHandle*.

        See https://playwright.dev/python/docs/api/class-page/#page-wait-for-selector for
        page variant documentation.

        See https://playwright.dev/python/docs/api/class-elementhandle#element-handle-wait-for-selector for
        element variant documentation.

        == Example ==

        === Wait For Selector with page and selector ===

        | =A=          | =B=               | =C=                   | =D=         | =E=            |
        | ${page}=     | New Page          | ${context}            |             |                |
        | ${selector}= | Convert To String | xpath=//some-selector |             |                |
        | ${element}=  | Wait For Selector | ${page}               | ${selector} |                |
        | ${element}=  | Wait For Selector | ${page}               | ${selector} | state=attached |

        === Wait For Selector with element and selector ===

        | =A=           | =B=               | =C=                    | =D=         | =E=            |
        | ${page}=      | New Page          | ${context}             |             |                |
        | ${selector}=  | Convert To String | xpath=//some-selector  |             |                |
        | ${selector_2} | Convert To String | xpath=//some-selector2 |             |                |
        | ${element}=   | Wait For Selector | ${page}                | ${selector} |                |
        | ${element2}=  | Wait For Selector | ${element}             | ${selector} | state=visible  |
        '''
        return handle.wait_for_selector(selector, **kwargs)

    @keyword
    def wait_for_timeout(self, page: PlaybotPage, timeout: float):
        '''Waits for given timeout provided in miliseconds.

        See https://playwright.dev/python/docs/api/class-page/#page-wait-for-timeout for
        documentation.

        == Example ==

        | =A=              | =B=      | =C=        |
        | ${page}=         | New Page | ${context} |
        | Wait For Timeout | ${page}  | 5000       |
        '''
        page.wait_for_timeout(page.page, timeout)

    @keyword
    def wait_for_url(
        self, page: PlaybotPage, url: Union[str, Pattern, Callable], **kwargs
    ):
        '''Waits until the navigation to the given _url_ is completed.

        This keyword can be used, when interaction (e.g. click) with some element of
        the page leads to indirect navigation.

        See https://playwright.dev/python/docs/api/class-page#page-wait-for-url for
        documentation.

        == Example ==

        | =A=          | =B=               | =C=                   | =D=                    | =E=           |
        | ${selector}= | Convert To String | xpath=//some-selector |                        |               |
        | ${page}=     | New Page          | ${context}            |                        |               |
        | Click        | ${page}           | ${selector}           |                        |               |
        | Wait For Url | ${page}           | **/page.html          | wait_until=networkidle | timeout=30000 |
        '''
        return page.wait_for_url(page.page, url, **kwargs)
