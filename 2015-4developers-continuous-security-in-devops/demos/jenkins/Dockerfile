FROM jenkins
MAINTAINER johan.haleby@jayway.com
 
# Switch user to root so that we can install apps (jenkins image switches to user "jenkins" in the end)
USER root
 
# Install Docker prerequisites
RUN apt-get update -qq && apt-get install -qqy \
    apt-transport-https \
    ca-certificates \
    lxc \
    supervisor
 
# Create log folder for supervisor, jenkins and docker
RUN mkdir -p /var/log/supervisor
RUN mkdir -p /var/log/docker
RUN mkdir -p /var/log/jenkins
 
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
 
# Install Docker from Docker Inc. repositories.
RUN echo deb https://get.docker.io/ubuntu docker main > /etc/apt/sources.list.d/docker.list \
  && apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9 \
  && apt-get update -qq \
  && apt-get install -qqy lxc-docker
 
# Add jenkins user to the docker groups so that the jenkins user can run docker without sudo
RUN gpasswd -a jenkins docker
 
# Install the magic wrapper
ADD ./wrapdocker /usr/local/bin/wrapdocker
RUN chmod +x /usr/local/bin/wrapdocker
 
CMD /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
