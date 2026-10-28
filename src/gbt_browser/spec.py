"""The capability contract, copied verbatim from the GBT V8 registry.

Do not hand-edit: ``tests/test_spec.py`` pins every field against the
registry snapshot so drift fails the build instead of shipping quietly.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple

_RAW = r"""{
 "name": "browser",
 "domain": "automation",
 "desc": "浏览器自动化入口（良性子集）。op=open/search/fetch/automate 走 browser_cap 三级后端；op=native（别名 deep/controller/cdp）走原生浏览器窗口 native_browser.py（Chrome DevTools Protocol，自带最小 RFC6455 客户端、零第三方依赖），动作放 action：status/list_tabs/get_title/get_url/get_text/dom_query/get_cookies/intercept_events/intercept_status 为只读免卡，launch/ensure/create_tab/close_tab/activate_tab/navigate/reload/back/forward/click_element/type_text/execute_script/inject_script/set_cookies/privacy_mode/intercept_requests/intercept_stop/pin_window 需 browser_control，screenshot 另需 filesystem_write",
 "handler": "browser",
 "safe": true,
 "external": false,
 "requires_params": true,
 "params": [
  "url"
 ],
 "params_hint": "默认 op=open 必须要 url；只读路请写 op=native + action=status",
 "multi_op": true,
 "ops": [
  "open",
  "search",
  "fetch",
  "automate"
 ],
 "ops_hint": "默认 op=open 必须要 url；只读路请写 op=native + action=status"
}"""


@dataclass(frozen=True)
class CapSpec:
    """Immutable description of one capability bit."""

    name: str
    domain: str
    desc: str
    handler: str
    safe: bool
    external: bool
    requires_params: bool
    params: Tuple[str, ...] = ()
    params_hint: str = ""
    multi_op: bool = False
    ops: Tuple[str, ...] = ()
    ops_hint: str = ""

    @property
    def gated(self) -> bool:
        """True when the registry marks this bit ``safe: false``.

        Gated does not mean "dangerous"; it means the action can change state
        that cannot be restored by running the inverse action.
        """
        return not self.safe

    @property
    def summary(self) -> str:
        """First clause of the description, for one-line listings."""
        for sep in ("\uff08", "\uff1b", "\u3002", ";"):
            if sep in self.desc:
                head = self.desc.split(sep, 1)[0].strip()
                if head:
                    return head
        return self.desc.strip()

    def as_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "domain": self.domain,
            "desc": self.desc,
            "handler": self.handler,
            "safe": self.safe,
            "gated": self.gated,
            "external": self.external,
            "requires_params": self.requires_params,
            "params": list(self.params),
            "params_hint": self.params_hint,
            "multi_op": self.multi_op,
            "ops": list(self.ops),
            "ops_hint": self.ops_hint,
        }


_data = json.loads(_RAW)

SPEC = CapSpec(
    name=_data["name"],
    domain=_data["domain"],
    desc=_data["desc"],
    handler=_data["handler"],
    safe=_data["safe"],
    external=_data["external"],
    requires_params=_data["requires_params"],
    params=tuple(_data["params"]),
    params_hint=_data["params_hint"],
    multi_op=_data["multi_op"],
    ops=tuple(_data["ops"]),
    ops_hint=_data["ops_hint"],
)
