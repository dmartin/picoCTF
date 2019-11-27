# picoCTF web UI

FROM node:12.13-buster AS builder
WORKDIR /app
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
      ruby-full build-essential zlib1g-dev && \
    gem install jekyll bundler
COPY ./package.json .
RUN npm install
COPY . .
RUN npm run-script compile && \
    jekyll build

FROM nginx:1.17 AS runner
RUN apt-get update && \
    apt-get install -y openssl
COPY self_signed.cnf /etc/pico-tls/self_signed.cnf
RUN openssl req -new -newkey rsa:4096 -x509 -sha256 -days 365 -nodes \
      -config /etc/pico-tls/self_signed.cnf -extensions 'v3_req' \
      -out /etc/pico-tls/pico-cert.crt -keyout /etc/pico-tls/pico-key.key
COPY nginx.conf /etc/nginx/nginx.conf
COPY ui.nginx /etc/nginx/sites-enabled/ui.nginx
COPY --from=builder /app/_site /app
EXPOSE 443
