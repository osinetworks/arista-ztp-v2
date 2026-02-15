FROM alpine:3.22

RUN apk add --no-cache dnsmasq python3 tini py3-requests

COPY dnsmasq.conf /etc/dnsmasq.conf

WORKDIR /var/www/ztp

ENTRYPOINT ["/sbin/tini", "--"]

CMD ["sh", "-c", "dnsmasq --no-daemon --log-dhcp --log-queries --log-facility=- & exec python3 -m http.server 8080"]