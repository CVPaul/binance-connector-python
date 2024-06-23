#!/usr/bin/env python
#-*- coding:utf-8 -*-


import os
import logging
import streamlit as st
import subprocess as sb


def get_auth_keys(src='env'):
    # ED25519 Keys
    stt_lin = "-----BEGIN PRIVATE KEY-----"
    end_lin = "-----END PRIVATE KEY-----"
    if src == 'file':
        prefix = 'config'
        api_key = f"{prefix}/api_key.txt"
        with open(api_key) as f:
            api_key = f.read().strip()
        prv_key = f"{prefix}/private_key.pem"
        with open(private_key, 'rb') as f:
            private_key = f.read().strip()
    elif src == 'env':
        api_key = os.environ.get('API_KEY')
        prv_key = os.environ.get('PRV_KEY')
        prv_key = f'{stt_lin}\n{prv_key}\n{end_lin}'
    elif src == 'secret':
        api_key = st.secrets['API_KEY']
        prv_key = st.sectets['PRV_KEY']
        prv_key = f'{stt_lin}\n{prv_key}\n{end_lin}'
    return api_key, prv_key


def on_open(self):
    logging.info("CONNECTED|snapshot={self.ctx.snapshot}")


def on_close(self):
    logging.warning("DISCONNECTED|snapshot={self.ctx.snapshot}")
    script = f'./status/{self.ctx.stgname}.sh'
    os.execv(script, ['sh', script])
