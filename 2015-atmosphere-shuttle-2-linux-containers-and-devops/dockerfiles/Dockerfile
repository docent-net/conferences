FROM ansible/centos7-ansible:stable
ADD ansible /srv/example
WORKDIR /srv/example
RUN ansible-playbook web.yml -c local
EXPOSE 80
CMD ["/usr/sbin/nginx"]
