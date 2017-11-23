FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /www
WORKDIR /www

ADD ./requirements.txt /www/requirements.txt
RUN pip install -r requirements.txt

# --------- BLENDER ---------

RUN apt-get update && \
	apt-get install -y \
		curl \
		git \
		bzip2 \
		libfreetype6 \
		libgl1-mesa-dev \
		libglu1-mesa \
		libxi6 \
		unzip \
		libxrender1 && \
	apt-get -y autoremove && \
	rm -rf /var/lib/apt/lists/*

ENV BLENDER_PATH /usr/local/blender

RUN mkdir $BLENDER_PATH


ENV BLENDER_MAJOR 2.78
ENV BLENDER_VERSION 2.78c
ENV BLENDER_PATH $BLENDER_PATH/$BLENDER_VERSION
RUN mkdir $BLENDER_PATH
ENV BLENDER_BZ2_URL https://www.blend4web.com/blender/release/Blender$BLENDER_MAJOR/blender-$BLENDER_VERSION-linux-glibc219-x86_64.tar.bz2

RUN curl -SL "$BLENDER_BZ2_URL" -o blender.tar.bz2 && \
	tar -jxvf blender.tar.bz2 -C $BLENDER_PATH --strip-components=1 && \
	rm blender.tar.bz2

ENV BLEND4WEB_VERSION 17_04_1
ENV BLEND4WEB_ZIP_URL https://www.blend4web.com/pub/blend4web_addon_$BLEND4WEB_VERSION.zip
ENV BLEND4WEB_PATH $BLENDER_PATH/$BLENDER_MAJOR/scripts/addons

RUN curl -SL "$BLEND4WEB_ZIP_URL" -o blend4web_addon.zip && \
	unzip -o blend4web_addon.zip -d $BLEND4WEB_PATH && \
	rm blend4web_addon.zip
