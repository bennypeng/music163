# -*- coding: utf-8 -*-


class Helper:

    @staticmethod
    def chinese(data):
        count = 0
        for s in data:
            if ord(s) > 127:
                count += 1
        return count
