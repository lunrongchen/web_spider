#!/bin/python2
# -*- encoding:utf-8 -*-


class Event:
	KEYWORDS = [u"聚众", u"强占", u"强征", u"强拆", u"非法集会", u"大众恐慌", u"骚乱", u"集会", u"集体怠工", u"上访", u"游行", u"示威", u"抗议",u"罢工",u"罢课",u"哄抢",u"斗殴",u"闹事",u"暴乱",u"暴动",u"劫机",u"劫船",u"劫持",u"暴力性犯罪"]

	def __init__(self):
		pass

	def label(self,  content):


		flag = False
		matched = None

		for word in self.KEYWORDS:
			
			if word in content:
				flag = True
				matched = word
				break

		return [content, matched]

if __name__ == '__main__':
	e = Event()
	ret = e.label(u'聚众吸毒,聚众吸毒 别墅 吸毒... 没想到,该别墅之前就被举报称常放劲爆音乐扰民,')
	print ret[0], ret[1]
