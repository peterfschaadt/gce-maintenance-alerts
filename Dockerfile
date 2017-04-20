FROM ubuntu:16.04
LABEL version='1.1.0' \
  maintainer='Peter Schaadt'


# Ansible Releases
# PyPI: https://pypi.python.org/pypi/ansible
# GitHub: https://github.com/ansible/ansible/releases

ENV ANSIBLE_STABLE=1.9.6
ENV ANSIBLE_DEV=2.2.2.0

ENV ANSIBLE_VERSION=${ANSIBLE_STABLE}

RUN echo '[DOCKER] Installing build-essential, libssl-dev, libffi-dev, python-dev, python-setuptools, and python-pip...' && \
  DEBIAN_FRONTEND=noninteractive apt-get update && \
  apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python-dev \
    python-setuptools \
    python-pip && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN echo '[DOCKER] Displaying Python version number...' && \
  python --version

RUN echo '[DOCKER] Upgrading pip with pip...' && \
  pip install --upgrade pip

RUN echo '[DOCKER] Displaying pip version number...' && \
  pip --version

RUN echo '[DOCKER] Upgrading distribute with pip...' && \
  pip install distribute --upgrade --force

RUN echo '[DOCKER] Installing Ansible v${ANSIBLE_VERSION} with pip...' && \
  pip install ansible==${ANSIBLE_VERSION}

ONBUILD RUN \
  echo '[DOCKER] Updating TLS certificates...' && \
    DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get install -y openssl ca-certificates

# RUN echo '[DOCKER] Creating deployer group and user...' && \
#   addgroup --system deployer && adduser --system --ingroup deployer --uid 5500 deployer

# USER deployer

RUN echo '[DOCKER] Installing git and vim...' && \
  DEBIAN_FRONTEND=noninteractive apt-get update && \
  apt-get install -y \
    sudo \
    git \
    vim && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY . /opt/gce-maintenance-alerts

WORKDIR /opt/gce-maintenance-alerts/build

# Set environment variables
ENV BUILD_ENV=build \
  ANSIBLE_HOST_KEY_CHECKING=False

ARG VAULT_PASS_BUILD

RUN echo "${VAULT_PASS_BUILD}" > vault_pass_build.txt

# Use Ansible to provision dependencies for build environment
RUN ansible-playbook provision_alerts.yml \
  -c local \
  -i inventories/${BUILD_ENV:-build} \
  --vault-password-file vault_pass_${BUILD_ENV:-build}.txt \
  -e "docker_build=true" \
  --become \
  -vvvv

# | tee /build/provision_alerts-log.txt

### Ports
# 22 - SSH

EXPOSE 22

WORKDIR /opt/gce-maintenance-alerts

# CMD ["python", "/opt/gce-maintenance-alerts/gce-maintenance-alerts.py"]
# CMD ["/usr/bin/supervisord"]
CMD ["/bin/bash"]
