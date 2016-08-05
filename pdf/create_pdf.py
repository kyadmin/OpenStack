#_*_ coding: UTF-8 _*_
import sys,time,os
reload(sys)
sys.setdefaultencoding('utf8')

from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph,Spacer,Image
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
'''
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
'''
###########
doc = SimpleDocTemplate("test_openstack.pdf",pagesize=letter,
                rightMargin=72,leftMargin=72,topMargin=72,bottomMargin=18)
styles=getSampleStyleSheet()
#styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
normalStyle = copy.deepcopy(styles['Normal'])
normalStyle.fontName ='song'
normalStyle.fontSize = 12

Story = []
#logo = "openstack.jpg"
logo = "openstack_logo.png"
magName = "Pythonista"
issueNum = 12
subPrice = "99.00"
limitedDate = "03/25/2015"
freeGift = "tin foil hat"

formatted_time = time.ctime()
full_name = "杨俊飞"
address_parts = ["博彦科技大厦北区501室", "北京市海淀区西北旺东路10号院东区7号楼"]

im = Image(logo,0.5*inch,0.5*inch)
Story.append(im)
#ptext = '<font size=12>%s</font>' % formatted_time
ptext = '<font size=12>%s</font>' % formatted_time

Story.append(Paragraph(ptext, normalStyle))
Story.append(Spacer(1, 12))

# Create return address
ptext = '<font size=12>%s</font>' % full_name
Story.append(Paragraph(ptext, normalStyle))
for part in address_parts:
	ptext = '<font size=12>%s</font>' % part.strip()
	Story.append(Paragraph(ptext, normalStyle))
	Story.append(Spacer(1, 12))

ptext = '<font size=12>Dear %s:</font>' % full_name.split()[0].strip()
Story.append(Paragraph(ptext, normalStyle))
Story.append(Spacer(1, 12))

ptext = '  OpenStack是一个开源的云计算管理平台项目，\
	由几个主要的组件组合起来完成具体工作。OpenStack支持几乎所有类型的云环境， \
	项目目标是提供实施简单、可大规模扩展、丰富、标准统一的云计算管理平台。\
	OpenStack通过各种互补的服务提供了基础设施即服务（IaaS）的解决方案， \
	每个服务提供API以进行集成。'
Story.append(Paragraph(ptext, normalStyle))
Story.append(Spacer(1, 12))

ptext = '<font size=12>OpenStack是IaaS(基础设施即服务)组件，让任何人都可以自行建立和提供云端运算服务。</font>'
Story.append(Paragraph(ptext, normalStyle))
Story.append(Spacer(1, 12))
ptext = '<font size=12>真诚的感谢,</font>'
Story.append(Paragraph(ptext, normalStyle))
Story.append(Spacer(1, 48))
ptext = '<font size=12>Openstack 团队</font>'
Story.append(Paragraph(ptext, normalStyle))
Story.append(Spacer(1, 12))
doc.build(Story)
