#!/bin/bash

set -e

BROWSERS="${1:-}" pytest -n "${2:-auto}" --reruns 2 --alluredir=allure-results
