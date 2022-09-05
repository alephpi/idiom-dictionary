from typing import Dict, Tuple, List
from constants import DICT_POLYPHONE
from pypinyin import pinyin, lazy_pinyin, STYLE_TONE3
from pypinyin.contrib.tone_convert import to_tone3


class idiom:
    def __init__(self, idiom) -> None:
        self.idiom = idiom
        self.phone = []
        self.char_polyphone: Dict[Tuple[int, str], List[str]] = {}
        for index, char in enumerate(self.idiom):
            if char in DICT_POLYPHONE.keys():
                self.char_polyphone[(index, char)] = []

    # init phone from pypinyin, may not correct
    def init_phone(self, phone: List[str]):
        # self.phone = lazy_pinyin(self.idiom, style=STYLE_TONE3)
        self.phone = phone
        self._update_polyphone(phone)

    def _update_polyphone(self, phone: List[str], style=STYLE_TONE3):
        for index, char in self.char_polyphone.keys():
            char_phone = phone[index]
            # 判断是否是正确读音，不同来源可能有错误（非多音字错误而是非常低级的笔误）
            # 此外还要排除两岸异读
            polyphones = list(map(to_tone3, DICT_POLYPHONE[char].split(',')))
            if char_phone in polyphones:
                # print(char_phone)
                self.char_polyphone[(index, char)].append(char_phone)

    def mark_phone(self, dict: Dict[str, List[str]]):
        if self.idiom in dict.keys():
            self._update_polyphone(dict[self.idiom])

    def is_monophone(self):
        return self.char_polyphone == []
