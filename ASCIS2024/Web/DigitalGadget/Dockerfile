FROM ubuntu:22.04
RUN apt-get update && apt-get install -y --no-install-recommends \
  mathtex \
  apache2 \
  dumb-init \
  # mysql-server \
  && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN a2enmod cgid
RUN ln -s /usr/bin/mathtex /usr/lib/cgi-bin/mathtex.cgi
RUN chmod -R 000 /tmp
RUN sed -i "s@works@doesn't work@g" /var/www/html/index.html
RUN sed -i "s@Timeout 300@Timeout 5@g" /etc/apache2/apache2.conf
EXPOSE 80
ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND", "-e", "info"]
