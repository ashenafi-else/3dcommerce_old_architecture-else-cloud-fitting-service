FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /www
WORKDIR /www

RUN apt-get update && apt-get install -y \
cmake \
git \
libeigen3-dev \
libgmp-dev \
libmpfr-dev \
libgmpxx4ldbl \
libumfpack5.6.2 \
libboost-dev \
libboost-thread-dev \
python-setuptools \
python \
swig \
&& apt-get clean

RUN git clone https://github.com/qnzhou/PyMesh.git
RUN cd PyMesh && git submodule init && git submodule update

ENV PYMESH_PATH /www/PyMesh

RUN pip install numpy scipy nose

RUN mkdir -p $PYMESH_PATH/third_party/build && mkdir -p $PYMESH_PATH/build
WORKDIR $PYMESH_PATH/third_party/build
RUN cmake .. && make -j 2 && make install && make clean
WORKDIR $PYMESH_PATH/build
RUN cmake .. && make -j 2 && make tools -j 2 && make all_tests
WORKDIR $PYMESH_PATH
RUN ./setup.py build && ./setup.py install && rm -rf build third_party/build && python -c "import pymesh; pymesh.test()"
WORKDIR /www
RUN rm -rf PyMesh

ADD ./requirements.txt /www/requirements.txt
RUN pip install -r requirements.txt

ADD ./transparent_environment.blend /www/transparent_environment.blend

RUN apt-get update && \
	apt-get install -y \
		curl \
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

# --------- BLENDER ---------

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
