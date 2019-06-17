# picoCTF frontend

FROM ubuntu:bionic AS build
RUN apt-get update && apt-get install -y curl jekyll
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash - && \
  apt-get install -y nodejs
RUN npm install -g coffee-react coffee-script jsxhint react-tools
WORKDIR /picoCTF
COPY ./web ./web-source
RUN cjsx -bc -o ./web-source/js ./web-source/coffee
RUN jekyll build -s ./web-source -d ./web-output

FROM nginx:alpine
COPY --from=build /picoCTF/web-output /picoCTF-web

