#!/bin/sh

alias ls='ls --color=auto'
alias ll='ls -l --color=auto'
alias la='ls -a --color=auto'
alias l='ls --color=auto'
alias s='ls --color=auto'
alias lA='ls -A --color=auto'
alias la='ls -a --color=auto'
alias lR='ls -R --color=auto'
alias llR='ls -R -l --color=auto'
alias lRl='llR'
export PS1="\[\e[01;32m\]\u@\h:\[\e[0m\]\[\e[00;31m\]\w\\$\[\e[0m\]\[\e[00;37m\] \[\e[0m\]"
alias cd..='cd ..'
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias .....='cd ../../../..'
alias grep='grep --color=auto'
mkcd() { mkdir -p "$@" && cd $_; } 


# Gurobi
export GUROBI_HOME="/opt/gurobi605/linux64"
export PATH="${PATH}:${GUROBI_HOME}/bin"
export LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:${GUROBI_HOME}/lib"

export PERL5LIB=/users/nfs/Etu8/3200338/Perl/share/perl/5.20.2
