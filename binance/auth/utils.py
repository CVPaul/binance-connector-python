#!/usr/bin/env python
#-*- coding:utf-8 -*-


import os
import logging
import subprocess as sb


def get_auth_keys(prefix='strategy'):
    # ED25519 Keys
    api_key = f"{prefix}/api_key.txt"
    with open(api_key) as f:
        api_key = f.read().strip()

    private_key = f"{prefix}/private_key.pem"
    with open(private_key, 'rb') as f:
        private_key = f.read().strip()
    return api_key, private_key


def on_open(self):
    logging.info("CONNECTED|snapshot={self.ctx.snapshot}")


def on_close(self):
    logging.warning("DISCONNECTED|snapshot={self.ctx.snapshot}")
    script = f'./status/{self.ctx.stgname}.sh'
    os.execv(script, ['sh', script])
