#! /usr/bin/bash

ps aux | grep '[p]ython' | awk '{print $2}' | xargs kill

