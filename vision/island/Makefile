
DIR = /tmp/island

all: $(DIR)/grey.jpg

PIC =https://i.dailymail.co.uk/i/pix/2013/05/17/article-2325880-19D30C78000005DC-510_634x443.jpg
$(DIR)/grey.jpg:
	mkdir -p $(DIR)
	wget -S -O $(DIR)/orig.jpg $(PIC)
	cd $(DIR) && convert orig.jpg -colorspace Gray grey.jpg
	cd $(DIR) && convert grey.jpg bw.pbm

clean:
	rm -rf $(DIR)
