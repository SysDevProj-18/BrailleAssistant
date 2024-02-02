FROM debian:latest
RUN apt-get update && apt-get install -y \
    autoconf \
    automake \
    curl \
    libtool \
    libyaml-dev \
    make \
    git \
    locales\
   && rm -rf /var/lib/apt/lists/*
ENV LANG='en_GB.UTF-8' LANGUAGE='en_GB:en' LC_ALL='en_GB.UTF-8'
RUN echo en_GB.UTF-8 UTF-8 >> /etc/locale.gen && locale-gen
WORKDIR /app
RUN git clone https://github.com/liblouis/liblouis.git
WORKDIR /app/liblouis
RUN ./autogen.sh && ./configure && make && make install && ldconfig
WORKDIR /app 
COPY main.c .
CMD ["sleep", "infinity"]
