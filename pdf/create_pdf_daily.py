#_*_ coding: UTF-8 _*_
import sys,time,os
reload(sys)
sys.setdefaultencoding('utf8')

from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph,Spacer,Image,PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import copy
# 注册中文字体
import reportlab.rl_config
reportlab.rl_config.warnOnMissingFontGlyphs = 0
import reportlab.pdfbase.pdfmetrics
import reportlab.pdfbase.ttfonts
reportlab.pdfbase.pdfmetrics.registerFont(reportlab.pdfbase.ttfonts.TTFont('song', '/usr/share/fonts/wqy-microhei/wqy-microhei.ttc'))
# 修改默认字体
import reportlab.lib.fonts
reportlab.lib.fonts.ps2tt = lambda psfn: ('song', 0, 0)
reportlab.lib.fonts.tt2ps = lambda fn,b,i: 'song'
## for CJK Wrap
import reportlab.platypus
def wrap(self, availWidth, availHeight):
	# work out widths array for breaking
	self.width = availWidth
	leftIndent = self.style.leftIndent
	first_line_width = availWidth - (leftIndent+self.style.firstLineIndent) - self.style.rightIndent
	later_widths = availWidth - leftIndent - self.style.rightIndent
	try:
		self.blPara = self.breakLinesCJK([first_line_width, later_widths])
	except:
		self.blPara = self.breakLines([first_line_width, later_widths])
	self.height = len(self.blPara.lines) * self.style.leading
	return (self.width, self.height)
reportlab.platypus.Paragraph.wrap = wrap
###########
doc = SimpleDocTemplate("openstack-daily.pdf",pagesize=letter,
                rightMargin=72,leftMargin=72,topMargin=72,bottomMargin=18)
styles=getSampleStyleSheet()

#styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
normalStyle = copy.deepcopy(styles['Normal'])
normalStyle.fontName ='song'
normalStyle.fontSize = 12
# 设置行距
normalStyle.leading = 20
##首行缩进
normalStyle.firstLineIndent = 32

Story = []
#logo = "openstack.jpg"
#logo = "openstack_logo.png"
magName = "北京壹号车云计算部系统日报"
title = "北京壹号车云计算部系统日报"
issueNum = 12
subPrice = "99.00"
limitedDate = "03/25/2015"
freeGift = "tin foil hat"

formatted_time = time.ctime()
#=============================
host1 = 'jumpclient02'
ip1 = '172.172.0.8'
#==================================
cpu = '1d_cpu.png'
mem = '1d_mem.png'
disk = '1d_disk.png'
network = '1d_nic.png'
login = '1d_login_user.png'
#ptext = '<font size=12>%s</font>' % formatted_time
ptext = '<font size=20>%s</font>' % title

Story.append(Paragraph(ptext, normalStyle))
Story.append(Spacer(1, 12))

# Create return address
ptext = '<font size=14>日期：%s</font>' % formatted_time
Story.append(Spacer(1, 24))
Story.append(Paragraph(ptext, normalStyle))

ptext = '<font size=14 color=#ff0000>目的：通过日报可以直观的了解操作系统的重要参数，\
通过这些我们可以判断系统资源是否长期闲置以及遇到瓶颈。比如：当内存使用\
长期在80%以上，内存上遇到了瓶颈。CPU idle 长期在20%，CPU使用率过高，\
需要优化系统或者增加CPU。</font>'
Story.append(Paragraph(ptext, normalStyle))
Story.append(Spacer(1, 24))

ptext = '以下是各个节点的监控指标，具体包括cpu，内存，磁盘，网络与登陆终端的数量。'
Story.append(Paragraph(ptext, normalStyle))
Story.append(Spacer(1, 48))

ptext = '<font size=12>主机名：%s</font>' %host1
Story.append(Paragraph(ptext, normalStyle))
Story.append(Spacer(1, 12))

ptext = '<font size=12>IP地址：%s</font>' % ip1
Story.append(Paragraph(ptext, normalStyle))
Story.append(Spacer(1, 12))
# cpu
ptext = '<font size=12>一：CPU使用率的监控</font>'
Story.append(Paragraph(ptext, normalStyle))
Story.append(Spacer(1, 12))

im = Image(cpu,3*inch,2*inch)
Story.append(im)
# mem
ptext = '<font size=12>二：内存使用状况的监控</font>'
Story.append(Paragraph(ptext, normalStyle))
Story.append(Spacer(1, 12))

im = Image(mem,3*inch,2*inch)
Story.append(im)
# disk
ptext = '<font size=12>三：磁盘使用情况的监控</font>'
Story.append(Paragraph(ptext, normalStyle))
Story.append(Spacer(1, 12))

im = Image(disk,3*inch,2*inch)
Story.append(im)
# network
ptext = '<font size=12>四：网络流量的监控</font>'
Story.append(Paragraph(ptext, normalStyle))
Story.append(Spacer(1, 12))

im = Image(network,3*inch,2*inch)
Story.append(im)
# login
ptext = '<font size=12>五：登陆终端数量的监控</font>'
Story.append(Paragraph(ptext, normalStyle))
Story.append(Spacer(1, 12))

im = Image(login,3*inch,2*inch)
Story.append(im)
Story.append(Spacer(1, 48))

ptext = '<font size=12>真诚的感谢,</font>'
Story.append(Paragraph(ptext, normalStyle))
Story.append(Spacer(1, 48))

ptext = '<font size=12>Openstack 团队</font>'
Story.append(Paragraph(ptext, normalStyle))
Story.append(Spacer(1, 12))

Story.append(PageBreak())
doc.build(Story)
